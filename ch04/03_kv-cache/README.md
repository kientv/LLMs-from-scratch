# Bonus Material: KV Cache



# Tài liệu bổ sung: KV Cache

**Thư mục này hiện thực việc bổ sung KV cache vào mô hình GPT.**

&nbsp;
## Tổng quan

Tóm tắt: KV cache lưu các tính toán trung gian của key (K) và value (V) để tái sử dụng trong quá trình suy luận, đem lại tăng tốc đáng kể khi sinh câu trả lời. Nhược điểm là làm mã phức tạp hơn, tăng tiêu thụ bộ nhớ và không thể dùng trong huấn luyện. Tuy nhiên, khi triển khai LLM, lợi ích về tốc độ suy luận thường bù đắp cho chi phí về độ phức tạp mã và bộ nhớ.

&nbsp;
## Cách hoạt động

Giả sử LLM được đưa một prompt: "Time flies".

Hình bên dưới cho thấy một đoạn tính toán attention với các vector key và value được tô sáng (được sửa đổi từ chương 3):

<img src="https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/kv-cache-attn-1.png?3" width=800>

Như đã học trong Chương 2 và 4, LLM sinh từng từ (token) một. Nếu mô hình sinh từ "fast" để prompt tiếp theo là "Time flies fast", thì:

<img src="https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/kv-cache-attn-2.png?3" width=800>

So sánh hai hình trên cho thấy các key và value cho hai token đầu tiên hoàn toàn giống nhau — việc tái tính toán chúng ở mỗi bước là lãng phí.

Ý tưởng của KV cache là lưu các vector key và value đã sinh trước đó để tái sử dụng, tránh tính toán thừa.

&nbsp;

## Hiện thực KV cache

Có nhiều cách để hiện thực KV cache; ý chính là chỉ tính toán key và value cho các token mới sinh ở mỗi bước sinh.

Ở đây tác giả chọn cách đơn giản, nhấn mạnh rõ ràng trong mã để dễ hiểu. Bạn có thể đọc nhanh các thay đổi trong mã để hiểu cách hoạt động.

Thư mục chứa hai file chính:

1. [`gpt_ch04.py`](gpt_ch04.py): Mã độc lập lấy từ Chương 3 và 4 để hiện thực LLM và chạy hàm sinh văn bản đơn giản.
2. [`gpt_with_kv_cache.py`](gpt_with_kv_cache.py): Tương tự nhưng đã bổ sung các thay đổi cần thiết để hiện thực KV cache.

Bạn có thể:

a. Mở [`gpt_with_kv_cache.py`](gpt_with_kv_cache.py) và tìm các phần được đánh dấu `# NEW` cho các thay đổi mới:

<img src="https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/new-sections.png?3" width=800>

b. Hoặc so sánh hai file mã bằng công cụ diff để thấy khác biệt:

<img src="https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/file-diff.png?3" width=800>

Tóm tắt các bước hiện thực:

&nbsp;

### 1. Đăng ký buffer cache

Trong constructor của `MultiHeadAttention` ta thêm hai buffer `cache_k` và `cache_v` để lưu key và value nối tiếp qua các bước:

```python
self.register_buffer("cache_k", None)
self.register_buffer("cache_v", None)
```

&nbsp;

### 2. Forward với cờ `use_cache`

Mở rộng `forward` của `MultiHeadAttention` để chấp nhận tham số `use_cache`. Sau khi chiếu các token mới thành `keys_new`, `values_new` và `queries`, ta khởi tạo hoặc nối vào cache:

```python
def forward(self, x, use_cache=False):
    b, num_tokens, d_in = x.shape

    keys_new = self.W_key(x)  # Shape: (b, num_tokens, d_out)
    values_new = self.W_value(x)
    queries = self.W_query(x)
    #...

    if use_cache:
        if self.cache_k is None:
            self.cache_k, self.cache_v = keys_new, values_new
        else:
            self.cache_k = torch.cat([self.cache_k, keys_new], dim=1)
            self.cache_v = torch.cat([self.cache_v, values_new], dim=1)
        keys, values = self.cache_k, self.cache_v
    else:
        keys, values = keys_new, values_new
        
    # ...
    
    num_tokens_Q = queries.shape[-2]
    num_tokens_K = keys.shape[-2]
    if use_cache:
        mask_bool = self.mask.bool()[
            self.ptr_current_pos:self.ptr_current_pos + num_tokens_Q, :num_tokens_K
        ]
        self.ptr_current_pos += num_tokens_Q
    else:
        mask_bool = self.mask.bool()[:num_tokens_Q, :num_tokens_K]
```

&nbsp;


### 3. Xóa cache

Khi sinh văn bản giữa các chuỗi độc lập (ví dụ gọi hàm sinh nhiều lần), ta phải reset cả hai buffer; do đó thêm phương thức reset vào `MultiHeadAttention`:

```python
def reset_cache(self):
    self.cache_k, self.cache_v = None, None
    self.ptr_current_pos = 0
```

&nbsp;

### 4. Truyền `use_cache` qua mô hình

Với thay đổi ở `MultiHeadAttention`, ta cập nhật `GPTModel`: thêm tracking vị trí token:

```python
self.current_pos = 0
```

Thay vì gọi block một dòng, ta dùng vòng lặp rõ ràng để truyền `use_cache` vào từng transformer block:

```python
def forward(self, in_idx, use_cache=False):
    # ...
 
    if use_cache:
        pos_ids = torch.arange(
            self.current_pos, self.current_pos + seq_len,            
            device=in_idx.device, dtype=torch.long
        )
        self.current_pos += seq_len
    else:
        pos_ids = torch.arange(
            0, seq_len, device=in_idx.device, dtype=torch.long
        )
    
    pos_embeds = self.pos_emb(pos_ids).unsqueeze(0)
    x = tok_embeds + pos_embeds
    # ...
    for blk in self.trf_blocks:
        x = blk(x, use_cache=use_cache)
```

Thay đổi này yêu cầu `TransformerBlock` chấp nhận `use_cache`:
```
    def forward(self, x, use_cache=False):
        # ...
        self.att(x, use_cache=use_cache)
```

Cuối cùng, thêm một reset mô hình để xóa cache ở tất cả block:

```python
def reset_kv_cache(self):
    for blk in self.trf_blocks:
        blk.att.reset_cache()
    self.current_pos = 0
```

&nbsp;

### 5. Dùng cache khi sinh

Với các thay đổi ở `GPTModel`, `TransformerBlock`, `MultiHeadAttention`, ta dùng KV cache trong hàm sinh như sau:

```python
def generate_text_simple_cached(model, idx, max_new_tokens, 
                                context_size=None, use_cache=True):
    model.eval()
    ctx_len = context_size or model.pos_emb.num_embeddings

    with torch.no_grad():
        if use_cache:
            # Init cache with full prompt
            model.reset_kv_cache()
            logits = model(idx[:, -ctx_len:], use_cache=True)

            for _ in range(max_new_tokens):
                # a) pick the token with the highest log-probability (greedy sampling)
                next_idx = logits[:, -1].argmax(dim=-1, keepdim=True)
                # b) append it to the running sequence
                idx = torch.cat([idx, next_idx], dim=1)
                # c) feed model only the new token
                logits = model(next_idx, use_cache=True)
        else:
            for _ in range(max_new_tokens):
                logits = model(idx[:, -ctx_len:], use_cache=False)
                next_idx = logits[:, -1].argmax(dim=-1, keepdim=True)
                idx = torch.cat([idx, next_idx], dim=1)

    return idx
```

Lưu ý: ở c) ta chỉ đưa token mới vào `logits = model(next_idx, use_cache=True)`. Nếu không dùng cache, ta phải đưa toàn bộ đầu vào `logits = model(idx[:, -ctx_len:], use_cache=False)` vì không có key/value lưu sẵn.

&nbsp;
## So sánh hiệu năng đơn giản

Để thử nghiệm, chạy hai file Python trên để sinh 200 token với mô hình 124M (prompt 4 token "Hello, I am"):

```bash
pip install -r https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/refs/heads/main/requirements.txt

python gpt_ch04.py

python gpt_with_kv_cache.py
```

Trên Mac Mini M4 (CPU), kết quả ví dụ như sau:

|                        | Tokens/sec |
| ---------------------- | ---------- |
| `gpt_ch04.py`          | 27         |
| `gpt_with_kv_cache.py` | 144        |

Với ví dụ này, ta có ~5x tốc độ nhanh hơn cho mô hình 124M và dãy dài 200 token. (Lưu ý: triển khai ở đây ưu tiên dễ đọc mã, không tối ưu cho CUDA/MPS — tối ưu cần tiền cấp phát tensor thay vì liên tục nối.)

**Ghi chú:** Mô hình ở ví dụ chưa được huấn luyện nên sinh ra văn bản "gibberish".

Quan trọng hơn, cả `gpt_ch04.py` và `gpt_with_kv_cache.py` sinh cùng một kết quả, chứng tỏ KV cache được hiện thực đúng (các lỗi indexing có thể gây sai lệch kết quả).

&nbsp;
## Ưu và nhược điểm của KV cache

Khi độ dài dãy tăng, lợi ích và hạn chế của KV cache thể hiện rõ:

- [Tốt] **Tăng hiệu năng tính toán**: Nếu không cache, attention ở bước t phải so sánh query mới với t key trước đó, dẫn tới phức tạp tích lũy O(n²). Với cache, mỗi key/value chỉ tính một lần và tái sử dụng, giảm độ phức tạp mỗi bước xuống tuyến tính O(n).

- [Xấu] **Bộ nhớ tăng tuyến tính**: Mỗi token mới nối vào KV cache. Với dãy dài và mô hình lớn, KV cache có thể chiếm nhiều bộ nhớ (GPU) — có thể gây vấn đề. Một phương án là cắt ngắn cache (truncate) hoặc dùng cửa sổ trượt, nhưng điều này làm tăng độ phức tạp.


&nbsp;
## Tối ưu hoá KV Cache

Triển khai khái niệm ở trên rõ ràng nhưng để dùng thực tế (mô hình lớn, dãy dài) cần tối ưu cẩn thận.

&nbsp;
### Những lỗi phổ biến khi scale cache

- **Phân mảnh bộ nhớ và cấp phát lặp**: Liên tục `torch.cat` gây tắc nghẽn do cấp phát lại.

- **Bộ nhớ tăng tuyến tính**: Nếu không quản lý, cache có thể trở nên không thực tế cho dãy rất dài.

&nbsp;
#### Mẹo 1: Tiền cấp phát bộ nhớ

Thay vì nối lặp, tiền cấp phát một tensor đủ lớn theo độ dài tối đa kỳ vọng giúp ổn định bộ nhớ và giảm overhead:

```python
# Example pre-allocation for keys and values
max_seq_len = 1024  # maximum expected sequence length
cache_k = torch.zeros((batch_size, num_heads, max_seq_len, head_dim), device=device)
cache_v = torch.zeros((batch_size, num_heads, max_seq_len, head_dim), device=device)
```

Trong quá trình suy luận, ta chỉ ghi vào các lát (slices) của tensor đã cấp phát.

&nbsp;
#### Mẹo 2: Truncate cache bằng Sliding Window

Để tránh dùng hết bộ nhớ GPU, dùng cửa sổ trượt giữ lại chỉ `window_size` token cuối:

```python
# Sliding window cache implementation
window_size = 512
cache_k = cache_k[:, :, -window_size:, :]
cache_v = cache_v[:, :, -window_size:, :]
```

&nbsp;
#### Tối ưu trong thực tế

Các tối ưu này có trong file [`gpt_with_kv_cache_optimized.py`](gpt_with_kv_cache_optimized.py).

Trên Mac Mini M4 với sinh 200 token và cửa sổ bằng context length, kết quả so sánh:

|                                  | Tokens/sec |
| -------------------------------- | ---------- |
| `gpt_ch04.py`                    | 27         |
| `gpt_with_kv_cache.py`           | 144        |
| `gpt_with_kv_cache_optimized.py` | 166        |

Trên GPU, lợi ích có thể biến mất cho mô hình rất nhỏ do overhead truyền thiết bị.


&nbsp;
## Tài nguyên tham khảo

1. [Qwen3 from-scratch KV cache benchmarks](../../ch05/11_qwen3#pro-tip-2-speed-up-inference-with-compilation)
2. [Llama 3 from-scratch KV cache benchmarks](../../ch05/07_gpt_to_llama/README.md#pro-tip-3-speed-up-inference-with-compilation)
3. [Understanding and Coding the KV Cache in LLMs from Scratch](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)


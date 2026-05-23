# Chương 4: Hiện thực mô hình GPT từ đầu để sinh văn bản

&nbsp;
## Mã chính của chương

- [01_main-chapter-code](01_main-chapter-code) chứa mã chính của chương.

&nbsp;
## Tài liệu bổ sung

- [02_performance-analysis](02_performance-analysis) chứa mã tùy chọn phân tích hiệu năng các mô hình GPT hiện thực trong chương chính
- [03_kv-cache](03_kv-cache) hiện thực KV cache để tăng tốc sinh văn bản khi suy luận
- [07_moe](07_moe) giải thích và hiện thực Mixture-of-Experts (MoE)
- [ch05/07_gpt_to_llama](../ch05/07_gpt_to_llama) hướng dẫn từng bước chuyển một triển khai GPT sang Llama 3.2 và tải trọng số đã tiền huấn luyện từ Meta AI (có thể khám phá kiến trúc thay thế sau chương 4 hoặc để sau khi đọc chương 5)


&nbsp;
## Các lựa chọn Attention thay thế

&nbsp;

<img src="https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/attention-alternatives/attention-alternatives.webp">

&nbsp;

- [04_gqa](04_gqa) giới thiệu Grouped-Query Attention (GQA), được dùng bởi nhiều LLM hiện đại như Llama 4, gpt-oss, Qwen3, Gemma 3, ... như một thay thế cho Multi-Head Attention (MHA)
- [05_mla](05_mla) giới thiệu Multi-Head Latent Attention (MLA), dùng trong DeepSeek V3
- [06_swa](06_swa) giới thiệu Sliding Window Attention (SWA), được dùng bởi Gemma 3 và các mô hình khác
- [08_deltanet](08_deltanet) giải thích Gated DeltaNet, một biến thể linear attention phổ biến (dùng trong Qwen3-Next và Kimi Linear)
- [10_kv-sharing](10_kv-sharing) giới thiệu chia sẻ KV giữa các lớp để giảm bộ nhớ KV-cache (dùng trong Gemma 4 E2B và E4B)


&nbsp;
## Thêm

Video dưới đây là buổi code-along bổ sung cho nội dung chương.

<br>
<br>

[![Link to the video](https://img.youtube.com/vi/YSAkgEarBGE/0.jpg)](https://www.youtube.com/watch?v=YSAkgEarBGE)

# Hướng dẫn khắc phục sự cố

Trang này tổng hợp các vấn đề thường gặp và mẹo cấu hình khi làm theo cuốn sách.

&nbsp;
## Vấn đề tải ảnh trong notebook

Các notebook trong các chương sử dụng liên kết ảnh Markdown được host tại `https://sebastianraschka.com/images/LLMs-from-scratch-images/...`. Điều này giúp giữ kích thước repo ở mức hợp lý, nhưng đồng nghĩa ảnh phụ thuộc vào máy chủ ảnh và kết nối mạng của bạn.

Nếu ảnh trong các `.ipynb` không hiển thị:

- Mở trực tiếp một trong các URL ảnh trong trình duyệt, ví dụ [https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/02.webp](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/02.webp).
- Nếu URL không tải trong trình duyệt, vấn đề có thể là do website tạm thời, DNS, VPN, proxy, firewall, hoặc mạng cục bộ chứ không phải notebook.
- Kiểm tra URL trên thiết bị hoặc mạng khác (ví dụ, mở ảnh trên điện thoại); nếu ảnh hiển thị trên điện thoại, có thể do VPN hoặc firewall trên máy tính của bạn.
- Nếu ảnh cũng không hiển thị trên điện thoại, vui lòng mở một GitHub [Issue](https://github.com/rasbt/LLMs-from-scratch/issues) để tôi hỗ trợ gỡ lỗi.

&nbsp;
## Giữ thay đổi cá nhân cho notebook khi cập nhật repository

Nếu bạn muốn chỉnh sửa notebook nhưng vẫn nhận được cập nhật từ repository, hãy fork repo trước rồi clone fork của bạn. Các notebook chính của cuốn sách được đồng bộ với bản in và thường không thay đổi, trừ các sửa lỗi quan trọng. Hầu hết cập nhật repo là thêm tài liệu bổ sung.

Notebook là file JSON, nên diff và xung đột merge có thể khó đọc. Để tránh xung đột không cần thiết, tôi khuyên bạn giữ thí nghiệm riêng biệt khỏi các notebook theo dõi của sách:

- Sao chép notebook trước khi chỉnh sửa, ví dụ từ `ch02.ipynb` sang `ch02_experiments.ipynb`.
- Giữ các notebook thử nghiệm trong thư mục riêng hoặc trên branch riêng.
- Thêm remote `upstream` trỏ tới repo gốc để fetch cập nhật, sau đó merge hoặc rebase khi cần.

Để fork và clone:

1. Mở [https://github.com/rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch).
2. Nhấn nút **Fork** ở góc trên bên phải trên GitHub.
3. Clone fork của bạn, thay `YOUR-USERNAME` bằng tên GitHub của bạn:

```bash
git clone https://github.com/YOUR-USERNAME/LLMs-from-scratch.git
cd LLMs-from-scratch
```

Sau đó thêm repo gốc làm `upstream` để fetch cập nhật:

```bash
git remote add upstream https://github.com/rasbt/LLMs-from-scratch.git
git fetch upstream
git merge upstream/main
```

Nếu bạn cần merge các notebook đã chỉnh sửa, hãy cân nhắc cài đặt [`nbdime`](https://nbdime.readthedocs.io/) để có diff và công cụ merge theo notebook:

```bash
pip install nbdime
nbdime config-git --enable
```

Xem thêm: [#1015](https://github.com/rasbt/LLMs-from-scratch/issues/1015).

&nbsp;
## Apple Silicon và hỗ trợ MPS

Một số notebook và script sử dụng `cuda` khi có và fallback về `cpu` nếu không có, mà không chọn backend `mps` của Apple. Việc không tích hợp `mps` ở nhiều chỗ là có chủ đích vì các phiên bản PyTorch/MPS trước đây có thể tạo ra kết quả không ổn định hoặc khác biệt trong vài ví dụ, đặc biệt khi training và finetuning.

Nếu bạn dùng Mac Apple Silicon và thấy loss khác kỳ vọng, spike, hoặc text sinh không tốt, chạy lại ví dụ trên `cpu` trước. Để huấn luyện nhanh hơn và khớp kết quả với sách, tôi khuyến nghị dùng `cuda` trên GPU NVIDIA cục bộ hoặc cloud GPU.

Phiên bản PyTorch mới hơn có thể cải thiện hành vi MPS; bạn có thể thử nghiệm `mps` cục bộ nếu xác thực kết quả cẩn thận. Nếu bạn thêm `mps` vào script, nhớ kiểm tra các tuỳ chọn CUDA như `pin_memory=True`, `torch.compile`, và code DDP/multi-GPU có thể cần điều kiện riêng.

Xem thêm: [#977](https://github.com/rasbt/LLMs-from-scratch/issues/977), [#625](https://github.com/rasbt/LLMs-from-scratch/discussions/625), [#644](https://github.com/rasbt/LLMs-from-scratch/discussions/644), [#442](https://github.com/rasbt/LLMs-from-scratch/discussions/442), và [#846](https://github.com/rasbt/LLMs-from-scratch/issues/846).

&nbsp;
## Các vấn đề khác

Với các vấn đề khác, vui lòng mở GitHub [Issue](https://github.com/rasbt/LLMs-from-scratch/issues).

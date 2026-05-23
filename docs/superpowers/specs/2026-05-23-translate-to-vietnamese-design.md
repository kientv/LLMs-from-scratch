---
title: Dịch sang tiếng Việt (keep code & terms in English)
date: 2026-05-23
---

Mục tiêu
- Dịch toàn bộ tài liệu Markdown của repo sang tiếng Việt, nhưng giữ nguyên mọi đoạn code, `inline code`, và các thuật ngữ kỹ thuật ở tiếng Anh.

Phạm vi
- Bao gồm: tất cả file `*.md` trong repository. Notebook (`.ipynb`) cũng được hỗ trợ theo nguyên tắc bên dưới.
- Loại trừ: file code (`.py`, `.js`, ...), và các file nhị phân.

Nguyên tắc dịch
- Không sửa nội dung trong code blocks (``` ... ```). Giữ nguyên mọi câu lệnh, tên biến, và chú thích code bằng tiếng Anh.
- Không sửa `inline code` (một hoặc vài ký tự được bọc bằng backticks).
- Các thuật ngữ kỹ thuật (ví dụ: model, tokenizer, attention, loss, optimizer, checkpoint, kv-cache, BPE, DDP, API, CLI, README) giữ bằng tiếng Anh.
- Dịch phần mô tả, hướng dẫn, ví dụ văn bản, chú thích, và tiêu đề sang tiếng Việt.
- Giữ cấu trúc Markdown (headings, lists, tables) nguyên vẹn, chỉ thay nội dung văn bản.

Ghi chú về Notebook (`.ipynb`)
- Chỉ dịch nội dung trong Markdown cells; giữ nguyên toàn bộ nội dung của code cells (không sửa code) và outputs.
- Không thay đổi cấu trúc JSON của notebook (cell order, metadata, outputs) ngoài việc cập nhật nội dung trường `source` cho các Markdown cells.
- Khi dịch notebook, đảm bảo encoding UTF-8 và không phá hủy các khối mã hoặc metadata.

Chiến lược file
- Ghi đè file gốc trên một branch mới `translate-vi` (user chọn phương án B). Điều này giữ lịch sử gốc trong `main`/`origin` và cho phép PR/merge khi cần.
- Quy tắc commit: mỗi batch (ví dụ 20 file) commit riêng với message rõ ràng: `docs(vi): translate <n> files`.

Quy trình (high-level)
1. Tạo branch `translate-vi` từ `main`.
2. Dịch theo batch (ví dụ 20 file mỗi batch). Mỗi file: mở `*.md` -> dịch phần văn bản -> bảo toàn code/inline-code -> lưu.
3. Tạo commit cho batch, push lên remote, và tạo PR khi muốn xem xét.
4. Sau xong toàn bộ, mở PR để maintainers review.

Công cụ & xác minh
- Việc dịch sẽ do assistant thực hiện (dịch từng file). Sau mỗi batch, sẽ có review nhanh: kiểm tra code blocks không bị thay đổi, kiểm tra danh sách file đã dịch.
- Kiểm tra tự động: chạy `git status` và `git diff --check` để đảm bảo không có thay đổi ở những chỗ không mong muốn.

Truyền thông với bạn (user)
- Tôi sẽ bắt đầu bằng việc tạo file spec (file này) và commit lên nhánh `translate-vi`.
- Xin bạn xác nhận spec này trước khi tôi bắt tay vào dịch mẫu `ch01/README.md`.

Kết luận
- Nếu bạn đồng ý, tôi sẽ tiếp tục: dịch `ch01/README.md` làm mẫu và gửi bạn xem, rồi tiến theo batch.

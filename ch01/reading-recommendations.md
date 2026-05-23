# Lời khuyên để tận dụng tối đa một cuốn sách kỹ thuật

Dưới đây là một vài ghi chú tôi đã chia sẻ trước đây khi bạn đọc hỏi cách tận dụng tốt nhất cuốn sách "building large language model from scratch" của tôi.

Tôi thường áp dụng cách tiếp cận tương tự khi đọc các sách kỹ thuật. Đây không phải là công thức bắt buộc, nhưng có thể là điểm khởi đầu hữu ích.

Với cuốn sách này, tôi khuyến nghị đọc theo thứ tự vì mỗi chương có phụ thuộc vào chương trước. Với mỗi chương, tôi đề xuất các bước sau.

&nbsp;
### 1) Đọc lần đầu (offline)

Tôi khuyên bạn đọc cả chương từ đầu đến cuối trước khi bắt đầu viết mã.
Mục tiêu của lần đọc đầu tiên là nắm được bức tranh tổng thể.

Lý tưởng nhất là đọc chương xa máy tính. Bản in sẽ giúp tập trung tốt,
nhưng thiết bị số không có các yếu tố gây phân tâm (không mở trình duyệt, mạng xã hội hay email) cũng được.

Cá nhân tôi đọc cả trên giấy và trên tablet e-ink. Dù tôi đã dùng tablet e-ink từ 2018 và cố gắng đọc nhiều trên e-ink hơn, tôi vẫn thấy bản in giúp tôi tập trung hơn. Đó là lý do đôi khi tôi in các bài nghiên cứu khó hiểu hoặc muốn đọc kỹ.

Tôi đề nghị lần đọc đầu nên là một phiên ngắn, tập trung khoảng 20 phút với ít phân tâm và không quá sa đà vào chi tiết.

Ghi chú hoặc đánh dấu những phần gây bối rối hay thú vị là ổn, nhưng giai đoạn này không nên tìm kiếm câu trả lời ngay. Chỉ đọc thôi, chưa chạy mã. Lần đọc đầu nhằm để hiểu bức tranh lớn.

&nbsp;
### 2) Đọc lần hai (với mã nguồn)

Ở lần đọc thứ hai, tôi khuyên bạn gõ lại và chạy mã từ chương. Sao chép mã là cách dễ dàng hơn vì gõ lại tốn thời gian, nhưng khi đọc sách kỹ thuật khác, việc gõ lại thường giúp tôi suy nghĩ kỹ hơn về mã (thay vì chỉ lướt qua).

Nếu kết quả khác với sách, hãy kiểm tra repo GitHub của sách và thử chạy mã từ repo đó. Nếu vẫn khác, kiểm tra các nguyên nhân như phiên bản thư viện, random seed, CPU/CUDA, v.v. Nếu vẫn chưa rõ, bạn có thể hỏi tác giả (qua diễn đàn sách, issues/discussions trên GitHub, hoặc email như lựa chọn sau cùng).

&nbsp;
### 3) Bài tập

Sau lần đọc thứ hai, gõ lại và chạy mã, đây thường là lúc thích hợp để thử các bài tập. Việc này giúp củng cố hiểu biết hoặc thử nghiệm một vấn đề theo cách có cấu trúc. Nếu bài tập quá khó, có thể xem lời giải, nhưng nên cố gắng tự làm trước.

&nbsp;
### 4) Rà soát ghi chú và tìm hiểu thêm

Sau khi đọc chương, chạy mã và làm bài tập, hãy quay lại các phần đã đánh dấu và xem còn điểm nào chưa rõ.

Đây cũng là lúc tốt để tra cứu thêm tài liệu tham khảo hoặc tìm kiếm nhanh để làm rõ những điều còn mơ hồ. Ngay cả khi mọi thứ đã rõ, đọc thêm về chủ đề quan tâm cũng không phải là ý tồi.

Ở giai đoạn này, bạn cũng nên ghi lại hoặc chuyển các hiểu biết, đoạn mã hữu ích vào ứng dụng ghi chú ưa thích.

&nbsp;
### 5) Áp dụng ý tưởng vào dự án

Các bước trước tập trung vào tiếp thu kiến thức. Bây giờ, hãy thử áp dụng một khía cạnh nào đó của chương vào dự án cá nhân. Hoặc xây dựng một dự án nhỏ lấy mã trong sách làm điểm bắt đầu. Để tìm cảm hứng, xem các tài liệu bổ sung (bonus materials) — đó là các dự án nhỏ tôi làm để thỏa mãn tò mò.

Ví dụ, sau khi học về cơ chế multi-head attention và triển khai LLM, bạn có thể tự hỏi một mô hình với grouped-query attention hoạt động thế nào, hoặc sự khác biệt giữa RMSNorm và LayerNorm có lớn không. Và còn nhiều ví dụ khác.

Cũng có những chi tiết nhỏ hữu ích cho dự án, ví dụ thử xem việc
gọi `torch.mps.manual_seed(seed)` có khác gì
so với chỉ gọi `torch.manual_seed(seed)` hay không.

Cuối cùng, tôi muốn bạn áp dụng kiến thức. Điều này có thể là dùng khái niệm chính từ chương, nhưng cũng có thể là những mẹo nhỏ học được trên đường đi, ví dụ như có nên gọi
`torch.mps.manual_seed(seed)` thay vì `torch.manual_seed(seed)` trong dự án của bạn.

&nbsp;
### Một vài suy nghĩ bổ sung

Tất nhiên, những điều trên không phải là bắt buộc. Nếu chủ đề đã rất quen thuộc hoặc đơn giản, và bạn chỉ đọc để lấy thông tin cho chương sau, lướt qua chương cũng được.

Với các chương không có mã (ví dụ chương giới thiệu 1), tất nhiên có thể bỏ qua các bước liên quan đến mã.

Hy vọng những gợi ý này hữu ích. Chúc bạn đọc và học vui vẻ!
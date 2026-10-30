# HƯỚNG DẪN TRÌNH BÀY VÀ CÂU HỎI PHỎNG VẤN

## Bài giới thiệu 60–90 giây
“Em xây dựng một dự án AI/NLP phân tích cảm xúc đánh giá tiếng Việt. Mục tiêu là nhận một câu đánh giá và phân loại thành tích cực, tiêu cực hoặc trung lập. Em dùng Python, pandas, scikit-learn và Streamlit. Pipeline gồm làm sạch dữ liệu cơ bản, chuyển văn bản thành vector bằng TF-IDF, sau đó dùng Logistic Regression để phân loại. Em tách train/test, đánh giá bằng Accuracy, Precision, Recall, F1-score và confusion matrix, rồi lưu pipeline bằng joblib để giao diện Streamlit nạp lại. Hiện tại dữ liệu đi kèm là dữ liệu demo tự biên soạn nên em không coi các chỉ số đó là kết quả triển khai thực tế. Hướng phát triển của em là thay bằng dataset tiếng Việt có nguồn rõ ràng, so sánh với Linear SVM/PhoBERT và đóng gói API bằng FastAPI hoặc Docker.”

## Câu hỏi thường gặp

### 1. AI giải quyết vấn đề gì?
Tự động phân loại phản hồi để hỗ trợ tổng hợp ý kiến và ưu tiên phản hồi tiêu cực. Đây là công cụ hỗ trợ, không thay thế quyết định của nhân viên.

### 2. Vì sao chọn bài toán này?
Bài toán thực tế, dễ trình diễn, có quy trình ML rõ ràng và có thể mở rộng từ baseline đến mô hình ngôn ngữ hiện đại.

### 3. TF-IDF là gì?
Là cách biến văn bản thành vector số. Từ xuất hiện nhiều trong một tài liệu nhưng phổ biến ở mọi tài liệu thường có trọng số thấp hơn từ/cụm từ có tính phân biệt cao.

### 4. Vì sao dùng Logistic Regression?
Nhanh, dễ làm baseline, hỗ trợ phân loại nhiều lớp và kết hợp tốt với vector TF-IDF. Sau này có thể so sánh Linear SVM hoặc mô hình transformer.

### 5. Vì sao dùng train/test?
Train để mô hình học; test để ước lượng khả năng tổng quát hóa trên dữ liệu chưa dùng khi huấn luyện. Không được dùng test để chọn mô hình lặp đi lặp lại mà không có validation.

### 6. Accuracy có đủ không?
Không. Nếu dữ liệu lệch lớp, accuracy có thể cao dù bỏ sót lớp quan trọng. Cần xem Precision, Recall, F1 từng lớp và confusion matrix.

### 7. Overfitting là gì?
Mô hình học quá sát dữ liệu huấn luyện và hoạt động kém trên dữ liệu mới. Cách kiểm tra là so sánh train/validation/test, dùng cross-validation và dữ liệu đa dạng.

### 8. Tại sao dữ liệu demo nhỏ là vấn đề?
Nó không đại diện ngôn ngữ thực tế, dễ khiến chỉ số dao động lớn và không chứng minh mô hình sẵn sàng cho doanh nghiệp. Cần dữ liệu lớn hơn, có nguồn và nhãn được kiểm soát.

### 9. Mô hình xử lý câu mỉa mai thế nào?
Baseline TF-IDF thường yếu vì dựa vào từ/cụm từ. Có thể bổ sung dữ liệu mỉa mai, ngữ cảnh hội thoại hoặc thử PhoBERT; vẫn cần đánh giá lỗi thực tế.

### 10. Nếu mô hình dự đoán sai thì làm gì?
Thu thập lỗi đã ẩn danh, phân loại nguyên nhân, kiểm tra nhãn dữ liệu, bổ sung ví dụ, so sánh mô hình và đánh giá lại trên test độc lập. Không chỉ sửa theo vài ví dụ test rồi báo chỉ số trên cùng tập đó.

### 11. Pipeline là gì?
Pipeline gói vectorizer và classifier thành một chuỗi thống nhất, giúp huấn luyện và dự đoán dùng cùng cách biến đổi văn bản, tránh quên bước tiền xử lý.

### 12. Vì sao dùng Streamlit?
Dễ tạo demo web từ Python, phù hợp trình bày prototype nhanh mà không cần xây frontend riêng.

### 13. Nếu đưa vào doanh nghiệp thì bổ sung gì?
Dữ liệu có quyền sử dụng, bảo vệ dữ liệu cá nhân, API, xác thực, logging, monitoring, versioning, CI/CD, kiểm soát drift và cơ chế người thật xem lại dự đoán quan trọng.

### 14. Đóng góp cá nhân của em là gì?
Chỉ nêu đúng phần bạn tự làm. Ví dụ nếu tự làm toàn bộ: thiết kế pipeline, xử lý CSV, huấn luyện/đánh giá, xây UI, viết tài liệu và kiểm thử demo. Không nhận phần chưa thực hiện.

### 15. Điểm yếu của dự án?
Dữ liệu demo nhỏ, baseline không hiểu ngữ cảnh sâu, chưa triển khai cloud và chưa có monitoring. Em nêu rõ các hạn chế này và kế hoạch cải tiến.

## Không nên nói khi phỏng vấn
- Không tuyên bố độ chính xác 95%/99% nếu chưa chạy và chưa có test độc lập.
- Không gọi dữ liệu tự tạo là dữ liệu khách hàng thực tế.
- Không nói đã triển khai production nếu mới chạy local.
- Không nói mô hình “hiểu cảm xúc như con người”; đây là dự đoán thống kê dựa trên dữ liệu.

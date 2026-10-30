# Hướng dẫn phỏng vấn — AI Fraud Detection

## Giới thiệu 60–90 giây
“Em xây dựng ứng dụng phát hiện giao dịch có dấu hiệu bất thường bằng Python và scikit-learn. Người dùng tải CSV, hệ thống xử lý đặc trưng số và dùng Isolation Forest để gắn cờ điểm dữ liệu khác thường. Giao diện dùng Streamlit, có dashboard và lịch sử lưu MySQL qua PyMySQL. Em đánh giá bằng Precision, Recall, F1-score và confusion matrix khi có nhãn. Đây là prototype học tập; điểm anomaly không phải xác suất gian lận và không dùng để tự động chặn giao dịch thật.”

## Câu hỏi thường gặp
### Fraud detection là gì?
Phát hiện giao dịch có dấu hiệu gian lận hoặc bất thường để ưu tiên kiểm tra.

### Vì sao chọn Isolation Forest?
Mô hình không giám sát, có thể fit khi thiếu nhãn. Tuy nhiên anomaly không đồng nghĩa fraud.

### Isolation Forest hoạt động ra sao?
Tạo cây phân chia ngẫu nhiên. Điểm bị cô lập bằng ít lần chia thường được xem là bất thường. `predict` trả -1 cho anomaly, 1 cho inlier.

### Vì sao không chỉ dùng Accuracy?
Gian lận rất hiếm; dự đoán tất cả bình thường có thể vẫn cho Accuracy cao nhưng bỏ sót gian lận. Cần Precision, Recall, F1 và confusion matrix.

### Precision và Recall?
Precision = TP/(TP+FP): tỷ lệ cảnh báo đúng. Recall = TP/(TP+FN): tỷ lệ gian lận thật phát hiện được. F1 là trung bình điều hòa của Precision và Recall.

### False positive/negative?
False positive: giao dịch bình thường bị cảnh báo, tốn công kiểm tra. False negative: gian lận bị bỏ sót, có thể gây thiệt hại.

### Điểm rủi ro có phải xác suất?
Không. Điểm được biến đổi để xếp hạng bất thường, không được hiệu chuẩn thành xác suất.

### MySQL dùng để làm gì?
Lưu bản ghi giao dịch, nhãn dự đoán, điểm rủi ro, model name và thời gian; hỗ trợ lịch sử/dashboard.

### Làm sao tránh data leakage?
Cột `Class` bị loại khỏi đặc trưng trước khi fit. Tuy nhiên cần tập test độc lập để đánh giá đáng tin cậy hơn.

### Hạn chế?
Dữ liệu công khai có thể không đại diện dữ liệu thật; mô hình không hiểu toàn bộ ngữ cảnh nghiệp vụ; bản demo thiếu xác thực, giám sát drift và bảo vệ dữ liệu production.

### Nếu phát triển tiếp?
So sánh mô hình có giám sát, chia train/validation/test, tối ưu ngưỡng theo chi phí, thêm giải thích cảnh báo và kiểm thử tự động.

### Nếu được hỏi đã kiểm thử chưa?
Trả lời đúng thực tế. Chỉ nêu metrics sau khi chạy `evaluate_model.py`; không tuyên bố đã triển khai production nếu chưa làm.

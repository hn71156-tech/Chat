# Báo cáo dự án: AI Fraud Detection

## 1. Mục tiêu
Xây dựng ứng dụng hỗ trợ phát hiện giao dịch bất thường bằng Machine Learning. Người dùng tải CSV, mô hình phân tích đặc trưng, giao diện hiển thị kết quả và MySQL lưu lịch sử.

## 2. Bài toán
Giao dịch gian lận thường hiếm và có thể khác biệt so với giao dịch thông thường. Mục tiêu là ưu tiên các giao dịch cần kiểm tra, không kết luận tự động giao dịch nào chắc chắn gian lận.

## 3. Dữ liệu
Dùng bộ Kaggle Credit Card Fraud Detection (`creditcard.csv`). Các cột thường gồm `Time`, `Amount`, `V1`–`V28`, `Class`. Các cột V đã biến đổi nên không thể diễn giải trực tiếp như thuộc tính nghiệp vụ. Dữ liệu công khai không đại diện cho mọi tổ chức tài chính.

## 4. Thuật toán
Isolation Forest là mô hình không giám sát. Thuật toán tạo các phép chia ngẫu nhiên; điểm bị cô lập nhanh hơn có xu hướng bất thường. `predict()` trả -1 cho anomaly và 1 cho inlier. Ứng dụng chuyển thành nhãn 1/0. Điểm 0–1 trên UI được biến đổi từ decision function để xếp hạng, không phải xác suất gian lận hiệu chuẩn. Cột `Class` bị loại khỏi dữ liệu fit.

## 5. Kiến trúc
- Data: CSV và pandas.
- ML: scikit-learn Isolation Forest, lưu model bằng joblib.
- UI: Streamlit, biểu đồ Plotly.
- Database: PyMySQL kết nối MySQL/MariaDB XAMPP.
- Bảng: `transactions`, `model_runs`.

## 6. Luồng
1. Đọc CSV.
2. Nhận diện cột nhãn, thời gian, số tiền.
3. Chọn cột số, xử lý giá trị thiếu.
4. Căn chỉnh đặc trưng theo model và dự đoán.
5. Hiển thị kết quả.
6. Lưu vào MySQL.
7. Đọc lịch sử và tổng hợp dashboard.

## 7. Đánh giá
Dùng confusion matrix, Precision, Recall và F1-score khi có nhãn thật. Accuracy có thể gây hiểu nhầm do lớp gian lận hiếm. Recall đo tỷ lệ gian lận thật được phát hiện; Precision đo tỷ lệ cảnh báo đúng trong số các cảnh báo. Phải chạy `python evaluate_model.py` để lấy số liệu thực nghiệm; không tự ghi số chưa đo. Đánh giá trên cùng tập fit chưa thay thế kiểm thử độc lập.

## 8. Giới hạn và an toàn
Bản demo chưa có xác thực/phân quyền, mã hóa dữ liệu nhạy cảm, audit trail, monitoring drift hoặc quy trình production. Chỉ dùng dữ liệu công khai/ẩn danh, không lưu số thẻ/CVV. Mọi cảnh báo cần người kiểm tra.

## 9. Hướng phát triển
So sánh mô hình có giám sát nếu có nhãn tin cậy; kiểm thử theo thời gian; tối ưu ngưỡng theo chi phí; thêm explainability, API, kiểm thử tự động và giám sát drift.

## 10. Kết luận
Đồ án minh họa quy trình từ dữ liệu, huấn luyện, dự đoán, giao diện, SQL đến đánh giá. Khi trình bày phỏng vấn, cần giải thích được vì sao chọn thuật toán, cách đọc metrics, giới hạn dataset và hướng cải tiến.

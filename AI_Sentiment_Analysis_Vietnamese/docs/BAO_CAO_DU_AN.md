# BÁO CÁO DỰ ÁN: AI PHÂN TÍCH CẢM XÚC ĐÁNH GIÁ TIẾNG VIỆT

## 1. Tóm tắt
Dự án xây dựng ứng dụng NLP phân loại câu đánh giá thành ba nhóm: tích cực, tiêu cực và trung lập. Mục tiêu là minh họa quy trình AI hoàn chỉnh từ dữ liệu, tiền xử lý, huấn luyện, đánh giá đến giao diện demo.

## 2. Bối cảnh và vấn đề
Doanh nghiệp có thể nhận hàng nghìn phản hồi từ khách hàng. Đọc thủ công tốn thời gian và khó theo dõi xu hướng. Phân tích cảm xúc có thể hỗ trợ nhóm chăm sóc khách hàng ưu tiên phản hồi tiêu cực, theo dõi trải nghiệm và tổng hợp báo cáo. Mô hình chỉ hỗ trợ ra quyết định, không thay thế nhân viên.

## 3. Mục tiêu
- Xây dựng pipeline NLP có thể tái huấn luyện.
- Phân loại văn bản tiếng Việt theo ba nhãn.
- Cung cấp giao diện nhập câu và xem kết quả.
- Lưu mô hình và báo cáo đánh giá.
- Có tài liệu giải thích được lựa chọn kỹ thuật và hạn chế.

## 4. Phạm vi và yêu cầu
### Chức năng
1. Đọc dữ liệu CSV có cột `text`, `label`.
2. Làm sạch dữ liệu cơ bản: loại hàng thiếu, bỏ khoảng trắng, loại câu trùng.
3. Chia dữ liệu train/test có stratify.
4. Huấn luyện TF-IDF + Logistic Regression.
5. Lưu pipeline, accuracy và classification report.
6. Nhập văn bản qua Streamlit và hiển thị nhãn dự đoán.

### Phi chức năng
- Chạy cục bộ trên máy tính.
- Cấu trúc mã dễ hiểu và tái sử dụng.
- Có thông báo nếu chưa huấn luyện mô hình.
- Nêu rõ giới hạn của mô hình và dữ liệu demo.

## 5. Dữ liệu
`data/reviews.csv` có hai cột:
- `text`: nội dung đánh giá
- `label`: `positive`, `negative`, `neutral`

Dữ liệu đi kèm được tự biên soạn để chạy thử, có quy mô nhỏ. Đây không phải bộ dữ liệu đại diện cho thị trường. Khi triển khai thật, cần thay bằng dữ liệu có nguồn, giấy phép rõ ràng, đủ đa dạng và được gán nhãn theo hướng dẫn thống nhất.

## 6. Phương pháp
### 6.1 TF-IDF
TF-IDF biểu diễn văn bản thành vector số dựa trên mức độ xuất hiện của từ/cụm từ và độ hiếm của chúng trong tập tài liệu. Dự án dùng unigram và bigram để giữ một số cụm từ như “rất tốt”, “không hài lòng”.

### 6.2 Logistic Regression
Mô hình học mối quan hệ giữa vector TF-IDF và nhãn cảm xúc. Đây là baseline phù hợp vì huấn luyện nhanh, tương đối dễ giải thích và hoạt động tốt với nhiều bài toán phân loại văn bản.

### 6.3 Quy trình
1. Đọc CSV.
2. Làm sạch tối thiểu.
3. Chia train/test.
4. Fit pipeline trên train.
5. Dự đoán tập test.
6. Tính Accuracy, Precision, Recall, F1 và confusion matrix.
7. Lưu pipeline.
8. Nạp pipeline trong Streamlit để dự đoán câu mới.

## 7. Kiến trúc
Người dùng → Streamlit UI → pipeline đã lưu → TF-IDF vectorizer → Logistic Regression → nhãn dự đoán và điểm xác suất tương đối.

## 8. Đánh giá
Dùng Accuracy để có cái nhìn tổng quát; Precision/Recall/F1 theo từng lớp để thấy mô hình có bỏ sót lớp nào không; confusion matrix để xác định các lớp hay bị nhầm lẫn. Không ghi sẵn một con số kết quả vì phải chạy huấn luyện mới sinh ra chỉ số. Dữ liệu demo nhỏ nên kết quả chỉ nhằm kiểm tra luồng kỹ thuật.

## 9. Kết quả bàn giao
- Mã nguồn ứng dụng và huấn luyện.
- CSV demo.
- Mô hình `models/sentiment_pipeline.joblib` sau khi train.
- Báo cáo trong `reports/`.
- Tài liệu cài đặt, demo và hỏi đáp phỏng vấn.

## 10. Hạn chế
- Dữ liệu ít và tự biên soạn.
- Khó hiểu mỉa mai, phủ định phức tạp, tiếng lóng, viết tắt và câu có nhiều cảm xúc.
- TF-IDF không nắm bắt ngữ cảnh sâu như mô hình ngôn ngữ hiện đại.
- Xác suất Logistic Regression không đảm bảo là độ tin cậy được hiệu chuẩn.
- Chưa có API, xác thực người dùng, monitoring hay triển khai cloud.

## 11. Hướng phát triển
- Dùng dataset tiếng Việt công khai có nguồn và giấy phép phù hợp.
- So sánh Naive Bayes, Linear SVM, Logistic Regression và PhoBERT.
- Thêm kiểm tra dữ liệu lệch lớp, cross-validation và tuning.
- Xây API FastAPI, Docker, logging, versioning.
- Thu thập phản hồi người dùng và đánh giá drift theo thời gian.

## 12. Đạo đức và quyền riêng tư
Ẩn danh thông tin cá nhân trong đánh giá. Chỉ sử dụng dữ liệu có quyền xử lý. Không tự động đưa ra quyết định bất lợi cho khách hàng chỉ dựa trên một nhãn dự đoán. Cần có người kiểm tra các trường hợp quan trọng.

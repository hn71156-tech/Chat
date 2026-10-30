# AI Sentiment Analysis – Phân tích cảm xúc đánh giá khách hàng

Dự án AI/NLP nhỏ theo hướng end-to-end, phù hợp để học, đưa lên GitHub và trình bày phỏng vấn thực tập.

## 1. Bài toán
Nhận một câu đánh giá tiếng Việt và dự đoán cảm xúc:
- `positive`: tích cực
- `negative`: tiêu cực
- `neutral`: trung lập

Ứng dụng minh họa cho việc tổng hợp phản hồi khách hàng trong thương mại điện tử, nhà hàng hoặc dịch vụ.

> Lưu ý: `data/reviews.csv` là dữ liệu mẫu tự biên soạn để chạy demo. Không nên trình bày kết quả trên dữ liệu mẫu này như kết quả nghiên cứu thực tế. Muốn đánh giá nghiêm túc, hãy thay bằng bộ dữ liệu có nguồn rõ ràng và kiểm tra giấy phép sử dụng.

## 2. Công nghệ
- Python
- pandas: đọc và xử lý dữ liệu
- scikit-learn: TF-IDF, Logistic Regression, chia tập và đánh giá
- Streamlit: giao diện web demo
- joblib: lưu/tải pipeline đã huấn luyện
- matplotlib: biểu đồ đánh giá

## 3. Cấu trúc thư mục
```text
AI_Sentiment_Analysis_Vietnamese/
├── app.py
├── train_model.py
├── evaluate_model.py
├── requirements.txt
├── data/
│   └── reviews.csv
├── models/              # được tạo sau khi chạy train_model.py
├── reports/             # được tạo sau khi chạy train_model.py
└── docs/
    ├── BAO_CAO_DU_AN.md
    ├── HUONG_DAN_PHONG_VAN.md
    ├── KICH_BAN_DEMO.md
    └── CV_GITHUB.md
```

## 4. Cài đặt trên Windows
Mở Terminal/PowerShell trong thư mục project:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

Nếu PowerShell chặn kích hoạt môi trường ảo, có thể bỏ qua bước activate và dùng:
```powershell
py -m pip install -r requirements.txt
py train_model.py
py -m streamlit run app.py
```

Trình duyệt thường mở tại `http://localhost:8501`.

## 5. Chạy đánh giá
```powershell
python evaluate_model.py
```
Kết quả được ghi vào `reports/metrics.json` và `reports/classification_report.txt`. Do dữ liệu demo nhỏ, các chỉ số chỉ dùng để kiểm tra pipeline, không phản ánh chất lượng triển khai thật.

## 6. Quy trình AI
1. Đọc dữ liệu đánh giá đã gán nhãn.
2. Kiểm tra dữ liệu thiếu/trùng và phân bố nhãn.
3. Chia train/test có stratify.
4. Dùng TF-IDF để chuyển văn bản thành vector số.
5. Dùng Logistic Regression phân loại.
6. Đánh giá bằng Accuracy, Precision, Recall, F1-score và confusion matrix.
7. Lưu pipeline để ứng dụng sử dụng.
8. Nhập câu mới trên giao diện Streamlit để dự đoán.

## 7. Điểm cần cải thiện trước khi đưa vào sản phẩm
- Thay dữ liệu mẫu bằng dataset lớn, có nguồn và giấy phép phù hợp.
- Tạo tập test độc lập, tránh trùng lặp câu giữa train/test.
- Thử baseline Naive Bayes, Linear SVM và mô hình tiếng Việt pretrained như PhoBERT.
- Theo dõi phản hồi sai, xử lý tiếng lóng, teencode, mỉa mai và câu có nhiều cảm xúc.
- Không gửi dữ liệu khách hàng nhạy cảm vào hệ thống demo.
- Triển khai bằng Docker/Cloud, thêm logging, versioning và kiểm soát truy cập nếu cần.

## 8. Tài khoản / dữ liệu
Không cần API key, không cần cơ sở dữ liệu và không cần Internet khi đã cài dependencies.

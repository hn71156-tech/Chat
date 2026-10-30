# AI Fraud Detection — Python, Streamlit, MySQL/XAMPP

Đồ án học tập phát hiện giao dịch có dấu hiệu bất thường bằng Isolation Forest. Có dashboard, tải CSV, phân tích, lịch sử lưu MySQL và xuất kết quả.

> Đây là prototype học tập, không phải hệ thống production. Gắn cờ bất thường không chứng minh gian lận. Không dùng để tự động chặn giao dịch thật hoặc nhập thông tin thẻ cá nhân.

## Công nghệ
Python, pandas, scikit-learn, Isolation Forest, Streamlit, Plotly, PyMySQL, MySQL/XAMPP, joblib.

## Yêu cầu
Windows 10/11, Python 3.10–3.12 khuyến nghị, XAMPP/MySQL, dataset công khai Kaggle **Credit Card Fraud Detection** (`creditcard.csv`).

## Cài đặt trên Windows
### 1. Giải nén và mở PowerShell
Giải nén vào ví dụ `C:\Users\ADMIN\Downloads\AI_Fraud_Detection_MySQL`. Mở PowerShell ở thư mục gốc và chạy `dir`. Phải thấy `app.py`, `requirements.txt`, `train_model.py`.

### 2. Tạo môi trường và cài thư viện
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
Nếu Python 3.12 không có, thử `py -m venv .venv`. Nếu bị chặn activate:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Tải dataset công khai
Trên Kaggle tìm **Credit Card Fraud Detection**, tải `creditcard.csv` theo điều khoản của nguồn. Đặt file vào `data\creditcard.csv`. File dữ liệu không kèm trong ZIP và đã được loại khỏi Git bằng `.gitignore`.

### 4. Huấn luyện AI
```powershell
python train_model.py
```
Mô hình dự kiến lưu tại `models\isolation_forest.joblib`. Chạy nhanh trên mẫu:
```powershell
python train_model.py --sample 20000
```
Đây là kết quả mong đợi nếu dữ liệu và thư viện cài đúng, không phải xác nhận đã chạy trên máy của bạn.

### 5. Tạo database trong XAMPP
1. Mở XAMPP Control Panel, bấm **Start** ở dòng MySQL.
2. Mở `http://localhost/phpmyadmin` (hoặc địa chỉ/cổng phpMyAdmin của bạn).
3. Chọn **Import**, chọn file `sql\schema.sql`, bấm **Go/Import**.
4. Database `fraud_detection_db` và hai bảng sẽ được tạo.

### 6. Cấu hình kết nối
```powershell
Copy-Item .env.example .env
notepad .env
```
Cấu hình mặc định thường gặp với XAMPP:
```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=fraud_detection_db
DB_USER=root
DB_PASSWORD=
```
Nếu MySQL dùng cổng khác hoặc tài khoản có mật khẩu, sửa `.env`. Không đưa `.env` lên GitHub.

### 7. Chạy ứng dụng
```powershell
python -m streamlit run app.py
```
Mở URL Streamlit được in trong PowerShell, thường là `http://localhost:8501`. Giữ cửa sổ PowerShell mở.

### 8. Demo
- Bấm **Kiểm tra kết nối MySQL** trong sidebar.
- Tab **Phân tích**, tải CSV hoặc dùng `data/creditcard.csv`.
- Bấm **Chạy AI và lưu vào MySQL**.
- Xem Dashboard và Lịch sử.
- Xuất kết quả thành CSV.

### 9. Đánh giá mô hình
```powershell
python evaluate_model.py
```
Dataset phải có nhãn `Class` (0/1). Nhãn chỉ dùng để đánh giá, không dùng để fit Isolation Forest. Xem Precision, Recall, F1-score và confusion matrix; với dữ liệu mất cân bằng, Accuracy đơn lẻ dễ gây hiểu nhầm. Đánh giá trên dữ liệu đã dùng để fit chỉ là tham khảo ban đầu, không thay thế test độc lập.

## Cấu trúc
```text
AI_Fraud_Detection_MySQL/
├── app.py
├── db.py
├── fraud_utils.py
├── train_model.py
├── evaluate_model.py
├── requirements.txt
├── .env.example
├── sql/schema.sql
├── data/creditcard.csv     # tự tải, không kèm ZIP
├── models/                 # model sau khi train
└── docs/
    ├── BAO_CAO_DU_AN.md
    ├── HUONG_DAN_PHONG_VAN.md
    └── KICH_BAN_DEMO.md
```

## Kiến trúc
```text
Kaggle CSV -> pandas -> Isolation Forest -> nhãn + điểm anomaly
                                      |-> Streamlit / Plotly
                                      `-> PyMySQL -> MySQL/XAMPP -> History / Dashboard
```

## Cấu trúc SQL
- `transactions`: giao dịch, nhãn thật nếu có, nhãn dự đoán, điểm rủi ro, model, thời điểm lưu.
- `model_runs`: thông tin mỗi lượt chạy.
Ứng dụng lưu bản ghi mới mỗi lần phân tích; chưa chống trùng khi tải cùng file nhiều lần.

## Lỗi thường gặp
- `requirements.txt not found`: PowerShell chưa ở đúng thư mục; dùng `dir` kiểm tra.
- `No module named streamlit`: kích hoạt `.venv`, chạy `python -m pip install -r requirements.txt`.
- Lỗi MySQL: bật MySQL trong XAMPP, kiểm tra `.env`, port và import `sql/schema.sql`.
- `Access denied`: kiểm tra user/password trong `.env`.
- `Model missing`: đặt CSV vào `data` và chạy `python train_model.py`.
- Không có cột số: CSV cần đặc trưng dạng số.
- Port Streamlit đang bận: `python -m streamlit run app.py --server.port 8502`.

## Hướng phát triển
So sánh với Logistic Regression/Random Forest trên dữ liệu có nhãn; chia train/validation/test hợp lý; tối ưu ngưỡng theo chi phí FP/FN; thêm giải thích cảnh báo, API, xác thực, phân quyền và monitoring drift.

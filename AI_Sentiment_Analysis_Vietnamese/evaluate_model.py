from pathlib import Path
import json
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parent

def main():
    data = pd.read_csv(ROOT / "data" / "reviews.csv").dropna(subset=["text", "label"])
    model_path = ROOT / "models" / "sentiment_pipeline.joblib"
    if not model_path.exists():
        raise FileNotFoundError("Chưa có model. Hãy chạy: python train_model.py")
    model = joblib.load(model_path)
    pred = model.predict(data["text"].astype(str))
    print("Lưu ý: đây là đánh giá trên toàn bộ dữ liệu demo, có thể gồm dữ liệu model đã học.")
    print("Không dùng kết quả này làm chỉ số test độc lập.")
    print(classification_report(data["label"].astype(str), pred, zero_division=0))
    print("Accuracy trên toàn bộ demo:", round(accuracy_score(data["label"].astype(str), pred), 3))

if __name__ == "__main__":
    main()

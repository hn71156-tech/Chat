import argparse
from pathlib import Path
import joblib, pandas as pd
from sklearn.ensemble import IsolationForest
from fraud_utils import prepare_features
ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",default=str(ROOT/"data"/"creditcard.csv"))
    p.add_argument("--contamination",type=float,default=.002)
    p.add_argument("--sample",type=int,default=0)
    a=p.parse_args(); path=Path(a.data)
    if not path.exists(): raise SystemExit(f"Không thấy {path}. Tải creditcard.csv theo hướng dẫn README.md.")
    df=pd.read_csv(path)
    if a.sample>0 and len(df)>a.sample: df=df.sample(a.sample,random_state=42)
    x,_,label=prepare_features(df)
    model=IsolationForest(n_estimators=200,contamination=a.contamination,random_state=42,n_jobs=-1)
    model.fit(x)
    dest=ROOT/"models"/"isolation_forest.joblib"; dest.parent.mkdir(exist_ok=True)
    joblib.dump(model,dest)
    print(f"Rows: {len(df):,} | Features: {len(x.columns)} | Label column (not used in training): {label}")
    print(f"Model saved: {dest}")
    print("Caution: anomaly score is a ranking, not a calibrated fraud probability.")
if __name__=="__main__": main()

import argparse
from pathlib import Path
import joblib,pandas as pd
from sklearn.metrics import classification_report,confusion_matrix,precision_score,recall_score,f1_score
from fraud_utils import prepare_features,predict_dataframe
ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser(); p.add_argument("--data",default=str(ROOT/"data"/"creditcard.csv")); p.add_argument("--sample",type=int,default=0); a=p.parse_args()
    path=Path(a.data); mp=ROOT/"models"/"isolation_forest.joblib"
    if not path.exists(): raise SystemExit(f"Missing dataset: {path}. See README.md.")
    if not mp.exists(): raise SystemExit("Model missing. Run python train_model.py")
    df=pd.read_csv(path)
    if a.sample>0 and len(df)>a.sample: df=df.sample(a.sample,random_state=42)
    _,_,label=prepare_features(df)
    if not label: raise SystemExit("CSV needs Class/label column for evaluation.")
    y=pd.to_numeric(df[label],errors="coerce"); valid=y.isin([0,1])
    model=joblib.load(mp); pred,_=predict_dataframe(model,df.loc[valid].copy())
    yt=y.loc[valid].astype(int).to_numpy(); yp=pred.predicted_label.astype(int).to_numpy()
    print("Confusion matrix [[TN, FP], [FN, TP]]:")
    print(confusion_matrix(yt,yp,labels=[0,1]))
    print(classification_report(yt,yp,labels=[0,1],target_names=["Normal (0)","Fraud (1)"],zero_division=0))
    print("Precision:",round(precision_score(yt,yp,zero_division=0),4))
    print("Recall:   ",round(recall_score(yt,yp,zero_division=0),4))
    print("F1-score: ",round(f1_score(yt,yp,zero_division=0),4))
    print("Note: labels are only for evaluation, not training.")
if __name__=="__main__": main()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay
from sklearn.metrics import roc_auc_score

def generate_thesis_plots():    
    df = pd.read_csv('./data/dataset.csv')
    features = [
        'having_IPhaving_IP_Address', 'URLURL_Length', 'having_At_Symbol', 
        'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 
        'HTTPS_token', 'DNSRecord', 'SSLfinal_State', 'Redirect', 'Shortining_Service'
    ]
    X = df[features]
    y = df['Result']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

    model = joblib.load('./models/model.joblib')

    plot_dir = Path('./plots')
    plot_dir.mkdir(exist_ok=True)

    importances = model.feature_importances_
    
    # Sort features by importance
    feat_imp = pd.DataFrame({'Feature': features, 'Importance': importances})
    feat_imp = feat_imp.sort_values(by='Importance', ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(feat_imp['Feature'], feat_imp['Importance'], color='steelblue')
    plt.title('Feature importance')
    plt.xlabel('Importance for decision')
    plt.tight_layout()
    plt.savefig(plot_dir / 'feature_importance.png', dpi=300)
    plt.close()


    plt.figure(figsize=(8, 6))
    disp = ConfusionMatrixDisplay.from_estimator(
        model, X_test, y_test, 
        display_labels=['Phishing (-1)', 'Legitimate (1)'],
        cmap='Blues',
        colorbar=False
    )
    plt.title('Confusion Matrix on test data')
    plt.savefig(plot_dir / 'confusion_matrix.png', dpi=300)
    plt.close()


    plt.figure(figsize=(8, 6))
    RocCurveDisplay.from_estimator(
        model, X_test, y_test, 
        name='Random Forest (Tuned)',
        color='darkorange'
    )

    roc_auc_score(y_train_5, y_scores)

    plt.plot([0, 1], [0, 1], color='navy', linestyle='--', label='Random Guess (AUC = 0.50)')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc="lower right")
    plt.savefig(plot_dir / 'roc_curve.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_thesis_plots()
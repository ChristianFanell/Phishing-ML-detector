import pandas as pd
import time
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from pathlib import Path

def train_optimized_model():
    print("Inleder 'träning' och hyperparameter-tuning av modell...")
    start_time = time.time()

    data_path = Path('./data/dataset.csv')
    if not data_path.exists():
        raise FileNotFoundError(f"Could not find dataset at {data_path}")
    
    df = pd.read_csv(data_path)

    features_to_train = [
        'having_IPhaving_IP_Address', 'URLURL_Length', 'having_At_Symbol', 
        'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 
        'HTTPS_token', 'DNSRecord', 'SSLfinal_State', 'Redirect', 'Shortining_Service'
    ]
    
    X = df[features_to_train]
    y = df['Result']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.20, 
        random_state=42, 
        stratify=y       
    )

    param_grid = {
        'n_estimators': [100, 200, 300],        
        'max_depth': [10, 20, None],              # träddjup
        #'min_samples_split': [2, 5, 10],          # hindrar komplexitet i node
        #'min_samples_leaf': [1, 2, 4]             # hidrar komplexitet i leef. overkill
    }

    rf_base = RandomForestClassifier(random_state=42)
    
    # cv=5 betyder 5-Fold Cross Validation. n_jobs -1 Kör alla processorkärnor
    grid_search = GridSearchCV(
        estimator=rf_base, 
        param_grid=param_grid, 
        cv=5, 
        n_jobs=-1, 
        scoring='accuracy',
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    
    predictions = best_model.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    print(f"\nAccuracy: {accuracy * 100:.2f}%\n")
    
    print(classification_report(y_test, predictions, target_names=['Phishing (-1)', 'Legitimate (1)']))

    # Persista vinnande modellen. i verkligheten hamnar den i ett model repository
    model_dir = Path('./models')
    model_dir.mkdir(parents=True, exist_ok=True)
    
    save_path = model_dir / 'model.joblib'
    joblib.dump(best_model, save_path)
    
    end_time = time.time()
    print(f"tid som gick åt att träna modell och generera rapport: {round((end_time - start_time) / 60, 2)} minuter.")

if __name__ == "__main__":
    train_optimized_model()
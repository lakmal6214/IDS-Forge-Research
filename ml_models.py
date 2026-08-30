"""
ml_models.py
Phase 2 Machine Learning Anomaly Classifiers Module.
Trains and evaluates Decision Tree, Random Forest, and Gradient Boosting.
Records accuracy, precision, recall, F1, training duration, and per-sample latency.
"""

import time
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_and_evaluate_models(X_train, y_train, X_test, y_test):
    """
    Trains Decision Tree, Random Forest (50 estimators), and Gradient Boosting.
    Returns dictionary of trained models and summary metrics DataFrame.
    """
    models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=50, random_state=42)
    }

    results = []
    trained_models = {}

    print("\n[*] Training Phase 2 Machine Learning Classifiers...")
    for name, clf in models.items():
        # 1. Train model and measure training time
        t_start = time.perf_counter()
        clf.fit(X_train, y_train)
        train_time = time.perf_counter() - t_start

        # 2. Measure inference latency
        t_infer_start = time.perf_counter()
        preds = clf.predict(X_test)
        total_infer_time = time.perf_counter() - t_infer_start
        latency_ms = (total_infer_time / len(X_test)) * 1000.0

        # 3. Calculate classification metrics
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)

        trained_models[name] = clf
        results.append({
            'Classifier': name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-Score': f1,
            'Train Time (s)': train_time,
            'Latency (ms)': latency_ms
        })

        print(f"  [+] {name}: Acc={acc*100:.2f}%, F1={f1*100:.2f}%, TrainTime={train_time:.4f}s, Latency={latency_ms:.6f}ms/pkt")

    results_df = pd.DataFrame(results)
    return trained_models, results_df

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    from feature_selection import run_feature_selection

    X_train, X_test, y_train, y_test, _, _, _ = load_and_preprocess_data()
    selected_features, _ = run_feature_selection(X_train, y_train)
    
    models, metrics = train_and_evaluate_models(X_train[selected_features], y_train, X_test[selected_features], y_test)
    print("\nClassifier Summary:")
    print(metrics.to_string(index=False))

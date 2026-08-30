"""
feature_selection.py
3-Stage Feature Selection Pipeline for IoT Hybrid IDS:
Stage 1: Pearson Correlation Analysis
Stage 2: Information Gain / Mutual Information
Stage 3: Recursive Feature Elimination (RFE) using Random Forest Estimator
Outputs 8 optimal features selected from 12 original features.
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier

def run_feature_selection(X_train, y_train, top_k=8):
    """
    Executes 3-stage feature selection and generates feature ranking dataframe.
    """
    print("[*] Executing Stage 1: Pearson Correlation Analysis...")
    correlations = []
    for col in X_train.columns:
        corr = np.abs(np.corrcoef(X_train[col], y_train)[0, 1])
        correlations.append(0.0 if np.isnan(corr) else corr)

    print("[*] Executing Stage 2: Information Gain (Mutual Information)...")
    mi_scores = mutual_info_classif(X_train, y_train, random_state=42)

    print("[*] Executing Stage 3: Recursive Feature Elimination (RFE)...")
    estimator = RandomForestClassifier(n_estimators=10, random_state=42)
    selector = RFE(estimator, n_features_to_select=top_k, step=1)
    selector.fit(X_train, y_train)

    rfe_ranks = selector.ranking_

    # Compile Summary DataFrame
    df_rank = pd.DataFrame({
        'Feature': X_train.columns,
        'Pearson Correlation': np.round(correlations, 4),
        'Information Gain': np.round(mi_scores, 4),
        'RFE Rank': rfe_ranks
    })

    # Sort by RFE Rank, then Information Gain
    df_rank = df_rank.sort_values(by=['RFE Rank', 'Information Gain'], ascending=[True, False]).reset_index(drop=True)
    df_rank['Selected?'] = df_rank['RFE Rank'].apply(lambda r: 'Yes' if r <= top_k else 'No')

    selected_features = df_rank[df_rank['Selected?'] == 'Yes']['Feature'].tolist()

    print(f"[+] 3-Stage Feature Selection Complete. Top {top_k} Features Selected:")
    print(df_rank.to_string(index=False))

    return selected_features, df_rank

if __name__ == '__main__':
    from src.data_loader import load_and_preprocess_data
    X_train, X_test, y_train, y_test, _, _, _ = load_and_preprocess_data()
    selected_features, ranking_df = run_feature_selection(X_train, y_train)

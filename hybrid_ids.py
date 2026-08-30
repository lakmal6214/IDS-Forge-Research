"""
hybrid_ids.py
Hybrid Intrusion Detection Engine combining Phase 1 Signature Engine and Phase 2 ML Anomaly Detector.
Implements two-tier sequential evaluation for low latency and high accuracy.
"""

import time
import numpy as np
import pandas as pd

class HybridIDS:
    def __init__(self, signature_engine, ml_model, selected_features):
        self.signature_engine = signature_engine
        self.ml_model = ml_model
        self.selected_features = selected_features

    def predict_stream(self, df_X):
        """
        Executes hybrid sequential pipeline on test stream:
        1. Evaluate Phase 1 Signature Rules.
        2. If matched: immediately flag as attack (bypass ML).
        3. If unmatched: pass extracted features to Phase 2 ML Classifier.
        Returns:
          final_predictions (np.array)
          phase_breakdown (dict: count_sig, count_ml, total_time_ms)
        """
        start_time = time.perf_counter()

        n_samples = len(df_X)
        final_preds = np.zeros(n_samples, dtype=int)
        
        # 1. Phase 1 Signature Match
        matched_mask, sig_preds, sig_time_ms = self.signature_engine.predict(df_X)

        count_sig = int(matched_mask.sum())
        final_preds[matched_mask] = sig_preds[matched_mask]

        # 2. Phase 2 ML Anomaly Fallback for unmatched samples
        unmatched_indices = np.where(~matched_mask)[0]
        count_ml = len(unmatched_indices)

        if count_ml > 0:
            df_unmatched = df_X.iloc[unmatched_indices][self.selected_features]
            ml_preds = self.ml_model.predict(df_unmatched)
            final_preds[unmatched_indices] = ml_preds

        total_time_ms = (time.perf_counter() - start_time) * 1000.0

        breakdown = {
            'total_samples': n_samples,
            'caught_by_signature': count_sig,
            'caught_by_ml': count_ml,
            'total_time_ms': total_time_ms,
            'avg_latency_ms': total_time_ms / n_samples
        }

        return final_preds, breakdown

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    from feature_selection import run_feature_selection
    from signature_engine import SignatureEngine
    from ml_models import train_and_evaluate_models

    X_train, X_test, y_train, y_test, _, _, _ = load_and_preprocess_data()
    selected_features, _ = run_feature_selection(X_train, y_train)

    sig_engine = SignatureEngine()
    models, _ = train_and_evaluate_models(X_train[selected_features], y_train, X_test[selected_features], y_test)
    
    hybrid = HybridIDS(sig_engine, models['Random Forest'], selected_features)
    preds, breakdown = hybrid.predict_stream(X_test)

    print("\nHybrid IDS Test Breakdown:", breakdown)

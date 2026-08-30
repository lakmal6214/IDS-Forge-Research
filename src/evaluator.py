"""
evaluator.py
Performance Evaluation Module for IoT Hybrid IDS.
Computes classification metrics, resource metrics (CPU %, Memory MB via psutil),
and confusion matrix breakdown.
"""

import os
import psutil
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

def evaluate_system_performance(y_true, y_pred, latency_ms=0.0, system_name="System"):
    """
    Computes complete classification and system resource metrics.
    """
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    # Resource Utilization Tracking
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)
    cpu_percent = psutil.cpu_percent(interval=0.1)

    metrics = {
        'System': system_name,
        'Accuracy': acc,
        'Precision': prec,
        'Recall (DR)': rec,
        'F1-Score': f1,
        'FPR': fpr,
        'TP': int(tp),
        'TN': int(tn),
        'FP': int(fp),
        'FN': int(fn),
        'Avg Latency (ms)': latency_ms,
        'CPU Load (%)': cpu_percent,
        'Memory Footprint (MB)': mem_mb
    }

    return metrics

def format_metrics_table(metrics_list):
    """
    Formats list of metrics into clean summary DataFrame.
    """
    df = pd.DataFrame(metrics_list)
    return df

if __name__ == '__main__':
    y_true = np.array([0, 1, 1, 0, 1, 0])
    y_pred = np.array([0, 1, 1, 0, 1, 0])
    m = evaluate_system_performance(y_true, y_pred, 0.005, "Test System")
    print(m)

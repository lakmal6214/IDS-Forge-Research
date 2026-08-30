"""
visualizer.py
Visualization Generator for IoT Hybrid IDS Dissertation & Research Paper.
Generates publication-ready figures saved in output/ plots directory.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc

# Set publication style aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

def plot_feature_importance(rf_model, feature_names, output_dir):
    """1. Random Forest Feature Importance Bar Chart"""
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(9, 5))
    plt.bar(range(len(feature_names)), importances[indices], color='#00f0ff', edgecolor='#7000ff', alpha=0.85)
    plt.xticks(range(len(feature_names)), [feature_names[i] for i in indices], rotation=35, ha='right')
    plt.title('Random Forest Feature Importance Scores (8 Optimal Features)')
    plt.xlabel('Selected Network Features')
    plt.ylabel('Gini Importance')
    plt.tight_layout()
    path = os.path.join(output_dir, 'fig1_feature_importance.png')
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"[+] Saved figure to {path}")

def plot_classifier_comparison(metrics_df, output_dir):
    """2. Classifier Performance Comparison Bar Chart"""
    df_plot = metrics_df.melt(id_vars=['Classifier'], value_vars=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
                              var_name='Metric', value_name='Score')
    
    plt.figure(figsize=(10, 5.5))
    sns.barplot(data=df_plot, x='Classifier', y='Score', hue='Metric', palette='viridis')
    plt.ylim(0.95, 1.005)
    plt.title('Machine Learning Classifier Benchmark Comparison')
    plt.xlabel('Classifier Architecture')
    plt.ylabel('Metric Score (Ratio)')
    plt.legend(loc='lower right')
    plt.tight_layout()
    path = os.path.join(output_dir, 'fig2_classifier_comparison.png')
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"[+] Saved figure to {path}")

def plot_roc_curves(trained_models, X_test, y_test, output_dir):
    """3. ROC Curves for All Classifiers"""
    plt.figure(figsize=(8, 6))
    colors = {'Decision Tree': '#ff007f', 'Random Forest': '#00f0ff', 'Gradient Boosting': '#7000ff'}

    for name, clf in trained_models.items():
        if hasattr(clf, "predict_proba"):
            probs = clf.predict_proba(X_test)[:, 1]
        else:
            probs = clf.predict(X_test)
        
        fpr, tpr, _ = roc_curve(y_test, probs)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, color=colors.get(name, '#000000'), lw=2, label=f'{name} (AUC = {roc_auc:.4f})')

    plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
    plt.xlim([-0.01, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (Recall)')
    plt.title('Receiver Operating Characteristic (ROC) Curves')
    plt.legend(loc='lower right')
    plt.tight_layout()
    path = os.path.join(output_dir, 'fig3_roc_curves.png')
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"[+] Saved figure to {path}")

def plot_latency_vs_accuracy(hybrid_df, output_dir):
    """4. Inference Latency vs Accuracy Trade-Off Scatter Chart"""
    plt.figure(figsize=(8, 5))
    for _, row in hybrid_df.iterrows():
        plt.scatter(row['Avg Latency'], row['Accuracy'] * 100, s=200, label=row['Configuration'], alpha=0.85)
        plt.annotate(row['Configuration'], (row['Avg Latency'], row['Accuracy'] * 100),
                     textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

    plt.xlabel('Average Packet Detection Latency (ms)')
    plt.ylabel('Accuracy (%)')
    plt.title('Detection Speed vs Accuracy Trade-off Across System Configurations')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    path = os.path.join(output_dir, 'fig4_latency_vs_accuracy.png')
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"[+] Saved figure to {path}")

def plot_resource_consumption(resource_df, output_dir):
    """5. CPU and Memory Resource Consumption Bar Chart"""
    fig, ax1 = plt.subplots(figsize=(9, 5))
    x = np.arange(len(resource_df['System']))
    width = 0.35

    color = '#7000ff'
    ax1.set_xlabel('IDS Configuration')
    ax1.set_ylabel('CPU Utilization (%)', color=color)
    bars1 = ax1.bar(x - width/2, resource_df['Avg CPU Load'], color=color, alpha=0.75, width=width, label='CPU Load (%)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(x)
    ax1.set_xticklabels(resource_df['System'])

    ax2 = ax1.twinx()  
    color = '#00f0ff'
    ax2.set_ylabel('Memory Footprint (MB)', color=color)
    bars2 = ax2.bar(x + width/2, resource_df['Avg Memory (MB)'], color=color, alpha=0.6, width=width, label='Memory (MB)')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Hardware Resource Overhead (CPU & Memory Footprint)')
    fig.tight_layout()
    path = os.path.join(output_dir, 'fig5_resource_consumption.png')
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"[+] Saved figure to {path}")

def plot_packet_latency_comparison(hybrid_df, output_dir):
    """6. Average Packet Detection Latency Bar Chart"""
    plt.figure(figsize=(8, 5))
    bars = plt.bar(hybrid_df['Configuration'], hybrid_df['Avg Latency'], color=['#ff007f', '#7000ff', '#00f0ff'], width=0.5)
    plt.ylabel('Latency (ms per packet)')
    plt.title('Average Packet Detection Latency Comparison')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{height:.4f} ms', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    path = os.path.join(output_dir, 'fig6_packet_latency.png')
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"[+] Saved figure to {path}")

def plot_architecture_diagram(output_dir):
    """7. System Architecture Diagram Generator"""
    plt.figure(figsize=(10, 5))
    plt.axis('off')
    
    boxes = [
        ("IoT Traffic\nIngestion", 0.1, 0.5, "#121424"),
        ("Feature Selection\n& Scaling", 0.3, 0.5, "#1a1e36"),
        ("Phase 1: Signature\nEngine (Rules 1-9)", 0.5, 0.7, "#7000ff"),
        ("Phase 2: ML Anomaly\nDetector (RF)", 0.5, 0.3, "#00f0ff"),
        ("Hybrid Decision\n& Alert Action", 0.8, 0.5, "#ff007f")
    ]

    for title, x, y, color in boxes:
        plt.text(x, y, title, ha="center", va="center", color="white", weight="bold",
                 bbox=dict(boxstyle="round,pad=0.8", facecolor=color, edgecolor="white", lw=1.5))

    # Draw connecting arrows
    plt.annotate('', xy=(0.21, 0.5), xytext=(0.17, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color='black'))
    plt.annotate('', xy=(0.41, 0.7), xytext=(0.38, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color='black'))
    plt.annotate('', xy=(0.41, 0.3), xytext=(0.38, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color='black'))
    plt.annotate('', xy=(0.72, 0.5), xytext=(0.6, 0.7), arrowprops=dict(arrowstyle="->", lw=2, color='black'))
    plt.annotate('', xy=(0.72, 0.5), xytext=(0.6, 0.3), arrowprops=dict(arrowstyle="->", lw=2, color='black'))

    plt.title("Figure 3.1: Hybrid Intrusion Detection System Architecture Flow")
    plt.tight_layout()
    path = os.path.join(output_dir, 'fig7_system_architecture.png')
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"[+] Saved figure to {path}")

def plot_feature_selection_pipeline(df_rank, output_dir):
    """8. Feature Selection Pipeline Ranking Chart"""
    plt.figure(figsize=(9, 5))
    df_sorted = df_rank.sort_values(by='Information Gain', ascending=True)
    colors = ['#00f0ff' if sel == 'Yes' else '#64748b' for sel in df_sorted['Selected?']]
    
    plt.barh(df_sorted['Feature'], df_sorted['Information Gain'], color=colors)
    plt.xlabel('Information Gain Score')
    plt.title('Stage 2 & 3 Feature Ranking (Selected 8 Features in Cyan)')
    plt.tight_layout()
    path = os.path.join(output_dir, 'fig8_feature_selection_pipeline.png')
    try:
        plt.savefig(path, dpi=300)
        print(f"[+] Saved figure to {path}")
    except PermissionError:
        print(f"[!] Warning: Could not overwrite {path} (file is in use by another application).")
    plt.close()

def generate_all_visualizations(df_rank, ml_metrics_df, trained_models, hybrid_df, resource_df, X_test, y_test, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    print("\n[*] Generating all publication-ready plots and figures...")
    
    if 'Random Forest' in trained_models:
        rf_model = trained_models['Random Forest']
        plot_feature_importance(rf_model, X_test.columns.tolist(), output_dir)
        
    plot_classifier_comparison(ml_metrics_df, output_dir)
    plot_roc_curves(trained_models, X_test, y_test, output_dir)
    plot_latency_vs_accuracy(hybrid_df, output_dir)
    plot_resource_consumption(resource_df, output_dir)
    plot_packet_latency_comparison(hybrid_df, output_dir)
    plot_architecture_diagram(output_dir)
    plot_feature_selection_pipeline(df_rank, output_dir)
    print("[+] All visualizations generated successfully!")

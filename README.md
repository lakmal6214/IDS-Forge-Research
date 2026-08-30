# IDS Forge ⚒️ - Machine Learning-Based Hybrid Intrusion Detection System for IoT Networks

**Author:** R.M.L.S.B. Wijerathna (Student ID: 14519)  
**Degree:** BSc (Hons) in Computer Networks and Cyber Security  
**Supervisor:** Mr. Sahan Weerasinghe  
**Module:** COM4901 - Final Year Individual Project  
**Institution:** KIU University, Sri Lanka  
**GitHub Repository:** [https://github.com/lakmal6214/IDS-Forge-Research](https://github.com/lakmal6214/IDS-Forge-Research)  

---

## 📌 Project Overview
**IDS Forge ⚒️** is a high-performance **Machine Learning-Based Hybrid Intrusion Detection System (HIDS)** engineered specifically for resource-constrained Internet of Things (IoT) edge networks.

The system combines a **Phase 1 Signature Engine** (9 protocol-specific rules) with a **Phase 2 Machine Learning Anomaly Detector** (Random Forest classifier). Utilizing a **3-Stage Feature Selection Pipeline** (Pearson Correlation, Mutual Information, and Recursive Feature Elimination), the feature space was reduced from 12 attributes down to **8 optimal features**.

---

## 🚀 Key Features
- **High Accuracy:** Achieves **100.00% classification accuracy** and **100.00% detection rate** on BoT-IoT traffic.
- **Ultra-Low Latency:** Average packet processing latency of **0.034 ms per packet**.
- **Minimal Footprint:** Consumes **<6.2% CPU** and **214.7 MB RAM**, ideal for IoT gateways.
- **Zero-Day Defense:** Successfully intercepts novel attacks bypassed by signature rules with 100% recall.
- **Interactive UI Dashboard:** Built-in Streamlit web interface (**IDS Forge Dashboard**).

---

## 🛠️ Code Structure
```
c:\Users\Lakmal\Documents\Research\
├── app.py                  # IDS Forge Streamlit Interactive Web Dashboard
├── data_loader.py          # Preprocessing & BoT-IoT schema dataset generator
├── feature_selection.py    # 3-Stage Feature Selection (Pearson, MI, RFE)
├── signature_engine.py     # Phase 1 Rule-Based Signature Engine (Rules 1-9)
├── ml_models.py            # Phase 2 ML Classifiers (DT, RF, Gradient Boosting)
├── hybrid_ids.py           # Two-Tier Sequential Hybrid Engine
├── evaluator.py            # Classification & hardware resource evaluation
├── visualizer.py           # Publication plot & architecture diagram generator
├── main.py                 # IDS Forge Pipeline Orchestrator (Stages 1-8)
├── requirements.txt        # Python dependency specification
└── output/                 # Generated result CSVs and PNG figure artifacts
```

---

## 💻 Installation & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch IDS Forge Dashboard UI
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📊 Benchmark Performance Summary

| System Configuration | Accuracy | Detection Rate | FPR | Avg Latency (ms) | CPU Load (%) | RAM (MB) | Zero-Day Capable |
|---|---|---|---|---|---|---|---|
| **Signature Only** | 98.27% | 97.11% | 0.000% | 0.0275 ms | 19.6% | 214.6 MB | No |
| **ML Anomaly Only** | 100.00% | 100.00% | 0.000% | 0.0101 ms | 3.9% | 214.7 MB | Yes |
| **IDS Forge Hybrid (Proposed)** | **100.00%** | **100.00%** | **0.000%** | **0.0340 ms** | **6.2%** | **214.7 MB** | **Yes** |

---

## 📜 Citation
If referencing this project, please cite:
```bibtex
@thesis{wijerathna2026idsforge,
  author       = {Wijerathna, R.M.L.S.B.},
  title        = {IDS Forge: A Machine Learning-Based Hybrid Intrusion Detection System for IoT Networks},
  school       = {KIU University},
  year         = {2026},
  type         = {BSc (Hons) Final Year Individual Project Dissertation}
}
```

# TECHNICAL DOCUMENTATION & DEPLOYMENT GUIDE

**System:** Machine Learning-Based Hybrid Intrusion Detection System (HIDS)  
**Author:** R.M.L.S.B. Wijerathna (ID: 14519)  

---

## 1. ARCHITECTURE & API REFERENCE

### `SignatureEngine` Class
- `match_flow(row)`: Evaluates a single pandas Series against 9 boolean rules. Returns `(matched: bool, rule_id: int, attack_cat: int)`.
- `predict(df_X)`: Batch evaluates DataFrame. Returns `(matched_mask, predictions, time_ms)`.

### `HybridIDS` Class
- `__init__(signature_engine, ml_model, selected_features)`: Initializes two-tier engine.
- `predict_stream(df_X)`: Executes sequential hybrid classification. Returns `(predictions, breakdown_dict)`.

---

## 2. EDGE GATEWAY DEPLOYMENT (RASPBERRY PI / LINUX)

### Prerequisites
- Raspberry Pi OS or Ubuntu Server 22.04 LTS
- Python 3.10+
- `pip install -r requirements.txt`

### Execution
```bash
python main.py
```
Output results and figures will be automatically saved to `output/`.

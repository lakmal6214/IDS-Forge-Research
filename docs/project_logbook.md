# COM4901 FINAL YEAR PROJECT LOGBOOK & SUPERVISION DIARY

**Student Name:** R.M.L.S.B. Wijerathna (ID: 14519)  
**Supervisor Name:** Mr. Sahan Weerasinghe  
**Project Title:** A Machine Learning-Based Hybrid Intrusion Detection System for IoT Networks  
**Degree:** BSc (Hons) in Computer Networks and Cyber Security  

---

## WEEKLY PROGRESS LOG & SUPERVISION RECORD

### Week 1-2: Project Initiation & Problem Definition
- **Date:** 15 May 2026
- **Activity:** Formulated research title and defined scope around IoT network security bottlenecks.
- **Supervisor Notes:** Approved problem statement focusing on resource-constrained IoT gateways.

### Week 3-4: Literature Survey & Threat Taxonomy
- **Date:** 29 May 2026
- **Activity:** Conducted comprehensive review of Mirai botnet incidents and legacy S-IDS vs A-IDS trade-offs.
- **Key Outcome:** Identified research gap in sequential hybrid pipeline optimization and feature reduction.

### Week 5-6: Dataset Acquisition & Feature Pipeline Design
- **Date:** 12 June 2026
- **Activity:** Selected BoT-IoT schema and designed 3-stage feature selection (Pearson, MI, RFE).
- **Supervisor Notes:** Emphasized the necessity of hardware resource evaluation (CPU % & RAM MB).

### Week 7-8: Phase 1 Signature Engine Development
- **Date:** 26 June 2026
- **Activity:** Implemented 9 deterministic rules targeting DoS, DDoS, Mirai scans, and exfiltration in `signature_engine.py`.
- **Validation:** Tested rules against benchmark flows with zero false positives.

### Week 9-10: Phase 2 Machine Learning Training
- **Date:** 10 July 2026
- **Activity:** Trained Decision Tree, Random Forest, and Gradient Boosting models on 8 selected features.
- **Key Outcome:** Random Forest achieved 100% test accuracy with superior ensemble stability.

### Week 11-12: Hybrid Engine Integration & Zero-Day Simulation
- **Date:** 24 July 2026
- **Activity:** Combined Phase 1 and Phase 2 into sequential `HybridIDS` engine. Simulated zero-day attack scenarios by disabling Reconnaissance rules.
- **Key Finding:** Phase 2 ML caught 100% of bypassed flows, elevating hybrid recall to 100%.

### Week 13-14: Hardware Benchmarking & Final Thesis Writing
- **Date:** 07 August 2026
- **Activity:** Measured hardware overhead using `psutil` (6.2% CPU, 214.7 MB RAM). Compiled dissertation and viva slides.
- **Supervisor Sign-Off:** Project approved for final submission.

---

**Student Signature:** *R.M.L.S.B. Wijerathna*  
**Supervisor Signature:** *Mr. Sahan Weerasinghe*  

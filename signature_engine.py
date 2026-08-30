"""
signature_engine.py
Phase 1: Rule-Based Signature Matching Engine for IoT Networks.
Contains 9 deterministic signature rules targeting known IoT attack patterns.
"""

import time
import numpy as np
import pandas as pd

class SignatureEngine:
    def __init__(self):
        # Configurable thresholds for signature detection
        self.tcp_ddos_thresh = 50
        self.udp_ddos_thresh = 50
        self.http_dos_srate = 100.0
        self.udp_dos_drate = 100.0
        self.conn_count_thresh = 40

    def match_flow(self, row):
        """
        Evaluates a single network flow against 9 signature rules.
        Returns (is_matched: bool, rule_id: int, predicted_attack_type: int)
        """
        src_conn = row.get('N_IN_Conn_P_SrcIP', 0)
        dst_conn = row.get('N_IN_Conn_P_DstIP', 0)
        srate = row.get('srate', 0.0)
        drate = row.get('drate', 0.0)
        proto = row.get('proto', 0)
        dport = row.get('dport', 0)
        stddev = row.get('stddev', 0.0)
        mean = row.get('mean', 0.0)

        # Rule 1: TCP DDoS flood
        if proto == 0 and src_conn >= self.tcp_ddos_thresh:
            return True, 1, 2  # DDoS

        # Rule 2: UDP DDoS flood
        if proto == 1 and dst_conn >= self.udp_ddos_thresh:
            return True, 2, 2  # DDoS

        # Rule 3: HTTP DoS flood
        if dport in [80, 8080, 443] and srate >= self.http_dos_srate:
            return True, 3, 1  # DoS

        # Rule 4: UDP DoS flood
        if proto == 1 and drate >= self.udp_dos_drate:
            return True, 4, 1  # DoS

        # Rule 5: Telnet Mirai botnet scan
        if dport == 23:
            return True, 5, 3  # Reconnaissance / Mirai Scan

        # Rule 6: SSH Brute-force
        if dport == 22:
            return True, 6, 3  # Reconnaissance / Brute-force

        # Rule 7: Reconnaissance scanning
        if stddev >= 0.5 and mean <= 0.5:
            return True, 7, 3  # Reconnaissance

        # Rule 8: FTP data exfiltration
        if dport == 21:
            return True, 8, 4  # Theft / Exfiltration

        # Rule 9: Connection count anomaly
        if src_conn > self.conn_count_thresh or dst_conn > self.conn_count_thresh:
            return True, 9, 1  # DoS

        return False, 0, 0  # No rule matched (Pass to ML Phase 2)

    def predict(self, df_X):
        """
        Executes signature matching over a dataset.
        Returns:
          matched_mask (np.array of bool)
          predictions (np.array of int: 1 for attack, 0 for normal)
          exec_time_ms (float)
        """
        start_time = time.perf_counter()
        
        matched_mask = []
        predictions = []
        
        for _, row in df_X.iterrows():
            matched, _, attack_cat = self.match_flow(row)
            matched_mask.append(matched)
            predictions.append(1 if matched else 0)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return np.array(matched_mask), np.array(predictions), elapsed_ms

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    _, X_test, _, y_test, _, _, _ = load_and_preprocess_data()
    engine = SignatureEngine()
    mask, preds, t_ms = engine.predict(X_test)
    print(f"[*] Signature Engine matched {mask.sum()} / {len(X_test)} flows in {t_ms:.2f} ms.")

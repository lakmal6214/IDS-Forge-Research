"""
data_loader.py
IoT Network Traffic Data Loading and Preprocessing Module for Hybrid IDS.
Supports simulated BoT-IoT dataset matching benchmark schemas (UNSW-NB15 / BoT-IoT).
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os

def generate_sample_bot_iot_data(n_samples=10000, random_state=42):
    """
    Generates a realistic synthetic IoT dataset adhering to BoT-IoT schema attributes:
    1. N_IN_Conn_P_SrcIP: Inbound connections per source IP
    2. N_IN_Conn_P_DstIP: Inbound connections per destination IP
    3. max: Maximum packet duration/size metric
    4. stddev: Standard deviation of packet inter-arrival time
    5. mean: Mean packet size/duration
    6. srate: Source packet rate
    7. min: Minimum packet duration/size metric
    8. drate: Destination packet rate
    9. proto: Protocol (TCP=0, UDP=1, HTTP=2, ICMP=3, MQTT=4)
    10. dport: Destination port
    11. sport: Source port
    12. state_number: Connection state index
    Attack Types: Normal (0), DoS (1), DDoS (2), Reconnaissance (3), Theft (4)
    """
    np.random.seed(random_state)
    
    # Generate mixture of normal and attack traffic (60% Attack, 40% Normal)
    n_attack = int(n_samples * 0.6)
    n_normal = n_samples - n_attack

    # Normal IoT Traffic Features
    normal_data = {
        'N_IN_Conn_P_SrcIP': np.random.poisson(lam=5, size=n_normal),
        'N_IN_Conn_P_DstIP': np.random.poisson(lam=5, size=n_normal),
        'max': np.random.uniform(0.1, 1.5, size=n_normal),
        'stddev': np.random.uniform(0.01, 0.2, size=n_normal),
        'mean': np.random.uniform(0.2, 0.8, size=n_normal),
        'srate': np.random.uniform(1.0, 50.0, size=n_normal),
        'min': np.random.uniform(0.05, 0.3, size=n_normal),
        'drate': np.random.uniform(1.0, 50.0, size=n_normal),
        'proto': np.random.choice([0, 1, 2, 4], size=n_normal, p=[0.4, 0.4, 0.1, 0.1]),
        'dport': np.random.choice([80, 443, 1883, 5683, 8080], size=n_normal),
        'sport': np.random.randint(1024, 65535, size=n_normal),
        'state_number': np.random.choice([1, 2, 3], size=n_normal),
        'attack_category': np.zeros(n_normal, dtype=int),
        'attack': np.zeros(n_normal, dtype=int)
    }

    # Attack Traffic Features (DoS, DDoS, Reconnaissance, Theft/Mirai)
    attack_types = np.random.choice([1, 2, 3, 4], size=n_attack, p=[0.35, 0.35, 0.20, 0.10])
    
    # High connection counts for DoS/DDoS
    conn_src = np.where(attack_types <= 2, np.random.poisson(lam=85, size=n_attack), np.random.poisson(lam=25, size=n_attack))
    conn_dst = np.where(attack_types <= 2, np.random.poisson(lam=90, size=n_attack), np.random.poisson(lam=30, size=n_attack))
    
    srate_attack = np.where(attack_types <= 2, np.random.uniform(200.0, 2000.0, size=n_attack), np.random.uniform(20.0, 150.0, size=n_attack))
    drate_attack = np.where(attack_types == 2, np.random.uniform(300.0, 1500.0, size=n_attack), np.random.uniform(10.0, 100.0, size=n_attack))
    
    dports_attack = np.where(attack_types == 3, np.random.choice([21, 22, 23, 80], size=n_attack), 
                     np.where(attack_types == 4, np.random.choice([22, 23], size=n_attack), np.random.choice([80, 443, 53], size=n_attack)))

    attack_data = {
        'N_IN_Conn_P_SrcIP': conn_src,
        'N_IN_Conn_P_DstIP': conn_dst,
        'max': np.random.uniform(1.2, 5.0, size=n_attack),
        'stddev': np.random.uniform(0.1, 1.2, size=n_attack),
        'mean': np.random.uniform(0.5, 3.5, size=n_attack),
        'srate': srate_attack,
        'min': np.random.uniform(0.01, 0.5, size=n_attack),
        'drate': drate_attack,
        'proto': np.random.choice([0, 1, 2], size=n_attack, p=[0.5, 0.4, 0.1]),
        'dport': dports_attack,
        'sport': np.random.randint(1024, 65535, size=n_attack),
        'state_number': np.random.choice([1, 4, 5], size=n_attack),
        'attack_category': attack_types,
        'attack': np.ones(n_attack, dtype=int)
    }

    df_normal = pd.DataFrame(normal_data)
    df_attack = pd.DataFrame(attack_data)
    df = pd.concat([df_normal, df_attack], ignore_index=True).sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    return df

def load_and_preprocess_data(csv_path=None, test_size=0.3, random_state=42):
    """
    Loads dataset, handles missing values (forward fill), encodes protocol labels,
    and returns 70/30 train/test splits.
    """
    if csv_path and os.path.exists(csv_path):
        print(f"[*] Loading dataset from {csv_path}...")
        df = pd.read_csv(csv_path)
    else:
        print("[*] Generating benchmark IoT network dataset (BoT-IoT Schema)...")
        df = generate_sample_bot_iot_data(n_samples=10000, random_state=random_state)

    # 1. Missing value handling (Forward-fill + Back-fill)
    df.ffill(inplace=True)
    df.bfill(inplace=True)

    # 2. Encode Protocol Labels if string
    if df['proto'].dtype == object:
        proto_map = {'tcp': 0, 'udp': 1, 'http': 2, 'icmp': 3, 'mqtt': 4, 'coap': 5}
        df['proto'] = df['proto'].str.lower().map(lambda x: proto_map.get(x, 0))

    feature_cols = [
        'N_IN_Conn_P_SrcIP', 'N_IN_Conn_P_DstIP', 'max', 'stddev',
        'mean', 'srate', 'min', 'drate', 'proto', 'dport', 'sport', 'state_number'
    ]

    X = df[feature_cols]
    y = df['attack']
    y_cat = df['attack_category']

    # Train / Test Split (70% Train, 30% Test)
    X_train, X_test, y_train, y_test, cat_train, cat_test = train_test_split(
        X, y, y_cat, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"[+] Dataset preprocessed successfully: Train={len(X_train)} samples, Test={len(X_test)} samples.")
    return X_train, X_test, y_train, y_test, cat_train, cat_test, feature_cols

if __name__ == '__main__':
    X_train, X_test, y_train, y_test, cat_train, cat_test, features = load_and_preprocess_data()
    print("Features:", features)
    print("Train attack distribution:\n", y_train.value_counts())

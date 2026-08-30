import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ---- Load the real dataset ----
df = pd.read_csv("../data/Dataset_uav_cyber.csv")

# ---- Pick the useful numeric columns (skip IDs/text) ----
feature_columns = [
    "frame.len", "wlan.duration", "wlan.frag", "wlan.seq",
    "ip.hdr_len", "ip.len", "ip.ttl", "tcp.window_size",
    "data.len", "wlan.fc.type", "wlan.fc.subtype", "time_since_last_packet"
]

X = df[feature_columns]

# ---- Turn "benign"/"DoS attack"/"Replay" into 0/1 ----
# 0 = normal, 1 = any kind of attack
y = df["class"].apply(lambda x: 0 if x == "benign" else 1)

# ---- Split into training data and testing data ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---- Train the model ----
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ---- Check how accurate it is ----
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"✅ Model trained! Accuracy: {accuracy * 100:.2f}%")
print()
print(classification_report(y_test, predictions, target_names=["benign", "attack"]))

# ---- Save it for later use ----
joblib.dump(model, "real_attack_model.pkl")
joblib.dump(feature_columns, "real_model_features.pkl")
print("Model saved as real_attack_model.pkl")

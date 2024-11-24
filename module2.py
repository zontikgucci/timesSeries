import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

def extract_features(data):
    features = {
        'mean': data.mean(),
        'std': data.std(),
        'min': data.min(),
        'max': data.max(),
        'kurtosis': data.kurtosis(),
        'skew': data.skew()
    }

    return features

def prepare_training_data(file_paths, labels):
    X = []
    y = []

    for file_path, label in zip(file_paths, labels):
        data = pd.read_csv(file_path)
        time_series = data['meantemp']
        features = extract_features(time_series)
        X.append(features)
        y.append(label)
    return pd.DataFrame(X), y

file_paths = [
    'annotated_time_series.csv',
    'test_no_anomalies0.csv',
    'test_weak_anomalies0.csv',
    'test_with_anomalies0.csv',
    'test_no_anomalies.csv',
    'test_weak_anomalies.csv',
    'test_with_anomalies.csv',
    'test_no_anomalies1.csv',
    'test_weak_anomalies1.csv',
    'test_with_anomalies1.csv',
    'test_no_anomalies2.csv',
    'test_weak_anomalies2.csv',
    'test_with_anomalies2.csv'
]
labels = [0, 0, 1]

X, y = prepare_training_data(file_paths, labels)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(random_state=42)
model.fit(X_scaled, y)

joblib.dump(model, 'anomaly_classifier.pkl')
joblib.dump(scaler, 'scaler.pkl')

# print("Модель успешно обучена и сохранена!")

def classify_time_series(file_path):
    data = pd.read_csv(file_path)
    time_series = data['meantemp']
    features = extract_features(time_series)

    model = joblib.load('anomaly_classifier.pkl')
    scaler = joblib.load('scaler.pkl')

    features_scaled = scaler.transform(pd.DataFrame([features]))
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]

    return prediction, probability


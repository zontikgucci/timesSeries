import pandas as pd
import numpy as np

def generate_time_series(n_points=100, with_anomalies=False, anomaly_strength=1.0):
    """
    Генерирует временной ряд.

    Parameters:
        n_points (int): Количество точек.
        with_anomalies (bool): Добавлять ли аномалии.
        anomaly_strength (float): Сила аномалий (степень выбросов).

    Returns:
        pd.DataFrame: Временной ряд с датами и значениями.
    """
    np.random.seed(42)  # Фиксируем для воспроизводимости
    dates = pd.date_range(start="2024-01-01", periods=n_points)
    values = np.sin(np.linspace(0, 3 * np.pi, n_points)) + np.random.normal(scale=0.2, size=n_points)

    if with_anomalies:
        num_anomalies = int(0.1 * n_points)  # 10% данных будут аномалиями
        anomaly_indices = np.random.choice(n_points, size=num_anomalies, replace=False)
        values[anomaly_indices] += anomaly_strength * np.random.choice([-1, 1], size=num_anomalies)

    return pd.DataFrame({"date": dates, "meantemp": values})

datasets = {
    "test_no_anomalies3.csv": generate_time_series(with_anomalies=False),
    "test_with_anomalies3.csv": generate_time_series(with_anomalies=True, anomaly_strength=3.0),
    "test_weak_anomalies3.csv": generate_time_series(with_anomalies=True, anomaly_strength=1.5),
}

for file_name, dataset in datasets.items():
    file_path = f"{file_name}"
    dataset.to_csv(file_path, index=False)
    print(f"Сгенерирован файл: {file_path}")

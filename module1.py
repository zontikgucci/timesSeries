import pandas as pd
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.models import MovingAverageFilter
import matplotlib.pyplot as plt


file_path = 'time_series.csv'  # Укажите путь к вашему файлу
data = pd.read_csv(file_path)
data['date'] = pd.to_datetime(data['date'])

column_to_analyze = 'meantemp'  # Метрика для анализа
series = TimeSeries.from_dataframe(data, 'date', column_to_analyze)

scaler = Scaler()
series_normalized = scaler.fit_transform(series)

ma_model = MovingAverageFilter(window=5)
moving_avg = ma_model.filter(series_normalized)

residuals = (series_normalized - moving_avg).pd_series()

threshold = 2 * residuals.std()
anomalies = (abs(residuals) > threshold).astype(int)

data['anomaly'] = anomalies.values

plt.figure(figsize=(12, 6))
plt.plot(data['date'], data[column_to_analyze], label='Original Data', color='blue')
plt.scatter(
    data['date'][data['anomaly'] == 1],
    data[column_to_analyze][data['anomaly'] == 1],
    color='red',
    label='Anomalies'
)
plt.title(f"Anomaly Detection in {column_to_analyze}")
plt.xlabel('Date')
plt.ylabel(column_to_analyze)
plt.legend()
plt.grid()

output_image_path = 'images/anomaly_detection_plot.png'
plt.savefig(output_image_path)
print(f"График сохранён: {output_image_path}")

plt.show()

output_file_path = 'annotated_time_series.csv'
data.to_csv(output_file_path, index=False)
print(f"Размеченный файл сохранён: {output_file_path}")


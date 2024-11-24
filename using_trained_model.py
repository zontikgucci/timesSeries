from module2 import classify_time_series

test_file = 'test_with_anomalies3.csv'

prediction, probability = classify_time_series(test_file)
print(f'Название файла: {test_file}')
print(f"Класс временного ряда: {prediction}")
print(f"Вероятности классов: {probability}")
import pandas as pd
import numpy as np
#создал таблицу с пропусками
table = pd.DataFrame({
    "country": ["Russia", "France", np.nan, "Germany", np.nan],
    "capital": ["Moscow", "Paris", "Berlin", np.nan, "Rome"]
})
print(table)

#заполнил пропуски значением "Unknown"
columns = table.select_dtypes(include=["object"]).columns
table[columns] = table[columns].fillna("Unknown")
print("\nпосле обработки:")
print(table)

#проверка метрики
assert (table.isna().sum() == 0).all(), "Ошибка"
print("\nпропусков нет")

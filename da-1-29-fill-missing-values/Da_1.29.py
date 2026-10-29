import pandas as pd

#функция загружает CSV в DataFrame
def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

#функция заполняет пропуски в выбранных столбцах
def fill_missing_values(table: pd.DataFrame, columns: list[str], fill_value: str = "Unknown") -> pd.DataFrame:
    missing_cols = [c for c in columns if c not in table.columns]
    if missing_cols:
        raise KeyError(f"В таблице нет столбцов: {missing_cols}")
    table = table.copy()
    table[columns] = table[columns].fillna(fill_value)
    return table

#функция проверяет отсутствие пропусков.
#если указан param columns, то проверяются только указанные столбцы, если нет, то вся таблица
def check_no_missing(table: pd.DataFrame, columns: list[str] or None = None) -> None:
    subset = columns if columns else table.columns.tolist()
    nulls = table[subset].isna().sum()
    if (nulls > 0).any():
        details = nulls[nulls > 0].to_string()
        raise AssertionError("Остались пропуски в столбцах:\n" + details)

if __name__ == "__main__":
    filepath = "data.csv"
    df = load_data(filepath)
    print("Исходные данные:\n", df)

    print("\nДоступные столбцы:", df.columns.tolist())
    user_cols = input("Введите названия столбцов через запятую: ").split(",")
    user_cols = [c.strip() for c in user_cols if c.strip()]

    fill_value = input('Чем заполнить пропуски? (Enter для "Unknown"): ').strip() or "Unknown"

    df_clean = fill_missing_values(df, user_cols, fill_value=fill_value)
    print("\nПосле обработки:\n", df_clean)

    # Проверяем только выбранные столбцы
    check_no_missing(df_clean, columns=user_cols)
    print("\nВ выбранных столбцах нет пропусков")

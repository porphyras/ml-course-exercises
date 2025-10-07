Вот полный текст README — можешь просто вставить в `README.md`:

````markdown
# DA-3-11: Сезонные и циклические признаки (sin/cos)

Мини-проект показывает, как из метки времени извлечь **час суток** и закодировать его
парами признаков **sin/cos**, чтобы модель «видела» цикличность (23:00 и 00:00 — соседи).
Идея объединяет карточки **DA-2-34** и **DA-2-07**.

## About the Libraries
- **pandas** — работа с временными рядами и датами/временем  
- **NumPy** — векторная математика (sin/cos)  
- **Matplotlib** — визуализация (scatter: sin vs cos)

## Program Description
Скрипт `Da-3-11.py` выполняет:
1. **Загрузка/генерация данных**  
   Чтение CSV со столбцом временных меток **или** генерация синтетического ряда `pandas.date_range()`.
2. **Проверка типа datetime**  
   Убеждается, что столбец существует и корректно парсится в `datetime` (без `NaT`).
3. **Извлечение часа**  
   Создаёт колонку `hour` (диапазон `0..23`) через `.dt.hour`.
4. **Циклическое кодирование**  
   Считает:  
   `hour_sin = sin(2π · hour / 24)`  
   `hour_cos = cos(2π · hour / 24)`
5. **Визуализация (опционально)**  
   Scatter `hour_sin` vs `hour_cos` — точки лежат на единичной окружности.
6. **Сохранение результата**  
   Пишет таблицу в **Da-3-11.csv** (по умолчанию).

## Requirements
- Python 3.9+
- pandas, numpy, matplotlib

Установка:
```bash
pip install pandas numpy matplotlib
````

## Running the Program

### Option A — Синтетический ряд

```bash
python Da-3-11.py --periods 24 --plot --plot-out hour_scatter.png
```

Параметры:

* `--periods` — количество точек (например, 24 часа)
* `--freq` — шаг для `date_range` (например, `h`, `15min`, `D`), по умолчанию `h`
* `--start` — начало ряда (строка времени)

### Option B — Свой CSV

```bash
python Da-3-11.py --input my_times.csv --ts-col timestamp --plot
```

`timestamp` — имя столбца с датой/временем.

### Option C — Кастомная частота и длина

```bash
python Da-3-11.py --start "2025-01-01 00:00:00" --periods 7*24 --freq h --plot
```

## Output files

* **Da-3-11.csv** — таблица с колонками: `timestamp, hour, hour_sin, hour_cos`
* **hour_scatter.png** — круговой scatter (если задан `--plot-out`)

## Sample Output

```
          timestamp  hour  hour_sin  hour_cos
2025-01-01 00:00:00     0  0.000000  1.000000
2025-01-01 01:00:00     1  0.258819  0.965926
2025-01-01 02:00:00     2  0.500000  0.866025
...
[OK] Saved: /path/to/Da-3-11.csv | Rows: 24
```

## Real-World Applications

* суточные паттерны активности пользователей
* энергопотребление / нагрузки ИТ-систем
* транспорт (часы пик), логистика
* прогноз спроса или web-трафика

## Functions Overview

### `build_synthetic(start: str, periods: int, freq: str, ts_col: str) -> pd.DataFrame`

Генерирует равномерный временной ряд и возвращает DataFrame с колонкой `ts_col`.

### `ensure_datetime(df: pd.DataFrame, ts_col: str) -> pd.DataFrame`

Проверяет наличие `ts_col`, приводит к `datetime`, гарантирует отсутствие `NaT`.

### `extract_hour(df: pd.DataFrame, ts_col: str, out_col: str = "hour") -> pd.DataFrame`

Извлекает час (`0..23`) из метки времени в колонку `out_col`.

### `encode_cyclical(series: pd.Series, period: int, prefix: str) -> pd.DataFrame`

Кодирует периодическую величину парой признаков `prefix_sin`, `prefix_cos`.

### `scatter_sin_cos(df: pd.DataFrame, sin_col: str, cos_col: str, title: str, save_path: Optional[Path])`

Строит scatter между `sin_col` и `cos_col`; сохраняет в файл при наличии `save_path`.

---

**Примечания:**

* Используйте **строчную** частоту `h` (а не `H`), чтобы избежать предупреждения pandas.
* Если картинка не появляется, укажите абсолютный путь в `--plot-out`.

```
```

# DA-3-11: Сезонные и циклические признаки (sin/cos)

Скрипт **Da-3-11.py** извлекает час из временной метки и кодирует его с помощью `sin`/`cos`, а также строит круговую визуализацию.

## Быстрый старт
```bash
python Da-3-11.py --periods 24 --plot --plot-out hour_scatter.png
```

## Выходные файлы
- `Da-3-11.csv` — результат с колонками: `timestamp, hour, hour_sin, hour_cos`.
- `hour_scatter.png` — круговая диаграмма (если указан `--plot-out`).

## Зависимости
```bash
pip install pandas numpy matplotlib
```

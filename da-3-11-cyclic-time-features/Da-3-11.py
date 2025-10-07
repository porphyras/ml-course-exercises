import argparse
from typing import Optional
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PI2 = 2.0 * np.pi

def build_synthetic(start: str = "2025-01-01 00:00:00",
                    periods: int = 24*7,
                    freq: str = "h",
                    ts_col: str = "timestamp") -> pd.DataFrame:
    """Создает синтетический временной ряд равномерного шага."""
    # pd.date_range генерирует последовательность меток времени
    rng = pd.date_range(start=start, periods=periods, freq=freq)
    # Возвращаем таблицу с одной колонкой временных меток
    return pd.DataFrame({ts_col: rng})

def ensure_datetime(df: pd.DataFrame, ts_col: str) -> pd.DataFrame:
    """Проверяет и приводит колонку к типу datetime, гарантирует валидность."""
    if ts_col not in df.columns:
        raise KeyError(f"Входной CSV не содержит столбец '{ts_col}'.")
    out = df.copy()
    # errors='raise' — если дата не парсится, не молчим, а падаем
    out[ts_col] = pd.to_datetime(out[ts_col], errors="raise")
    if out[ts_col].isna().any():
        raise ValueError("Столбец временных меток содержит NaT.")
    return out

def extract_hour(df: pd.DataFrame, ts_col: str, out_col: str = "hour") -> pd.DataFrame:
    """Извлекает час из временной метки (0..23) в отдельную колонку."""
    out = df.copy()
    out[out_col] = out[ts_col].dt.hour
    return out

def encode_cyclical(series: pd.Series, period: int, prefix: str) -> pd.DataFrame:
    """Возвращает sin/cos кодировку величины series с заданным периодом."""
    angle = PI2 * series.astype(float) / float(period)
    return pd.DataFrame(
        {f"{prefix}_sin": np.sin(angle),
         f"{prefix}_cos": np.cos(angle)},
        index=series.index
    )

def scatter_sin_cos(df: pd.DataFrame,
                    sin_col: str,
                    cos_col: str,
                    title: str = "Циклическое кодирование часа: sin vs cos",
                    save_path: Optional[Path] = None) -> None:
    """Рисует scatter между sin и cos (круговая визуализация)."""
    plt.figure()
    plt.scatter(df[sin_col], df[cos_col], s=18, alpha=0.8)
    plt.xlabel(sin_col)
    plt.ylabel(cos_col)
    plt.title(title)
    # Одинаковый масштаб по осям, чтобы окружность не искажалась
    plt.axis("equal")
    plt.tight_layout()
    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()


def main(argv=None):
    p = argparse.ArgumentParser(
        description=(
            "DA-2-34 / DA-2-07: сезонные и циклические признаки. "
            "Извлекаем час из временной метки и кодируем его sin/cos."
        )
    )
    # Источник данных
    p.add_argument("--input", type=Path, default=None,
                   help="CSV с временными метками; если не задан — создадим синтетический ряд.")
    p.add_argument("--ts-col", type=str, default="timestamp",
                   help="Имя столбца с временными метками (по умолчанию 'timestamp').")

    # Синтетика
    p.add_argument("--start", type=str, default="2025-01-01 00:00:00",
                   help="Начало синтетического ряда.")
    p.add_argument("--periods", type=int, default=24*7,
                   help="Число точек синтетики (по умолчанию неделя часовыми метками).")
    p.add_argument("--freq", type=str, default="h",
                   help="Частота синтетики (например, 'h', '15min').")

    # Выводы
    p.add_argument("--out", type=Path, default=Path("Da-3-11.csv"),
                   help="Куда сохранить итоговый CSV (по умолчанию Da-3-11.csv).")
    p.add_argument("--plot", action="store_true",
                   help="Построить scatter график sin vs cos.")
    p.add_argument("--plot-out", type=Path, default=None,
                   help="Сохранить график в файл (если не задано — показать на экране).")
    p.add_argument("--head", type=int, default=0,
                   help="Печать первых N строк результата в stdout для просмотра.")

    args = p.parse_args(argv)

    # 1) Получаем данные: читаем CSV или генерируем синтетику
    if args.input is not None:
        df = pd.read_csv(args.input)
    else:
        df = build_synthetic(args.start, args.periods, args.freq, ts_col=args.ts_col)

    # 2) Преобразуем к datetime и извлекаем час
    df = ensure_datetime(df, args.ts_col)
    df = extract_hour(df, args.ts_col, out_col="hour")

    # 3) Циклическое кодирование часа
    cyc = encode_cyclical(df["hour"], period=24, prefix="hour")
    result = pd.concat([df, cyc], axis=1)

    # 4) Сохраняем CSV (по умолчанию Da-3-11.csv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.out, index=False)

    # 5) График sin vs cos для часа
    if args.plot:
        scatter_sin_cos(result, "hour_sin", "hour_cos", save_path=args.plot_out)

    # 6) Опциональный превью в консоли
    if args.head and args.head > 0:
        print(result.head(args.head).to_string(index=False))

    print(f"[OK] Сохранено: {args.out.resolve()} | Строк: {len(result)}")


if __name__ == "__main__":
    main()

import argparse
import os
from typing import List, Tuple
import cv2
import numpy as np
from PIL import Image, ImageDraw

HSV_RED_LOWER_1 = np.array([0, 100, 100])
HSV_RED_UPPER_1 = np.array([10, 255, 255])
HSV_RED_LOWER_2 = np.array([170, 100, 100])
HSV_RED_UPPER_2 = np.array([180, 255, 255])

# загружает изображение по пути с помощью OpenCV
# бросает ошибку, если файл не найден или не читается
def load_image(path: str):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Не удалось открыть изображение: {path}")
    return img

#переводит изображение в HSV и строит бинарную маску красного цвета
#использует два диапазона красного и морфологические операции для очистки
def red_mask_hsv(image_bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, HSV_RED_LOWER_1, HSV_RED_UPPER_1)
    mask2 = cv2.inRange(hsv, HSV_RED_LOWER_2, HSV_RED_UPPER_2)
    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    return mask

#находит контуры в маске и возвращает только те, чья площадь находится в заданном диапазоне (min_area–max_area)
def filter_contours_by_area(mask: np.ndarray, min_area: int, max_area: int) -> List[Tuple[np.ndarray, float]]:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    kept = []
    for c in contours:
        area = cv2.contourArea(c)
        if min_area <= area <= max_area:
            kept.append((c, float(area)))
    return kept

#рисует найденные контуры, отмечает центр масс и подписывает площадь каждого объекта
def draw_results(image_bgr: np.ndarray, kept_contours: List[Tuple[np.ndarray, float]]) -> np.ndarray:
    out = image_bgr.copy()
    for c, area in kept_contours:
        cv2.drawContours(out, [c], -1, (0,255,0), 2)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"]/M["m00"]); cy = int(M["m01"]/M["m00"])
            cv2.circle(out, (cx,cy), 2, (255,0,0), -1)
            cv2.putText(out, f"{int(area)}", (cx+4, cy-4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,0), 2, cv2.LINE_AA)
            cv2.putText(out, f"{int(area)}", (cx+4, cy-4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 1, cv2.LINE_AA)
    return out

#создаёт тестовое изображение: красные кружки разных размеров + шумовые фигуры других цветов
#сохраняет результат в файл
def generate_synthetic(path: str, w: int=400, h: int=300, seed: int=10):
    rng = np.random.default_rng(seed)
    img = Image.new("RGB", (w,h), (240,240,240))
    draw = ImageDraw.Draw(img)
    reds = [(255,30,60), (230,0,0), (200,20,80)]
    for _ in range(8):
        x, y = int(rng.integers(20, w-20)), int(rng.integers(20, h-20))
        r = int(rng.integers(5, 25))
        draw.ellipse((x-r, y-r, x+r, y+r), fill=reds[int(rng.integers(0, len(reds)))], outline=(120,0,0))
    for _ in range(2):
        x, y = int(rng.integers(50, w-50)), int(rng.integers(50, h-50))
        r = int(rng.integers(28, 40))
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,10), outline=(100,0,0))
    for _ in range(10):
        x, y = int(rng.integers(20, w-20)), int(rng.integers(20, h-20))
        r = int(rng.integers(6, 22))
        color = tuple(int(v) for v in rng.integers(0,200, size=3))
        draw.rectangle((x-r, y-r, x+r, y+r), fill=color)
    img.save(path)

#основной рабочий процесс: загружает изображение, создаёт маску красного, находит и фильтрует контуры по площади, рисует результат,
#сохраняет исходник, маску и результат в папку out.
def run(input_path: str, out_dir: str, min_area: int, max_area: int):
    os.makedirs(out_dir, exist_ok=True)
    img = load_image(input_path)
    mask = red_mask_hsv(img)
    kept = filter_contours_by_area(mask, min_area, max_area)
    result = draw_results(img, kept)

    src_path = os.path.join(out_dir, "source.png")
    mask_path = os.path.join(out_dir, "mask.png")
    res_path  = os.path.join(out_dir, "result.png")

    cv2.imwrite(src_path, img)
    cv2.imwrite(mask_path, mask)
    cv2.imwrite(res_path, result)

    print(f"Найдено объектов в диапазоне [{min_area}, {max_area}]: {len(kept)}")
    print("Площади:", [int(a) for _, a in kept])
    print("Сохранено:")
    print("  ", src_path)
    print("  ", mask_path)
    print("  ", res_path)

#разбирает аргументы командной строки (--input, --generate, --out-dir, --min-area, --max-area),
#возвращает объект с параметрами запуска
def parse_args():
    ap = argparse.ArgumentParser(description="CV-2-17: поиск красных объектов заданного размера")
    ap.add_argument("--input", type=str, help="Путь к входному изображению (BGR/RGB).")
    ap.add_argument("--generate", action="store_true", help="Сгенерировать синтетическое изображение и использовать его.")
    ap.add_argument("--out-dir", type=str, default="out", help="Каталог для сохранения результатов.")
    ap.add_argument("--min-area", type=int, default=200, help="Минимальная площадь контура.")
    ap.add_argument("--max-area", type=int, default=1000, help="Максимальная площадь контура.")
    return ap.parse_args()

#если указан generate, то создаёт тестовое изображение,
#иначе берёт путь к пользовательскому файлу
#Запускает обработку через run
def main():
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    if args.generate:
        synth_path = os.path.join(args.out_dir, "synthetic.png")
        generate_synthetic(synth_path)
        input_path = synth_path
    else:
        if not args.input:
            raise SystemExit("Укажите --input ИЛИ флаг --generate")
        input_path = args.input
    run(input_path=input_path, out_dir=args.out_dir, min_area=args.min_area, max_area=args.max_area)

if __name__ == "__main__":
    main()

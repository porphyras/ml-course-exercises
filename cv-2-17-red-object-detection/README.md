# CV-2-17: Detecting Red Objects by Size with OpenCV

This project demonstrates how to detect **red objects** in an image using color filtering and contour analysis.  
It combines techniques from two tasks: **CV-1-12 (HSV red mask)** and **CV-2-01 (contour features)**.

## About the OpenCV Library

[OpenCV](https://opencv.org/) is a powerful computer vision library. It provides tools for:
- **Image processing** (color spaces, filtering, morphological operations)  
- **Contour detection** and feature extraction  
- **Object detection** and analysis  

We use OpenCV together with **NumPy** (for array operations) and **Pillow** (for generating synthetic images).

## Program Description

The program detects **red objects of specific size (200–1000 pixels area)** in an image.

### 1. Loading an Image
- Images are loaded using `cv2.imread()` (supports PNG, JPG, BMP, TIFF).  
- Optionally, a synthetic test image can be generated automatically.  

### 2. Red Mask Creation
- The image is converted to HSV color space.  
- Two red ranges are used:  
  - `[0–10°]` (HSV lower red)  
  - `[170–180°]` (HSV upper red)  
- Masks are combined and cleaned with morphological operations.  

### 3. Contour Detection
- Contours are extracted using `cv2.findContours()`.  
- Areas are computed with `cv2.contourArea()`.  

### 4. Filtering by Area
- Only contours with area between **200–1000 pixels** are kept.  

### 5. Drawing Results
- Detected contours are drawn in green.  
- Centers of mass are marked with blue dots.  
- Areas are annotated as text near each object.  

### 6. Output
The program saves:  
- `source.png` – original image  
- `mask.png` – binary mask of red objects  
- `result.png` – final image with contours and labels  

## Requirements

- Python 3.8+  
- OpenCV  
- NumPy  
- Pillow  

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Program

### Option A — Generate a synthetic test image
```bash
python cv_2_17.py --generate --out-dir out
```

### Option B — Use your own image
Place your image in the `data/` folder and run:
```bash
python cv_2_17.py --input data/my_image.png --out-dir out
```

### Option C — Change area thresholds
```bash
python cv_2_17.py --input data/my_image.png --min-area 150 --max-area 2000
```

## Sample Output

```
Найдено объектов в диапазоне [200, 1000]: 4
Площади: [481, 662, 250, 250]
Сохранено:
   out/source.png
   out/mask.png
   out/result.png
```

## Real-World Applications

This approach can be used for:
- Detecting traffic signs (e.g., **STOP** signs)  
- Counting red fruits (e.g., apples, cherries, tomatoes)  
- Identifying warning signals (e.g., red lights on machinery)  
- Tracking red objects in robotics or games  

## Functions Overview

### `red_mask_hsv(image_bgr: np.ndarray) -> np.ndarray`
Creates a binary mask of red pixels in the image.

### `filter_contours_by_area(mask: np.ndarray, min_area: int, max_area: int)`
Finds contours in the mask and filters them by area.

### `draw_results(image_bgr: np.ndarray, kept_contours)`
Draws contours, centers, and areas on the image.

### `generate_synthetic(path: str, w: int = 400, h: int = 300, seed: int = 2)`
Generates a synthetic image with red and non-red shapes for testing.

---

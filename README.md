# ML Course Exercises

Short exercises from the data analysis and computer vision course at Novosibirsk State University.
Each folder is self-contained, with its own README and `requirements.txt`.

| Exercise | Topic | Stack |
|---|---|---|
| [DA-1-29](da-1-29-fill-missing-values) | Filling missing values in a table, choosing columns interactively | pandas |
| [DA-3-11](da-3-11-cyclic-time-features) | Cyclic time features: encoding the hour of day as sin/cos | pandas, NumPy, Matplotlib |
| [CV-2-17](cv-2-17-red-object-detection) | Detecting red objects of a given size with an HSV mask and contours | OpenCV, NumPy |

## Run

```sh
cd <exercise-folder>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python <script>.py
```

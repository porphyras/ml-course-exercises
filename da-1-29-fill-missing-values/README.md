# Filling Missing Values in Pandas DataFrame

This project demonstrates how to detect and handle missing values in a Pandas DataFrame.

## About the Pandas Library

Pandas is a Python library for working with tabular data. It provides:
- **Series** – one-dimensional arrays with labels
- **DataFrame** – two-dimensional tables with row and column labels
- Convenient tools for detecting, analyzing, and handling missing values

## Program Description

The program shows a simple workflow for filling missing values in a DataFrame.

### 1. Creating Source Data
A DataFrame is created with missing values (`NaN`) in the `country` and `capital` columns.

### 2. Filling Missing Values
- Only object-type (string) columns are selected  
- All missing values are replaced with the string `"Unknown"` using the `fillna()` method

### 3. Validation
- After filling, the program checks that no missing values remain using:
  ```python
  assert (table.isna().sum() == 0).all(), "Ошибка"
  ```

### 4. Output
The program prints:
- The original DataFrame with missing values
- The cleaned DataFrame after processing
- Confirmation that no missing values remain

## Requirements

- Python 3.6+
- Pandas
- NumPy

Install dependencies:
```bash
pip install pandas numpy
```

## Running the Program

Save the code to a file, e.g. `Da_1.29.py`, and run:
```bash
python Da_1.29.py
```

## Sample Output

```
   country  capital
0   Russia   Moscow
1   France    Paris
2      NaN   Berlin
3  Germany      NaN
4      NaN     Rome

после обработки:
   country  capital
0   Russia   Moscow
1   France    Paris
2  Unknown   Berlin
3  Germany  Unknown
4  Unknown     Rome

пропусков нет
```

## Real-World Applications

This approach is useful for:
- Preparing raw datasets for machine learning
- Cleaning survey data with missing answers
- Ensuring data consistency in reports and dashboards
- Replacing unknown values in categorical features

# Filling Missing Values from CSV with Pandas

This project demonstrates how to load data from a CSV file, interactively choose columns, and fill missing values in a Pandas DataFrame.

## About the Pandas Library

Pandas is a Python library for working with tabular data. It provides:
- **Series** – one-dimensional arrays with labels  
- **DataFrame** – two-dimensional tables with row and column labels  
- Convenient tools for detecting, analyzing, and handling missing values  

## Program Description

The program implements a workflow for filling missing values with user interaction.

### 1. Loading Data
- Data is loaded from a CSV file using `pd.read_csv()`.  
- Example CSV (`data.csv`):  
  ```csv
  country,capital
  Russia,Moscow
  France,Paris
  ,Berlin
  Germany,
  ,Rome
  ```

### 2. User Interaction
- The program displays available columns in the DataFrame.  
- The user chooses which columns to process (comma-separated input).  
- The user specifies the replacement value (default is `"Unknown"`).  

### 3. Filling Missing Values
- Selected columns are processed using the `fillna()` method.  
- Missing values are replaced with the chosen value.  

### 4. Validation
- After filling, the program checks the selected columns for remaining missing values.  
- If any are found, an error is raised with details.  

### 5. Output
The program prints:
- The original DataFrame with missing values  
- The cleaned DataFrame after processing  
- Confirmation that no missing values remain in the chosen columns  

## Requirements

- Python 3.8+  
- Pandas  

Install dependencies:
```bash
pip install pandas
```

## Running the Program

Save the code to a file, e.g. `main.py`, and run:
```bash
python main.py
```

Follow the prompts in the console to choose columns and replacement value.

## Sample Output

```
Initial data:
   country capital
0   Russia  Moscow
1   France   Paris
2      NaN  Berlin
3  Germany    NaN
4      NaN    Rome

Available columns: ['country', 'capital']
Enter column names separated by comma: capital
Replacement value? (Enter for "Unknown"):

Processed data:
   country  capital
0   Russia   Moscow
1   France    Paris
2      NaN   Berlin
3  Germany  Unknown
4      NaN     Rome

No missing values in the selected columns
```

## Real-World Applications

This approach is useful for:
- Cleaning datasets before analysis or machine learning  
- Handling survey results with incomplete answers  
- Preparing CSV data for reporting and dashboards  
- Replacing missing categorical values in production datasets  

## Functions Overview

### `load_data(filepath: str) -> pd.DataFrame`
Loads data from a CSV file into a Pandas DataFrame.

### `fill_missing_values(table: pd.DataFrame, columns: list[str], fill_value: str = "Unknown") -> pd.DataFrame`
Fills missing values in the specified columns with the given value.

### `check_no_missing(table: pd.DataFrame, columns: list[str] or None = None) -> None`
Checks that no missing values remain.  
- If `columns` is provided, only those columns are checked.  
- If `columns` is `None`, the entire DataFrame is checked.

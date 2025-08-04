# Generic Google API Python script

This folder contains `search_google.py` - a Python script that searches a custom Google search with queries specified in `queries.csv` and saves the results in search_results.csv.

Requirements: Python installed

To run the script:
1. Install the requirements
    ```bash
    pip install -r requirements.txt
    ```
2. Run the Python script
    ```python
    python search_google.py
    ```

## `queries.csv`
This is the csv which the script expects to contain the queries in the first column only.
> Note: the first row is the field title and not included in the searches.

## `search_results_{timestamp}.csv`
This is the csv where the results will be stored.

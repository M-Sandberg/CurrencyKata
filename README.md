# Handling Missing Exchange Rates

## The Data
You will be working with two tables:

### `currency_exchange`
This table contains exchange rates for various currencies to SEK (Swedish Krona) on specific dates.

| Column                 | Type   | Description                                 |
|------------------------|--------|---------------------------------------------|
| `currency_to_sek`      | REAL   | Exchange rate from the currency to SEK      |
| `date`                 | DATE   | Date of the exchange rate                   |
| `currency`             | TEXT   | Currency code (e.g., USD, EUR)              |
| `currency_description` | TEXT   | Full name of the currency                   |

### `orders`
This table contains transaction data for orders. Orders are recorded in various currencies but do not include any exchange rate.

| Column         | Type     | Description                                               |
|----------------|----------|-----------------------------------------------------------|
| `order_id`     | INTEGER  | Unique ID for the order (Primary Key)                    |
| `paid_date`    | DATE     | Date the order was paid                                  |
| `order_total`  | REAL     | Total amount of the order in the original currency       |
| `site_name`    | TEXT     | Name of the website where the order was placed           |
| `site_country` | TEXT     | Country of the website                                   |
| `currency`     | TEXT     | Currency code of the order (e.g., USD, EUR)             |

## The Task
Your goal is to match each order with the correct exchange rate from `currency_exchange`. However, some dates are missing in the exchange rate table due to holidays or non-banking days. If a `paid_date` in the order does not have a corresponding exchange rate, you should instead use the **most recent available rate before that date**.

### Example Scenario
**Available exchange rate dates:**

| Date         | Exchange Rate Available? |
|--------------|---------------------------|
| 2024-03-01   | ✅ Yes                     |
| 2024-03-02   | ✅ Yes                     |
| 2024-03-03   | ✅ Yes                     |
| 2024-03-04   | ✅ Yes                     |
| 2024-03-05   | ✅ Yes                     |
| 2024-03-06   | ✅ Yes                     |
| 2024-03-07   | ✅ Yes                     |
| 2024-03-08   | ❌ No                      |
| 2024-03-09   | ❌ No                      |
| 2024-03-10   | ❌ No                      |
| 2024-03-11   | ✅ Yes                     |
| 2024-03-12   | ✅ Yes                     |

**And an order with:**
- `paid_date`: `2024-03-10`

Since there is no exchange rate recorded for `2024-03-10`, we use the most recent available rate before that date, which is from `2024-03-07`.

## How You Can Approach the Problem
You can solve this problem however you prefer – using SQL, Python, or another approach. The most important thing is that you can explain your thought process and your choices.

## Helper Functions Available
These utility functions are available to simplify interaction with the SQLite database (`db.sqlite3`):

### `select(sql: str, params: tuple = (), return_as_pandas: bool = False)`
Executes a SQL query with optional parameters and returns the result.

- `sql`: The SQL query to run.  
- `params`: A tuple of parameters for parameterized queries (default is empty).  
- `return_as_pandas`:  
  - If `True`, returns a **pandas DataFrame**.  
  - If `False`, returns a **list of dictionaries**, one per row.

### `insert(table: str, df: pd.DataFrame, if_exists: str = "append") -> int`
Inserts a pandas DataFrame into the specified SQLite table.

- `table`: Name of the table to insert into.  
- `df`: The DataFrame containing the data to be inserted.  
- `if_exists`:  
  - `"fail"` – raise error if the table already exists  
  - `"replace"` – drop the table before inserting  
  - `"append"` – add to existing table (default)  
- **Returns** the number of rows inserted.

## Things to Keep in Mind
- The exchange rate for an order should be the most recent one available before the `paid_date`.
- All order currencies exist in `currency_exchange`, so a matching exchange rate will always be available.
- The `currency_exchange` table always contains dates both before and after the orders, so there's always at least one rate available before the earliest order.

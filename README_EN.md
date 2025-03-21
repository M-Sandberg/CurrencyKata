# Coding Test: Handling Missing Currency Exchange Data

## The Data

You’ll be working with two tables:

### `currency_exchange`

This table contains exchange rates for various currencies to SEK (Swedish Krona) on specific dates.

| Column                | Type  | Description                                     |
|------------------------|-------|-------------------------------------------------|
| `currency_to_sek`     | REAL  | Exchange rate of the currency to SEK           |
| `date`                | DATE  | Date of the exchange rate                      |
| `currency`            | TEXT  | Currency code (e.g., USD, EUR)                |
| `currency_description`| TEXT  | Full name of the currency                     |

### `orders`

This table contains order data. Orders are placed in various currencies, but the exchange rate is not included.

| Column         | Type    | Description                                             |
|----------------|---------|---------------------------------------------------------|
| `order_id`     | INTEGER | Unique ID for the order (Primary Key)                  |
| `paid_date`    | DATE    | Date the order was paid                                |
| `order_total`  | REAL    | Total amount of the order in its original currency     |
| `site_name`    | TEXT    | Name of the site where the order was placed            |
| `site_country` | TEXT    | Country of the site                                     |
| `currency`     | TEXT    | Currency code of the order (e.g., USD, EUR)           |

---

## The Task

Your goal is to match each order with the correct exchange rate from `currency_exchange`. However, the exchange rate table is missing entries for some dates (e.g., weekends, holidays). If there’s no rate for the exact `paid_date`, use the most recent available exchange rate *before* that date.

### Example Scenario

**Available exchange rate dates:**

| Date        | Exchange Rate Available? |
|-------------|---------------------------|
| 2024-03-01  | ✅ Yes                     |
| 2024-03-02  | ✅ Yes                     |
| 2024-03-03  | ✅ Yes                     |
| 2024-03-04  | ✅ Yes                     |
| 2024-03-05  | ✅ Yes                     |
| 2024-03-06  | ✅ Yes                     |
| 2024-03-07  | ✅ Yes                     |
| 2024-03-08  | ❌ No                      |
| 2024-03-09  | ❌ No                      |
| 2024-03-10  | ❌ No                      |
| 2024-03-11  | ✅ Yes                     |
| 2024-03-12  | ✅ Yes                     |

**And an order with:**
- `paid_date`: `2024-03-10`

There’s no rate for that day, so we look backwards and take the last known rate before it — `2024-03-07`.

---

## How You Can Approach This

You can solve this however you prefer — SQL, Python, or a mix of both. The most important part is being able to explain your thinking and walk through your choices.

---

## A Few Things to Keep in Mind

- The exchange rate for an order should be the **most recent one before** the `paid_date`.
- Every currency used in orders exists in the `currency_exchange` table — there will always be a rate available.
- The `currency_exchange` table includes dates both before and after all orders, so you don’t need to worry about missing initial data.

---

## Helper Functions Available

To make things easier, you have a few utility functions already set up in the notebook. They help you interact with the SQLite database:

### `list_select(sql: str) -> list`
Runs a SQL query and returns the result as a list of dictionaries — one per row.

### `pd_select(sql: str) -> pd.DataFrame`
Runs a SQL query and returns the result as a pandas DataFrame.

### `list_insert(table: str, data: list, if_exists: str = "fail") -> int`
Takes a list of dictionaries (representing rows) and inserts them into the specified table. You can control whether to replace existing rows by setting `if_exists` to `"replace"`.

### `pd_insert(table: str, df: pd.DataFrame, if_exists: str = "fail") -> int`
Same as above, but works with a whole pandas DataFrame instead of a list.

> 💡 **Tip:** These functions handle the database connection and cleanup for you.

---

Let us know if you run into any questions — and good luck!

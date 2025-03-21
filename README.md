# Hantering av Saknade Valutakurser

## Datan
Du kommer att arbeta med två tabeller:

### `currency_exchange`
Denna tabell innehåller valutakurser för olika valutor till SEK (svenska kronor) på specifika datum.

| Kolumn                | Typ   | Beskrivning                                |
|------------------------|--------|---------------------------------------------|
| `currency_to_sek`     | REAL   | Växelkurs från valutan till SEK             |
| `date`                | DATE   | Datum för växelkursen                       |
| `currency`            | TEXT   | Valutakod (t.ex. USD, EUR)                  |
| `currency_description`| TEXT   | Valutans fullständiga namn                  |

### `orders`
Denna tabell innehåller transaktionsdata för beställningar. Beställningar är registrerade i olika valutor men innehåller inte någon växelkurs.

| Kolumn         | Typ     | Beskrivning                                               |
|----------------|----------|------------------------------------------------------------|
| `order_id`     | INTEGER  | Unikt ID för beställningen (Primärnyckel)                 |
| `paid_date`    | DATE     | Datum då beställningen betalades                          |
| `order_total`  | REAL     | Totalt belopp för beställningen i ursprungsvalutan       |
| `site_name`    | TEXT     | Namn på webbplatsen där beställningen gjordes            |
| `site_country` | TEXT     | Landet för webbplatsen                                   |
| `currency`     | TEXT     | Valutakod för beställningen (t.ex. USD, EUR)             |

## Uppgiften
Ditt mål är att matcha varje beställning med rätt växelkurs från `currency_exchange`. Dock saknas vissa datum i växelkurs-tabellen på grund av helgdagar eller bankfria dagar. Om ett datum i `paid_date` inte har någon motsvarande växelkurs, ska du istället använda den senaste tillgängliga växelkursen före det datumet.

### Exempelscenario
**Tillgängliga växelkursdatum:**

| Datum        | Växelkurs Tillgänglig? |
|--------------|-------------------------|
| 2024-03-01   | ✅ Ja                    |
| 2024-03-02   | ✅ Ja                    |
| 2024-03-03   | ✅ Ja                    |
| 2024-03-04   | ✅ Ja                    |
| 2024-03-05   | ✅ Ja                    |
| 2024-03-06   | ✅ Ja                    |
| 2024-03-07   | ✅ Ja                    |
| 2024-03-08   | ❌ Nej                   |
| 2024-03-09   | ❌ Nej                   |
| 2024-03-10   | ❌ Nej                   |
| 2024-03-11   | ✅ Ja                    |
| 2024-03-12   | ✅ Ja                    |

**Och en beställning med:**
- `paid_date`: `2024-03-10`

Eftersom det inte finns någon växelkurs registrerad för `2024-03-10`, använder vi den senaste tillgängliga kursen före detta datum, vilket är från `2024-03-07`.

## Hur Du Kan Angripa Problemet
Du kan lösa detta problem på vilket sätt du vill – med SQL, Python eller annat tillvägagångssätt. Det viktigaste är att du kan förklara din tankegång och dina val.

## Hjälpfunktioner tillgängliga
Dessa hjälpfunktioner finns tillgängliga för att förenkla interaktionen med SQLite-databasen (`db.sqlite3`):

### `select(sql: str, params: tuple = (), return_as_pandas: bool = False)`
Kör en SQL-fråga med valfria parametrar och returnerar resultatet.

- `sql`: SQL-frågan som ska köras.  
- `params`: En tuple med parametrar för parameteriserade frågor (standard är tom).  
- `return_as_pandas`:  
  - Om `True`, returneras ett **pandas DataFrame**.  
  - Om `False`, returneras en **lista med dictionaries**, en per rad.

### `insert(table: str, df: pd.DataFrame, if_exists: str = "append") -> int`
Infogar ett pandas DataFrame i den angivna SQLite-tabellen.

- `table`: Namn på tabellen att infoga i.  
- `df`: DataFrame som innehåller datan som ska infogas.  
- `if_exists`:  
  - `"fail"` – ger fel om tabellen redan finns  
  - `"replace"` – raderar tabellen innan data infogas  
  - `"append"` – lägger till data i befintlig tabell (standard)  
- **Returnerar** antalet rader som infogats.

## Några Saker att Tänka På
- Växelkursen för en beställning ska vara den senast tillgängliga före `paid_date`.
- Alla beställningars valutor finns i `currency_exchange`, så det kommer alltid finnas en växelkurs tillgänglig.
- Tabellen `currency_exchange` innehåller alltid datum både före och efter `orders`, så det finns minst en kurs före den tidigaste beställningen.

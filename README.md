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

## Tillgängliga Hjälpfunktioner

Du har några färdiga funktioner att använda i notebooken:

### `list_select(sql: str) -> list`
Kör en SQL-fråga och ger dig tillbaka resultatet som en lista med dictionaries – en för varje rad i resultatet.

### `pd_select(sql: str) -> pd.DataFrame`
Kör en SQL-fråga och returnerar resultatet som en Pandas DataFrame direkt.

### `list_insert(table: str, data: list, if_exists: str = "fail") -> int`
Stoppar in en lista med dictionaries (dvs. rader) i en tabell i databasen. Du kan styra om befintliga rader ska ersättas genom att sätta if_exists till "replace".

### `pd_insert(table: str, df: pd.DataFrame, if_exists: str = "fail") -> int`
Samma sak som ovan, fast med en hel DataFrame istället för en lista. Du kan styra om befintliga rader ska ersättas genom att sätta if_exists till "replace".

## Några Saker att Tänka På

- Växelkursen för en beställning ska vara den senast tillgängliga före `paid_date`.
- Alla beställningars valutor finns i `currency_exchange`, så det kommer alltid finnas en växelkurs tillgänglig.
- Tabellen `currency_exchange` innehåller alltid datum både före och efter `orders`, så det finns minst en kurs före den tidigaste beställningen.

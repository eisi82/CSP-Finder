# S&P 500 CSP-Finder

## Überblick
Der **S&P 500 CSP-Strike-Finder** ist eine in Python und Streamlit entwickelte Anwendung, die Benutzern hilft, die besten Cash Secured Puts (CSPs) für bis zu drei ausgewählte Aktien aus dem S&P 500 Index zu finden. Anhand benutzerdefinierter Selektionskriterien wie der Laufzeit in Tagen und des CAGR (Compound Annual Growth Rate) werden die optimalen CSPs ermittelt und in übersichtlichen Tabellen präsentiert.

## Funktionen
- Auswahl von bis zu drei Aktien aus dem S&P 500 Index
- Festlegung benutzerdefinierter Selektionskriterien (z.B. Laufzeit in Tagen)
- Anzeige der besten CSPs basierend auf dem CAGR
- Präsentation der Ergebnisse in übersichtlichen Tabellen

## Anforderungen
- Python 3.x
- Streamlit
- Pandas
- Weitere Abhängigkeiten können der `requirements.txt` Datei entnommen werden

## Installation
1. **Repository klonen:**
    ```sh
    git clone https://github.com/dein-benutzername/sp500-csp-strike-finder.git
    cd sp500-csp-strike-finder
    ```

2. **Virtuelle Umgebung erstellen und aktivieren:**
    ```sh
    python -m venv env
    source env/bin/activate  # Auf Windows: .\env\Scripts\activate
    ```

3. **Abhängigkeiten installieren:**
    ```sh
    pip install -r requirements.txt
    ```

## Nutzung
1. **Streamlit-Anwendung starten:**
    ```sh
    streamlit run app.py
    ```

2. **Aktien auswählen und Kriterien festlegen:**
    - Wähle bis zu drei Aktien aus dem S&P 500 Index.
    - Lege die gewünschten Selektionskriterien fest (z.B. Laufzeit in Tagen).

3. **Ergebnisse anzeigen:**
    - Die besten CSPs basierend auf dem CAGR werden in übersichtlichen Tabellen präsentiert.

## Beispiel
Hier ist ein Beispiel für die Nutzung der Anwendung:

1. Starte die Anwendung mit:
    ```sh
    streamlit run app.py
    ```

2. Wähle Aktien wie Apple (AAPL), Microsoft (MSFT) und Amazon (AMZN) aus.

3. Lege die Laufzeit in Tagen fest und lasse die Anwendung die besten CSPs für dich finden.

## Beiträge
Beiträge sind willkommen! Wenn du Ideen hast oder Fehler findest, eröffne bitte ein Issue oder erstelle einen Pull Request.

## Lizenz
Dieses Projekt steht unter der MIT-Lizenz. Siehe die [LICENSE](LICENSE) Datei für weitere Details.

## Autoren
- Dein Name - [dein-github-benutzername](https://github.com/dein-github-benutzername)

---

Vielen Dank fürs Ausprobieren des S&P 500 CSP-Strike-Finders! Wir freuen uns auf dein Feedback.


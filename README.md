# Investment Analysis
## Python Flask application for analysing your investment in three different currencies

Aplikacja powstała w celu przeanalizowania za pomocą API Narodowego Banku Polskiego inwestycji w trzy waluty kwotą 100zł na 30 dni. Analiza pokazuje jak zmieniała się wartość zainwestowanych pieniędzy w czasie, jak zmianiły się kursy walut oraz procentowy udział walut w ciągu inwestycji i po wypłacie (wymianie) pieniędzy.

## Technologie
- [NBP API](https://api.nbp.pl/) - Pobieranie kursów walut
- [Flask](https://flask.palletsprojects.com/) - Tworzenie aplikacji WEBowej, obsługa formularzy i wyświetlanie wyników
- [Matplotlib](https://matplotlib.org/stable/index.html) - Tworzenie wykresów
- [Requests](https://requests.readthedocs.io/en/latest/) - Pobieranie danych z API NBP

## Instalacja aplikacji
Aplikacja stworzona została przy użyciu Pythona w wersji 3.12.3. Aby zainstalować aplikacje zaleca się skonfigurować i uruchomić wirtualne środowisko Python ([Link](https://docs.python.org/pl/3/tutorial/venv.html) do dokumentacji) następnie za pomocą PIP Python ([dokumentacja](https://pip.pypa.io/en/stable/)) zainstalować zależności z pliku requirements.txt.
```
pip install -r requirements.txt
```
Jeśli instalacja przebiegła pomyślnie można uruchomić aplikację:
```
python app.py
```
Domyślnie aplikacja powinna uruchomić się pod adresem: http://127.0.0.1:5000

## Używanie aplikacji
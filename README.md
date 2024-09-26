# Investment Analysis
## Python Flask application for analysing your investment in three different currencies

![ISS_17050_05987-1](https://github.com/user-attachments/assets/922826b8-f6d6-49b2-973e-7dada62663bd)

Aplikacja powstała w celu przeanalizowania za pomocą API Narodowego Banku Polskiego inwestycji w trzy waluty kwoty 1000zł na 30 dni. Analiza pokazuje jak zmieniała się wartość zainwestowanych pieniędzy w czasie, jak zmieniały się kursy walut oraz procentowy udział walut w ciągu inwestycji i po wypłacie (wymianie) pieniędzy.

## Technologie
- [NBP API](https://api.nbp.pl/) - Pobieranie kursów walut
- [Flask](https://flask.palletsprojects.com/) - Tworzenie aplikacji WEBowej, obsługa formularzy i wyświetlanie wyników
- [Matplotlib](https://matplotlib.org/stable/index.html) - Tworzenie wykresów
- [Requests](https://requests.readthedocs.io/en/latest/) - Pobieranie danych z API NBP

## Instalacja aplikacji
Aplikacja została stworzona przy użyciu Pythona w wersji 3.12.3. Aby zainstalować aplikację zaleca się skonfigurować i uruchomić wirtualne środowisko Python ([Link](https://docs.python.org/pl/3/tutorial/venv.html) do dokumentacji) następnie za pomocą PIP Python ([dokumentacja](https://pip.pypa.io/en/stable/)) zainstalować zależności z pliku requirements.txt:
```
pip install -r requirements.txt
```
Jeśli instalacja przebiegła pomyślnie można uruchomić aplikację:
```
python app.py
```
Domyślnie aplikacja powinna uruchomić się pod adresem: http://127.0.0.1:5000

## Używanie aplikacji

Strona główna:
![1](https://github.com/user-attachments/assets/f6256a6c-49d9-4d59-9407-e209eaed696c)

Z rozwijanych list wybieramy trzy waluty, w które chcemy zainwestować:
![2](https://github.com/user-attachments/assets/2060fb84-2e61-4eb7-b4bd-c9071e7fdbc0)

Uzupełniamy procent w jakim chcemy zainwestować w daną walutę:
![3](https://github.com/user-attachments/assets/145f240c-48b6-4cd4-b11f-38ad2f69817c)

Wybieramy datę początku inwestycji (maksymalna data rozpoczęcia inwestycji ograniczona jest do miesiąca wstecz aby uniknąć błędnie pobranych danych z API):
![4](https://github.com/user-attachments/assets/fcd13cff-5261-43c0-9f73-e53315e23d7d)

Po uzupełnieniu danych rozpoczynamy analizę.

Wynik analizy:
![5](https://github.com/user-attachments/assets/abb0da8f-b6e5-489d-b07a-d440be1ecf03)
![6](https://github.com/user-attachments/assets/4fbb3299-49cc-4600-9856-e7cf22231ba7)
![7](https://github.com/user-attachments/assets/65331ea4-814d-4631-896f-cda44898521f)
![8](https://github.com/user-attachments/assets/24be5697-0e49-452b-ba8b-f0dc761e8778)









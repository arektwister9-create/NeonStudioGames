# NEON EMPIRE 0.8.0 — Android

Polska gra idle offline. `versionName 0.8.0`, `versionCode 10`; identyfikatory Android i zasoby startowe z 0.7.0 pozostają zachowane.

## Nowość: kampania „Przebudzenie rdzenia”

Cel gry: zdobyć sześć fragmentów i otworzyć bramę międzygwiezdną. Przy rdzeniu widać aktualny rozdział, fabułę, wymagania, nagrodę i skróty prowadzące do potrzebnych kolonii, badań i ulepszeń. Celami są konkretne konstrukcje i technologie, nie samo przekraczanie kolejnych progów energii.

Każde dotknięcie ładuje pierścień rdzenia. Po 12 dotknięciach gracz może **wyzwolić puls**, który daje energię i zasila latarnie potrzebne w kampanii. Ładunek nie wygasa. Kolejne fragmenty zwiększają siłę pulsów o 15% wartości bazowej i co dwa rozdziały zmniejszają liczbę wymaganych dotknięć. Nagroda pulsu: `ceil(max(25, produkcja × 15 + energiaDotknięcia × 8) × (1 + 0.15 × ukończoneRozdziały))`. Puls nie zmienia stałych bonusów planet ani produkcji offline.

| Rozdział | Cel rozwoju | Pulsy łącznie | Nagroda energii |
| --- | --- | ---: | ---: |
| Pierwszy sygnał | 3 drony | 1 | 250 |
| Latarnia Luna-9 | Luna, poziom 2 | 3 | 2 500 |
| Przekaźnik Marsa | Mars, poziom 3; Nadprzewodnictwo | 5 | 15 000 |
| Echo Tytana | Tytan, poziom 2; Sieć nadprzewodząca | 8 | 75 000 |
| Stabilizacja bramy | Każda kolonia, poziom 5; Rezonans rdzenia | 12 | 250 000 |
| Po drugiej stronie | Każda kolonia, poziom 7; Tytan, poziom 10; Serce Tytana | 18 | 1 000 000 |

Po spełnieniu wymagań gracz powtarza sekwencję trzech ponumerowanych, kolorowych węzłów. Nie ma limitu czasu ani kary zasobowej za błąd. Numery umożliwiają grę bez rozróżniania kolorów; przyciski obsługują klawiaturę. Krok synchronizacji, rozdziały, liczba pulsów i ładunek są zapisywane jako opcjonalne `coreCampaign` w istniejącym formacie `version: 5`. Zapisy 0.6.1, 0.7.0 i 0.7.1 zachowują postęp i otrzymują pustą kampanię. Posiadane kolonie i technologie od razu liczą się do celów. Nagroda za rozdział jest jednorazowa.

Finał otwiera widoczną bramę wokół rdzenia i pokazuje zakończenie. Gra pozostaje dostępna po finale; nie ma resetu ani utraty kolonii. Nowe efekty respektują ograniczenie animacji i ustawienia dźwięku z 0.7.1.

## Rdzeń i dźwięk

Usunięto prostokątne podświetlenie dotyku WebView przez `-webkit-tap-highlight-color: transparent` i natywny wygląd przycisku. Rdzeń pozostaje przyciskiem HTML obsługującym dotyk, mysz, Enter i spację, z widocznym obrysem fokusu klawiatury.

Naciśnięcie dodaje krótki impuls światła, falę energii, cztery iskry i unoszącą się wartość energii. Efekty animują transformację i przezroczystość; mają limit ośmiu grup i znikają po 720 ms. Preferencja ograniczenia ruchu wyłącza efekty. Listy ulepszeń i planet są przebudowywane przy zmianie stanu, nie przy każdym dotknięciu.

Web Audio API generuje osobne efekty kliknięcia, ulepszenia, odkrycia planety, budowy i ewolucji rdzenia. Oryginalna suita kosmiczna składa się z wolnych akordów minorowych/add9, basu i pojedynczych wysokich tonów. Nie używa nagrań, sampli, zewnętrznych plików ani zapożyczonych melodii. Muzyka domyślnie jest wyłączona; gracz włącza ją świadomie w **Menu → Dźwięk i muzyka**. Nawet zapamiętana zgoda nie rozpoczyna audio bez gestu gracza po uruchomieniu aplikacji. Muzyka i efekty mają osobne suwaki. Preferencje są przechowywane w `neonEmpireAudio`, niezależnie od zapisów gry. Audio zatrzymuje się w tle. Brak Web Audio nie blokuje gry.

## Kolonie: 10 poziomów każdej planety

Odblokowanie nadal wymaga łącznej energii 1 000 / 25 000 / 250 000 i nie pobiera opłaty. Daje pierwszy poziom kolonii. Stare odblokowane planety również otrzymują poziom 1; zamknięte pozostają na poziomie 0. Poziomy 2–10 kupuje się za bieżącą energię. Koszt kolejnego poziomu: `floor(prógPlanety × 0.75 × 1.85^(obecnyPoziom−1))`. Zakupy nie zmniejszają łącznej zdobytej energii.

| Planeta | Nowa korzyść kolonii | Zachowany bonus |
| --- | --- | --- |
| Luna-9 | Kopalnie: `20 × poziom²` energii/s przed mnożnikami | +10% |
| Mars Prime | Przemysł: mnożnik `1 + 0.08 × poziom` | +25% |
| Tytan | Rdzeń: +10% energii z dotknięcia na poziom; dostęp do technologii | +50% |

Widoki planet pokazują poziom, obecną korzyść, korzyść kolejnego poziomu, koszt rozbudowy i rosnącą liczbę budynków. Odblokowanie i budowa mają animację i własne dźwięki.

Technologie Tytana:

| Technologia | Wymagany poziom | Koszt energii | Efekt |
| --- | ---: | ---: | --- |
| Sieć nadprzewodząca | 1 | 300 000 | +10% produkcji |
| Rezonans rdzenia | 4 | 1 800 000 | +50% energii z dotknięcia |
| Energia próżni | 7 | 10 000 000 | +25% produkcji |
| Serce Tytana | 10 | 50 000 000 | +100% energii z dotknięcia |

Stałe bonusy planet są sumowane **raz**: `1 + 0.10 + 0.25 + 0.50 = 1.85` po odkryciu wszystkich planet. Pełny wzór produkcji:

```
(ulepszenia + kopalnie Luny)
× (1 + suma bonusów badań)
× (1 + suma stałych bonusów odblokowanych planet)
× (1 + 0.08 × poziom Marsa)
× (1 + suma zakupionych bonusów produkcyjnych Tytana)
```

Energia z dotknięcia: `ceil((1 + floor(produkcja × 0.05)) × (1 + 0.10 × poziom Tytana) × (1 + suma bonusów dotknięcia z technologii))`.

## Zgodność zapisów i offline

Zachowano klucz `neonEmpireSave` i format `version: 5`, energię, łączną energię, ulepszenia, badania, flagi planet, misje, osiągnięcia, nagrody i kliknięcia. Dodano opcjonalne pola `colonies` i `technologies`; ich brak jest bezpiecznie uzupełniany podczas ładowania/importu zapisów 0.6.1 i 0.7.0. Wszystkie korzyści nowych kolonii uwzględniane są także w produkcji offline, z zachowanym limitem ośmiu godzin. Główny timer nie nalicza jednocześnie produkcji w tle.

Import/eksport JSON i Android Storage Access Framework pozostają dostępne. Zasoby gry, efekty i muzyka są lokalne. Aktualizacja Androida zachowuje dane tylko przy tym samym identyfikatorze i podpisie aplikacji; przed reinstalacją eksportuj zapis. Nie umieszczaj kluczy podpisu w repozytorium.

## Testy i budowanie

```sh
for file in app/src/main/assets/*.js; do node --check "$file"; done
node tests/economy.test.cjs
node tests/audio.test.cjs
node tests/campaign.test.cjs
# Python Playwright i Chromium wymagane do testu UI:
python tests/browser_smoke.py
# JDK 17+, Gradle 8.9, Android SDK 35:
gradle --no-daemon assembleDebug bundleRelease
```

GitHub Actions uruchamia te kontrole, buduje APK/AAB, sprawdza podpis, wersję i integralność wszystkich zasobów w APK, a następnie instaluje i uruchamia aplikację w emulatorze Androida. Po powodzeniu artefakt `neon-empire-0.8.0-apk` zawiera `app-debug.apk` i `SHA256SUMS`. `neon-empire-0.8.0-aab` zawiera bundle. Bez sekretów podpisu AAB pozostaje niepodpisany.

Opcjonalne sekrety wydawnicze: `NEON_KEYSTORE_BASE64`, `NEON_KEYSTORE_PASSWORD`, `NEON_KEY_ALIAS`, `NEON_KEY_PASSWORD`. Ranking globalny nadal wymaga konfiguracji Google Play Games.

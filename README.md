# NEON EMPIRE 0.7.1 — Android

Polska gra idle offline. `versionName 0.7.1`, `versionCode 9`; identyfikatory Android i zasoby startowe z 0.7.0 pozostają zachowane.

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
# Python Playwright i Chromium wymagane do testu UI:
python tests/browser_smoke.py
# JDK 17+, Gradle 8.9, Android SDK 35:
gradle --no-daemon assembleDebug bundleRelease
```

GitHub Actions uruchamia te kontrole, buduje APK/AAB, sprawdza podpis, wersję i integralność wszystkich zasobów w APK, a następnie instaluje i uruchamia aplikację w emulatorze Androida. Po powodzeniu artefakt `neon-empire-0.7.1-apk` zawiera `app-debug.apk` i `SHA256SUMS`. `neon-empire-0.7.1-aab` zawiera bundle. Bez sekretów podpisu AAB pozostaje niepodpisany.

Opcjonalne sekrety wydawnicze: `NEON_KEYSTORE_BASE64`, `NEON_KEYSTORE_PASSWORD`, `NEON_KEY_ALIAS`, `NEON_KEY_PASSWORD`. Ranking globalny nadal wymaga konfiguracji Google Play Games.

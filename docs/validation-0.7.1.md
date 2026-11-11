# Walidacja NEON EMPIRE 0.7.1

Wersja przygotowana na bazie zdalnego `main` (`d371c40`), z zachowaniem dostarczonej grafiki i poprawki ekranu startowego Androida 12.

- Kontrola składni wszystkich czterech plików JavaScript: poprawna.
- 8 testów ekonomii: migracja starych odblokowań, stałe bonusy naliczane dokładnie raz, realne korzyści planet, wszystkie 30 poziomów i limity, rosnące koszty, brak zakupu bez energii, blokady technologii i brak powtórnego zakupu.
- 8 testów audio: brak automatycznego odtwarzania, jawna zgoda na muzykę, niezależne i trwałe głośności, wyciszenie, ograniczanie szybkich efektów, wstrzymanie w tle i bezpieczny fallback.
- Chromium/Playwright: dotyk i klawiatura, widoczny fokus, przezroczysty tap highlight, ograniczenie liczby i sprzątanie efektów, menu audio i zgoda, zachowanie danych zapisów 0.6.1/0.7.0, migracja kolonii, limit 8 godzin offline, rozbudowa wszystkich planet do poziomu 10, technologie Tytana, import/eksport, kliknięcie bez sieci, szerokości 320/390/800 px, ograniczenie animacji, animacja odblokowania. Brak błędów JavaScript.
- Gradle 8.9 / AGP 8.7.3 / SDK 35 / OpenJDK 21: `assembleDebug bundleRelease` — BUILD SUCCESSFUL, 44 s. CI używa JDK 17.
- `apksigner verify`: poprawne podpisy debug v1/v2.
- `aapt dump badging`: `pl.neonempire.game.debug`, versionCode 9, versionName 0.7.1, minSdk 23, targetSdk 35.
- Archiwum APK bez błędów; każdy plik `assets/` identyczny z aktualnymi źródłami.
- SHA-256 lokalnego APK: `80ba6916b8ee7bfd1db2608a23c0a195bc240e031997ee35b3de45d37480e333`.

Testy lokalne nie zastępują pomiaru płynności na fizycznym telefonie ani instalacji w emulatorze Androida. Workflow zawiera test instalacji, uruchomienia i kontroli awarii. W momencie przygotowania raportu zapis do GitHuba jest blokowany HTTP 403; nie ma jeszcze przebiegu Actions dla tej wersji. Lokalny AAB nie jest podpisany kluczem wydawniczym.

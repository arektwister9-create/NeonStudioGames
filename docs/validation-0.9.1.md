# NEON EMPIRE 0.9.1 — kandydat do pierwszego testu w Google Play

- `pl.neonempire.game`, versionName 0.9.1, versionCode 12; minSdk 23, targetSdk/compileSdk 36.
- AGP 8.10.1, Gradle 8.11.1, pełny Temurin JDK 17. Podpisane `assembleRelease`, `bundleRelease`, `assembleDebug` i `lintRelease` zakończone powodzeniem.
- Lint: 0 błędów, 11 ostrzeżeń (głównie starsze ikony, opcjonalna ikona monochromatyczna, atrybut zgodności i włączony JavaScript wymagany przez grę). Zewnętrzne strony nie są ładowane do WebView z mostem gry.
- 37 testów logiki oraz testy Chromium przeszły. Sprawdzono politykę prywatności, powrót do gry bez utraty stanu i układ poziomy 1280×720, oprócz wcześniejszych kontroli mobilnych, audio, kolonii, kampanii i 30 ekspedycji.
- `bundletool validate`, weryfikacja podpisu JAR i kontrola manifestu AAB zakończone powodzeniem. Sprawdzono produkcyjny identyfikator, numer wersji, brak debugowania, target API oraz zgodność wszystkich zasobów z aktualnym źródłem. Brak natywnych bibliotek `.so` w AAB.
- Z podpisanego AAB wygenerowano uniwersalny APK za pomocą bundletool. Podpis APK również przeszedł kontrolę.
- Nowy prywatny upload key RSA 4096 bitów utworzono po potwierdzeniu pierwszej publikacji. Publiczny SHA-256 certyfikatu: `56aa95b460e4f1229a3fd8a7ac42cf11a98ef7088f5211b4d1d8b7e3e0d70eb7`. Prywatny klucz i hasła są poza repozytorium.
- Metadane spełniają limity 30/80/4000 znaków. Ikona 512×512, grafika 1024×500, cztery rzeczywiste zrzuty 1080×1920.

Nie wykonano jeszcze przesłania do Play Console, instalacji z Google Play ani oceny pre-launch Google. Publiczna polityka wymaga włączenia GitHub Pages przez właściciela; dostęp aplikacji GitHub nie obejmuje administracji Pages ani sekretów Actions. Workflow wydawniczy ma obowiązkowe sekrety upload key, walidację podpisu i test produkcyjnego APK na Androidzie 16 — nie został uruchomiony bez tych sekretów. Nie należy mylić go z lokalnymi wynikami powyżej.

Przed pierwszą publiczną publikacją należy przejść test wewnętrzny, uzupełnić prawdziwe deklaracje konsoli, sprawdzić urządzenia w raporcie pre-launch i spełnić warunki konta. Wersja debug ma inny identyfikator; postęp przenosi się przez eksport/import JSON.

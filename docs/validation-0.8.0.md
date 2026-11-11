# Walidacja NEON EMPIRE 0.8.0 — Przebudzenie rdzenia

- 24 testy Node: 8 ekonomii, 8 audio, 8 kampanii. Wszystkie przeszły.
- Nowe testy kampanii obejmują start starych zapisów bez utraty postępu, limit i trwałość ładunku, jednorazowe wyzwolenie pulsu, rzeczywiste wymagania konstrukcyjne, sekwencje synchronizacji, brak kary za błąd, zapis kroku próby, jednorazowe nagrody i otwarcie bramy po sześciu rozdziałach.
- Chromium/Playwright: utrzymane testy 0.7.1 (dotyk, klawiatura, fokus, audio, stare zapisy, offline, kolonie, technologie, import/eksport i responsywność). Dodatkowo przejście pierwszej misji od ładowania przez puls i próbę do fragmentu; błędny węzeł; skrót do celu bez usuwania rdzenia z kolejności Tab; końcowa sekwencja i widoczne otwarcie bramy. Brak błędów JavaScript.
- Gradle 8.9 / Android SDK 35 / OpenJDK 21: końcowe `assembleDebug bundleRelease` — BUILD SUCCESSFUL, 15 s. Workflow korzysta z JDK 17.
- APK: poprawne podpisy v1/v2, integralne archiwum, wszystkie pliki assets identyczne ze źródłem.
- Pakiet: `pl.neonempire.game.debug`, versionName `0.8.0`, versionCode `10`, minSdk `23`, targetSdk `35`.
- SHA-256 lokalnego debug APK: `56e73328563f86612972d9a1583319c830b2567294d63f100a910c986a9e5e90`.

Kampania jest opcjonalnym rozszerzeniem `coreCampaign` w formacie zapisu `version: 5`. Nie zmienia stałych bonusów planet, dotychczasowych zasobów, technologii ani naliczania offline. Nie wymaga połączenia z siecią, nie ma limitów czasu ani płatności.

Nie wykonano testu na fizycznym telefonie. Workflow zawiera test instalacji i uruchomienia w emulatorze, lecz zapis do repozytorium był blokowany przez GitHub HTTP 403; raport opisuje lokalne testy i lokalny APK, nie przebieg GitHub Actions. Release AAB bez klucza wydawniczego pozostaje niepodpisany.

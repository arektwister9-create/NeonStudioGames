# NEON EMPIRE 0.9.2 — automatyczna ochrona Google Play

- `minSdk 24` (Android 7.0+), `targetSdk 36`, versionCode 13.
- Produkcyjny identyfikator `pl.neonempire.game` i dotychczasowy upload key są zachowane.
- Walidator AAB sprawdza minSdk zgodny z konfiguracją i minimum 24, aby błąd ochrony Play nie wrócił.
- Brak zmian w ekonomii, poziomach, mechanizmie zapisów i kodzie rozgrywki.
- Podpisany pakiet trzeba wgrać jako nowy AAB w edytowanym wydaniu Play Console; nie używać poprzedniego pliku 0.9.1.

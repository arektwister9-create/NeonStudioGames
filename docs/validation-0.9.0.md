# NEON EMPIRE 0.9.0 — aktywne poziomy i rozbudowa stacji

- 37 testów Node: ekonomia 8, audio 8, kampania 8, ekspedycje 13. Wszystkie przeszły.
- Test ekspedycji przechodzi wszystkie 30 poziomów i rozbudowuje wszystkie trzy moduły do poziomu 6 za materiały z pierwszych zwycięstw, bez powtórek.
- Sprawdzono dwie fale, trzy fazy strażników, zmianę słabości, blokady sektorów, odblokowania narzędzi, atak dronów, rosnące koszty budowy, brak utraty materiałów po porażce, zapis fazy/HP/narzędzia oraz jednokrotną naprawę za energię.
- Chromium/Playwright: zachowane kontrole starej ekonomii, audio, importu/eksportu, zapisów 0.6.1/0.7.0, offline, kolonii i kampanii. Dodatkowo rzeczywiste sterowanie pierwszymi pięcioma poziomami, błędne narzędzie, budowa widocznego doku, import aktywnej walki, naprawa osłony, przejście do sektora 2, finał poziomu 30 i pełna stacja przy szerokości 320 px. Brak błędów JavaScript i poziomego przewijania.
- Obejrzano zrzuty aktywnego strażnika i ukończonego rdzenia/stacji: widoczne cele, HP, moduły orbitalne i różne sektory. Starsza kampania/pulsy są dostępne w rozwijanym panelu pod mapą.
- Gradle 8.9 / SDK 35 / JDK 21: `assembleDebug bundleRelease` — BUILD SUCCESSFUL, 33 s. CI używa JDK 17.
- `apksigner`: podpisy v1/v2 poprawne; certyfikat debug ten sam co lokalne APK 0.7.1 i 0.8.0.
- `aapt`: `pl.neonempire.game.debug`, versionCode 11, versionName 0.9.0, minSdk 23, targetSdk 35.
- Archiwum APK poprawne, każdy plik assets identyczny z bieżącymi źródłami.
- SHA-256 APK: `8b6202637e411d2a0f08294fbab920d0ef7cd0a350336fc17cf61b6ad61a8179`.

Ekspedycje są zapisane w opcjonalnym `expedition`, w tym samym kluczu `neonEmpireSave` i formacie `version: 5`. Stare postępy nie są resetowane. Nowa nagroda energii dotyczy wyłącznie pierwszego ukończenia poziomu; naprawa wydaje bieżącą energię, nie zmniejsza lifetime total. Stałe bonusy planet i produkcja offline nie zmieniły wzorów. Walki są turowe i nie postępują w tle.

Nie wykonano pomiarów na fizycznym Androidzie. Lokalna kompilacja i testy nie są przebiegiem GitHub Actions. Workflow zawiera budowanie i test instalacji w emulatorze; wcześniejsze wysyłanie zmian było odrzucane przez GitHub HTTP 403. AAB bez klucza wydawniczego pozostaje niepodpisany.

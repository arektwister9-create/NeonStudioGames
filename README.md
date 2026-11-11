# NEON EMPIRE 0.6.1 — Android

Wersja 0.6.1 bazuje na oryginalnym HTML 0.6.0, zachowując format zapisu `version: 5` i klucz `neonEmpireSave`.

## Zmiany
- Naliczanie produkcji offline po powrocie aplikacji z tła (limit 8 godzin).
- Opcjonalne podpisywanie AAB w GitHub Actions z wykorzystaniem GitHub Secrets.
- Kontrola składni JavaScript w workflow.
- `versionCode 7`, `versionName 0.6.1`.

## Kompilacja

GitHub Actions uruchamia kompilację automatycznie po zmianach na gałęzi `main` oraz ręcznie przez **Actions → Build NEON EMPIRE Android → Run workflow**. Po udanym przebiegu pobierz artefakt `neon-empire-0.6.1-apk`; zawiera instalacyjny `app-debug.apk`.

Lokalnie projekt wymaga JDK 17, Android SDK 35 i Gradle 8.9. Polecenie kompilacji:

```shell
gradle --no-daemon assembleDebug bundleRelease
```

Do podpisania wydania ustaw sekrety repozytorium:
- `NEON_KEYSTORE_BASE64`: plik JKS zakodowany Base64
- `NEON_KEYSTORE_PASSWORD`
- `NEON_KEY_ALIAS`
- `NEON_KEY_PASSWORD`

Bez tych sekretów debug APK będzie działać, ale release AAB pozostanie niepodpisany i nie nadaje się do przesłania do Google Play. **Nigdy nie umieszczaj pliku JKS ani haseł w repozytorium.**

Ranking Google Play Games nadal wymaga konfiguracji w Play Console. Nie przetestowano jeszcze aplikacji na fizycznym telefonie ani nie uruchomiono kompilacji Android w tym środowisku.

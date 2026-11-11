# NEON EMPIRE 0.7.0 — Android

Wersja 0.7.0 rozwija klikalny rdzeń i ekspansję planetarną. Zachowuje klucz `neonEmpireSave`, format zapisu `version: 5`, dotychczasowe bonusy planet oraz produkcję offline z limitem 8 godzin.

## Nowości

- Sześć form rdzenia: Iskra, Pulsator, Reaktor, Nexus, Osobliwość i Serce Imperium.
- Animowane pierścienie i efekty ewolucji z obsługą `prefers-reduced-motion`.
- Wizualne kolonie Luna-9, Mars Prime i Tytan, rozwijające się wraz z postępem.
- Oryginalna neonowa ikona Android w pięciu gęstościach oraz ekran startowy.
- `versionCode 8`, `versionName 0.7.0`.

## Kompilacja

GitHub Actions waliduje JavaScript i buduje instalacyjny APK oraz AAB. Artefakty nazywają się `neon-empire-0.7.0-apk` i `neon-empire-0.7.0-aab`.

Lokalnie wymagane są JDK 17, Android SDK 35 i Gradle 8.9:

```shell
gradle --no-daemon assembleDebug bundleRelease
```

Opcjonalne podpisanie AAB korzysta z sekretów `NEON_KEYSTORE_BASE64`, `NEON_KEYSTORE_PASSWORD`, `NEON_KEY_ALIAS` i `NEON_KEY_PASSWORD`. Kluczy i haseł nie należy umieszczać w repozytorium.

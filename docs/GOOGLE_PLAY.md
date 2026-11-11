# Pierwsza publikacja NEON EMPIRE w Google Play

Wydawca: NEON GAMES STUDIO. Kontakt publiczny: arektwister9@gmail.com.

## Przygotowany pakiet

- Produkcyjny identyfikator: `pl.neonempire.game` (bez `.debug`). Dostępność identyfikatora ostatecznie sprawdzi Play Console.
- Wersja: 0.9.1, versionCode 12; minSdk 23, targetSdk 36 (Android 16).
- Plik do wgrania: podpisany **Android App Bundle `.aab`**, nie debug APK, nie ZIP źródeł i nie kopia klucza.
- Wybrany model: Play App Signing z kluczem podpisu aplikacji generowanym przez Google. Lokalny prywatny klucz służy tylko do podpisywania przesyłanych AAB (upload key).
- Polskie metadane w `fastlane/metadata/android/pl-PL/`; grafiki w `store-assets/`.
- Publiczna polityka po włączeniu Pages: https://arektwister9-create.github.io/NeonStudioGames/privacy/

## Najpierw test wewnętrzny

1. Otwórz https://play.google.com/console i wybierz **Utwórz aplikację**.
2. Nazwa **NEON EMPIRE**, język polski, typ **Gra**. Przy pierwszej publikacji można wybrać **Bezpłatna**; wybierz ją tylko jeśli chcesz bezpłatnej dystrybucji — bezpłatnej aplikacji nie można później przełączyć na płatną w tej samej karcie. Gra obecnie nie zawiera reklam ani zakupów. Na urządzeniu powinien być aktualny, zgodny z jego systemem Android System WebView.
3. Zaakceptuj właściwe oświadczenia konsoli po ich przeczytaniu.
4. Wejdź w **Testowanie i publikowanie → Testowanie → Testy wewnętrzne** (nazwy mogą różnić się zależnie od widoku), utwórz wersję i wybierz Play App Signing z kluczem Google.
5. Wgraj podpisany AAB 0.9.1, nadaj nazwę wersji i użyj opisu zmian z `changelogs/12.txt`.
6. Dodaj adresy testerów, zapisz wydanie testowe, sprawdź ostrzeżenia konsoli i uruchom test. Otwórz link do dołączenia na telefonie zalogowanym na konto testera.
7. Sprawdź rzeczywistą instalację z Google Play, dźwięk, menu, import/eksport, obrót/duży ekran, powrót z tła i politykę prywatności. Obejrzyj raport przed publikacją (pre-launch report), jeśli konsola go wygeneruje.

Wydanie testowe nie oznacza publicznej publikacji w sklepie. Nie wysłano aplikacji do Play Console automatycznie — to środowisko nie ma połączenia z tym kontem.

## Karta i deklaracje przed testami zamkniętymi/produkcją

- Wklej tytuł, krótki i pełny opis z metadanych.
- Dodaj ikonę 512×512, grafikę funkcji 1024×500 i cztery zrzuty telefonu 1080×1920. Są to rzeczywiste widoki gry z przykładowymi stanami rozwoju.
- Kategoria: Gra; wybierz najlepiej odpowiadającą rozgrywce kategorię, np. strategiczna/symulacyjna. Nie wybieraj kategorii wyłącznie dla popularności.
- Wpisz kontakt i działający publiczny URL polityki. Włącz Pages: repozytorium → Settings → Pages → Deploy from a branch → main → /docs → Save. Sprawdź publiczny URL przed podaniem Google.
- Dostęp do aplikacji: wszystkie funkcje dostępne bez konta/logowania.
- Reklamy: nie. Zakupy w aplikacji: nie. Bieżąca wersja nie zawiera reklamowych/analitycznych SDK ani kont gracza.
- Bezpieczeństwo danych: na podstawie obecnego kodu gra nie zbiera ani nie udostępnia danych przez serwery wydawcy. Postęp, stan walki i ustawienia pozostają lokalne. Wyjątki wymagające rozważenia w formularzu: dobrowolny eksport do wybranego dostawcy plików, kopia systemowa Androida i e-mail wysyłany poza aplikacją — opisane w polityce. Odpowiedzi formularza potwierdza właściciel konta zgodnie z definicjami Google.
- Wypełnij ankietę klasyfikacji treści: gra zawiera abstrakcyjne kosmiczne starcia, bez krwi, czatu i hazardu. Nie wpisuj samodzielnie „PEGI 3” jako przyznanej oceny; ocenę nada ankieta.
- Określ rzeczywistą grupę wiekową, kraje, cenę i pozostałe deklaracje wymagane przez Twoją konsolę. Nie zadeklarowano aplikacji jako kierowanej do dzieci bez decyzji wydawcy.

Dla osobistych kont utworzonych po 13 listopada 2023 r. Google wymaga przed dostępem do produkcji testu zamkniętego z co najmniej 12 testerami zapisanymi nieprzerwanie przez 14 dni i wniosku o dostęp do produkcji. Test wewnętrzny tego wymogu nie zastępuje. Stosuj wymagania widoczne dla Twojego konta.

## Klucz i kolejne wydania

Prywatna kopia klucza została przygotowana **poza repozytorium**. Zawiera PKCS12, hasła, alias, publiczny certyfikat i pliki tekstowe do ustawienia sekretów. Pobierz ją i przechowuj prywatnie, najlepiej w szyfrowanej kopii. Nie wgrywaj tej kopii do repozytorium ani do karty aplikacji.

Do powtarzalnego podpisywania w GitHub Actions dodaj w Settings → Secrets and variables → Actions:

- `NEON_KEYSTORE_BASE64`
- `NEON_KEYSTORE_PASSWORD`
- `NEON_KEY_ALIAS`
- `NEON_KEY_PASSWORD`

Wartości znajdują się w plikach o tych nazwach w prywatnej kopii. To środowisko nie ma uprawnienia do zarządzania sekretami repozytorium; nie wpisuj haseł w czacie. Workflow **Build signed Google Play bundle** uruchamia się ręcznie i celowo kończy się błędem, jeśli brakuje któregokolwiek sekretu. Weryfikuje podpis, produkcyjny identyfikator, wersję, target API, prywatność i wszystkie lokalne zasoby oraz instaluje produkcyjny APK w emulatorze Androida 16. Zwykła kompilacja deweloperska nie zastępuje tego workflow.

Zwiększaj versionCode przy każdym kolejnym AAB wysyłanym do Play. Zachowaj identyfikator i upload key. Debug APK używa `pl.neonempire.game.debug`, więc nie aktualizuje bezpośrednio aplikacji produkcyjnej. **Przed przejściem z debug do Google Play wyeksportuj zapis JSON i zaimportuj go w wersji sklepowej.** Format zapisów pozostaje zgodny; debug i release mają osobne pamięci aplikacji. Gdy podpisem APK zarządza Play App Signing, lokalny APK podpisany upload key nie zastąpi automatycznie APK podpisanego przez Google.

## Źródła wymagań sprawdzone 11 listopada 2026 r.

- API 36: https://support.google.com/googleplay/android-developer/answer/11926878
- Testy nowych kont: https://support.google.com/googleplay/android-developer/answer/14151465
- Tworzenie aplikacji: https://support.google.com/googleplay/android-developer/answer/9859152
- Play App Signing: https://support.google.com/googleplay/android-developer/answer/9842756
- Grafiki i zrzuty: https://support.google.com/googleplay/android-developer/answer/9866151
- Bezpieczeństwo danych: https://support.google.com/googleplay/android-developer/answer/10787469

Spełnienie kontroli technicznych nie jest gwarancją akceptacji przez Google; końcowe formularze i ocenę wydania weryfikuje Play Console.

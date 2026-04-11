#!/usr/bin/env python3
"""Met à jour extDescription dans les 26 messages.json + réécrit store-descriptions.md."""

import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "mysnips/_locales"

# ── Résumés courts (≤132 chars, champ extDescription dans messages.json) ──────
# Objectif : inclure "text expander", "snippet", "templates" ou équivalents locaux

SUMMARIES = {
"en": "Text expander & snippet manager — instantly insert templates, canned responses and shortcuts into any field. Press Alt+S.",
"fr": "Extension de texte & gestionnaire de snippets — insérez vos modèles et réponses types instantanément. Touche Alt+S.",
"de": "Textexpander & Snippet-Manager — Vorlagen, Standardantworten, Kürzel sofort einfügen. Alt+S drücken.",
"es": "Expansor de texto & gestor de snippets — inserta plantillas y respuestas rápidas al instante. Pulsa Alt+S.",
"it": "Text expander & gestore snippet — inserisci modelli e risposte predefinite all'istante. Premi Alt+S.",
"pt": "Expansor de texto & gestor de snippets — insira modelos e respostas rápidas instantaneamente. Prima Alt+S.",
"nl": "Tekst-expander & snippetbeheer — voeg sjablonen en standaardantwoorden direct in elk veld in. Alt+S.",
"pl": "Ekspander tekstu & menedżer snippetów — wstawiaj szablony i gotowe odpowiedzi błyskawicznie. Alt+S.",
"sv": "Textexpander & snippethanterare — infoga mallar och snabbsvar direkt i vilket fält som helst. Alt+S.",
"da": "Tekstekspander & snippet-manager — indsæt skabeloner og standardsvar øjeblikkeligt. Tryk Alt+S.",
"nb": "Tekst-ekspander & snippet-manager — lim inn maler og standardsvar øyeblikkelig. Trykk Alt+S.",
"fi": "Tekstilaajennus & snippet-hallinta — lisää mallit ja vakiovastaukset välittömästi. Paina Alt+S.",
"cs": "Textový expander & správce snippetů — vkládejte šablony a připravené odpovědi okamžitě. Alt+S.",
"sk": "Textový expander & správca snippetov — vkladajte šablóny a pripravené odpovede okamžite. Alt+S.",
"hu": "Szövegbővítő & snippet-kezelő — illesszen be sablonokat és előre írt válaszokat azonnal. Alt+S.",
"ro": "Expander de text & manager de snippets — inserați șabloane și răspunsuri rapide instant. Alt+S.",
"hr": "Proširivač teksta & upravljač isječcima — umetnite predloške i gotove odgovore trenutno. Alt+S.",
"bg": "Разширител на текст & мениджър на фрагменти — вмъквайте шаблони и готови отговори мигновено. Alt+S.",
"el": "Επεκτάτης κειμένου & διαχειριστής snippets — εισαγάγετε πρότυπα και έτοιμες απαντήσεις άμεσα. Alt+S.",
"tr": "Metin genişletici & snippet yöneticisi — şablonları ve hazır yanıtları anında yapıştırın. Alt+S.",
"et": "Teksti laiendaja & katkendite haldur — lisage mallid ja valmisvastused koheselt. Alt+S.",
"lt": "Teksto plėstuvas & fragmentų tvarkyklė — įterpkite šablonus ir paruoštus atsakymus akimirksniu. Alt+S.",
"lv": "Teksta paplašinātājs & fragmentu pārvaldnieks — ievietojiet veidnes un gatavas atbildes uzreiz. Alt+S.",
"sl": "Razširjevalnik besedila & upravljalnik odlomkov — vstavite predloge in pripravljene odgovore takoj. Alt+S.",
"mt": "Espansur tat-test & manager ta' snippets — daħħal mudelli u tweġibiet lesti minnufih. Alt+S.",
"ga": "Leathnaitheoirí téacs & bainisteoir snippets — cuir isteach teimpléid agus freagraí réidhe láithreach. Alt+S.",
}

# Vérification longueur
print("=== Vérification longueurs extDescription ===")
for lang, s in SUMMARIES.items():
    n = len(s)
    flag = "⚠ TOO LONG" if n > 132 else "✓"
    print(f"  {lang}: {n} chars {flag}")

# ── Mise à jour messages.json ─────────────────────────────────────────────────
print("\n=== Mise à jour messages.json ===")
for lang, summary in SUMMARIES.items():
    path = LOCALES_DIR / lang / "messages.json"
    if not path.exists():
        print(f"  {lang}: ⚠ fichier manquant, skip")
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    data["extDescription"]["message"] = summary
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {lang}: ✓")

# ── Réécriture store-descriptions.md ─────────────────────────────────────────
print("\n=== Génération store-descriptions.md ===")

DESCRIPTIONS = {
"en": {
    "name": "English",
    "summary": SUMMARIES["en"],
    "desc": """MySnips is a free text expander and snippet manager for Chrome. Store your most-used text templates, canned responses, email snippets, keyboard shortcuts, URLs, addresses, codes and signatures — then insert them instantly into any text field on any website with a single keystroke.

🔑 Press Alt+S (fully customizable shortcut) or right-click any text field
🗂 Organize snippets and templates in folders
🔍 Search as you type — instant results
✏️ Edit inline — no popups, no dialogs, no lag
📁 Import / Export your snippet library as JSON
🌍 Available in 26 languages

Works everywhere: Gmail, Outlook, LinkedIn, Salesforce, Jotform, support tools, CRMs, web forms…

100% private — your data never leaves your browser. No account, no sync, no tracking.

Perfect for:
• Customer support agents (canned responses, quick replies)
• Sales teams (email templates, follow-up scripts)
• Developers (code snippets, boilerplate)
• Anyone who types the same things over and over""",
},
"fr": {
    "name": "French (fr)",
    "summary": SUMMARIES["fr"],
    "desc": """MySnips est une extension de texte et un gestionnaire de snippets gratuit pour Chrome. Stockez vos modèles de texte, réponses types, raccourcis clavier, URLs, adresses, codes et signatures — puis insérez-les instantanément dans n'importe quel champ sur n'importe quel site.

🔑 Touche Alt+S (personnalisable) ou clic droit sur n'importe quel champ
🗂 Organisez vos snippets et modèles en dossiers
🔍 Recherche en temps réel
✏️ Édition en ligne — sans popups ni fenêtres
📁 Importez / Exportez votre bibliothèque en JSON
🌍 Disponible en 26 langues

Fonctionne partout : Gmail, Outlook, LinkedIn, Salesforce, formulaires web…

100% privé — vos données ne quittent jamais votre navigateur. Pas de compte, pas de synchronisation.

Idéal pour :
• Support client (réponses types, réponses rapides)
• Équipes commerciales (modèles d'e-mails, scripts)
• Développeurs (fragments de code, boilerplate)
• Toute personne qui tape les mêmes choses en boucle""",
},
"de": {
    "name": "German (de)",
    "summary": SUMMARIES["de"],
    "desc": """MySnips ist ein kostenloser Textexpander und Snippet-Manager für Chrome. Speichere deine häufigsten Textbausteine, Standardantworten, E-Mail-Vorlagen, Tastaturkürzel, URLs, Adressen, Codes und Signaturen — und füge sie per Tastendruck in jedes Textfeld ein.

🔑 Alt+S drücken (anpassbar) oder Rechtsklick auf ein Textfeld
🗂 Snippets und Vorlagen in Ordnern organisieren
🔍 Suche während der Eingabe
✏️ Inline bearbeiten — keine Popups, keine Dialoge
📁 Snippet-Bibliothek als JSON importieren / exportieren
🌍 In 26 Sprachen verfügbar

Funktioniert überall: Gmail, Outlook, LinkedIn, Salesforce, Webformulare…

100% lokal — deine Daten verlassen nie deinen Browser. Kein Konto, keine Synchronisierung.

Ideal für:
• Kundensupport (Standardantworten, Schnellantworten)
• Vertriebsteams (E-Mail-Vorlagen, Skripte)
• Entwickler (Code-Snippets, Boilerplate)
• Alle, die ständig dasselbe tippen""",
},
"es": {
    "name": "Spanish (es)",
    "summary": SUMMARIES["es"],
    "desc": """MySnips es un expansor de texto y gestor de snippets gratuito para Chrome. Guarda tus plantillas de texto, respuestas predefinidas, atajos de teclado, URLs, direcciones, códigos y firmas — e insértalos al instante en cualquier campo de texto con una sola tecla.

🔑 Pulsa Alt+S (personalizable) o clic derecho en cualquier campo
🗂 Organiza snippets y plantillas en carpetas
🔍 Búsqueda en tiempo real
✏️ Edición inline — sin ventanas emergentes ni diálogos
📁 Importa / Exporta tu biblioteca como JSON
🌍 Disponible en 26 idiomas

Funciona en todas partes: Gmail, Outlook, LinkedIn, Salesforce, formularios web…

100% privado — tus datos nunca salen de tu navegador. Sin cuenta, sin sincronización.

Perfecto para:
• Atención al cliente (respuestas predefinidas, respuestas rápidas)
• Equipos de ventas (plantillas de correo, guiones)
• Desarrolladores (fragmentos de código, boilerplate)
• Cualquiera que escriba las mismas cosas una y otra vez""",
},
"it": {
    "name": "Italian (it)",
    "summary": SUMMARIES["it"],
    "desc": """MySnips è un text expander e gestore di snippet gratuito per Chrome. Salva i tuoi modelli di testo, risposte predefinite, scorciatoie da tastiera, URL, indirizzi, codici e firme — e inseriscili istantaneamente in qualsiasi campo di testo con un solo tasto.

🔑 Premi Alt+S (personalizzabile) o clic destro su qualsiasi campo
🗂 Organizza snippet e modelli in cartelle
🔍 Ricerca in tempo reale
✏️ Modifica inline — nessun popup, nessuna finestra
📁 Importa / Esporta la libreria come JSON
🌍 Disponibile in 26 lingue

Funziona ovunque: Gmail, Outlook, LinkedIn, Salesforce, moduli web…

100% privato — i tuoi dati non lasciano mai il browser. Nessun account, nessuna sincronizzazione.

Perfetto per:
• Supporto clienti (risposte predefinite, risposte rapide)
• Team vendite (modelli email, script)
• Sviluppatori (frammenti di codice, boilerplate)
• Chiunque digiti sempre le stesse cose""",
},
"pt": {
    "name": "Portuguese (pt)",
    "summary": SUMMARIES["pt"],
    "desc": """MySnips é um expansor de texto e gestor de snippets gratuito para Chrome. Guarde os seus modelos de texto, respostas predefinidas, atalhos de teclado, URLs, endereços, códigos e assinaturas — e insira-os instantaneamente em qualquer campo de texto com uma tecla.

🔑 Prima Alt+S (personalizável) ou clique direito em qualquer campo
🗂 Organize snippets e modelos em pastas
🔍 Pesquisa em tempo real
✏️ Edição inline — sem popups nem janelas
📁 Importe / Exporte a biblioteca como JSON
🌍 Disponível em 26 idiomas

Funciona em todo o lado: Gmail, Outlook, LinkedIn, Salesforce, formulários web…

100% privado — os seus dados nunca saem do navegador. Sem conta, sem sincronização.

Perfeito para:
• Suporte ao cliente (respostas predefinidas, respostas rápidas)
• Equipas de vendas (modelos de e-mail, scripts)
• Programadores (fragmentos de código, boilerplate)
• Qualquer pessoa que escreva as mesmas coisas repetidamente""",
},
"nl": {
    "name": "Dutch (nl)",
    "summary": SUMMARIES["nl"],
    "desc": """MySnips is een gratis tekst-expander en snippetbeheer voor Chrome. Sla je meestgebruikte tekstsjablonen, standaardantwoorden, toetsenbordsnelkoppelingen, URL's, adressen, codes en handtekeningen op — en plak ze met één toets in elk tekstveld.

🔑 Druk op Alt+S (aanpasbaar) of rechtsklik op een tekstveld
🗂 Organiseer snippets en sjablonen in mappen
🔍 Zoeken terwijl je typt
✏️ Inline bewerken — geen popups, geen dialogen
📁 Bibliotheek importeren / exporteren als JSON
🌍 Beschikbaar in 26 talen

Werkt overal: Gmail, Outlook, LinkedIn, Salesforce, webformulieren…

100% privé — je gegevens verlaten nooit je browser. Geen account, geen synchronisatie.

Perfect voor:
• Klantenservice (standaardantwoorden, snelle antwoorden)
• Verkoopteams (e-mailsjablonen, scripts)
• Ontwikkelaars (codeSnippets, boilerplate)
• Iedereen die steeds dezelfde dingen typt""",
},
"pl": {
    "name": "Polish (pl)",
    "summary": SUMMARIES["pl"],
    "desc": """MySnips to darmowy ekspander tekstu i menedżer snippetów dla Chrome. Przechowuj najczęściej używane szablony tekstu, gotowe odpowiedzi, skróty klawiaturowe, URL-e, adresy, kody i podpisy — i wklejaj je błyskawicznie w dowolne pole tekstowe jednym klawiszem.

🔑 Naciśnij Alt+S (konfigurowalny) lub kliknij prawym przyciskiem pole tekstowe
🗂 Organizuj snippety i szablony w folderach
🔍 Wyszukiwanie w czasie rzeczywistym
✏️ Edycja w miejscu — bez okienek i okien dialogowych
📁 Importuj / Eksportuj bibliotekę jako JSON
🌍 Dostępny w 26 językach

Działa wszędzie: Gmail, Outlook, LinkedIn, Salesforce, formularze internetowe…

100% prywatny — dane nigdy nie opuszczają przeglądarki. Brak konta, brak synchronizacji.

Idealny dla:
• Obsługi klienta (gotowe odpowiedzi, szybkie odpowiedzi)
• Zespołów sprzedaży (szablony e-maili, skrypty)
• Programistów (fragmenty kodu, boilerplate)
• Każdego, kto wciąż wpisuje te same rzeczy""",
},
"sv": {
    "name": "Swedish (sv)",
    "summary": SUMMARIES["sv"],
    "desc": """MySnips är en gratis textexpander och snippethanterare för Chrome. Spara dina vanligaste textmallar, standardsvar, tangentbordsgenvägar, URL:er, adresser, koder och signaturer — och klistra in dem i vilket textfält som helst med ett enda knapptryck.

🔑 Tryck Alt+S (anpassningsbar) eller högerklicka på ett textfält
🗂 Organisera snippets och mallar i mappar
🔍 Sök medan du skriver
✏️ Redigera direkt inline — inga popups, inga dialogrutor
📁 Importera / Exportera biblioteket som JSON
🌍 Tillgänglig på 26 språk

Fungerar överallt: Gmail, Outlook, LinkedIn, Salesforce, webbformulär…

100% privat — din data lämnar aldrig webbläsaren. Inget konto, ingen synkronisering.

Perfekt för:
• Kundtjänst (standardsvar, snabbsvar)
• Säljteam (e-postmallar, manus)
• Utvecklare (kodsnippets, boilerplate)
• Alla som skriver samma saker om och om igen""",
},
"da": {
    "name": "Danish (da)",
    "summary": SUMMARIES["da"],
    "desc": """MySnips er en gratis tekstekspander og snippet-manager til Chrome. Gem dine hyppigste tekstskabeloner, standardsvar, tastaturgenveje, URL'er, adresser, koder og signaturer — og indsæt dem i ethvert tekstfelt med et enkelt tastetryk.

🔑 Tryk Alt+S (tilpasbar) eller højreklik på et tekstfelt
🗂 Organiser snippets og skabeloner i mapper
🔍 Søg mens du skriver
✏️ Rediger direkte inline — ingen popups, ingen dialogbokse
📁 Importér / Exportér biblioteket som JSON
🌍 Tilgængelig på 26 sprog

Fungerer overalt: Gmail, Outlook, LinkedIn, Salesforce, webformularer…

100% privat — dine data forlader aldrig browseren. Ingen konto, ingen synkronisering.

Perfekt til:
• Kundesupport (standardsvar, hurtige svar)
• Salgsteams (e-mailskabeloner, scripts)
• Udviklere (kodesnippets, boilerplate)
• Alle der skriver det samme igen og igen""",
},
"nb": {
    "name": "Norwegian (nb)",
    "summary": SUMMARIES["nb"],
    "desc": """MySnips er en gratis tekst-ekspander og snippet-manager for Chrome. Lagre dine hyppigste tekstmaler, standardsvar, tastatursnarveier, URL-er, adresser, koder og signaturer — og lim dem inn i ethvert tekstfelt med ett tastetrykk.

🔑 Trykk Alt+S (tilpassbar) eller høyreklikk på et tekstfelt
🗂 Organiser snippets og maler i mapper
🔍 Søk mens du skriver
✏️ Rediger direkte inline — ingen popups, ingen dialogbokser
📁 Importer / Eksporter biblioteket som JSON
🌍 Tilgjengelig på 26 språk

Fungerer overalt: Gmail, Outlook, LinkedIn, Salesforce, webskjemaer…

100% privat — dataene dine forlater aldri nettleseren. Ingen konto, ingen synkronisering.

Perfekt for:
• Kundestøtte (standardsvar, hurtigsvar)
• Salgsteam (e-postmaler, skript)
• Utviklere (kodesnippets, boilerplate)
• Alle som skriver de samme tingene om og om igjen""",
},
"fi": {
    "name": "Finnish (fi)",
    "summary": SUMMARIES["fi"],
    "desc": """MySnips on ilmainen tekstilaajennus ja snippet-hallinta Chromelle. Tallenna käytetyimmät tekstipohjat, vakiovastaukset, pikanäppäimet, URL-osoitteet, osoitteet, koodit ja allekirjoitukset — ja liitä ne välittömästi mihin tahansa tekstikenttään yhdellä näppäinpainalluksella.

🔑 Paina Alt+S (muokattavissa) tai napsauta hiiren kakkospainikkeella tekstikenttää
🗂 Järjestä snippetit ja pohjat kansioihin
🔍 Hae kirjoittaessa
✏️ Muokkaa suoraan paikan päällä — ei ponnahdusikkunoita
📁 Tuo / Vie kirjasto JSON-muodossa
🌍 Saatavilla 26 kielellä

Toimii kaikkialla: Gmail, Outlook, LinkedIn, Salesforce, verkkolomakkeet…

100% yksityinen — tietosi eivät koskaan poistu selaimesta. Ei tiliä, ei synkronointia.

Täydellinen:
• Asiakaspalvelu (vakiovastaukset, pikavastaukset)
• Myyntitiimit (sähköpostipohjat, skriptit)
• Kehittäjät (koodikatkelmat, boilerplate)
• Kaikki, jotka kirjoittavat samoja asioita uudestaan ja uudestaan""",
},
"cs": {
    "name": "Czech (cs)",
    "summary": SUMMARIES["cs"],
    "desc": """MySnips je bezplatný textový expander a správce snippetů pro Chrome. Ukládejte nejpoužívanější textové šablony, připravené odpovědi, klávesové zkratky, URL adresy, adresy, kódy a podpisy — a vkládejte je okamžitě do libovolného textového pole jedním stisknutím klávesy.

🔑 Stiskněte Alt+S (přizpůsobitelné) nebo klikněte pravým tlačítkem na textové pole
🗂 Organizujte snippety a šablony do složek
🔍 Hledejte za psaní
✏️ Upravujte přímo na místě — bez vyskakovacích oken
📁 Importujte / Exportujte knihovnu ve formátu JSON
🌍 Dostupné ve 26 jazycích

Funguje všude: Gmail, Outlook, LinkedIn, Salesforce, webové formuláře…

100% soukromé — vaše data nikdy neopustí prohlížeč. Žádný účet, žádná synchronizace.

Ideální pro:
• Zákaznickou podporu (připravené odpovědi, rychlé odpovědi)
• Obchodní týmy (e-mailové šablony, skripty)
• Vývojáře (úryvky kódu, boilerplate)
• Kohokoli, kdo stále dokola píše stejné věci""",
},
"sk": {
    "name": "Slovak (sk)",
    "summary": SUMMARIES["sk"],
    "desc": """MySnips je bezplatný textový expander a správca snippetov pre Chrome. Ukladajte najpoužívanejšie textové šablóny, pripravené odpovede, klávesové skratky, URL adresy, adresy, kódy a podpisy — a vkladajte ich okamžite do ľubovoľného textového poľa jedným stlačením klávesu.

🔑 Stlačte Alt+S (prispôsobiteľné) alebo kliknite pravým tlačidlom na textové pole
🗂 Organizujte snippety a šablóny do priečinkov
🔍 Hľadajte počas písania
✏️ Upravujte priamo na mieste — bez vyskakovacích okien
📁 Importujte / Exportujte knižnicu vo formáte JSON
🌍 Dostupné v 26 jazykoch

Funguje všade: Gmail, Outlook, LinkedIn, Salesforce, webové formuláre…

100% súkromné — vaše dáta nikdy neopustia prehliadač. Žiadny účet, žiadna synchronizácia.

Ideálne pre:
• Zákaznícku podporu (pripravené odpovede, rýchle odpovede)
• Obchodné tímy (e-mailové šablóny, skripty)
• Vývojárov (úryvky kódu, boilerplate)
• Kohokoľvek, kto stále dookola píše tie isté veci""",
},
"hu": {
    "name": "Hungarian (hu)",
    "summary": SUMMARIES["hu"],
    "desc": """A MySnips egy ingyenes szövegbővítő és snippet-kezelő Chrome-hoz. Tárolja a leggyakrabban használt szövegsablonjait, előre megírt válaszait, billentyűparancsait, URL-jeit, címeit, kódjait és aláírásait — majd illessze be azokat azonnal bármely szövegmezőbe egyetlen billentyűleütéssel.

🔑 Nyomja meg az Alt+S-t (testreszabható) vagy kattintson jobb gombbal bármely szövegmezőre
🗂 Rendezze a snippeteket és sablonokat mappákba
🔍 Keresés gépelés közben
✏️ Helyszíni szerkesztés — felugró ablakok nélkül
📁 Könyvtár importálása / exportálása JSON formátumban
🌍 Elérhető 26 nyelven

Mindenhol működik: Gmail, Outlook, LinkedIn, Salesforce, webes űrlapok…

100% privát — adatai soha nem hagyják el a böngészőt. Nincs fiók, nincs szinkronizálás.

Tökéletes:
• Ügyfélszolgálat számára (előre megírt válaszok, gyorsválaszok)
• Értékesítési csapatoknak (e-mail sablonok, szkriptek)
• Fejlesztőknek (kódrészletek, boilerplate)
• Mindenkinek, aki újra és újra ugyanazokat a dolgokat írja""",
},
"ro": {
    "name": "Romanian (ro)",
    "summary": SUMMARIES["ro"],
    "desc": """MySnips este un expander de text și manager de snippets gratuit pentru Chrome. Stocați cele mai folosite șabloane de text, răspunsuri predefinite, comenzi rapide, URL-uri, adrese, coduri și semnături — și inserați-le instant în orice câmp de text cu o singură tastă.

🔑 Apăsați Alt+S (personalizabil) sau clic dreapta pe orice câmp
🗂 Organizați snippet-urile și șabloanele în foldere
🔍 Căutare în timp real
✏️ Editare inline — fără ferestre pop-up
📁 Importați / Exportați biblioteca ca JSON
🌍 Disponibil în 26 de limbi

Funcționează peste tot: Gmail, Outlook, LinkedIn, Salesforce, formulare web…

100% privat — datele nu părăsesc niciodată browserul. Fără cont, fără sincronizare.

Perfect pentru:
• Suport clienți (răspunsuri predefinite, răspunsuri rapide)
• Echipe de vânzări (șabloane email, scripturi)
• Dezvoltatori (fragmente de cod, boilerplate)
• Oricine tastează aceleași lucruri la nesfârșit""",
},
"hr": {
    "name": "Croatian (hr)",
    "summary": SUMMARIES["hr"],
    "desc": """MySnips je besplatni proširivač teksta i upravljač isječcima za Chrome. Pohranite najčešće korištene tekstualne predloške, gotove odgovore, tipkovničke prečace, URL-ove, adrese, kodove i potpise — i umetajte ih trenutačno u bilo koje tekstualno polje jednim pritiskom tipke.

🔑 Pritisnite Alt+S (prilagodljivo) ili desnom tipkom kliknite na polje
🗂 Organizirajte isječke i predloške u mape
🔍 Pretraživanje u stvarnom vremenu
✏️ Uređivanje izravno u polju — bez skočnih prozora
📁 Uvezite / Izvezite biblioteku kao JSON
🌍 Dostupno na 26 jezika

Radi svugdje: Gmail, Outlook, LinkedIn, Salesforce, web obrasci…

100% privatno — vaši podaci nikad ne napuštaju preglednik. Bez računa, bez sinkronizacije.

Savršeno za:
• Korisničku podršku (gotovi odgovori, brzi odgovori)
• Prodajne timove (predlošci e-pošte, skripte)
• Programere (isječci kôda, boilerplate)
• Svakoga tko uvijek iznova tipka iste stvari""",
},
"bg": {
    "name": "Bulgarian (bg)",
    "summary": SUMMARIES["bg"],
    "desc": """MySnips е безплатен разширител на текст и мениджър на фрагменти за Chrome. Съхранявайте най-използваните текстови шаблони, готови отговори, клавишни комбинации, URL адреси, адреси, кодове и подписи — и ги вмъквайте мигновено в произволно текстово поле с едно натискане.

🔑 Натиснете Alt+S (персонализируемо) или десен клик върху поле
🗂 Организирайте фрагментите и шаблоните в папки
🔍 Търсене в реално време
✏️ Редактиране директно на място — без изскачащи прозорци
📁 Импортирайте / Експортирайте библиотеката като JSON
🌍 Налично на 26 езика

Работи навсякъде: Gmail, Outlook, LinkedIn, Salesforce, уеб формуляри…

100% поверително — данните ви никога не напускат браузъра. Без акаунт, без синхронизация.

Идеален за:
• Клиентска поддръжка (готови отговори, бързи отговори)
• Търговски екипи (имейл шаблони, скриптове)
• Разработчици (фрагменти от код, boilerplate)
• Всеки, който непрекъснато въвежда едни и същи неща""",
},
"el": {
    "name": "Greek (el)",
    "summary": SUMMARIES["el"],
    "desc": """Το MySnips είναι ένας δωρεάν επεκτάτης κειμένου και διαχειριστής snippets για το Chrome. Αποθηκεύστε τα πιο συχνά χρησιμοποιούμενα πρότυπα κειμένου, έτοιμες απαντήσεις, συντομεύσεις πληκτρολογίου, URL, διευθύνσεις, κωδικούς και υπογραφές — και εισαγάγετέ τα άμεσα σε οποιοδήποτε πεδίο.

🔑 Πατήστε Alt+S (παραμετροποιήσιμο) ή δεξί κλικ σε πεδίο κειμένου
🗂 Οργανώστε snippets και πρότυπα σε φακέλους
🔍 Αναζήτηση σε πραγματικό χρόνο
✏️ Επεξεργασία κατευθείαν στο πεδίο — χωρίς αναδυόμενα παράθυρα
📁 Εισαγωγή / Εξαγωγή βιβλιοθήκης ως JSON
🌍 Διαθέσιμο σε 26 γλώσσες

Λειτουργεί παντού: Gmail, Outlook, LinkedIn, Salesforce, φόρμες ιστού…

100% ιδιωτικό — τα δεδομένα σας δεν εγκαταλείπουν ποτέ τον browser. Χωρίς λογαριασμό.

Ιδανικό για:
• Υποστήριξη πελατών (έτοιμες απαντήσεις, γρήγορες απαντήσεις)
• Ομάδες πωλήσεων (πρότυπα email, σενάρια)
• Προγραμματιστές (αποσπάσματα κώδικα, boilerplate)
• Όποιον γράφει τα ίδια πράγματα ξανά και ξανά""",
},
"tr": {
    "name": "Turkish (tr)",
    "summary": SUMMARIES["tr"],
    "desc": """MySnips, Chrome için ücretsiz bir metin genişletici ve snippet yöneticisidir. En sık kullandığın metin şablonlarını, hazır yanıtları, klavye kısayollarını, URL'leri, adresleri, kodları ve imzaları kaydet — ve tek tuşla herhangi bir metin alanına anında yapıştır.

🔑 Alt+S'e bas (özelleştirilebilir) veya herhangi bir alana sağ tıkla
🗂 Snippetleri ve şablonları klasörlerde düzenle
🔍 Yazarken gerçek zamanlı arama
✏️ Yerinde düzenle — açılır pencere yok
📁 Kütüphaneyi JSON olarak içe / dışa aktar
🌍 26 dilde kullanılabilir

Her yerde çalışır: Gmail, Outlook, LinkedIn, Salesforce, web formları…

100% gizli — verilerın hiçbir zaman tarayıcıyı terk etmez. Hesap yok, senkronizasyon yok.

Şunlar için mükemmel:
• Müşteri desteği (hazır yanıtlar, hızlı yanıtlar)
• Satış ekipleri (e-posta şablonları, senaryolar)
• Geliştiriciler (kod parçacıkları, boilerplate)
• Sürekli aynı şeyleri yazan herkes""",
},
"et": {
    "name": "Estonian (et)",
    "summary": SUMMARIES["et"],
    "desc": """MySnips on tasuta teksti laiendaja ja katkendite haldur Chrome'ile. Salvesta kõige sagedamini kasutatavad tekstimallid, valmisvastused, kiirklahvid, URL-id, aadressid, koodid ja allkirjad — ja liita need kohe mis tahes tekstiväljale ühe klahvivajutusega.

🔑 Vajuta Alt+S (kohandatav) või paremklõpsa tekstiväljal
🗂 Korrasta katkendeid ja malle kaustades
🔍 Otsi kirjutamise ajal
✏️ Muuda kohapeal — ilma hüpikakendeta
📁 Impordi / Ekspordi kogu JSON-formaadis
🌍 Saadaval 26 keeles

Töötab kõikjal: Gmail, Outlook, LinkedIn, Salesforce, veebivormid…

100% privaatne — sinu andmed ei lahku kunagi brauserist. Konto puudub, sünkroonimine puudub.

Ideaalne:
• Klienditeenindusele (valmisvastused, kiirvasTused)
• Müügimeeskondadele (e-posti mallid, skriptid)
• Arendajatele (koodikatkendid, boilerplate)
• Kõigile, kes pidevalt samu asju kirjutavad""",
},
"lt": {
    "name": "Lithuanian (lt)",
    "summary": SUMMARIES["lt"],
    "desc": """MySnips yra nemokamas teksto plėstuvas ir fragmentų tvarkyklė Chrome naršyklei. Saugokite dažniausiai naudojamus teksto šablonus, paruoštus atsakymus, klaviatūros sparčiuosius klavišus, URL adresus, adresus, kodus ir parašus — ir įterpkite juos akimirksniu į bet kurį teksto lauką vienu mygtuko paspaudimu.

🔑 Paspauskite Alt+S (pritaikoma) arba dešiniuoju mygtuku spustelėkite teksto lauką
🗂 Tvarkykite fragmentus ir šablonus aplankuose
🔍 Ieškokite realiuoju laiku
✏️ Redaguokite vietoje — be iššokančių langų
📁 Importuokite / Eksportuokite biblioteką JSON formatu
🌍 Prieinama 26 kalbomis

Veikia visur: Gmail, Outlook, LinkedIn, Salesforce, žiniatinklio formos…

100% privatūs — jūsų duomenys niekada nepalieka naršyklės. Jokios paskyros, jokios sinchronizacijos.

Puikiai tinka:
• Klientų aptarnavimui (paruošti atsakymai, greiti atsakymai)
• Pardavimų komandoms (el. laiškų šablonai, scenarijai)
• Kūrėjams (kodo fragmentai, boilerplate)
• Visiems, kurie nuolat rašo tuos pačius dalykus""",
},
"lv": {
    "name": "Latvian (lv)",
    "summary": SUMMARIES["lv"],
    "desc": """MySnips ir bezmaksas teksta paplašinātājs un fragmentu pārvaldnieks Chrome pārlūkam. Saglabājiet biežāk lietotos teksta veidnes, gatavas atbildes, tastatūras saīsnes, URL, adreses, kodus un parakstus — un ievietojiet tos uzreiz jebkurā teksta laukā ar vienu taustiņu.

🔑 Nospiediet Alt+S (pielāgojams) vai ar labo peles pogu noklikšķiniet uz lauka
🗂 Kārtojiet fragmentus un veidnes mapēs
🔍 Meklēšana reāllaikā
✏️ Rediģējiet tieši vietā — bez uznirstošiem logiem
📁 Importējiet / Eksportējiet bibliotēku JSON formātā
🌍 Pieejams 26 valodās

Darbojas visur: Gmail, Outlook, LinkedIn, Salesforce, tīmekļa veidlapas…

100% privāts — jūsu dati nekad neatstāj pārlūku. Nav konta, nav sinhronizācijas.

Lieliski piemērots:
• Klientu atbalstam (gatavas atbildes, ātras atbildes)
• Pārdošanas komandām (e-pasta veidnes, skripti)
• Izstrādātājiem (koda fragmenti, boilerplate)
• Ikvienam, kurš atkal un atkal raksta vienas un tās pašas lietas""",
},
"sl": {
    "name": "Slovenian (sl)",
    "summary": SUMMARIES["sl"],
    "desc": """MySnips je brezplačni razširjevalnik besedila in upravljalnik odlomkov za Chrome. Shranite najpogosteje uporabljene besedilne predloge, pripravljene odgovore, tipkovne bližnjice, URL-je, naslove, kode in podpise — in jih takoj vstavite v katero koli besedilno polje z enim pritiskom tipke.

🔑 Pritisnite Alt+S (prilagodljivo) ali z desno tipko kliknite na polje
🗂 Organizirajte odlomke in predloge v mape
🔍 Iskanje v realnem času
✏️ Urejajte neposredno na mestu — brez pojavnih oken
📁 Uvozite / Izvozite knjižnico kot JSON
🌍 Na voljo v 26 jezikih

Deluje povsod: Gmail, Outlook, LinkedIn, Salesforce, spletni obrazci…

100% zasebno — vaši podatki nikoli ne zapustijo brskalnika. Brez računa, brez sinhronizacije.

Odlično za:
• Podporo strankam (pripravljeni odgovori, hitri odgovori)
• Prodajne ekipe (e-poštne predloge, skripte)
• Razvijalce (odlomki kode, boilerplate)
• Vsakogar, ki znova in znova tipka enake stvari""",
},
"mt": {
    "name": "Maltese (mt)",
    "summary": SUMMARIES["mt"],
    "desc": """MySnips huwa espansur tat-test u manager ta' snippets b'xejn għal Chrome. Aħżen l-iktar mudelli ta' test użati, tweġibiet lesti, shortcuts tal-keyboard, URLs, indirizzi, kodiċi u firem — u daħħalhom minnufih f'kull qasam tat-test b'buttuna waħda.

🔑 Agħfas Alt+S (personalizzabbli) jew ikklikkja bil-lemin fuq kull qasam
🗂 Organizza snippets u mudelli fi folderji
🔍 Fittex f'ħin reali
✏️ Editja direttament fuq il-post — mingħajr pop-ups
📁 Importa / Esporta l-librerija bħala JSON
🌍 Disponibbli f'26 lingwa

Jaħdem kullimkien: Gmail, Outlook, LinkedIn, Salesforce, formoli tal-web…

100% privat — id-data tiegħek qatt ma tħalli l-browser. L-ebda kont, l-ebda sinkronizzazzjoni.

Perfett għal:
• Appoġġ tal-klijenti (tweġibiet lesti, tweġibiet veloċi)
• Timijiet tal-bejgħ (mudelli tal-email, skripts)
• Żviluppaturi (frammenti tal-kodiċi, boilerplate)
• Kull min jikteb l-istess affarijiet darba wara l-oħra""",
},
"ga": {
    "name": "Irish (ga)",
    "summary": SUMMARIES["ga"],
    "desc": """Is leathnaitheoirí téacs agus bainisteoir snippets saor in aisce é MySnips do Chrome. Stóráil do theimpléid téacs is mó úsáide, freagraí réidhe, aicearraí méarchláir, URLanna, seoltaí, cóid agus sínithe — agus cuir isteach iad láithreach in aon réimse téacs le haon bhuille méarchláir.

🔑 Brúigh Alt+S (inoiriúnaithe) nó cliceáil ar dheis ar réimse ar bith
🗂 Eagraigh snippets agus teimpléid i bhfillteáin
🔍 Cuardaigh i bhfíor-am
✏️ Cuir in eagar go díreach sa réimse — gan fuinneoga aníos
📁 Iomportáil / Easpórtáil an leabharlann mar JSON
🌍 Ar fáil i 26 theanga

Oibríonn sé gach áit: Gmail, Outlook, LinkedIn, Salesforce, foirmeacha gréasáin…

100% príobháideach — ní fhágann do chuid sonraí an brabhsálaí riamh. Gan cuntas, gan sioncrónú.

Foirfe do:
• Tacaíocht custaiméirí (freagraí réidhe, freagraí tapa)
• Foirne díolacháin (teimpléid ríomhphoist, scripteanna)
• Forbróirí (blúirí cóid, boilerplate)
• Duine ar bith a chlóscríobhann na rudaí céanna arís agus arís eile""",
},
}

# Écriture du fichier
out = Path(__file__).parent / "store-descriptions.md"
lines = ["# MySnips — Store Descriptions (26 languages)\n",
         "> **Store listing title (all languages):** `MySnips — Text Expander & Snippet Manager`\n",
         "> SEO keywords: text expander, snippet manager, templates, canned responses, shortcuts, auto text, quick replies\n\n",
         "---\n\n"]

for lang_code, d in DESCRIPTIONS.items():
    lines.append(f"## {d['name']} ({lang_code})\n\n")
    lines.append(f"**Summary** *(132 chars max)*:\n{d['summary']}\n\n")
    lines.append(f"**Description**:\n{d['desc']}\n\n")
    lines.append("---\n\n")

out.write_text("".join(lines), encoding="utf-8")
print(f"\nstore-descriptions.md écrit ({out.stat().st_size // 1024} KB)")
print("\n✅ Tout terminé.")

class Strings:
    START_MESSAGE = ("Ciao,\n\n"
                     "Digita una query per cercare tra lo storico delle release di TNTVillage, ([che ha chiuso il 30 "
                     "Agosto 2019](http://forum.tntvillage.scambioetico.org/)), io cercherò di darti l'indirizzo al "
                     "thread ed al backup di esso su https://web.archive.org/"
                     "\n\n"
                     "/help per alcune info utili, /disclaimer per il disclaimer")

    HELP_MESSAGE = ("Alcuni suggerimenti:\n\n"
                    "• la ricerca è case-insensitive (non fa differenza tra maiuscole e minuscole) e puoi specificare "
                    "anche solo delle parole chiave per la ricerca, per esempio "
                    "<code>\"notte leoni\"</code> troverà anche <code>\"Una Notte da Leoni\"</code>.\n"
                    "• se sei da mobile, ti basta toccare/tenere premuto sul link magnet per copiarlo negli appunti\n"
                    "• questo bot <b>non è ufficiale</b>\n"
                    "\n"
                    "<a href=\"https://github.com/zeroone2numeral2/tnt-village-bot\">codice sorgente</a>")
    
    RELEASES_EMPTY = "Mi dispiace, non sono riuscito a trovare nulla :("
    
    RELEASE_TOO_SHORT = "La tua richiesta deve essere lunga lameno 3 caratteri"
    
    SELECT_RELEASE = "Scegli una delle possibili release dalla tastiera qui sotto (vengono elencate solo le prime " \
                     "80), inviami una nuova query, oppure /annulla: "

    SELECT_RELEASE_INVALID = "Selezione non valida. Seleziona una release valida dalla tastiera, oppure /annulla"
    
    RELEASE = ("<b>{titolo_escaped}</b>\n"
               "<code>{descrizione_escaped}</code>\n\n"
               "<b>Dimensione:</b> {dimensione}\n"
               "<b>Caricato il:</b> {data} da {autore_escaped}\n"
               "<b>Categoria:</b> {categoria}\n"
               "<b>Magnet:</b> <code>{magnet}</code>\n"
               "<b>File torrent:</b> {torrent_url}\n\n"
               "Usa /fatto quando hai terminato la ricerca o per rimuovere la tastiera")

    DISCLAIMER = ("<b>Disclaimer:</b>\n"
                  "Al momento questo bot è solo un mirror navigabile per l'archivio pubblicato dal "
                  "sito http://tntvillage.scambioetico.org. Noi non ospitiamo alcun file che violi il diritto "
                  "d'autore, pubblichiamo solo informazioni non verificate e qualsiasi utilizzo di questi dati è "
                  "fatto a proprio rischio. Riteniamo fondamentale un compromesso tra il rispetto del diritto d'autore "
                  "e il rispetto del diritto alla diffusione dell'arte e della conoscenza.")
    
    CANCEL = "Ok, a posto così"

    CB_ANSWER_TRACKERS = "Ecco il magnet coi trackers"

    CB_ANSWER_COLLAPSED = "Informazioni sulla release"

    TORRENT_URL_NO_MAGNET = ("Non ho a disposizione il magnet di questa release, ma puoi scaricare "
                             "il file torrent <a href=\"{torrent_url}\">da qui</a>")

    MAGNET_NOT_AVAILABLE = "Mi dispiace, non ho il magnet di questo torrent :("

    CHANNEL_NOTIFICATION_TEMPLATE = ("<b>Nuova release</b>: {titolo} ({categoria_pretty})\n"
                                     "<code>{descrizione}</code>\n\n"
                                     "<b>File torrent:</b> {torrent_url}")

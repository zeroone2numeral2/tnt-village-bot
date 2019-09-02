class Strings:
    START_MESSAGE = ("Ciao,\n\n"
                     "Digita una query per cercare tra lo storico delle release di TNTVillage, ([che ha chiuso il 30 "
                     "Agosto 2019](http://forum.tntvillage.scambioetico.org/)), io cercherò di darti l'indirizzo al "
                     "thread ed al backup di esso su https://web.archive.org/")
    
    RELEASES_EMPTY = "Mi dispiace, non sono riuscito a trovare nulla :("
    
    RELEASE_TOO_SHORT = "La tua richiesta deve essere lunga lameno 3 caratteri"
    
    SELECT_RELEASE = "Scegli una delle possibili release dalla tastiera qui sotto (vengono elencate solo le prime " \
                     "80), inviami una nuova query, oppure /annulla: "

    SELECT_RELEASE_INVALID = "Selezione non valida. Seleziona una release valida dalla tastiera, oppure /annulla"
    
    RELEASE = ("<b>{titolo}</b>\n"
               "<code>{descrizione}</code>\n\n"
               "<b>Dimensione:</b> {dimensione}\n"
               "<b>Caricato il:</b> {data} da {autore}\n"
               "<b>Categoria:</b> {categoria}\n"
               "<b>Magnet:</b> <code>{magnet}</code>\n\n"
               "Usa /fatto quando hai terminato la ricerca o per rimuovere la tastiera")
    
    CANCEL = "Ok, apposto così"

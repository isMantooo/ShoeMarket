# ShoeMarket

**Autore:** Angelo Mantolini — Matricola 187852

Applicazione Web per la compravendita di scarpe tra utenti, sviluppata con Django.

---

## Tecnologie e librerie utilizzate

- **Python** 3.13.14
- **Django** 6.1
- **Database:** SQLite (di default, nessuna configurazione aggiuntiva richiesta)
- **Pillow** — libreria necessaria per la gestione dei campi immagine (`ImageField`) dei prodotti

---

## Struttura del progetto

* `my_app/`: Cartella principale di configurazione del progetto.
   * `settings.py`: Impostazioni globali.
   * `urls.py`: Instradamento principale degli URL.
* `accounts/`: Autenticazione utenti e gestione dei ruoli.
   * `models.py`: Definizione del modello `Utente` personalizzato con campo ruolo (venditore/acquirente).
   * `forms.py`: Form di registrazione.
   * `views.py`: Vista per registrazione e per login/logout.
   * `urls.py`: Instradamento degli URL specifico dell'app.
* `catalog/`: Applicazione principale del progetto.
   * `models.py`: Definizione dei modelli `Prodotto` e `Categoria`.
   * `views.py`: Vista per il catalogo, per l'aggiunta, l'eliminazione e visione dei dettagli di un prodotto, per la vista della pagina del venditore.
   * `forms.py`: Form di creazione prodotto.
   * `urls.py`: Instradamento degli URL specifico dell'app.
   * `tests.py`: Test unitari.
* `favorites/`: Prodotti preferiti dell'utente.
   * `models.py`: Definizione del modello `Preferito`.
   * `views.py`: Vista per aggiunta/rimozione dai preferiti, per elenco preferiti.
   * `urls.py`: Instradamento degli URL specifico dell'app.
* `orders/`: Acquisti e storico ordini.
   * `models.py`: Definizione del modello `Ordine`.
   * `views.py`: Vista per acquisto, per storico ordini.
   * `urls.py`: Instradamento degli URL specifico dell'app.
* `recommendations/`: Consigli personalizzati sui prodotti.
   * `models.py`: Definizione del modello `Ricerca` (tracciamento dello storico ricerche).
   * `views.py`: Vista per consigliati (basata su preferiti, ordini e storico ricerche).
   * `urls.py`: Instradamento degli URL specifico dell'app.
* `reviews/`: Recensioni e valutazioni dei prodotti.
   * `models.py`: Definizione del modello `Recensione`.
   * `forms.py`: Form di recensione.
   * `views.py`: Vista per recensione e valutazione.
   * `urls.py`: Instradamento degli URL specifico dell'app.

---

# Funzionalità e Design

## 1. `accounts` — Autenticazione e gestione utenti

**Modello**
- `Utente` (estende `AbstractUser`): aggiunge il campo `ruolo`, con scelta obbligatoria tra `venditore` e `acquirente` (default `acquirente`), tramite `choices`.

**Funzionalità**
- **Registrazione**: form personalizzato (`RegistrazioneForm`, basato su `UserCreationForm`) che estende il form standard di Django aggiungendo il campo `ruolo`. Alla creazione dell'account, l'utente sceglie se registrarsi come venditore o acquirente (scelta fissa e non modificabile successivamente).
- **Login/Logout**: gestiti tramite le class-based view native di Django (`LoginView`, `LogoutView`), personalizzate con template dedicati e redirect verso il catalogo dopo l'operazione. Il logout richiede una richiesta POST (tramite form con pulsante), non un semplice link, per motivi di sicurezza.

**Scelte di design**
- Ruoli fissi decisi in fase di registrazione (un singolo utente non può ricoprire entrambi i ruoli).
- Utilizzo del meccanismo standard `AUTH_USER_MODEL` per sostituire il modello utente di Django fin dall'inizio del progetto, prima di qualunque migrazione, per evitare problemi di ricostruzione del database.

## 2. `catalog` — Catalogo, prodotti e filtri

**Modelli**
- `Categoria`: set di scelte predefinite (Sneakers, Running, Eleganti, Stivali, Sandali).
- `Prodotto`: nome, immagine (obbligatoria), taglia (decimale, per supportare le mezze taglie), prezzo, descrizione, disponibilità (booleano), data di pubblicazione (automatica), categoria (ForeignKey) e venditore (ForeignKey). Include il metodo `valutazione_media()`, che calcola dinamicamente la media delle valutazioni delle recensioni collegate tramite aggregazione (`Avg`), gestendo il caso di assenza di recensioni.

**Funzionalità**
- **Catalogo pubblico**: visibile anche ad utenti anonimi, mostra solo i prodotti disponibili, ordinati dal più recente al meno recente.
- **Filtri combinabili**: categoria (menu a tendina generato dinamicamente dalle choices del modello), taglia (lista statica di taglie, incluse le mezze misure), fascia di prezzo (minimo/massimo), ricerca testuale libera sul nome (case-insensitive, tramite `icontains`). I filtri sono sono tutti opzionali e combinabili tra loro.
- **Dettaglio prodotto**: pagina raggiungibile tramite URL con parametro dinamico (`pk`), mostra tutti i dati del prodotto, la valutazione media, le recensioni esistenti, e i pulsanti per recensire, aggiungere ai preferiti e acquistare.
- **Creazione prodotto**: form riservato agli utenti con ruolo `venditore` (controllo esplicito nella vista), con associazione automatica del venditore tramite l'utente loggato (non selezionabile dal form).
- **Pagina venditore**: elenco dei prodotti messi in vendita dall'utente con ruolo `venditore`, con statistiche (numero di vendite, guadagno totale calcolato tramite aggregazione `Sum`), ordinati per disponibilità e data di creazione. I prodotti venduti sono mostrati in modo visivamente distinto (opacità ridotta, etichetta "Venduto") invece di scomparire, mantenendo lo storico (non rimuovibile) visibile al venditore.
- **Rimozione prodotto**: consentita solo al venditore proprietario, e solo se il prodotto non è già stato venduto (per non compromettere l'integrità delle statistiche/storico ordini collegati).

**Scelte di design**
- Tracciamento dei filtri di ricerca (tramite l'app `recommendations`) per alimentare il sistema di consigli personalizzati.
- Validazione lato server dei filtri di prezzo, con gestione esplicita di input non numerici o negativi tramite `try/except` e messaggi di errore, indipendentemente dalle limitazioni del browser.

## 3. `favorites` — Prodotti preferiti

**Modello**
- `Preferito`: prodotto e acquirente (ForeignKey), data di aggiunta automatica. Vincolo `unique_together` per evitare duplicati.

**Funzionalità**
- Meccanismo a **toggle**: un unico pulsante/link che aggiunge il prodotto ai preferiti se non presente, o lo rimuove se già presente, verificato tramite `.exists()`.
- Pagina **"I miei preferiti"**: elenco dei prodotti salvati dall'utente, accessibile solo agli acquirenti.
- Il testo del pulsante nel dettaglio prodotto cambia dinamicamente ("Aggiungi ai preferiti" / "Rimuovi dai preferiti") in base allo stato attuale, calcolato nella vista e passato al template.

**Scelte di design**
- I preferiti relativi a prodotti nel frattempo venduti non vengono eliminati automaticamente dal database: restano visibili nello storico dell'utente (utile anche come dato storico per il sistema dei consigliati), pur non essendo più acquistabili, e differenziandoli da quelli ancora disponibili attraverso scelte grafiche.

## 4. `orders` — Acquisti e storico ordini

**Modello**
- `Ordine`: prodotto e acquirente (ForeignKey), stato (campo testuale con valore di default fisso "completato", per semplicità dato che il pagamento è simulato), data di acquisto automatica.

**Funzionalità**
- **Acquisto**: azione riservata agli acquirenti, che crea immediatamente l'ordine (nessun flusso di conferma/spedizione, dato che il pagamento è fittizio) e aggiorna il prodotto a `disponibile=False`, facendolo sparire dal catalogo pubblico.
- **Storico ordini**: pagina personale dell'acquirente con l'elenco di tutti i prodotti acquistati, comprensiva di data.

**Scelte di design**
- Semplificazione consapevole del flusso di stati (niente "in attesa", "spedito", "ricevuto") rispetto a un e-commerce reale, motivata dalla natura simulata della transazione: l'attenzione progettuale è stata posta sulla logica applicativa (aggiornamento disponibilità, tracciamento statistiche).

## 5. `recommendations` — Sistema di consigli personalizzati

**Modello**
- `Ricerca`: traccia ogni filtro applicato nel catalogo da un utente autenticato (categoria, taglia, prezzo minimo/massimo, tutti opzionali), con data automatica. Salvata solo se l'utente è loggato e ha specificato almeno un criterio di ricerca.

**Funzionalità**
- **Consigli personalizzati**, costruiti con una logica a più livelli:
    - I. **Fonte primaria** (segnale forte): categoria e taglia più frequenti tra i prodotti che l'utente ha nei preferiti o ha acquistato, calcolate con `collections.Counter` su liste ottenute tramite `values_list` attraverso le relazioni tra i modelli.
    - II. **Fonte di fallback** (segnale debole): se la fonte primaria non produce risultati, la stessa logica viene applicata allo storico delle ricerche/filtri salvati.
    - III. Se nessuna delle due fonti produce un segnale utilizzabile, la sezione consigliati resta vuota.
- I prodotti già preferiti o già acquistati vengono sempre esclusi dai risultati finali, per non consigliare qualcosa che l'utente conosce già.

**Scelte di design**
- Combinazione di due fonti di dati (comportamentale forte + ricerche deboli) per aumentare la probabilità di avere sempre consigli rilevanti, evitando sia risultati vuoti ingiustificati sia di mostrare l'intero catalogo come "consigliato" in assenza di segnali reali.

## 6. `reviews` — Recensioni e valutazioni

**Modello**
- `Recensione`: valutazione (da 1 a 5, obbligatoria), commento (facoltativo), prodotto e acquirente (ForeignKey). Vincolo `unique_together` su prodotto-acquirente per impedire recensioni multiple dello stesso utente sullo stesso prodotto.

**Funzionalità**
- Scrittura recensione riservata agli utenti con ruolo `acquirente`.
- Controllo esplicito, prima del salvataggio, sull'esistenza di una recensione già presente per la stessa combinazione prodotto/acquirente, con messaggio di errore dedicato (evitando che l'utente incontri un errore di integrità del database non gestito).
- Le recensioni sono visibili nella pagina di dettaglio prodotto; il commento, se assente, viene sostituito da un messaggio placeholder ("Nessun commento").

**Scelte di design**
- Inizialmente era stato previsto un vincolo "si può recensire solo se si è acquistato il prodotto", poi scartato: dato che un prodotto acquistato diventa immediatamente non disponibile (modello di vendita "pezzo unico"), il vincolo avrebbe reso la funzionalità di recensione difficilmente utilizzabile in pratica.

---

## Funzionalità trasversali

- **Template base condiviso** (`base.html`) con menu di navigazione dinamico in base allo stato di autenticazione e al ruolo dell'utente (link differenti per venditore/acquirente/anonimo).
- **Messaggi di conferma/errore** (Django messages framework) su tutte le operazioni rilevanti: registrazione, creazione prodotto, recensione, acquisto, gestione preferiti, rimozione prodotto, validazione filtri.
- **Controlli di accesso** coerenti in tutte le viste sensibili, basati su autenticazione e ruolo, con redirect verso il catalogo in caso di accesso non autorizzato.
- **Validazione input**: controlli sui form (campi obbligatori, vincoli di unicità) e validazione esplicita lato server per i parametri di ricerca (prezzo).
- **Test automatici**: 7 test complessivi, su tre aree diverse: 
    - logica applicativa (`valutazione_media`, con e senza recensioni).
    - vista pubblica (`catalogo_view`, caso base ed esclusione prodotti non disponibili). 
    - controllo di accesso (`crea_prodotto`, verificato per anonimo, acquirente e venditore).

---

## Istruzioni per l'installazione e l'avvio

### 1. Clonare/scaricare il progetto

Assicurarsi di avere la cartella del progetto (contenente `manage.py`) sul proprio computer:

```bash
git clone https://github.com/isMantooo/ShoeMarket.git
```

### 2. Creare e attivare un virtual environment

```bash
python -m venv venv
```

Su Windows:
```bash
venv\Scripts\activate
```

Su macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Installare le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Applicare le migrazioni al database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Creare un superuser (per accedere al pannello di amministrazione)
Scrivere il seguente comando e eguire le istruzioni a schermo per impostare username, email e password:


```bash
python manage.py createsuperuser
```

### 6. Avviare il server di sviluppo

```bash
python manage.py runserver
```

### 7. Accedere al sito

Aprire il browser e visitare:

```
http://127.0.0.1:8000/
```

Il pannello di amministrazione è raggiungibile su:

```
http://127.0.0.1:8000/admin/
```

---

## Note sull'utilizzo

- Alla registrazione, ogni utente deve scegliere se registrarsi come **venditore** o **acquirente**: i due ruoli hanno permessi e funzionalità distinte.
- Gli utenti **anonimi** (non registrati) possono comunque navigare il catalogo e visualizzare i prodotti, ma non possono acquistare, recensire o mettere in vendita.

---

## Esecuzione dei test

Per poter eseguire i test automatici (unit test Django):

```bash
python manage.py test
```
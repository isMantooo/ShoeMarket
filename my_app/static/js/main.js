document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const imagePreview = document.getElementById('imagePreview');

    // --- FETCH API PER I FILTRI DEL CATALOGO ---
    const formFiltri = document.getElementById('form-filtri');
    const grigliaProdotti = document.getElementById('griglia-prodotti');

    if (formFiltri && grigliaProdotti) {
        
        // Funzione che fa la magia dietro le quinte
        function aggiornaCatalogo() {
            // Estrae tutti i valori (taglia, prezzo, ecc.) dal form
            const url = new URL(window.location.href);
            const formData = new FormData(formFiltri);
            const searchParams = new URLSearchParams(formData);

            // Abbassa l'opacità per far capire all'utente che sta caricando
            grigliaProdotti.style.opacity = '0.4';
            grigliaProdotti.style.transition = 'opacity 0.3s ease';

            // Fa la chiamata al server con i filtri
            fetch(`${url.pathname}?${searchParams.toString()}`)
                .then(response => response.text())
                .then(htmlString => {
                    // Trasforma il testo ricevuto in un documento HTML leggibile da JS
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(htmlString, 'text/html');

                    // Estrae solo la nuova griglia aggiornata
                    const nuovaGriglia = doc.getElementById('griglia-prodotti');

                    // Sostituisce il contenuto della griglia
                    if (nuovaGriglia) {
                        grigliaProdotti.innerHTML = nuovaGriglia.innerHTML;
                    }

                    // --- NUOVA PARTE: AGGIORNA I MESSAGGI DI NOTIFICA ---
                    const nuoviMessaggi = doc.getElementById('blocco-notifiche-ajax');
                    const vecchiMessaggi = document.getElementById('blocco-notifiche-ajax');
                    
                    // Se trova messaggi nuovi dal server, li stampa a schermo
                    if (nuoviMessaggi && vecchiMessaggi) {
                        vecchiMessaggi.innerHTML = nuoviMessaggi.innerHTML;
                    }

                    // Riporta l'opacità a 1 (normale)
                    grigliaProdotti.style.opacity = '1';
                })
                .catch(error => {
                    console.error('Errore durante il filtraggio:', error);
                    grigliaProdotti.style.opacity = '1';
                });
        }

        // Se l'utente clicca il bottone "Filtra", impediamo il ricaricamento e usiamo JS
        formFiltri.addEventListener('submit', function(event) {
            event.preventDefault(); 
            aggiornaCatalogo();
        });

        // EFFETTO WOW: Aggiorna automaticamente appena l'utente cambia una categoria o taglia!
        formFiltri.addEventListener('change', function() {
            aggiornaCatalogo();
        });
    }

    // --- ANTEPRIMA IMMAGINE (Nuovo Prodotto) ---
    if (fileInput && imagePreview) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0]; 
            
            if (file) {
                imagePreview.src = URL.createObjectURL(file);
                imagePreview.classList.remove('d-none');
            } else {
                imagePreview.src = "#";
                imagePreview.classList.add('d-none');
            }
        });
    }

    // --- ANIMAZIONE POPUP ELIMINAZIONE PRODOTTO (Dettagli) ---
    const formAnimato = document.getElementById('form-eliminazione-animata');
    
    if (formAnimato) {
        formAnimato.addEventListener('submit', function(event) {
            // Blocca l'invio immediato del form
            event.preventDefault(); 
            
            // Modifica il testo della modale
            const titolo = document.getElementById('titolo-modale');
            const testo = document.getElementById('testo-modale');
            const bottoni = document.getElementById('bottoni-modale');

            if (titolo && testo && bottoni) {
                titolo.innerHTML = '✅ Prodotto eliminato!';
                titolo.className = 'fw-bold mb-3 text-success';
                testo.innerText = 'Ti stiamo riportando ai tuoi articoli...';
                
                // Nascondi i bottoni per evitare doppi click
                bottoni.style.display = 'none';
                
                // Aspetta 1.5 secondi e poi invia fisicamente i dati
                setTimeout(function() {
                    formAnimato.submit();
                }, 1500);
            }
        });
    }

    // --- ANIMAZIONE POPUP ACQUISTO PRODOTTO (Dettagli) ---
    const formAcquisto = document.getElementById('form-acquisto-animato');
    
    if (formAcquisto) {
        formAcquisto.addEventListener('submit', function(event) {
            event.preventDefault(); 
            
            const titoloAcquisto = document.getElementById('titolo-modale-acquisto');
            const testoAcquisto = document.getElementById('testo-modale-acquisto');
            const bottoniAcquisto = document.getElementById('bottoni-modale-acquisto');

            if (titoloAcquisto && testoAcquisto && bottoniAcquisto) {
                titoloAcquisto.innerHTML = '🎉 Ordine confermato!';
                titoloAcquisto.className = 'fw-bold mb-3 text-success';
                testoAcquisto.innerText = 'Grazie per il tuo acquisto. Elaborazione in corso...';
                
                bottoniAcquisto.style.display = 'none';
                
                setTimeout(function() {
                    formAcquisto.submit();
                }, 1500);
            }
        });
    }
});
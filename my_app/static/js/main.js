document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const imagePreview = document.getElementById('imagePreview');

    const formFiltri = document.getElementById('form-filtri');
    const grigliaProdotti = document.getElementById('griglia-prodotti');

    if (formFiltri && grigliaProdotti) {
        
        function aggiornaCatalogo() {
            const url = new URL(window.location.href);
            const formData = new FormData(formFiltri);
            const searchParams = new URLSearchParams(formData);

            grigliaProdotti.style.opacity = '0.4';
            grigliaProdotti.style.transition = 'opacity 0.3s ease';

            fetch(`${url.pathname}?${searchParams.toString()}`)
                .then(response => response.text())
                .then(htmlString => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(htmlString, 'text/html');

                    const nuovaGriglia = doc.getElementById('griglia-prodotti');

                    if (nuovaGriglia) {
                        grigliaProdotti.innerHTML = nuovaGriglia.innerHTML;
                    }

                    const nuoviMessaggi = doc.getElementById('blocco-notifiche-ajax');
                    const vecchiMessaggi = document.getElementById('blocco-notifiche-ajax');
                    
                    if (nuoviMessaggi && vecchiMessaggi) {
                        vecchiMessaggi.innerHTML = nuoviMessaggi.innerHTML;
                    }

                    grigliaProdotti.style.opacity = '1';
                })
                .catch(error => {
                    console.error('Errore durante il filtraggio:', error);
                    grigliaProdotti.style.opacity = '1';
                });
        }

        formFiltri.addEventListener('submit', function(event) {
            event.preventDefault(); 
            aggiornaCatalogo();
        });

        formFiltri.addEventListener('change', function() {
            aggiornaCatalogo();
        });
    }

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

    const formAnimato = document.getElementById('form-eliminazione-animata');
    
    if (formAnimato) {
        formAnimato.addEventListener('submit', function(event) {
            event.preventDefault(); 
            
            const titolo = document.getElementById('titolo-modale');
            const testo = document.getElementById('testo-modale');
            const bottoni = document.getElementById('bottoni-modale');

            if (titolo && testo && bottoni) {
                titolo.innerHTML = '✅ Prodotto eliminato!';
                titolo.className = 'fw-bold mb-3 text-success';
                testo.innerText = 'Ti stiamo riportando ai tuoi articoli...';
                
                bottoni.style.display = 'none';
                
                setTimeout(function() {
                    formAnimato.submit();
                }, 1500);
            }
        });
    }

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
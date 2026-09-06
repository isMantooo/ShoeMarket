from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Prodotto, Categoria
from accounts.models import Utente
from reviews.models import Recensione

# Create your tests here.
class CatalogTests(TestCase):
    def setUp(self):
        self.utente1 = Utente.objects.create_user(username='paolo', password='password123', ruolo='venditore')
        self.utente2 = Utente.objects.create_user(username='mario', password='password123', ruolo='acquirente')
        self.utente3 = Utente.objects.create_user(username='luigi', password='password123', ruolo='acquirente')

        self.categoria = Categoria.objects.create(nome='sneakers')

        immagine_finta = SimpleUploadedFile(name='test_image.jpg', content=b'contenuto finto', content_type='image/jpeg')
        self.prodotto1 = Prodotto.objects.create(nome='scarpa', immagine=immagine_finta, taglia=43, prezzo=90, descrizione='Nuova', categoria=self.categoria, venditore=self.utente1, disponibile=True)
        self.prodotto2 = Prodotto.objects.create(nome='scarpa_venduta', immagine=immagine_finta, taglia=43, prezzo=90, descrizione='Nuova', categoria=self.categoria, venditore=self.utente1, disponibile=False)


    def test_valutazione_media_senza_recensioni(self):
        risultato = self.prodotto1.valutazione_media()
        self.assertEqual(risultato, "Nessuna recensione")

    def test_valutazione_media_con_recensioni(self):
        self.recensione1 = Recensione.objects.create(acquirente=self.utente2, prodotto=self.prodotto1, valutazione=5, commento='')
        self.recensione2 = Recensione.objects.create(acquirente=self.utente3, prodotto=self.prodotto1, valutazione=4, commento='')

        risultato = self.prodotto1.valutazione_media()
        self.assertEqual(risultato, 4.5)

    def test_catalogo_view(self):
        response = self.client.get('/catalog/catalogo/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'scarpa')

    def test_catalogo_esclude_non_disponibili(self):
        response = self.client.get('/catalog/catalogo/')

        self.assertNotContains(response, 'scarpa_venduta')

    def test_accesso_crea_prodotto_anonimo(self):
        response = self.client.get('/catalog/nuovo_prodotto/')
        self.assertEqual(response.status_code, 302)

    def test_accesso_crea_prodotto_acquirente(self):
        self.client.login(username='mario', password='password123')
        response = self.client.get('/catalog/nuovo_prodotto/')
        self.assertEqual(response.status_code, 302)

    def test_accesso_crea_prodotto_venditore(self):
        self.client.login(username='paolo', password='password123')
        response = self.client.get('/catalog/nuovo_prodotto/')
        self.assertEqual(response.status_code, 200)

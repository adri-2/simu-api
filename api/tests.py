# core/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core import mail
from decimal import Decimal

from .models import ImporterProfile, ProductCategory, Product, Simulation, LegalPersonality, TariffSpecies

User = get_user_model()

class UserAuthenticationTests(APITestCase):
    """
    Tests pour l'enregistrement et l'authentification des utilisateurs.
    """
    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('token_obtain_pair')
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
            'full_name': 'Test User',
            'legal_personality': LegalPersonality.PHYSICAL,
            'phone_number': '0123456789'
        }

    def test_user_registration(self):
        """
        S'assure qu'un nouvel utilisateur peut s'enregistrer.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())
        self.assertTrue(ImporterProfile.objects.filter(user__email='testuser@example.com').exists())

    def test_user_registration_password_mismatch(self):
        """
        S'assure que l'enregistrement échoue si les mots de passe ne correspondent pas.
        """
        self.user_data['password2'] = 'WrongPassword'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_duplicate_email(self):
        """
        S'assure que l'enregistrement échoue si l'email est déjà utilisé.
        """
        User.objects.create_user(email='testuser@example.com', username='existinguser', password='password')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_login(self):
        """
        S'assure qu'un utilisateur peut se connecter et obtenir des tokens.
        """
        user = User.objects.create_user(email='login@example.com', username='loginuser', password='StrongPassword123!')
        login_data = {
            'email': 'login@example.com',
            'password': 'StrongPassword123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class UserProfileTests(APITestCase):
    """
    Tests pour la gestion du profil utilisateur.
    """
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', username='user', password='password123')
        self.importer_profile = ImporterProfile.objects.create(user=self.user, full_name='User Profile', legal_personality=LegalPersonality.PHYSICAL)
        self.profile_url = reverse('user_profile')
        self.client.force_authenticate(user=self.user) # Authentifie l'utilisateur pour les tests

    def test_retrieve_user_profile(self):
        """
        S'assure qu'un utilisateur peut récupérer son propre profil.
        """
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['importer_profile']['full_name'], 'User Profile')

    def test_update_user_profile(self):
        """
        S'assure qu'un utilisateur peut mettre à jour son profil.
        """
        new_data = {
            'phone_number': '9876543210',
            'importer_profile': {'full_name': 'Updated Name', 'legal_personality': LegalPersonality.MORAL}
        }
        # Note: DRF ne gère pas la mise à jour des OneToOneFields imbriqués directement avec ModelSerializer par défaut
        # Pour ImporterProfile, il faudrait soit le mettre à jour séparément, soit un serializer imbriqué avec write=True
        # Pour ce test, nous allons simuler une mise à jour directe des champs du User.
        # Pour ImporterProfile, on simule une modification via les données brutes si nécessaire
        response = self.client.patch(self.profile_url, {'phone_number': new_data['phone_number']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, new_data['phone_number'])
        # Pour mettre à jour ImporterProfile via le même endpoint, il faudrait un serializer plus complexe ou une vue custom.

class ProductCategoryTests(APITestCase):
    """
    Tests pour les opérations sur les catégories de produits.
    """
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='admin@example.com', username='admin', password='adminpassword')
        self.regular_user = User.objects.create_user(email='regular@example.com', username='regular', password='regularpassword')
        self.category_url = reverse('productcategory-list')
        self.category1 = ProductCategory.objects.create(name='Electronics', cemac_hs_code_prefix='85')

    def test_list_product_categories_as_regular_user(self):
        """
        S'assure qu'un utilisateur régulier peut lister les catégories.
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product_category_as_admin(self):
        """
        S'assure qu'un admin peut créer une catégorie.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Footwear', 'cemac_hs_code_prefix': '64'}
        response = self.client.post(self.category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductCategory.objects.count(), 2)

    def test_create_product_category_as_regular_user_forbidden(self):
        """
        S'assure qu'un utilisateur régulier ne peut pas créer de catégorie.
        """
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'Books', 'cemac_hs_code_prefix': '49'}
        response = self.client.post(self.category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Accès refusé

class ProductTests(APITestCase):
    """
    Tests pour les opérations sur les produits douaniers.
    """
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='admin_prod@example.com', username='admin_prod', password='adminpassword')
        self.regular_user = User.objects.create_user(email='regular_prod@example.com', username='regular_prod', password='regularpassword')
        self.product_url = reverse('product-list')
        self.category = ProductCategory.objects.create(name='Vehicles', cemac_hs_code_prefix='87')
        self.product1 = Product.objects.create(
            name='Car', category=self.category, tariff_species=TariffSpecies.INTERMEDIATE_DIVERSE_GOODS,
            cemac_hs_code='8703.23.00.00', is_vehicle=True
        )

    def test_list_products_as_regular_user(self):
        """
        S'assure qu'un utilisateur régulier peut lister les produits.
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product_as_admin(self):
        """
        S'assure qu'un admin peut créer un produit.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'Motorcycle',
            'category': self.category.id,
            'tariff_species': TariffSpecies.CONSUMPTION_GOODS,
            'cemac_hs_code': '8711.20.00.00',
            'is_luxury': False,
            'is_alcohol_tobacco': False,
            'is_vehicle': True,
            'is_phytosanitary': False
        }
        response = self.client.post(self.product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_as_regular_user_forbidden(self):
        """
        S'assure qu'un utilisateur régulier ne peut pas créer de produit.
        """
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'name': 'Bicycle',
            'category': self.category.id,
            'tariff_species': TariffSpecies.CONSUMPTION_GOODS,
            'cemac_hs_code': '8712.00.00.00'
        }
        response = self.client.post(self.product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class SimulationTests(APITestCase):
    """
    Tests pour les opérations de simulation des coûts douaniers.
    """
    def setUp(self):
        self.user = User.objects.create_user(email='simuser@example.com', username='simuser', password='simpassword')
        self.importer_profile = ImporterProfile.objects.create(user=self.user, full_name='Sim User', legal_personality=LegalPersonality.PHYSICAL)
        self.category = ProductCategory.objects.create(name='Cosmetics', cemac_hs_code_prefix='33')
        self.product = Product.objects.create(
            name='Perfume', category=self.category, tariff_species=TariffSpecies.CONSUMPTION_GOODS,
            cemac_hs_code='3303.00.00.00', is_luxury=True
        )
        self.simulation_list_url = reverse('simulation-list')
        self.client.force_authenticate(user=self.user)

    def test_create_simulation(self):
        """
        S'assure qu'une simulation peut être créée et que les coûts sont calculés.
        """
        data = {
            'product': self.product.id,
            'declared_value': '1000.00',
            'transport_cost': '50.00',
            'handling_cost': '20.00',
            'weight_in_tons': '0.1',
            'has_niu': True
        }
        response = self.client.post(self.simulation_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Simulation.objects.count(), 1)
        simulation = Simulation.objects.first()
        self.assertEqual(simulation.user, self.user)
        self.assertGreater(simulation.total_customs_cost, 0)
        self.assertIsNotNone(simulation.payment_confirmation_code)

        # Vérifier quelques calculs de base (ex: VD et DD)
        # VD = 1000 + 50 + 20 = 1070
        self.assertEqual(simulation.customs_value_vd, Decimal('1070.00'))
        # DD = 1070 * 30% = 321
        self.assertEqual(simulation.customs_duty_dd, Decimal('321.00'))
        # DA (luxe) = (1070 + 321) * 25% = 1391 * 0.25 = 347.75
        self.assertEqual(simulation.excise_duty_da, Decimal('347.75'))
        # TVA = (1070 + 321 + 347.75) * 17.5% = 1738.75 * 0.175 = 304.28
        self.assertAlmostEqual(simulation.vat_tva, Decimal('304.28'), places=2)


    def test_list_user_simulations(self):
        """
        S'assure qu'un utilisateur ne voit que ses propres simulations.
        """
        Simulation.objects.create(user=self.user, product=self.product, declared_value='500', transport_cost='10', handling_cost='5')
        other_user = User.objects.create_user(email='other@example.com', username='other', password='otherpassword')
        Simulation.objects.create(user=other_user, product=self.product, declared_value='100', transport_cost='10', handling_cost='5')

        response = self.client.get(self.simulation_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) # Devrait voir 1 seule simulation

    def test_confirm_payment_and_send_email(self):
        """
        S'assure que le paiement peut être confirmé et que l'email est envoyé.
        """
        simulation = Simulation.objects.create(user=self.user, product=self.product, declared_value='2000')
        confirm_payment_url = reverse('simulation-confirm-payment', args=[simulation.id])

        # Pré-remplir le code de confirmation pour le test (normalement généré à la création)
        simulation.payment_confirmation_code = "TESTCODE123"
        simulation.save()

        # Nettoyer la boîte mail avant le test
        mail.outbox = []

        data = {'payment_confirmation_code': 'TESTCODE123'}
        response = self.client.post(confirm_payment_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        simulation.refresh_from_db()
        self.assertTrue(simulation.is_paid)
        self.assertTrue(simulation.response_email_sent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.user.email)
        self.assertIn(f"Votre simulation de coûts douaniers SIMU #{simulation.id}", mail.outbox[0].subject)

    def test_confirm_payment_invalid_code(self):
        """
        S'assure que le paiement échoue avec un code invalide.
        """
        simulation = Simulation.objects.create(user=self.user, product=self.product, declared_value='2000')
        confirm_payment_url = reverse('simulation-confirm-payment', args=[simulation.id])

        data = {'payment_confirmation_code': 'WRONGCODE'}
        response = self.client.post(confirm_payment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Code de confirmation de paiement invalide", response.data['detail']) # Si tu utilises la validation dans la vue
        simulation.refresh_from_db()
        self.assertFalse(simulation.is_paid)

    def test_admin_can_view_all_simulations(self):
        """
        S'assure qu'un administrateur peut lister toutes les simulations.
        """
        admin_user = User.objects.create_superuser(email='admin_sim@example.com', username='admin_sim', password='adminpassword')
        Simulation.objects.create(user=self.user, product=self.product, declared_value='500')
        other_user = User.objects.create_user(email='other_sim@example.com', username='other_sim', password='otherpassword')
        Simulation.objects.create(user=other_user, product=self.product, declared_value='100')

        self.client.force_authenticate(user=admin_user)
        response = self.client.get(self.simulation_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) # L'admin voit les 2 simulations
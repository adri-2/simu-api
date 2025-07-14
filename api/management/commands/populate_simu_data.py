# core/management/commands/populate_simu_data.py

from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import ProductCategory, Product, TariffSpecies

class Command(BaseCommand):
    """
    Commande de gestion pour peupler la base de données avec des données initiales
    de catégories de produits et de produits douaniers pour SIMU.
    """
    help = 'Peuple la base de données avec des catégories et produits douaniers initiaux.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Démarrage du peuplement de la base de données SIMU...'))

        # Utilise une transaction atomique pour garantir que toutes les opérations
        # sont complétées ou qu'aucune n'est effectuée en cas d'erreur.
        with transaction.atomic():
            self._create_product_categories()
            self._create_products()

        self.stdout.write(self.style.SUCCESS('Peuplement de la base de données terminé avec succès !'))

    def _create_product_categories(self):
        """
        Crée les catégories de produits initiales si elles n'existent pas déjà.
        """
        self.stdout.write(self.style.MIGRATE_HEADING('Création des catégories de produits...'))
        categories_data = [
            {'name': 'Produits Alimentaires de Première Nécessité', 'cemac_hs_code_prefix': '01-24'},
            {'name': 'Matières Premières', 'cemac_hs_code_prefix': '25-49'},
            {'name': 'Biens Intermédiaires', 'cemac_hs_code_prefix': '50-84'},
            {'name': 'Biens de Consommation Courante', 'cemac_hs_code_prefix': '85-97'},
            {'name': 'Produits de Luxe', 'cemac_hs_code_prefix': '98'}, # Généralement, pas un préfixe SH strict mais une catégorie fiscale
            {'name': 'Boissons et Tabacs', 'cemac_hs_code_prefix': '22-24'},
            {'name': 'Véhicules', 'cemac_hs_code_prefix': '87'},
            {'name': 'Produits Pharmaceutiques', 'cemac_hs_code_prefix': '30'},
            {'name': 'Chaussures', 'cemac_hs_code_prefix': '64'},
            {'name': 'Vêtements', 'cemac_hs_code_prefix': '61-62'},
            {'name': 'Animaux Vivants', 'cemac_hs_code_prefix': '01'},
            {'name': 'Meubles', 'cemac_hs_code_prefix': '94'},
            {'name': 'Produits Surgelés', 'cemac_hs_code_prefix': '02-04'},
        ]

        for cat_data in categories_data:
            category, created = ProductCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'cemac_hs_code_prefix': cat_data['cemac_hs_code_prefix']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Catégorie '{category.name}' créée."))
            else:
                self.stdout.write(self.style.WARNING(f"  Catégorie '{category.name}' existe déjà."))
        self.stdout.write(self.style.MIGRATE_HEADING('Catégories créées/vérifiées.'))

    def _create_products(self):
        """
        Crée les produits douaniers initiaux et les associe à leurs catégories.
        """
        self.stdout.write(self.style.MIGRATE_HEADING('Création des produits douaniers...'))

        # Récupère les catégories pour les associations
        cat_necessity = ProductCategory.objects.get(name='Produits Alimentaires de Première Nécessité')
        cat_raw_materials = ProductCategory.objects.get(name='Matières Premières')
        cat_intermediate = ProductCategory.objects.get(name='Biens Intermédiaires')
        cat_consumption = ProductCategory.objects.get(name='Biens de Consommation Courante')
        cat_luxury = ProductCategory.objects.get(name='Produits de Luxe')
        cat_drinks_tobacco = ProductCategory.objects.get(name='Boissons et Tabacs')
        cat_vehicles = ProductCategory.objects.get(name='Véhicules')
        cat_pharma = ProductCategory.objects.get(name='Produits Pharmaceutiques')
        cat_shoes = ProductCategory.objects.get(name='Chaussures')
        cat_clothes = ProductCategory.objects.get(name='Vêtements')
        cat_animals = ProductCategory.objects.get(name='Animaux Vivants')
        cat_furniture = ProductCategory.objects.get(name='Meubles')
        cat_frozen = ProductCategory.objects.get(name='Produits Surgelés')

        products_data = [
    # Biens de 1ère nécessité (5%)
    {'name': 'Riz (sacs de 50kg)', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1006.30.00.00', 'is_phytosanitary': True},
    {'name': 'Huile de palme raffinée', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1511.90.10.00'},
    {'name': 'Lait en poudre (paquets)', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '0402.10.00.00'},
    {'name': 'Farine de maïs', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1102.20.00.00'},
    {'name': 'Sel alimentaire', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '2501.00.10.00'},
    {'name': 'Sucre raffiné', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1701.99.10.00'},
    {'name': 'Macaroni (paquets)', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1902.19.00.00'},
    {'name': 'Pain industriel', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1905.90.00.00'},
    {'name': 'Conserves de tomates', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '2002.10.00.00'},
    {'name': 'Légumes secs (haricots)', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '0713.33.00.00'},

    # Matières premières (10%)
    {'name': 'Coton brut', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '5201.00.00.00'},
    {'name': 'Fèves de cacao non torréfiées', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '1801.00.00.00', 'is_phytosanitary': True},
    {'name': 'Bois brut de sciage', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '4403.99.00.00', 'is_phytosanitary': True},
    {'name': 'Sable de rivière', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '2505.10.00.00'},
    {'name': 'Graviers concassés', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '2517.10.00.00'},
    {'name': 'Pierre calcaire', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '2521.00.00.00'},
    {'name': 'Caoutchouc naturel', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '4001.10.00.00'},
    {'name': 'Latex brut', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '4001.21.00.00'},

    # Biens intermédiaires (20%)
    {'name': 'Panneaux solaires (module)', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '8541.40.00.00'},
    {'name': 'Ciments (sacs)', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '2523.29.00.00'},
    {'name': 'Tôles en acier', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '7210.41.00.00'},
    {'name': 'Tuyaux en PVC', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '3917.22.00.00'},
    {'name': 'Câbles électriques', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '8544.49.00.00'},
    {'name': 'Peinture en bidon', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '3208.10.00.00'},
    {'name': 'Carrelage en céramique', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '6907.21.00.00'},
    {'name': 'Planches en contreplaqué', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '4412.31.00.00'},

    # Biens de consommation courante (30%)
    {'name': 'Téléphones portables standards', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8517.12.00.00'},
    {'name': 'Chaussures de sport', 'category': cat_shoes, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '6403.99.00.00'},
    {'name': 'T-shirts en coton', 'category': cat_clothes, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '6109.10.00.00'},
    {'name': 'Détergent en poudre', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '3402.20.00.00'},
    {'name': 'Ordinateurs portables', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8471.30.00.00'},
    {'name': 'Luminaires LED', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9405.40.00.00'},
    {'name': 'Savon de toilette', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '3401.11.00.00'},
    {'name': 'Frigos domestiques', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8418.10.00.00'},
    {'name': 'Ventilateurs électriques', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8414.51.00.00'},
    {'name': 'Fer à repasser', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8516.40.00.00'},
    {'name': 'Téléviseurs LED', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8528.72.00.00'},
    {'name': 'Bouteilles d’eau minérale', 'category': cat_drinks_tobacco, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '2201.10.00.00'},

    # Produits de Luxe (DA 25%)
    {'name': 'Montres de marque de luxe', 'category': cat_luxury, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9102.11.00.00', 'is_luxury': True},
    {'name': 'Parfums de haute-couture', 'category': cat_luxury, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '3303.00.00.00', 'is_luxury': True},
    {'name': 'Sacs à main de luxe', 'category': cat_luxury, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '4202.21.00.00', 'is_luxury': True},

    # Alcools et Tabacs (DA 25%)
    {'name': 'Cigarettes', 'category': cat_drinks_tobacco, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '2402.20.00.00', 'is_alcohol_tobacco': True},
    {'name': 'Bières (bouteilles)', 'category': cat_drinks_tobacco, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '2203.00.00.00', 'is_alcohol_tobacco': True},
    {'name': 'Vin rouge (bouteilles)', 'category': cat_drinks_tobacco, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '2204.21.00.00', 'is_alcohol_tobacco': True},
    {'name': 'Whisky importé', 'category': cat_drinks_tobacco, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '2208.30.00.00', 'is_alcohol_tobacco': True},

    # Véhicules (DA 12.5%)
    {'name': 'Véhicule neuf (berline essence)', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8703.23.00.00', 'is_vehicle': True},
    {'name': 'Véhicule occasion (SUV diesel)', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8703.32.00.00', 'is_vehicle': True},
    {'name': 'Camion benne', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8704.10.00.00', 'is_vehicle': True},
    {'name': 'Moto 125cc', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8711.20.00.00', 'is_vehicle': True},

    # Autres
    {'name': 'Animaux vivants (volaille)', 'category': cat_animals, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '0105.11.00.00', 'is_phytosanitary': True},
    {'name': 'Produits pharmaceutiques (médicaments essentiels)', 'category': cat_pharma, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '3004.90.00.00'},
    {'name': 'Vaccins vétérinaires', 'category': cat_pharma, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '3002.30.00.00'},
    {'name': 'Chaussures pour enfants', 'category': cat_shoes, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '6402.91.00.00'},
    {'name': 'Vestes en jeans', 'category': cat_clothes, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '6201.91.00.00'},
    {'name': 'Congélateur domestique', 'category': cat_consumption, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8418.21.00.00'},
    {'name': 'Poissons surgelés (maquereaux)', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '0303.22.00.00', 'is_phytosanitary': True},
        {'name': 'Pâtes alimentaires (spaghetti)', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1902.11.00.00'},
    {'name': 'Légumineuses (lentilles)', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '0713.40.00.00'},
    {'name': 'Maïs en grain', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1005.90.00.00'},
    {'name': 'Huile d’arachide', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '1508.10.00.00'},
    {'name': 'Lait liquide UHT', 'category': cat_necessity, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '0401.20.11.00'},

    {'name': 'Bois traité pour menuiserie', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '4407.99.00.10'},
    {'name': 'Fer brut', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '7201.10.00.00'},
    {'name': 'Bauxite brute', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '2606.00.00.00'},
    {'name': 'Minerai de fer', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '2601.11.00.00'},
    {'name': 'Sables siliceux', 'category': cat_raw_materials, 'tariff_species': TariffSpecies.RAW_MATERIALS, 'cemac_hs_code': '2505.10.90.00'},

    {'name': 'Tuiles en terre cuite', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '6905.10.00.00'},
    {'name': 'Briques creuses', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '6904.10.00.00'},
    {'name': 'Tôles ondulées', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '7210.49.00.00'},
    {'name': 'Colles industrielles', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '3506.91.00.00'},
    {'name': 'Poutrelles en acier', 'category': cat_intermediate, 'tariff_species': TariffSpecies.INTERMEDIATE_DIVERSE_GOODS, 'cemac_hs_code': '7216.10.00.00'},

    {'name': 'Canapés en tissu', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9401.61.90.00'},
    {'name': 'Tables à manger', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9403.30.90.00'},
    {'name': 'Chaises en plastique', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9401.80.00.00'},
    {'name': 'Meubles TV en bois', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9403.60.00.00'},
    {'name': 'Bureaux métalliques', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9403.10.00.00'},

    {'name': 'Conserves de sardines', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '1604.13.00.00', 'is_phytosanitary': True},
    {'name': 'Poulet congelé', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '0207.14.10.00', 'is_phytosanitary': True},
    {'name': 'Légumes surgelés (carottes)', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '0710.10.00.00', 'is_phytosanitary': True},
    {'name': 'Viande de bœuf congelée', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '0202.30.00.00', 'is_phytosanitary': True},
    {'name': 'Poisson tilapia congelé', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '0303.75.00.00', 'is_phytosanitary': True},

    {'name': 'Moto tricycle', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8711.60.00.00', 'is_vehicle': True},
    {'name': 'Pick-up double cabine', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8704.21.00.00', 'is_vehicle': True},
    {'name': 'Bus de transport urbain', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8702.10.00.00', 'is_vehicle': True},
    {'name': 'Remorque agricole', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8716.20.00.00', 'is_vehicle': True},
    {'name': 'Scooter électrique', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8711.60.90.00', 'is_vehicle': True},
    {'name': 'Bateau de pêche (petit)', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8903.99.00.00', 'is_vehicle': True},
    {'name': 'Tracteur agricole', 'category': cat_vehicles, 'tariff _species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8701.90.00.00', 'is_vehicle': True},
    {'name': 'Camion frigorifique', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8704.22.00.00', 'is_vehicle': True},
    {'name': 'Quad tout-terrain', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8703.90.00.00', 'is_vehicle': True},
    {'name': 'Bateau de plaisance', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8903.10.00.00', 'is_vehicle': True},
    {'name': 'Tricycle à moteur', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8711.20.00.00', 'is_vehicle': True},
    {'name': 'Camion de livraison', 'category': cat_vehicles, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '8704.10.00.00', 'is_vehicle': True},

    {'name': 'Antibiotiques (pénicilline)', 'category': cat_pharma, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '2941.10.00.00'},
    {'name': 'Vaccins humains (hépatite B)', 'category': cat_pharma, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '3002.20.00.00'},
    {'name': 'Bandages et pansements', 'category': cat_pharma, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '3005.90.00.00'},
    {'name': 'Sérums antivenimeux', 'category': cat_pharma, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '3002.90.00.00'},
    {'name': 'Produits de soins dentaires', 'category': cat_pharma, 'tariff_species': TariffSpecies.NECESSITY_GOODS, 'cemac_hs_code': '3306.10.00.00'},

    {'name': 'Chaises en bois massif', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9401.61.90.00'},
    {'name': 'Canapés en cuir', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9401.61.10.00'},
    {'name': 'Tables basses en verre', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9403.70.00.00'},
    {'name': 'Armoires en bois', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9403.40.00.00'},
    {'name': 'Bureaux en bois', 'category': cat_furniture, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '9403.10.00.00'},

    {'name': 'Fruits congelés (mangues)', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '0811.90.00.00', 'is_phytosanitary': True},
    {'name': 'Frites surgelées', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '2004.10.00.00', 'is_phytosanitary': True},
    {'name': 'Glaces et sorbets', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '2105.00.00.00', 'is_phytosanitary': True},
    {'name': 'Fruits de mer congelés (crevettes)', 'category': cat_frozen, 'tariff_species': TariffSpecies.CONSUMPTION_GOODS, 'cemac_hs_code': '0306.13.00.00', 'is_phytosanitary': True},
    
    

]

        for prod_data in products_data:
            # Utilise update_or_create pour éviter les doublons et mettre à jour si le produit existe déjà
            try:
                product, created = Product.objects.update_or_create(
                    cemac_hs_code=prod_data['cemac_hs_code'], # Utilise le code SH comme identifiant unique
                    defaults={
                        'name': prod_data['name'],
                        'category': prod_data['category'],
                        'tariff_species': prod_data['tariff_species'],
                        'is_luxury': prod_data.get('is_luxury', False),
                        'is_alcohol_tobacco': prod_data.get('is_alcohol_tobacco', False),
                        'is_vehicle': prod_data.get('is_vehicle', False),
                        'is_phytosanitary': prod_data.get('is_phytosanitary', False),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"  Produit '{product.name}' ({product.cemac_hs_code}) créé."))
                else:
                    self.stdout.write(self.style.WARNING(f"  Produit '{product.name}' ({product.cemac_hs_code}) mis à jour."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Erreur pour le produit '{prod_data.get('name', 'inconnu')}' ({prod_data.get('cemac_hs_code', 'inconnu')}): {e}"))
                continue
        self.stdout.write(self.style.MIGRATE_HEADING('Produits créés/vérifiés.'))
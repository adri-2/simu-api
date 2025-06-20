from django.core.management.base import BaseCommand
from api.models import Product, Category

class Command(BaseCommand):
    help = "Génère des produits fictifs pour les tests"

    def handle(self, *args, **kwargs):
        print("Génération des catégories...")
        category_map = {
            "Biens de première nécessité": {"duty_rate": 5},
            "Matières premières": {"duty_rate": 10},
            "Biens intermédiaires": {"duty_rate": 20},
            "Biens de consommation": {"duty_rate": 30},
        }

        category_objs = {}

        for name, attrs in category_map.items():
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={
                    "description": f"Catégorie : {name}",
                    "duty_rate": attrs["duty_rate"]
                }
            )
            category_objs[name] = category

        print("Génération des produits...")

        products = [
            # Exemple pour "Biens de première nécessité"
            {"name": "Riz blanc", "category": "Biens de première nécessité", "description": "Riz importé"},
            {"name": "Farine de blé", "category": "Biens de première nécessité", "description": "Farine de blé tendre"},
            {"name": "Téléphones portables", "category": "Biens de consommation", "description": "Smartphones Android"},
            {"name": "Pétrole brut", "category": "Matières premières", "description": "Pétrole brut non raffiné"},
            {"name": "Planches de bois traitées", "category": "Biens intermédiaires", "description": "Bois transformé"},
            # ... (ajoute les autres ici)
             {"name": "Riz blanc", "category": "Biens de première nécessité", "description": " ", "duty_rate": 5},
            {"name": "Bauxite", "category": "Matières premières", "description": " ", "duty_rate": 10},
            {"name": "Tôles en aluminium", "category": "Biens intermédiaires", "description": " ", "duty_rate": 20},
            {"name": "Téléphones portables", "category": "Biens de consommation", "description": " ", "duty_rate": 30},
            # ... complète ici
            # Biens de première nécessité (5%)
        {"name": "Riz blanc", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Farine de blé", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Sucre", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Sel", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Huile végétale", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Haricots secs", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Lentilles", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Lait en poudre", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Pain", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        {"name": "Œufs", "category": "Biens de première nécessité", "description":" ","duty_rate": 5},
        # ... (ajoute les 40 restants ici)

        # Matières premières (10%)
        {"name": "Bauxite", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Minerai de fer", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Coton brut", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Bois brut", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Latex naturel", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Charbon minéral", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Cuivre brut", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Pétrole brut", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Gaz naturel", "category": "Matières premières", "description":" ","duty_rate": 10},
        {"name": "Pierre calcaire", "category": "Matières premières", "description":" ","duty_rate": 10},
        # ... (ajoute les 40 restants ici)

        # Biens intermédiaires et divers (20%)
        {"name": "Planches de bois traitées", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Tôles en aluminium", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Acier laminé", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Fil de cuivre", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Textile en coton (rouleaux)", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Roulements mécaniques", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Pneus", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Engrais chimiques", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Insecticides", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        {"name": "Lubrifiants industriels", "category": "Biens intermédiaires", "description":" ","duty_rate": 20},
        # ... (ajoute les 40 restants ici)

        # Biens de consommation courante (30%)
        {"name": "Téléphones portables", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Téléviseurs", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Réfrigérateurs", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Climatiseurs", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Ordinateurs portables", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Voitures neuves", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Vêtements de marque", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Chaussures de sport", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Bijoux", "category": "Biens de consommation", "description":" ","duty_rate": 30},
        {"name": "Parfums", "category": "Biens de consommation", "description":" ","duty_rate": 30}
        ]

        for item in products:
            Product.objects.create(
                name=item["name"],
                category=category_objs[item["category"]],
                description=item["description"]
            )

        print(f"{len(products)} produits créés.")



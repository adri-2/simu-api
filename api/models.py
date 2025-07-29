# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

class User(AbstractUser):
    """
    Modèle d'utilisateur personnalisé.
    Utilise email comme identifiant unique pour l'authentification.
    """
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_professional = models.BooleanField(default=False, help_text="Indique si l'utilisateur est un professionnel ou non.")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # 'username' sera demandé lors de la création de superuser, mais l'auth se fera par email

    def __str__(self):
        return self.email

class TariffSpecies(models.TextChoices):
    """
    Espèces tarifaires basées sur les réglementations douanières.
    """
    NECESSITY_GOODS = 'VG1', 'Biens de 1ère nécessité (5%)'
    RAW_MATERIALS = 'MP', 'Matières premières (10%)'
    INTERMEDIATE_DIVERSE_GOODS = 'BID', 'Biens intermédiaires et divers (20%)'
    CONSUMPTION_GOODS = 'BCC', 'Biens de consommation courante (30%)'

class ProductCategory(models.Model):
    """
    Catégories de produits, comme les chaussures, vêtements, etc.
    Un produit appartient à une catégorie.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description de la catégorie")
    cemac_hs_code_prefix = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Préfixe Code SH CEMAC",
        help_text="Préfixe du code SH (Système Harmonisé) pour cette catégorie, ex: 6403 pour chaussures."
    )

    class Meta:
        verbose_name = "Catégorie de Produit"
        verbose_name_plural = "Catégories de Produits"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Produit spécifique avec son espèce tarifaire et son code SH CEMAC complet.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Nom du produit")
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Catégorie")
    tariff_species = models.CharField(
        max_length=3,
        choices=TariffSpecies.choices,
        default=TariffSpecies.CONSUMPTION_GOODS,
        verbose_name="Espèce tarifaire"
    )
    cemac_hs_code = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="Code SH CEMAC",
        help_text="Code du Système Harmonisé (SH) complet pour le produit (ex: 6403.99.00.00)."
    )
    is_luxury = models.BooleanField(default=False, verbose_name="Produit de luxe")
    is_alcohol_tobacco = models.BooleanField(default=False, verbose_name="Alcool ou Tabac")
    is_vehicle = models.BooleanField(default=False, verbose_name="Véhicule")
    is_phytosanitary = models.BooleanField(default=False, verbose_name="Nécessite Taxe Phytosanitaire")

    class Meta:
        verbose_name = "Produit Douanier"
        verbose_name_plural = "Produits Douaniers"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.cemac_hs_code})"

class Simulation(models.Model):
    """
    Représente une simulation de calcul des coûts douaniers effectuée par un utilisateur.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations', verbose_name="Utilisateur")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produit simulé")
    declared_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valeur Déclarée (VD)")
    transport_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Coût de Transport")
    handling_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Coût de Manutention")
    weight_in_tons = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Poids en Tonnes (pour taxe phytosanitaire)")
    has_niu = models.BooleanField(default=True, verbose_name="Opérateur a un NIU (Numéro d'Identifiant Unique)")
    simulated_at = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de la simulation")
    is_paid = models.BooleanField(default=False, verbose_name="Paiement confirmé")
    payment_confirmation_code = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Code de confirmation de paiement")
    response_email_sent = models.BooleanField(default=False, verbose_name="Email de réponse envoyé")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création",null=True)
    # date_updated = models.DateTimeField(auto_now=True, verbose_name="Date de mise à

    # Champs pour stocker les résultats de la simulation
    customs_value_vd = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valeur en Douane (VD) calculée")
    customs_duty_dd = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Droits de Douane (DD)")
    excise_duty_da = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Droits d'Accise (DA)")
    vat_tva = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="TVA")
    communal_additional_cac = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Centimes Additionnels Communaux (CAC)")
    it_royalty_ri = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Redevance Informatique (RI)")
    community_integration_tci = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Taxe Communautaire d'Intégration (TCI)")
    integration_contribution_cia = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Contribution pour l'Intégration (CIA)")
    ohada_levy_pro = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Prélèvement OHADA (PRO)")
    purchase_prepayment_prd = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Précompte sur Achat (PRD)")
    guce_facilitation_fee = models.DecimalField(max_digits=15, decimal_places=2, default=12500, verbose_name="Frais de Facilitation GUCE")
    phytosanitary_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Taxe Phytosanitaire")
    tel_fee = models.DecimalField(max_digits=15, decimal_places=2, default=10000, verbose_name="Frais TEL")
    total_customs_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Coût total des douanes")

    class Meta:
        verbose_name = "Simulation de Coût Douanier"
        verbose_name_plural = "Simulations de Coûts Douaniers"
        ordering = ['-simulated_at']

    def __str__(self):
        return f"Simulation #{self.id} par {self.user.email} pour {self.product.name}"

    def calculate_customs_cost(self):
        """
        Calcule les différents éléments du coût douanier et met à jour les champs de la simulation.
        Cette méthode centralise la logique de calcul.
        """
        # Détermination de la Valeur en Douane (VD)
        self.customs_value_vd = self.declared_value + self.transport_cost + self.handling_cost

        # Droit de Douane (DD)
        dd_rate_map = {
            TariffSpecies.NECESSITY_GOODS: Decimal(0.05),
            TariffSpecies.RAW_MATERIALS: Decimal(0.10),
            TariffSpecies.INTERMEDIATE_DIVERSE_GOODS: Decimal(0.20),
            TariffSpecies.CONSUMPTION_GOODS: Decimal(0.30),
        }
        dd_rate = dd_rate_map.get(self.product.tariff_species,  Decimal(0))
        self.customs_duty_dd = self.customs_value_vd * dd_rate

        # Droit d'Accise (DA)
        self.excise_duty_da = 0
        base_for_da = self.customs_value_vd + self.customs_duty_dd
        if self.product.is_luxury:
            self.excise_duty_da = base_for_da * Decimal(0.25)
        elif self.product.is_alcohol_tobacco:
            self.excise_duty_da = base_for_da * Decimal(0.25)
        elif self.product.is_vehicle:
            self.excise_duty_da = base_for_da * Decimal(0.125)

        # TVA (17,5%)
        base_for_tva = self.customs_value_vd + self.customs_duty_dd + self.excise_duty_da
        self.vat_tva = base_for_tva *Decimal( 0.175)

        # Centimes Additionnels Communaux (CAC) 10% de la TVA
        self.communal_additional_cac = self.vat_tva * Decimal(0.10)

        # Redevance Informatique (RI) 0,45% de VD
        self.it_royalty_ri = self.customs_value_vd * Decimal(0.0045)

        # Taxe Communautaire d'Intégration (TCI) 0,6% de VD
        self.community_integration_tci = self.customs_value_vd * Decimal(0.006)

        # Contribution pour l'Intégration (CIA) 0,4% de VD
        self.integration_contribution_cia = self.customs_value_vd * Decimal(0.004)

        # Prélèvement OHADA (PRO) 0,05% VD
        self.ohada_levy_pro = self.customs_value_vd * Decimal(0.0005)

        # Précompte sur Achat (PRD)
        self.purchase_prepayment_prd = self.customs_value_vd * (Decimal(0.01) if self.has_niu else Decimal(0.05))

        # Frais de facilitation GUCE
        # Initialisé à 12500 par défaut dans le modèle, pas de calcul ici

        # Taxe phytosanitaire
        self.phytosanitary_tax =  Decimal(0)
        if self.product.is_phytosanitary:
            self.phytosanitary_tax = self.weight_in_tons * 50

        # TEL (Taxe d'Enlèvement Local)
        # Initialisé à 10000 par défaut dans le modèle, pas de calcul ici

        # Coût de douane import total
        self.total_customs_cost = sum([
            self.customs_value_vd, # La VD est incluse dans la somme pour obtenir le coût total à l'import
            self.customs_duty_dd,
            self.excise_duty_da,
            self.vat_tva,
            self.communal_additional_cac,
            self.it_royalty_ri,
            self.community_integration_tci,
            self.integration_contribution_cia,
            self.ohada_levy_pro,
            self.purchase_prepayment_prd,
            self.guce_facilitation_fee,
            self.phytosanitary_tax,
            self.tel_fee,
        ])
        return self.total_customs_cost

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour s'assurer que les coûts sont calculés
        avant la sauvegarde.
        """
        self.calculate_customs_cost()
        super().save(*args, **kwargs)


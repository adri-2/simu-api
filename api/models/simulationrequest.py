from django.db import models
from decimal import Decimal
from .product import Product
from .users import UserInfo


class SimulationHistorique(models.Manager):
    
    def get_all_simulation(self,user):
        simulation_historique = ImportSimulation.objects.filter(user=user)
        
        return simulation_historique

class ImportSimulation(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.PROTECT ,null=True)
    country_of_origin = models.CharField(max_length=100)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='simulations')
    value_cif = models.DecimalField(max_digits=12, decimal_places=2, help_text="Valeur CIF ou valeur en douane (VD)")
    
    TRANSPORT_CHOICES = [
        ('maritime', 'Maritime'),
        ('aerien', 'Aérien'),
        ('terrestre', 'Terrestre'),
    ]
    moyen_transport = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    value_fret = models.DecimalField(max_digits=12, decimal_places=2, help_text="Coût du transport international (FRET)")

    is_origin_cemac = models.BooleanField(default=True, help_text="Exonération du DD si origine CEMAC")

    total_duties = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), help_text="Total des droits et taxes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = SimulationHistorique()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Nécessaire pour avoir un ID si nouvel objet

        # Calculs des taxes
        dd = Decimal(0) if self.is_origin_cemac else self.value_cif * (self.product_name.category.duty_rate / 100)
        da = Decimal(0)  # Peut être calculé si nécessaire
        tva = dd * Decimal('0.175')
        cac = tva * Decimal('0.10')
        pct = Decimal(0)
        dao = Decimal(0)
        ri = self.value_cif * Decimal('0.45')
        tci = self.value_cif * Decimal('0.6')
        cia = self.value_cif * Decimal('0.4')
        ohada = Decimal(0)
        prd = self.value_cif * Decimal('0.01')
        taxe_phytosanitaire = Decimal('50')
        guce = Decimal('12500')
        tel = Decimal('10000')

        total = sum([
            dd, da, tva, cac, pct, dao,
            ri, tci, cia, ohada, prd,
            taxe_phytosanitaire, guce, tel
        ])

        # Créer ou mettre à jour le détail des taxes
        breakdown, _ = DutiesBreakdown.objects.get_or_create(simulation=self)
        breakdown.dd = dd
        breakdown.da = da
        breakdown.tva = tva
        breakdown.cac = cac
        breakdown.pct = pct
        breakdown.dao = dao
        breakdown.ri = ri
        breakdown.tci = tci
        breakdown.cia = cia
        breakdown.ohada = ohada
        breakdown.prd = prd
        breakdown.taxe_phytosanitaire = taxe_phytosanitaire
        breakdown.save()

        self.total_duties = total
        super().save(update_fields=["total_duties"])

    def get_total_import_cost(self):
        return self.value_cif + self.value_fret + self.total_duties

    def __str__(self):
        return f"{self.product_name} - {self.created_at.date()}"

class DutiesBreakdown(models.Model):
    simulation = models.OneToOneField(ImportSimulation, on_delete=models.CASCADE, related_name='duties_detail')

    dd = models.DecimalField("Droit de Douane", max_digits=10, decimal_places=2, default=0)
    da = models.DecimalField("Droit d'Accise", max_digits=10, decimal_places=2, default=0)
    tva = models.DecimalField("TVA", max_digits=10, decimal_places=2, default=0)
    cac = models.DecimalField("CAC", max_digits=10, decimal_places=2, default=0)
    pct = models.DecimalField("PCT", max_digits=10, decimal_places=2, default=0)
    dao = models.DecimalField("DAO", max_digits=10, decimal_places=2, default=0)
    ri = models.DecimalField("Redevence Informatique", max_digits=10, decimal_places=2, default=0)
    tci = models.DecimalField("TCI", max_digits=10, decimal_places=2, default=0)
    cia = models.DecimalField("CIA", max_digits=10, decimal_places=2, default=0)
    ohada = models.DecimalField("Prélèvement OHADA", max_digits=10, decimal_places=2, default=0)
    prd = models.DecimalField("PRD", max_digits=10, decimal_places=2, default=0)
    taxe_phytosanitaire = models.DecimalField("Taxe Phytosanitaire", max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Détails taxes pour la simulation #{self.simulation.id}"

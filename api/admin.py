# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,  ProductCategory, Product, Simulation

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Administration personnalisée pour le modèle User.
    Affiche les champs spécifiques et permet la gestion.
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'is_professional')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'is_professional')}),
    )
    list_display = ('email', 'username', 'is_staff', 'is_professional', 'date_joined')
    search_fields = ('email', 'username', 'full_name')

# @admin.register(ImporterProfile)
# class ImporterProfileAdmin(admin.ModelAdmin):
#     """
#     Administration pour le modèle ImporterProfile.
#     """
#     list_display = ('user', 'full_name', 'legal_personality')
#     search_fields = ('user__email', 'full_name')
#     list_filter = ('legal_personality',)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle ProductCategory.
    """
    list_display = ('name', 'cemac_hs_code_prefix')
    search_fields = ('name', 'cemac_hs_code_prefix')
    prepopulated_fields = {'cemac_hs_code_prefix': ('name',)} # Rempli auto le slug

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Product.
    Permet de gérer les codes SH et les espèces tarifaires.
    """
    list_display = (
        'name', 'category', 'tariff_species', 'cemac_hs_code',
        'is_luxury', 'is_alcohol_tobacco', 'is_vehicle', 'is_phytosanitary'
    )
    list_filter = ('category', 'tariff_species', 'is_luxury', 'is_alcohol_tobacco', 'is_vehicle', 'is_phytosanitary')
    search_fields = ('name', 'cemac_hs_code', 'category__name')
    raw_id_fields = ('category',) # Pour les FK, si beaucoup d'objets, mieux d'utiliser raw_id_fields

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Simulation.
    Affiche les détails de la simulation et les résultats.
    """
    list_display = (
        'user', 'product', 'simulated_at', 'total_customs_cost',
        'is_paid', 'payment_confirmation_code', 'response_email_sent'
    )
    list_filter = ('is_paid', 'response_email_sent', 'simulated_at', 'product__category')
    search_fields = (
        'user__email', 'product__name', 'product__cemac_hs_code',
        'payment_confirmation_code'
    )
    readonly_fields = (
        'customs_value_vd', 'customs_duty_dd', 'excise_duty_da', 'vat_tva',
        'communal_additional_cac', 'it_royalty_ri', 'community_integration_tci',
        'integration_contribution_cia', 'ohada_levy_pro', 'purchase_prepayment_prd',
        'guce_facilitation_fee', 'phytosanitary_tax', 'tel_fee', 'total_customs_cost'
    )
    date_hierarchy = 'simulated_at' # Permet de naviguer par date
    raw_id_fields = ('user', 'product')
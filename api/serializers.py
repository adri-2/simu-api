# core/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ProductCategory, Product, Simulation,  TariffSpecies

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'enregistrement d'un nouvel utilisateur.
    Crée automatiquement username à partir de first_name + last_name.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'email', 'password', 'password2',
            'phone_number', 'first_name', 'last_name',
            'is_professional'  # lecture seule
        )
        extra_kwargs = {
            'is_professional': {'read_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # Création automatique du username
        first_name = validated_data.get('first_name', '').strip()
        last_name = validated_data.get('last_name', '').strip()
        username = (first_name +' ' +last_name).lower()

        user = User(
            email=validated_data['email'],
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=validated_data.get('phone_number'),
            is_professional=False
        )
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pour la consultation et la mise à jour du profil utilisateur.
    """
    # importer_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone_number','first_name','last_name', 'is_professional', 'date_joined', 'last_login', )
        read_only_fields = ('email', 'username', 'is_professional', 'date_joined', 'last_login')

    # def get_importer_profile(self, obj):
    #     """
    #     Retourne les détails du profil importateur si existant.
    #     """
    #     if hasattr(obj, 'importer_profile'):
    #         return ImporterProfileSerializer(obj.importer_profile).data
    #     return None

# class ImporterProfileSerializer(serializers.ModelSerializer):
#     """
#     Serializer pour le profil importateur.
#     """
#     class Meta:
#         model = ImporterProfile
#         fields = ('full_name', 'legal_personality')

class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle ProductCategory.
    """
    class Meta:
        model = ProductCategory
        fields = '__all__'
        read_only_fields = ('cemac_hs_code_prefix',) # Le préfixe est géré par l'admin

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Product.
    Affiche le nom de la catégorie au lieu de son ID.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    tariff_species_display = serializers.CharField(source='get_tariff_species_display', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'category_name', 'tariff_species',
            'tariff_species_display', 'cemac_hs_code', 'is_luxury',
            'is_alcohol_tobacco', 'is_vehicle', 'is_phytosanitary'
        )
        read_only_fields = ('cemac_hs_code', 'tariff_species') # Géré par l'admin pour l'exactitude

class SimulationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création d'une nouvelle simulation.
    Prend les entrées de l'utilisateur et les valide.
    """
    class Meta:
        model = Simulation
        fields = (
            'product', 'declared_value', 'transport_cost', 'handling_cost',
            'weight_in_tons', 'has_niu'
        )
        extra_kwargs = {
            'declared_value': {'min_value': 0},
            'transport_cost': {'min_value': 0},
            'handling_cost': {'min_value': 0},
            'weight_in_tons': {'min_value': 0},
        }

    def validate(self, data):
        """
        Valide que les coûts ne sont pas négatifs et que le produit existe.
        """
        if data['declared_value'] < 0:
            raise serializers.ValidationError({"declared_value": "La valeur déclarée ne peut pas être négative."})
        if data['transport_cost'] < 0:
            raise serializers.ValidationError({"transport_cost": "Le coût de transport ne peut pas être négatif."})
        if data['handling_cost'] < 0:
            raise serializers.ValidationError({"handling_cost": "Le coût de manutention ne peut pas être négatif."})
        if data['weight_in_tons'] < 0:
            raise serializers.ValidationError({"weight_in_tons": "Le poids ne peut pas être négatif."})

        # S'assurer que le produit existe
        product_id = data.get('product')
        if not product_id or not Product.objects.filter(id=product_id.id).exists():
            raise serializers.ValidationError({"product": "Le produit spécifié n'existe pas."})

        return data

class SimulationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer pour afficher les détails complets d'une simulation, y compris les résultats.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_hs_code = serializers.CharField(source='product.cemac_hs_code', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Simulation
        fields = '__all__'
        read_only_fields = (
            'user', 'simulated_at', 'is_paid', 'payment_confirmation_code',
            'response_email_sent', 'customs_value_vd', 'customs_duty_dd',
            'excise_duty_da', 'vat_tva', 'communal_additional_cac',
            'it_royalty_ri', 'community_integration_tci', 'integration_contribution_cia',
            'ohada_levy_pro', 'purchase_prepayment_prd', 'guce_facilitation_fee',
            'phytosanitary_tax', 'tel_fee', 'total_customs_cost',
            'product_name', 'product_hs_code', 'user_email'
        )

# Serializer pour la confirmation de paiement
class PaymentConfirmationSerializer(serializers.Serializer):
    """
    Serializer pour la confirmation de paiement d'une simulation.
    """
    payment_confirmation_code = serializers.CharField(required=True, max_length=50)

    def validate_payment_confirmation_code(self, value):
        """
        Valide que le code de confirmation est unique si il est fourni.
        """
        if Simulation.objects.filter(payment_confirmation_code=value).exists():
            raise serializers.ValidationError("Ce code de confirmation a déjà été utilisé.")
        return value
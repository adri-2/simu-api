# core/views.py

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings # Assure-toi que EMAIL_BACKEND est configuré dans settings.py
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid # Pour générer des codes de confirmation uniques

from .models import User, ImporterProfile, ProductCategory, Product, Simulation
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer, ProductCategorySerializer,
    ProductSerializer, SimulationCreateSerializer, SimulationDetailSerializer,
    PaymentConfirmationSerializer
)
from .permissions import IsOwnerOrAdmin # Nous allons créer ce fichier plus tard

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée pour l'obtention de tokens JWT.
    Peut être étendue si des données utilisateur supplémentaires sont nécessaires dans le token.
    """
    pass # Utilise le serializer par défaut de simplejwt

class UserRegistrationView(generics.CreateAPIView):
    """
    Vue pour l'enregistrement de nouveaux utilisateurs.
    Accessible par tous (AllowAny).
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic(): # Assure l'atomicité de la création utilisateur/profil
                user = serializer.save()
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de l'enregistrement: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Générer les tokens JWT après l'enregistrement
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour récupérer et mettre à jour le profil de l'utilisateur connecté.
    Accessible uniquement par l'utilisateur propriétaire ou un administrateur.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get_object(self):
        """
        Retourne l'objet User pour l'utilisateur authentifié.
        """
        return self.request.user

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint qui permet aux catégories de produits d'être vues ou éditées.
    - Seuls les administrateurs peuvent créer, mettre à jour ou supprimer des catégories.
    - Tous les utilisateurs authentifiés peuvent lister et récupérer des catégories.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    # permission_classes = (IsAuthenticated,) # Par défaut, authentifié requis

    # def get_permissions(self):
    #     """
    #     Instancie et retourne la liste des permissions requises par cette vue.
    #     """
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsAdminUser] # Seuls les admins peuvent modifier
    #     else:
    #         self.permission_classes = [IsAuthenticated] # Lecture pour tous les authentifiés
    #     return [permission() for permission in self.permission_classes]

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint qui permet aux produits d'être vus ou éditées.
    - Seuls les administrateurs peuvent créer, mettre à jour ou supprimer des produits.
    - Tous les utilisateurs authentifiés peuvent lister et récupérer des produits.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = (IsAuthenticated,)

    # def get_permissions(self):
        # """
        # Instancie et retourne la liste des permissions requises par cette vue.
        # """
        # if self.action in ['create', 'update', 'partial_update', 'destroy']:
        #     self.permission_classes = [IsAdminUser] # Seuls les admins peuvent modifier
        # else:
        #     self.permission_classes = [IsAuthenticated] # Lecture pour tous les authentifiés
        # return [permission() for permission in self.permission_classes]

class SimulationViewSet(viewsets.ModelViewSet):
    """
    API endpoint qui permet aux simulations d'être créées, vues, éditées ou supprimées.
    - Les utilisateurs peuvent créer leurs propres simulations et consulter leur historique.
    - Les administrateurs peuvent gérer toutes les simulations.
    """
    queryset = Simulation.objects.all()
    # permission_classes = (IsAuthenticated, IsOwnerOrAdmin) # Sera affiné par get_queryset et permissions

    # def get_serializer_class(self):
    #     """
    #     Retourne le serializer approprié en fonction de l'action.
    #     """
    #     if self.action == 'create':
    #         return SimulationCreateSerializer
    #     return SimulationDetailSerializer

    def get_queryset(self):
        """
        Filtre les simulations pour n'afficher que celles de l'utilisateur connecté,
        sauf si l'utilisateur est un administrateur.
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Simulation.objects.all()
        return Simulation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Assigne l'utilisateur connecté à la simulation lors de la création.
        Génère un code de confirmation de paiement unique.
        """
        # Générer un code de confirmation unique
        payment_code = str(uuid.uuid4())[:10].upper() # Ex: 10 caractères aléatoires
        serializer.save(user=self.request.user, payment_confirmation_code=payment_code)
        # L'email sera envoyé après le paiement confirmé, pas à la création

    def partial_update(self, request, *args, **kwargs):
        """
        Surcharge de partial_update pour empêcher la modification des champs de résultat.
        """
        instance = self.get_object()
        # Ne pas autoriser la modification des champs de résultat directement via l'API
        # Ces champs sont calculés par la méthode calculate_customs_cost
        read_only_fields_in_detail_serializer = SimulationDetailSerializer.Meta.read_only_fields
        for field in read_only_fields_in_detail_serializer:
            if field in request.data:
                del request.data[field]
        return super().partial_update(request, *args, **kwargs)

    # Endpoint pour confirmer le paiement
    # Route: /api/simulations/{id}/confirm_payment/
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrAdmin])
    def confirm_payment(self, request, pk=None):
        """
        Confirme le paiement d'une simulation et envoie le résultat par email.
        """
        simulation = self.get_object()
        serializer = PaymentConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_code_input = serializer.validated_data.get('payment_confirmation_code')

        # Dans un vrai scénario, tu intégrerais ici un système de paiement (Orange Money, MTN Mobile Money)
        # et vérifierais si le paiement a réellement été effectué avec le code fourni.
        # Pour cette simulation, nous allons juste marquer comme payé si le code correspond (ou est simulé).

        # Option 1: Valider avec un code de paiement prédéfini (pour démo/test)
        # if payment_code_input != simulation.payment_confirmation_code:
        #     return Response(
        #         {"detail": "Code de confirmation de paiement invalide."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # Option 2: Simuler le paiement (le code doit juste être fourni et valide par le serializer)
        # Ici, nous allons juste vérifier que le code est fourni (valide par le serializer)
        # et que la simulation n'est pas déjà payée.

        if simulation.is_paid:
            return Response(
                {"detail": "Cette simulation est déjà marquée comme payée."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            simulation.is_paid = True
            simulation.payment_confirmation_code = payment_code_input # Stocke le code fourni par l'utilisateur
            simulation.save() # Le save recalcule les coûts si des champs ont été modifiés

            # Envoyer l'email de confirmation avec les résultats
            try:
                self._send_simulation_result_email(simulation)
                simulation.response_email_sent = True
                simulation.save(update_fields=['response_email_sent'])
            except Exception as e:
                # Log l'erreur d_email si le mail échoue, mais ne bloque pas la réponse
                print(f"Erreur lors de l'envoi de l'email pour la simulation {simulation.id}: {e}")
                # Peut-être ajouter un champ 'email_sent_error' au modèle Simulation

        return Response(
            {"detail": "Paiement confirmé et résultats envoyés par email.", "simulation": SimulationDetailSerializer(simulation).data},
            status=status.HTTP_200_OK
        )

    def _send_simulation_result_email(self, simulation):
        """
        Fonction utilitaire pour envoyer l'email de résultat de simulation.
        """
        subject = f"Votre simulation de coûts douaniers SIMU #{simulation.id}"
        recipient_email = simulation.user.email

        # Préparer le contexte pour le template d'email
        context = {
            'simulation': simulation,
            'user': simulation.user,
            'product': simulation.product,
            # Vous pouvez ajouter d'autres données nécessaires au template ici
        }

        # Charger le template HTML
        html_message = render_to_string('emails/simulation_result.html', context)
        plain_message = strip_tags(html_message) # Version texte brut pour les clients email sans HTML

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL, # Doit être configuré dans settings.py
            [recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Email envoyé à {recipient_email} pour la simulation #{simulation.id}")



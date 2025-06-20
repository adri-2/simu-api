from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur non trouvé avec cet email")

        if not user.check_password(password):
            raise serializers.ValidationError("Mot de passe incorrect")

        if not user.is_active:
            raise serializers.ValidationError("Utilisateur inactif")

        data = super().validate({
            'username': user.username,  # trick: pass username to original validate
            'password': password
        })

        return data


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

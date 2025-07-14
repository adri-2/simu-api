# core/permissions.py
# Crée ce fichier pour les permissions personnalisées

from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission personnalisée pour permettre l'accès uniquement au propriétaire de l'objet
    ou à un administrateur (is_staff ou is_superuser).
    """

    def has_object_permission(self, request, view, obj):
        # Les permissions de lecture sont autorisées pour tout utilisateur authentifié
        # si l'objet est une simulation liée à lui. L'admin peut tout lire.
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user or request.user.is_staff or request.user.is_superuser

        # Les permissions d'écriture ne sont autorisées qu'au propriétaire de l'objet ou à un administrateur.
        return obj.user == request.user or request.user.is_staff or request.user.is_superuser





# from rest_framework.permissions import BasePermission

# class IsAdminAuthenticated(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
    


# class IsOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.user == request.user
    
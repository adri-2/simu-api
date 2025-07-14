# Documentation API de la Plateforme SIMU

Bienvenue dans la documentation de l'API de la plateforme SIMU, votre outil de simulation de calcul des coûts douaniers dans la zone CEMAC.  
Cette API permet aux utilisateurs de s'enregistrer, de gérer leur profil, de consulter des informations sur les produits et catégories, de réaliser des simulations de coûts douaniers, et de consulter l'historique de leurs simulations.

---

## 1. URL de Base de l'API

Toutes les requêtes API doivent être préfixées par l'URL de base :  
`https://votre-domaine.com/api/`  
_(Remplacez votre-domaine.com par l'URL de votre déploiement)_

---

## 2. Authentification

L'API utilise l'authentification basée sur les tokens JWT via `djangorestframework-simplejwt`.  
Inclure le token d'accès dans l'en-tête `Authorization` :

```
Authorization: Bearer <YOUR_ACCESS_TOKEN>
```

### 2.1. Obtenir un Token JWT

- **Endpoint** : `/api/auth/token/`
- **Méthode** : `POST`
- **Authentification** : Aucune (AllowAny)

**Corps de la requête (JSON)** :

```json
{
    "email": "votre_email@example.com",
    "password": "votre_mot_de_passe"
}
```

**Réponse (Succès - 200 OK)** :

```json
{
    "refresh": "eyJ0eXAiOiJKV1Qi...",
    "access": "eyJ0eXAiOiJKV1Qi..."
}
```

**Réponse (Erreur - 401 Unauthorized)** :

```json
{
    "detail": "No active account found with the given credentials"
}
```

### 2.2. Rafraîchir un Token JWT

- **Endpoint** : `/api/auth/token/refresh/`
- **Méthode** : `POST`
- **Authentification** : Aucune (AllowAny)

**Corps de la requête (JSON)** :

```json
{
    "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

**Réponse (Succès - 200 OK)** :

```json
{
    "access": "eyJ0eXAiOiJKV1Qi..."
}
```

### 2.3. Vérifier la Validité d'un Token JWT

- **Endpoint** : `/api/auth/token/verify/`
- **Méthode** : `POST`
- **Authentification** : Aucune (AllowAny)

**Corps de la requête (JSON)** :

```json
{
    "token": "eyJ0eXAiOiJKV1Qi..."
}
```

**Réponse (Succès - 200 OK)** : (Corps vide si valide)  
**Réponse (Erreur - 401 Unauthorized)** :

```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

---

## 3. Gestion des Erreurs

L'API retourne des codes de statut HTTP standard.  
Les erreurs sont accompagnées d'un corps de réponse JSON expliquant le problème.

- **2xx (Succès)**

  - `200 OK` : Requête réussie.
  - `201 Created` : Ressource créée avec succès.
  - `204 No Content` : Requête réussie, aucune information à retourner.

- **4xx (Erreur Client)**

  - `400 Bad Request`
    ```json
    { "field_name": ["Message d'erreur spécifique au champ."] }
    ```
  - `401 Unauthorized`
    ```json
    { "detail": "Authentication credentials were not provided." }
    ```
  - `403 Forbidden`
    ```json
    { "detail": "You do not have permission to perform this action." }
    ```
  - `404 Not Found`
    ```json
    { "detail": "Not found." }
    ```

- **5xx (Erreur Serveur)**
  - `500 Internal Server Error` : Erreur générique du serveur.

---

## 4. Pagination

Les endpoints qui retournent des listes de ressources sont paginés.

- **Paramètres de requête** :
  - `?page=<num>` : Numéro de la page à récupérer.
  - `?page_size=<num>` : Nombre d'éléments par page.

**Exemple de réponse paginée** :

```json
{
    "count": 25,
    "next": "https://votre-domaine.com/api/products/?page=2",
    "previous": null,
    "results": [
        { /* ... données du produit ... */ }
    ]
}
```

---

## 5. Endpoints de l'API

### 5.1. Gestion des Utilisateurs et Profils

#### 5.1.1. Enregistrement d'un Nouvel Utilisateur

- **Endpoint** : `/api/auth/register/`
- **Méthode** : `POST`
- **Authentification** : Aucune (AllowAny)

**Corps de la requête (JSON)** :

```json
{
    "email": "nouvel_utilisateur@example.com",
    "username": "nouvel_utilisateur",
    "password": "MotDePasseFort123!",
    "password2": "MotDePasseFort123!",
    "full_name": "Nom Complet de l'Utilisateur",
    "legal_personality": "PF",
    "phone_number": "00237699000000"
}
```

**Réponse (Succès - 201 Created)** :

```json
{
    "user": {
        "id": 1,
        "email": "nouvel_utilisateur@example.com",
        "username": "nouvel_utilisateur",
        "phone_number": "00237699000000",
        "is_professional": false,
        "date_joined": "2023-10-27T10:00:00Z",
        "last_login": null,
        "importer_profile": {
            "full_name": "Nom Complet de l'Utilisateur",
            "legal_personality": "PF"
        }
    },
    "access": "eyJ0eXAiOiJKV1Qi...",
    "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

**Réponse (Erreur - 400 Bad Request)** :

```json
{
    "password": ["Les deux mots de passe ne correspondent pas."],
    "email": ["Cet email est déjà utilisé."],
    "username": ["Ce champ est obligatoire."]
}
```

#### 5.1.2. Récupérer et Mettre à Jour le Profil Utilisateur

- **Endpoint** : `/api/profile/`
- **Méthode** : `GET`, `PATCH`
- **Authentification** : Requise (IsAuthenticated, IsOwnerOrAdmin)

**GET** : Récupère les détails du profil  
**PATCH** : Met à jour certains champs

**Corps de la requête (PATCH, JSON partiel)** :

```json
{
    "phone_number": "00237678901234",
    "importer_profile": {
        "full_name": "Nouveau Nom Complet"
    }
}
```

_Note : Les champs email, username, is_professional, date_joined, last_login sont en lecture seule._

---

### 5.2. Gestion des Catégories de Produits

#### 5.2.1. Lister les Catégories de Produits

- **Endpoint** : `/api/product-categories/`
- **Méthode** : `GET`
- **Authentification** : Requise (IsAuthenticated)

#### 5.2.2. Récupérer une Catégorie de Produit

- **Endpoint** : `/api/product-categories/{id}/`
- **Méthode** : `GET`
- **Authentification** : Requise (IsAuthenticated)

#### 5.2.3. Créer une Catégorie de Produit

- **Endpoint** : `/api/product-categories/`
- **Méthode** : `POST`
- **Authentification** : Requise (IsAdminUser)

#### 5.2.4. Mettre à Jour une Catégorie de Produit

- **Endpoint** : `/api/product-categories/{id}/`
- **Méthode** : `PUT`, `PATCH`
- **Authentification** : Requise (IsAdminUser)

#### 5.2.5. Supprimer une Catégorie de Produit

- **Endpoint** : `/api/product-categories/{id}/`
- **Méthode** : `DELETE`
- **Authentification** : Requise (IsAdminUser)

---

### 5.3. Gestion des Produits Douaniers

#### 5.3.1. Lister les Produits Douaniers

- **Endpoint** : `/api/products/`
- **Méthode** : `GET`
- **Authentification** : Requise (IsAuthenticated)

#### 5.3.2. Récupérer un Produit Douanier

- **Endpoint** : `/api/products/{id}/`
- **Méthode** : `GET`
- **Authentification** : Requise (IsAuthenticated)

#### 5.3.3. Créer un Produit Douanier

- **Endpoint** : `/api/products/`
- **Méthode** : `POST`
- **Authentification** : Requise (IsAdminUser)

#### 5.3.4. Mettre à Jour un Produit Douanier

- **Endpoint** : `/api/products/{id}/`
- **Méthode** : `PUT`, `PATCH`
- **Authentification** : Requise (IsAdminUser)

_Note : Les champs cemac_hs_code et tariff_species sont en lecture seule._

#### 5.3.5. Supprimer un Produit Douanier

- **Endpoint** : `/api/products/{id}/`
- **Méthode** : `DELETE`
- **Authentification** : Requise (IsAdminUser)

---

### 5.4. Gestion des Simulations de Coûts Douaniers

#### 5.4.1. Créer une Simulation

- **Endpoint** : `/api/simulations/`
- **Méthode** : `POST`
- **Authentification** : Requise (IsAuthenticated)

#### 5.4.2. Lister l'Historique des Simulations

- **Endpoint** : `/api/simulations/`
- **Méthode** : `GET`
- **Authentification** : Requise (IsAuthenticated)

#### 5.4.3. Récupérer les Détails d'une Simulation

- **Endpoint** : `/api/simulations/{id}/`
- **Méthode** : `GET`
- **Authentification** : Requise (IsAuthenticated, IsOwnerOrAdmin)

#### 5.4.4. Confirmer le Paiement d'une Simulation

- **Endpoint** : `/api/simulations/{id}/confirm_payment/`
- **Méthode** : `POST`
- **Authentification** : Requise (IsAuthenticated, IsOwnerOrAdmin)

#### 5.4.5. Mettre à Jour une Simulation (Partiel)

- **Endpoint** : `/api/simulations/{id}/`
- **Méthode** : `PATCH`
- **Authentification** : Requise (IsAuthenticated, IsOwnerOrAdmin)

_Note : Les champs de résultats, is_paid, payment_confirmation_code, response_email_sent sont en lecture seule._

#### 5.4.6. Supprimer une Simulation

- **Endpoint** : `/api/simulations/{id}/`
- **Méthode** : `DELETE`
- **Authentification** : Requise (IsAuthenticated, IsOwnerOrAdmin)

---

## 6. Bonnes Pratiques de Développement

- **Tests Unitaires** : Utilisez `APITestCase` pour tester les vues et `TestCase` pour les modèles et serializers.
- **Sécurité** : Ne stockez jamais de clés API ou de secrets dans le code. Utilisez des variables d'environnement. Servez l'API via HTTPS.
- **Journalisation (Logging)** : Implémentez une journalisation adéquate.
- **Gestion des Dépendances** : Utilisez un fichier `requirements.txt`.
- **Versionnement de l'API** : Envisagez de versionner votre API (`/api/v1/`, `/api/v2/`).

---

Cette documentation fournit toutes les informations nécessaires pour interagir avec l'API SIMU.  
Mettez-la à jour au fur et à mesure de l'évolution de votre projet !

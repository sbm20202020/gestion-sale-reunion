# Gestion de Salle de Réunion

Application complète de gestion de salles de réunion avec **React**, **Django REST Framework** et **PostgreSQL**.

## Fonctionnalités

- Réservation de salles (création, modification, annulation)
- Détection automatique de conflits de réservation
- Réservations récurrentes (quotidienne, hebdomadaire, mensuelle)
- Gestion des équipements et association aux salles
- Authentification JWT (inscription/connexion)
- Rôles utilisateur standard / administrateur
- Visualisation calendrier (jour, semaine, mois)
- Filtrage par salle, période et utilisateur

## Structure du projet

```
gestion-sale-reunion/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   ├── rooms/
│   ├── reservations/
│   └── users/
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
├── docker-compose.yml
├── .env.example
└── README.md
```

## Installation rapide (Docker)

1. Copier les variables d'environnement :
   ```bash
   cp .env.example .env
   ```
2. Lancer les services :
   ```bash
   docker compose up --build
   ```
3. Appliquer les migrations et charger des données démo :
   ```bash
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py seed_demo
   ```

Accès:
- Frontend: http://localhost:5173
- API Backend: http://localhost:8000/api
- Admin Django: http://localhost:8000/admin

## Installation manuelle

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Endpoints API principaux

- `POST /api/auth/register/` : inscription
- `POST /api/auth/token/` : connexion JWT
- `POST /api/auth/token/refresh/` : refresh token
- `GET/PATCH /api/auth/profile/` : profil utilisateur
- `GET/POST /api/rooms/rooms/` : salles
- `GET/POST /api/rooms/equipments/` : équipements
- `GET/POST /api/reservations/reservations/` : réservations

### Gestion des séries récurrentes

- Modifier toute la série : `PATCH /api/reservations/reservations/{id}/?scope=series`
- Supprimer toute la série : `DELETE /api/reservations/reservations/{id}/?scope=series`

## Données de démonstration

Commande incluse:

```bash
python manage.py seed_demo
```

Crée:
- admin: `admin/admin12345`
- utilisateur: `demo/demo12345`
- salles, équipements et une réservation exemple

## Tests

```bash
cd backend
USE_SQLITE_FOR_TESTS=true python manage.py test reservations
```


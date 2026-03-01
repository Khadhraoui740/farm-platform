# 🚜 Farm Platform

Système complet de gestion de ferme avec suivi de prix, eau, électricité, plantes et gestion d'annonces.

**Stack:** FastAPI (backend) + SQLite (BD) + Expo (mobile)

---

## 📋 Fonctionnalités

### ✅ Module Ferme
- Gestion des parcelles et cultures
- Suivi des semis et récoltes
- Gestion du stock d'intrants
- Tâches équipe

### 📊 Module Marché
- Suivi des prix (engrais, semences, carburant, produits)
- Historique des variations
- Alertes prix configurables

### 💧 Module Ressources
- Consommation d'eau (compteurs/jour)
- Production électrique (solaire/groupe)
- Coûts et rendement

### 📱 Application Mobile
- Saisie hors ligne
- Photos/captures
- Scan QR parcelle
- Notifications d'alertes

---

## 🚀 Démarrage Rapide

### Backend Local

#### Prérequis
- Python 3.8+
- pip

#### Installation
```bash
cd backend
pip install -r requirements.txt
```

#### Lancer le serveur
```bash
python main.py
```

✓ API disponible sur `http://localhost:8000`
✓ Swagger docs: `http://localhost:8000/docs`
✓ Base SQLite créée automatiquement: `farm.db`

#### Endpoints clés

**Plantes**
```bash
GET    /api/plants        # Lister toutes les plantes
POST   /api/plants        # Ajouter une plante
GET    /api/plants/{id}   # Détail plante
PUT    /api/plants/{id}   # Modifier
DELETE /api/plants/{id}   # Supprimer
```

**Prix Marchandises**
```bash
GET    /api/prices            # Historique prix
POST   /api/prices            # Ajouter prix
GET    /api/prices/alert      # Vérifier alertes
GET    /api/prices/{item_id}  # Prix d'un item
```

**Consommation Eau**
```bash
GET    /api/water              # Historique eau
POST   /api/water              # Enregistrer consommation
GET    /api/water/usage/daily  # Usage quotidien
```

**Électricité**
```bash
GET    /api/electricity            # Historique électricité
POST   /api/electricity            # Enregistrer production/consommation
GET    /api/electricity/stats      # Statistiques
```

**Tâches Ferme**
```bash
GET    /api/tasks              # Lister les tâches
POST   /api/tasks              # Créer tâche
PUT    /api/tasks/{id}/status  # Mettre à jour statut
```

**Dashboard**
```bash
GET    /api/dashboard  # Résumé complet KPI
```

#### Exemple de requête
```bash
# Ajouter une plante
curl -X POST http://localhost:8000/api/plants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Blé",
    "variety": "Variété locale",
    "planting_date": "2026-03-01",
    "parcelle": "Parcelle 1",
    "surface_ha": 5.5
  }'
```

---

## 📱 Application Mobile (Expo)

### Prérequis
- Node.js 16+
- Expo CLI: `npm install -g expo-cli`

### Installation
```bash
cd mobile
npm install
```

### Lancer l'app
```bash
expo start
```

Scannez le QR code avec :
- **iOS**: Appareil photo (vous redirige vers Expo Go)
- **Android**: Expo Go (application PlayStore)

### Écrans
1. **Dashboard** - KPI temps réel (eau, électricité, prix, plantes)
2. **Prix Marchandises** - Suivi et alertes
3. **Plantes** - Gestion parcelles et cultures
4. **Eau/Électricité** - Consommation et production

---

## 🗄️ Structure Projet

```
farm-platform/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── models.py            # Modèles SQLAlchemy
│   ├── schemas.py           # Schémas Pydantic
│   ├── database.py          # Config BD
│   ├── seed.py              # Données de démo
│   └── requirements.txt     # Dépendances
│
├── mobile/
│   ├── App.js               # Point d'entrée
│   ├── screens/             # Écrans React Native
│   ├── navigation/          # Navigation
│   ├── api/                 # Client API
│   └── package.json         # Dépendances
│
└── README.md               # Ce fichier
```

---

## 🔧 Configuration

### Variables d'environnement (optionnel)

Créer `.env` dans le dossier `backend/`:
```
DATABASE_URL=sqlite:///farm.db
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:3000", "exp://localhost:19000"]
```

---

## 📊 Données de Démo

Au premier démarrage, la base est peuplée avec :
- ✅ 5 plantes (Blé, Maïs, Tomate, Courgette, Salade)
- ✅ 10 entrées de prix marchandises
- ✅ 20 relevés eau (sur 20 jours)
- ✅ 20 relevés électricité (sur 20 jours)
- ✅ 15 tâches ferme

Pour réinitialiser les données :
```bash
# Supprimer la BD existante
rm backend/farm.db

# Redémarrer le serveur (BD recréée)
python backend/main.py
```

---

## 🧪 Tests

### Tester l'API avec curl

```bash
# Vérifier que le serveur répond
curl http://localhost:8000/api/dashboard

# Ajouter un prix
curl -X POST http://localhost:8000/api/prices \
  -H "Content-Type: application/json" \
  -d '{
    "item": "Engrais NPK",
    "category": "engrais",
    "price_per_unit": 450,
    "unit": "kg",
    "date": "2026-03-01",
    "supplier": "Agro-shop local"
  }'

# Enregistrer consommation eau
curl -X POST http://localhost:8000/api/water \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-03-01",
    "amount_liters": 1500,
    "parcelle": "Parcelle 1",
    "notes": "Irrigation main"
  }'
```

---

## 🐳 Docker (optionnel)

### Build
```bash
docker build -t farm-platform-backend ./backend
```

### Run
```bash
docker run -p 8000:8000 farm-platform-backend
```

---

## 📝 API Complète

Swagger automatique: `http://localhost:8000/docs`

Redoc: `http://localhost:8000/redoc`

---

## 🚢 Déploiement

### Heroku
```bash
cd backend
heroku create farm-platform-api
git push heroku main
```

### Railway / Render
Connecter le dépôt GitHub directement (automatique)

### Cloud Run (Google)
```bash
gcloud run deploy farm-platform-api \
  --source . \
  --platform managed \
  --region europe-west1
```

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature: `git checkout -b feature/nom`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/nom`
5. Pull Request

---

## 📞 Support

Problème ? Consultez :
- Swagger docs: `http://localhost:8000/docs`
- Issues GitHub
- Logs serveur: `python backend/main.py`

---

## 📄 Licence

MIT - Libre d'usage personnel et commercial

---

**💡 Prochaines étapes**
- [ ] Authentification utilisateur (JWT)
- [ ] Export données (CSV/PDF)
- [ ] Tableau de bord web (React)
- [ ] Intégration capteurs IoT
- [ ] Alertes SMS/Email
- [ ] Analyses IA (prédictions récolte)

---

**Créé le 01/03/2026** | Farm Platform MVP

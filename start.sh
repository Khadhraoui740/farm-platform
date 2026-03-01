#!/bin/bash

echo ""
echo "========================================"
echo "  🚜 FARM PLATFORM - DÉMARRAGE RAPIDE"
echo "========================================"
echo ""

echo "Que voulez-vous faire ?"
echo "1. Lancer le backend API"
echo "2. Lancer l'app mobile Expo"
echo "3. Lancer les deux (dans des terminals)"
echo "4. Afficher la documentation"
echo ""

read -p "Choisissez (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📡 Démarrage du backend API..."
        echo "Installation des dépendances..."
        
        cd backend
        pip install -q -r requirements.txt
        
        echo ""
        echo "✅ Démarrage du serveur FastAPI..."
        echo "📍 Accédez à : http://localhost:8000/docs"
        echo ""
        
        python main.py
        ;;
    
    2)
        echo ""
        echo "📱 Démarrage de l'app mobile..."
        
        if [ ! -d "mobile/node_modules" ]; then
            echo "Installation des dépendances..."
            cd mobile
            npm install
        else
            cd mobile
        fi
        
        echo ""
        echo "✅ Lancement d'Expo..."
        echo "📍 Scannez le QR code avec Expo Go"
        echo ""
        
        npm start
        ;;
    
    3)
        echo ""
        echo "🚀 Démarrage des deux services..."
        echo ""
        
        echo "Terminal 1: Lancement du backend..."
        (cd backend && pip install -q -r requirements.txt && python main.py) &
        
        sleep 3
        
        echo "Terminal 2: Lancement de l'app mobile..."
        (cd mobile && npm install -q && npm start) &
        
        echo ""
        echo "✅ Les deux services se lancent !"
        echo "   - Backend: http://localhost:8000/docs"
        echo "   - Mobile: Scannez le QR code Expo"
        ;;
    
    4)
        echo ""
        echo "📖 DOCUMENTATION"
        echo "==============="
        echo ""
        
        echo "🔹 Endpoints API: http://localhost:8000/docs"
        echo "🔹 README détaillé:"
        echo ""
        
        if [ -f "README.md" ]; then
            cat README.md | less
        else
            echo "README.md non trouvé"
        fi
        ;;
    
    *)
        echo "Choix invalide"
        ;;
esac

echo ""

# Démarrage Rapide - Farm Platform

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  🚜 FARM PLATFORM - DÉMARRAGE RAPIDE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

# Menu
Write-Host "Que voulez-vous faire ?" -ForegroundColor Yellow
Write-Host "1. Lancer le backend API"
Write-Host "2. Lancer l'app mobile Expo"
Write-Host "3. Lancer les deux (dans des terminals)"
Write-Host "4. Afficher la documentation"
Write-Host ""

$choice = Read-Host "Choisissez (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`n📡 Démarrage du backend API..." -ForegroundColor Green
        Write-Host "Installation des dépendances..." -ForegroundColor Yellow
        
        Set-Location backend
        pip install -q -r requirements.txt
        
        Write-Host "`n✅ Démarrage du serveur FastAPI..." -ForegroundColor Green
        Write-Host "📍 Accédez à : http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host ""
        
        python main.py
    }
    
    "2" {
        Write-Host "`n📱 Démarrage de l'app mobile..." -ForegroundColor Green
        
        if (-not (Test-Path "mobile/node_modules")) {
            Write-Host "Installation des dépendances..." -ForegroundColor Yellow
            Set-Location mobile
            npm install
        } else {
            Set-Location mobile
        }
        
        Write-Host "`n✅ Lancement d'Expo..." -ForegroundColor Green
        Write-Host "📍 Scannez le QR code avec Expo Go" -ForegroundColor Cyan
        Write-Host ""
        
        npm start
    }
    
    "3" {
        Write-Host "`n🚀 Démarrage des deux services..." -ForegroundColor Green
        Write-Host "Assurez-vous d'avoir 2 terminals ouverts !" -ForegroundColor Yellow
        Write-Host ""
        
        Write-Host "Terminal 1: Lancement du backend..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$PSScriptRoot\backend'; pip install -q -r requirements.txt; python main.py`""
        
        Start-Sleep 3
        
        Write-Host "Terminal 2: Lancement de l'app mobile..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$PSScriptRoot\mobile'; npm install -q; npm start`""
        
        Write-Host "`n✅ Les deux terminaux se sont ouvert !" -ForegroundColor Green
        Write-Host "   - Backend: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "   - Mobile: Scannez le QR code Expo" -ForegroundColor Cyan
    }
    
    "4" {
        Write-Host "`n📖 DOCUMENTATION" -ForegroundColor Green
        Write-Host "===============`n" -ForegroundColor Green
        
        Write-Host "🔹 Endpoints API: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "🔹 README détaillé:" -ForegroundColor Cyan
        
        if (Test-Path "README.md") {
            notepad "README.md"
        } else {
            Write-Host "README.md non trouvé" -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "Choix invalide" -ForegroundColor Red
    }
}

Write-Host ""

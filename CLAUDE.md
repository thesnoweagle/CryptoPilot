# CryptoPilot

Bot de trading Bitcoin sur compte **paper trade** (argent simulé, aucun risque réel).
Projet d'apprentissage : l'utilisateur écrit le code lui-même.

## Rôle de Claude
- Relire les commits de l'utilisateur et signaler les erreurs avec la correction.
- Ne modifier les fichiers que si l'utilisateur le demande explicitement.
- Toujours demander avant de commit et de push.
- Pas de conseil d'investissement : aide technique uniquement.
- Répondre en français, expliquer simplement (l'utilisateur est en bachelor, vise un cycle ingénieur généraliste, intérêt principal : le ML).

## Stack prévue
- **Python** : analyse, backtest, bot, API FastAPI.
- **SQL** (SQLite) : bougies, analyses, trades, alertes.
- **HTML / CSS / JavaScript** : tableau de bord (graphique en chandeliers avec Lightweight Charts).
- **Rust** : calcul des indicateurs (RSI, Fibonacci), appelé depuis Python avec PyO3.
- **ML** (plus tard) : scikit-learn puis PyTorch, prédiction de la direction du prix.

## Structure actuelle
- `config.py` : paramètres (symbole, intervalles, niveaux de Fibonacci, RSI).
- `data.py` : récupération des bougies Binance (`get_bougies`).
- `analyse.py` : Fibonacci, position du prix, RSI de Wilder, affichage.

## Feuille de route
1. [fait] Analyse de base (Fibonacci, RSI) et nettoyage de `analyse.py`.
2. **Prochaine étape** : `signaux.py` avec `generer_signal(analyse)` qui renvoie `"ACHAT"`, `"VENTE"` ou `"ATTENDRE"`.
   - ACHAT : RSI en survente et prix proche d'un niveau de Fibonacci.
   - VENTE : RSI en surachat.
   - Ajouter `TOLERANCE_FIBO` (ex. 0.005) dans `config.py`.
   - Fonction pure (pas d'appel réseau), pour faciliter les tests.
3. Backtest sur l'historique, avec les frais Binance (~0,1 % par ordre).
4. Compte virtuel : solde, positions, stop-loss, take-profit, historique en SQLite.
5. Exécution en boucle (paper trade ou testnet Binance), décisions sur bougies clôturées uniquement.
6. API FastAPI et tableau de bord.
7. Module Rust pour les indicateurs.
8. Couche ML.

## Règles de sécurité
- Clés API et secrets dans `.env`, jamais commités (ajouter `.env` au `.gitignore`).
- Requêtes SQL paramétrées uniquement.
- Valider les entrées de l'API (Pydantic), limiter le nombre de requêtes.
- Risque : 1 à 2 % du capital par trade, stop-loss obligatoire.

## Points connus
- La dernière bougie renvoyée par Binance n'est pas clôturée (à traiter lors des signaux).
- Pas encore de `requirements.txt` (dépendances : `requests`, `pandas`).

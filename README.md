# Projet de Recherche Opérationnelle - 2026

**Étudiants :**
- C25496 Chighaly Khairy
- C26144 Mostapha Mohamed Lfadel

Ce dossier contient les livrables finaux pour le projet académique de Recherche Opérationnelle.

## Sujets Traités

Conformément aux consignes, trois problèmes de trois catégories distinctes ont été modélisés et résolus :
1. **Problème de Tournées de Véhicules (VRP)** - Catégorie : Logistique
2. **Ordonnancement de Machines (Job Shop Scheduling)** - Catégorie : Industrie
3. **Transport de Poissons (Nouadhibou - Nouakchott)** - Catégorie : Problèmes réels en Mauritanie

## Structure des Fichiers

- `vrp.py` : Script Python résolvant le problème VRP avec Google OR-Tools.
- `scheduling.py` : Script Python résolvant le problème d'ordonnancement avec OR-Tools (CP-SAT solver).
- `fish_transport.py` : Script Python modélisant et résolvant le problème de transport de poissons avec PuLP.
- `README.md` : Le fichier que vous lisez actuellement.

## Prérequis et Installation

Pour exécuter les codes Python, vous devez avoir installé Python (>= 3.8) et les bibliothèques d'optimisation `ortools` et `pulp`.

Ouvrez un terminal et installez les dépendances via `pip` :

```bash
pip install ortools pulp
```

## Exécution des codes

Chaque script peut être exécuté de manière autonome.

1. **VRP (Logistique)**
   ```bash
   python vrp.py
   ```
   *Sortie attendue : L'itinéraire de chaque camion, la distance et la charge pour satisfaire la demande des clients.*

2. **Ordonnancement (Industrie)**
   ```bash
   python scheduling.py
   ```
   *Sortie attendue : Le makespan optimal (temps total d'exécution) et les heures de début et fin de chaque tâche sur chaque machine.*

3. **Transport de Poissons (Mauritanie)**
   ```bash
   python fish_transport.py
   ```
   *Sortie attendue : Le nombre minimum de camions frigorifiques (10T et 20T) nécessaires pour transporter la demande de poissons (Courbine, Daurade, Mulet) de Nouadhibou à Nouakchott, et le coût total minimisé.*


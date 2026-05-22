"""
Transport de poissons (Nouadhibou - Nouakchott) - Catégorie Problèmes réels en Mauritanie
Résolution avec PuLP
"""
import pulp

def main():
    """Modèle le problème de transport de poissons de Nouadhibou vers Nouakchott."""
    # Création du problème de minimisation (coût de transport)
    prob = pulp.LpProblem("Transport_Poissons_Mauritanie", pulp.LpMinimize)

    # Données
    types_poissons = ['Courbine', 'Daurade', 'Mulet']
    demande_nktt = {'Courbine': 50, 'Daurade': 30, 'Mulet': 20}  # en tonnes
    offre_ndb = {'Courbine': 60, 'Daurade': 40, 'Mulet': 30}     # en tonnes
    
    # Types de camions disponibles (Frigorifiques)
    types_camions = ['Camion_10T', 'Camion_20T']
    capacite_camions = {'Camion_10T': 10, 'Camion_20T': 20}
    cout_par_camion = {'Camion_10T': 5000, 'Camion_20T': 8500} # MRU (Monnaie)

    # Variables de décision
    # 1. Quantité de chaque poisson transportée
    quantites = pulp.LpVariable.dicts("Quantite", types_poissons, lowBound=0, cat='Continuous')
    
    # 2. Nombre de camions de chaque type utilisés
    nb_camions = pulp.LpVariable.dicts("NbCamions", types_camions, lowBound=0, cat='Integer')

    # Fonction Objectif : Minimiser le coût total d'utilisation des camions
    prob += pulp.lpSum([nb_camions[c] * cout_par_camion[c] for c in types_camions]), "Cout_Total_Transport"

    # Contraintes
    # 1. Satisfaire la demande à Nouakchott
    for p in types_poissons:
        prob += quantites[p] >= demande_nktt[p], f"Demande_NKTT_{p}"
    
    # 2. Respecter la limite d'offre à Nouadhibou
    for p in types_poissons:
        prob += quantites[p] <= offre_ndb[p], f"Offre_NDB_{p}"
    
    # 3. La capacité totale des camions doit être suffisante pour transporter toute la quantité
    prob += pulp.lpSum([nb_camions[c] * capacite_camions[c] for c in types_camions]) >= \
            pulp.lpSum([quantites[p] for p in types_poissons]), "Capacite_Totale_Camions"

    # Résolution
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # Affichage des résultats
    print(f"Statut de la résolution : {pulp.LpStatus[prob.status]}")
    if pulp.LpStatus[prob.status] == 'Optimal':
        print(f"Coût Total Minimisé : {pulp.value(prob.objective)} MRU\n")
        
        print("--- Quantités Transportées (Tonnes) ---")
        for p in types_poissons:
            print(f"- {p} : {quantites[p].varValue} T")
        
        print("\n--- Camions Utilisés ---")
        for c in types_camions:
            print(f"- {c} : {nb_camions[c].varValue} camions")

if __name__ == '__main__':
    main()

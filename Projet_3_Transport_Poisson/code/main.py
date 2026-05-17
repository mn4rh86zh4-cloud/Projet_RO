"""
Projet 3 : Transport de Poisson (Nouadhibou - Nouakchott)
Modélisation simplifiée VRPTW (Vehicle Routing Problem with Time Windows)
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    """Données pour le transport frigorifique."""
    data = {}
    data['time_matrix'] = [
        [0, 6, 9, 8],
        [6, 0, 8, 3],
        [9, 8, 0, 11],
        [8, 3, 11, 0],
    ]
    # Fenêtres de temps pour préserver le poisson (début, fin) en heures
    data['time_windows'] = [
        (0, 5),   # Dépôt (Nouadhibou)
        (7, 12),  # Point A
        (10, 15), # Point B
        (16, 18), # Destination Finale (Nouakchott)
    ]
    data['num_vehicles'] = 2
    data['depot'] = 0
    return data

def main():
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        30,  # temps d'attente maximum autorisé
        30,  # temps total maximum par véhicule
        False,  # forcer start cumul à zéro
        time)
    time_dimension = routing.GetDimensionOrDie(time)

    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    
    if solution:
        print("Solution logistique trouvée : Temps minimisé avec respect de la chaîne du froid.")
        print(f"Temps total d'acheminement : {solution.ObjectiveValue()} heures")
    else:
        print("Aucune solution possible (fenêtres de temps ou distances trop restrictives).")

if __name__ == '__main__':
    main()

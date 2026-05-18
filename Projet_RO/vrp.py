"""
Problème de tournées de véhicules (VRP) - Catégorie Logistique
Résolution avec OR-Tools
"""
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    """Stocke les données du problème."""
    data = {}
    # Matrice des distances entre le dépôt (0) et les clients (1 à 4)
    data['distance_matrix'] = [
        [0, 10, 15, 20, 25],
        [10, 0, 35, 25, 30],
        [15, 35, 0, 30, 20],
        [20, 25, 30, 0, 15],
        [25, 30, 20, 15, 0],
    ]
    data['demands'] = [0, 10, 15, 20, 10]  # Demandes (le dépôt est 0)
    data['vehicle_capacities'] = [30, 30, 30]  # Capacité des 3 véhicules
    data['num_vehicles'] = 3
    data['depot'] = 0
    return data

def print_solution(data, manager, routing, solution):
    """Affiche la solution sur la console."""
    print(f'Objectif: {solution.ObjectiveValue()} (Distance totale)')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = f'Tournée du véhicule {vehicle_id}:\n'
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += f' {node_index} Load({route_load}) -> '
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        node_index = manager.IndexToNode(index)
        plan_output += f' {node_index} Load({route_load})\n'
        plan_output += f'Distance de la tournée: {route_distance}m\n'
        plan_output += f'Charge de la tournée: {route_load}\n'
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f'Distance totale de toutes les tournées: {total_distance}m')
    print(f'Charge totale de toutes les tournées: {total_load}')

def main():
    """Résout le problème de VRP avec capacités."""
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('Aucune solution trouvée !')

if __name__ == '__main__':
    main()

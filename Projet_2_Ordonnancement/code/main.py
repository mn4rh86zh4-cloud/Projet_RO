"""
Projet 2 : Ordonnancement de Machines
Exemple simple d'ordonnancement (Job Shop) utilisant Google OR-Tools.
"""

import collections
from ortools.sat.python import cp_model

def main():
    # Données du problème: (machine_id, processing_time)
    jobs_data = [
        [(0, 3), (1, 2), (2, 2)],  # Job 0
        [(0, 2), (2, 1), (1, 4)],  # Job 1
        [(1, 4), (2, 3)]           # Job 2
    ]

    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)

    model = cp_model.CpModel()

    # Variables
    task_type = collections.namedtuple('task_type', 'start end interval')
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            suffix = f'_{job_id}_{task_id}'
            start_var = model.NewIntVar(0, 100, 'start' + suffix)
            end_var = model.NewIntVar(0, 100, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var, 'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    # Contraintes disjonctives (1 tâche par machine)
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Contraintes de précédence au sein d'un même job
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end)

    # Objectif : minimiser le makespan
    obj_var = model.NewIntVar(0, 100, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Résolution
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Makespan optimal : {solver.ObjectiveValue()}')
    else:
        print('Pas de solution trouvée.')

if __name__ == '__main__':
    main()

"""
Ordonnancement de machines (Job Shop Scheduling) - Catégorie Industrie
Résolution avec OR-Tools (CP-SAT)
"""
import collections
from ortools.sat.python import cp_model

def main():
    """Résout un problème de Job Shop Scheduling simple."""
    # Données du problème: [machine_id, processing_time]
    jobs_data = [
        [(0, 3), (1, 2), (2, 2)],  # Job 0
        [(0, 2), (2, 1), (1, 4)],  # Job 1
        [(1, 4), (2, 3)]           # Job 2
    ]

    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)

    horizon = sum(task[1] for job in jobs_data for task in job)
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
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var, 'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    # Contraintes de non-chevauchement sur les machines
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Contraintes de précédence dans un job
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end)

    # Fonction objectif (Makespan)
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Résolution
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Solution trouvée:')
        print(f'Makespan optimal : {solver.ObjectiveValue()}')
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                start = solver.Value(all_tasks[job_id, task_id].start)
                end = solver.Value(all_tasks[job_id, task_id].end)
                print(f'  Job {job_id} Tâche {task_id} (Machine {task[0]}): Début {start}, Fin {end}')
    else:
        print('Aucune solution trouvée.')

if __name__ == '__main__':
    main()

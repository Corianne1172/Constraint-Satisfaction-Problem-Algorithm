import csv
import sys

# --- Load data from CSV files ---
def load_data():
    # --- Read zones ---
    with open("zones.csv", newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        states_list = header[1:]
        zones_row = next(reader)[1:]
        zone_of = {s: int(z) for s, z in zip(states_list, zones_row)}

    # --- Read parks ---
    with open("parks.csv", newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        parks_row = next(reader)[1:]
        parks = {s: int(p) for s, p in zip(states_list, parks_row)}

    # --- Read driving distances ---
    adj_matrix = {}
    with open("driving2.csv", newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        header = rows[0][1:]
        for row in rows[1:]:
            state = row[0]
            distances = row[1:]
            adj_matrix[state] = {
                header[i]: (int(d) if d != "-1" else -1)
                for i, d in enumerate(distances)
            }

    return states_list, zone_of, parks, adj_matrix

# --- CSP Class Definition ---
class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

# ---- helper: select next zone variable in order ----
def SELECT_UNASSIGNED_VARIABLE(csp, assignment):
    for var in csp.variables:
        if var not in assignment:
            return var
    return None

# ---- ORDER-DOMAIN-VALUES: alphabetical ----
def ORDER_DOMAIN_VALUES(csp, var):
    return sorted(csp.domains[var])

# ---- IS_CONSISTENT: adjacency and uniqueness checks; also final parks checked at completion ----
def IS_CONSISTENT(csp, var, value, assignment):
    if value not in csp.domains[var]:
        return False
    if value in assignment.values():
        return False

    idx = csp.variables.index(var)
    if idx > 0:
        prev_var = csp.variables[idx - 1]
        if prev_var in assignment:
            prev_state = assignment[prev_var]
            dist = distances.get(prev_state, {}).get(value, -1)
            if dist == -1:
                return False

    return True


# ---- INFERENCE: forward checking ----
def INFERENCE(csp, var, assignment):
    idx = csp.variables.index(var)
    if idx + 1 >= len(csp.variables):
        return {}  # no next variable
    next_var = csp.variables[idx + 1]
    if next_var in assignment:
        return {}

    current_state = assignment[var]
    # prune domain of next_var to only values reachable from current_state
    pruned_values = [val for val in csp.domains[next_var] if distances[current_state].get(val, -1) != -1]

    if not pruned_values:
        return "failure"
    return {next_var: pruned_values}  # only for domain pruning

# --- Backtracking Algorithm ---
def BACKTRACKING_SEARCH(csp):
    return BACKTRACK(csp, {})


# ---- Backtrack Function ----
def BACKTRACK(csp, assignment):
    if len(assignment) == len(csp.variables):
        return assignment

    var = SELECT_UNASSIGNED_VARIABLE(csp, assignment)

    for value in ORDER_DOMAIN_VALUES(csp, var):
        if IS_CONSISTENT(csp, var, value, assignment):
            assignment[var] = value

            # Forward checking / inference
            inferences = INFERENCE(csp, var, assignment)

            if inferences != "failure":
                # Save domains to restore later
                saved_domains = {inf_var: list(csp.domains[inf_var]) for inf_var in inferences}
                for inf_var, vals in inferences.items():
                    csp.domains[inf_var] = vals

                result = BACKTRACK(csp, assignment)
                if result is not None:
                    return result

                # Restore domains after backtracking
                for inf_var in inferences:
                    csp.domains[inf_var] = saved_domains[inf_var]

            # Remove current assignment before trying next value
            del assignment[var]

    return None


# ---- Compute path cost and total parks ----
def compute_path_info(path):
    total_cost = 0
    total_parks = 0
    for i, state in enumerate(path):
        total_parks += parks[state]
        if i > 0:
            total_cost += distances[path[i-1]][state]
    return total_cost, total_parks

# ---- Main Program ----
if len(sys.argv) != 3:
    print("ERROR: Not enough or too many input arguments")
    sys.exit()

INITIAL, NO_OF_PARKS = sys.argv[1].upper(), int(sys.argv[2])

print("Konan, Otioh Marie-Lynn Corianne Delon, A20541182 solution:")
print(f"Initial state: {INITIAL}")
print(f"Minimum number of parks: {NO_OF_PARKS}\n")

states, zones, parks, distances = load_data()

# --- Determine path variables from initial zone to Z12 ---
initial_zone = zones[INITIAL]
variables = [f"Z{z}" for z in range(initial_zone, 13)]

# --- Define domains for each zone variable ---
domains = {}
zone_states = {}
for state, z in zones.items():
    if z >= initial_zone:
        zone_states.setdefault(z, []).append(state)
for i, var in enumerate(variables):
    zone_num = initial_zone + i
    domains[var] = zone_states.get(zone_num, [])

# --- Neighbors (unused but required for CSP) ---
neighbors = {var: [] for var in variables}

csp = CSP(variables, domains, neighbors, None)
solution = BACKTRACKING_SEARCH(csp)

if solution:
    # Order solution by zones
    path = [solution[var] for var in variables]
    path_cost, total_parks = compute_path_info(path)

    if total_parks < NO_OF_PARKS:
        print("Solution path: FAILURE: NO PATH FOUND")
        print("Number of states on a path: 0")
        print("Path cost: 0")
        print("Number of national parks visited: 0")
    else:
        print(f"Solution path: {', '.join(path)}")
        print(f"Number of states on a path: {len(path)}")
        print(f"Path cost: {path_cost}")
        print(f"Number of national parks visited: {total_parks}")
else:
    print("Solution path: FAILURE: NO PATH FOUND")
    print("Number of states on a path: 0")
    print("Path cost: 0")
    print("Number of national parks visited: 0")
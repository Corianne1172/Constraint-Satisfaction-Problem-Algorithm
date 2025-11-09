import csv
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
#Load the data
states, zones, parks, distances = load_data()

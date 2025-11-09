# Constraint Satisfaction Problem: US Road Trip Planner

## 🧩 Overview  
This project implements a **Constraint Satisfaction Problem (CSP)** solver using the **Backtracking Search Algorithm** to plan an optimal road trip across the contiguous United States.  

Each U.S. state (and the District of Columbia) is treated as a node in a directed graph, where edges represent direct roads between state capitals. States are divided into **12 travel zones (Z1–Z12)**, and each state is assigned the number of **national parks** it contains.  

The algorithm searches for a valid path starting from a given state and ending in one of the **Z12 states (CA, NV, OR, WA)** while satisfying these constraints:  
1. The trip includes **exactly one state per zone** from the starting zone to zone Z12.  
2. All states in the path must be **directly connected** by roads.  
3. The total number of **national parks visited** must be **at least the desired number (`NO_OF_PARKS`)**.

---

## ⚙️ Features  
- Implements **backtracking CSP** following textbook pseudocode exactly.  
- Uses helper functions:  
  - `SELECT_UNASSIGNED_VARIABLE`  
  - `ORDER_DOMAIN_VALUES`  
  - `IS_CONSISTENT`  
  - `INFERENCE`  
- Supports **forward checking** (domain pruning).  
- Reads data dynamically from `.csv` files:  
  - `zones.csv` – Zone IDs for each state  
  - `parks.csv` – National park counts per state  
  - `driving2.csv` – Driving distances (adjacency matrix between states)  
- Reports the final solution with:  
  - Ordered path of visited states  
  - Total number of states visited  
  - Path cost (total driving distance)  
  - Number of national parks visited  

---

## 🧮 Algorithm Description  

**Backtracking-Search Pseudocode (Implemented Exactly):**
```
function BACKTRACKING-SEARCH(csp) returns a solution or failure
    return BACKTRACK(csp, {})

function BACKTRACK(csp, assignment) returns a solution or failure
    if assignment is complete then return assignment
    var ← SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
        if value is consistent with assignment then
            add {var = value} to assignment
            inferences ← INFERENCE(csp, var, assignment)
            if inferences ≠ failure then
                add inferences to csp
                result ← BACKTRACK(csp, assignment)
                if result ≠ failure then return result
                remove inferences from csp
            remove {var = value} from assignment
    return failure
```

The algorithm explores valid westward routes zone by zone, ensuring adjacency and non-repetition of states while maintaining a running count of parks visited.

---

## 📂 Input Files  

| File | Description |
|------|--------------|
| `zones.csv` | Assigns each state to a travel zone (Z1–Z12) |
| `parks.csv` | Lists the number of national parks per state |
| `driving2.csv` | Adjacency matrix of driving distances between capitals |

**Important:**  
- These files must remain in the same directory as the main Python script.  
- Do **not rename or modify** the input files.  

---

## 🖥️ Running the Program  

### Command Syntax  
```bash
python3 cs480_P02_A20541182.py INITIAL NO_OF_PARKS
```

### Example  
```bash
python3 cs480_P02_A20541182.py MD 5
```

### Output Example  
```
Konan, Otioh Marie-Lynn Corianne Delon, A20541182 solution:
Initial state: MD
Minimum number of parks: 5

Solution path: MD, VA, KY, IL, IA, NE, CO, UT, NV
Number of states on a path: 9
Path cost: 3068
Number of national parks visited: 13
```

If no valid path is found:  
```
Solution path: FAILURE: NO PATH FOUND
Number of states on a path: 0
Path cost: 0
Number of national parks visited: 0
```

---

## 🧠 Key Concepts Demonstrated  
- **Constraint Satisfaction Problems (CSPs)**  
- **Backtracking Search**  
- **Forward Checking and Inference**  
- **Heuristic Variable Selection**  
- **Graph-based Search and Adjacency Reasoning**  

---

## 🗺️ Data Visualization  
The graph below (from the assignment handout) shows the 48 contiguous states grouped by zones (Z1–Z12), illustrating the westward travel constraint.

![US Zones Graph](Picture1.png)

---

## 🧑‍💻 Author  
**Otioh Marie-Lynn Corianne Delon Konan**  
CS 480 – Illinois Institute of Technology  
Fall 2025  

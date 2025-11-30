import time

def successor_fct(x, y, visited):
   
    knight_moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]
    successors = []
    for dx, dy in knight_moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in visited:
            successors.append((nx, ny))
    return successors


def backtracking_simple(assignment):
    """
    Backtracking simple pour le Knight's Tour
    """
    if len(assignment) == 64:
        return assignment  # solution trouvée
    
    current_x, current_y = assignment[-1]
    visited = set(assignment)
    
    successors = successor_fct(current_x, current_y, visited)
    
    for x, y in successors:
        assignment.append((x, y))
        result = backtracking_simple(assignment)
        if result is not None:
            return result
        assignment.pop()  # backtrack
    
    return None

'''
start_time = time.time()
assignment = [(0, 0)]
solution = backtracking_simple(assignment)
print(solution)
end_time = time.time()
print(f"Temps : {end_time - start_time} s")  
print(solution)
'''

assignment = [(0, 0)]
solution = backtracking_simple(assignment)
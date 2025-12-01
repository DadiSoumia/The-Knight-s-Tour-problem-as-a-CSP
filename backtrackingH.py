import time

def successor_fct(current_x, current_y, visited):
   
    knight_moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]
    
    successors = []
    for x, y in knight_moves:
        new_x, new_y = current_x + x, current_y + y
        
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if (new_x, new_y) not in visited:
                successors.append((new_x, new_y))
    
    return successors


def count_onward_moves(x, y, visited):
   
    knight_moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]
    
    count = 0
    for dx, dy in knight_moves:
        new_x, new_y = x + dx, y + dy
        
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if (new_x, new_y) not in visited:
                count += 1
    
    return count


def MRV(successors, visited):
   
    if not successors:
        return []
    
    scored = []
    for pos in successors:
        x, y = pos
        visited_temp = visited | {pos}
        onward_moves = count_onward_moves(x, y, visited_temp)
        scored.append((onward_moves, pos))
    
    scored.sort(key=lambda item: item[0])
    
    return [pos for _, pos in scored]


def LCV(successors, visited):
   
    if not successors:
        return []
    
    scored = []
    for pos in successors:
        x, y = pos
        visited_temp = visited | {pos}
        
        neighbors = successor_fct(x, y, visited)
        
        total_freedom = 0
        for nx, ny in neighbors:
            if (nx, ny) not in visited_temp:
                neighbor_moves = count_onward_moves(nx, ny, visited_temp)
                total_freedom += neighbor_moves
        
        scored.append((total_freedom, pos))
    
    scored.sort(key=lambda item: item[0], reverse=True)
    
    return [pos for _, pos in scored]


def backtracking(assignment):
  
    if len(assignment) == 64:
        return assignment
    
    current_x, current_y = assignment[-1]
    visited = set(assignment)
    
    successors = successor_fct(current_x, current_y, visited)
    
    if not successors:
        return None
    
    successors = MRV(successors, visited)
    

    
    min_score = count_onward_moves(successors[0][0], successors[0][1], visited)  
    equal_MRV = [pos for pos in successors if count_onward_moves(pos[0], pos[1], visited) == min_score]


    successors = LCV(equal_MRV, visited)

    
    for x, y in successors:
        assignment.append((x, y))
        result = backtracking(assignment)
        if result is not None:
            return result
        assignment.pop()
    
    return None

'''
start_time = time.time()
assignment = [(0, 0)]
solution = backtracking(assignment)

end_time = time.time()
print(f"Temps mrv&lcv : {end_time - start_time} s")  
print(solution)
'''


assignment = [(0, 0)]
solution = backtracking(assignment)
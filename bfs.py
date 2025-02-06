# -*- coding: utf-8 -*-

from collections import deque

def get_neighbors(state):
    """
    根据当前状态 state，生成所有合法的下一步状态
    """
    neighbors = []
    state_list = list(state)
    n = len(state_list)
    
    for i, piece in enumerate(state_list):
        if piece == 'R':
            # 红棋只能向右移动
            # 一步移动：当前位置右侧一个位置为空
            if i + 1 < n and state_list[i+1] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i+1] = 'R'
                neighbors.append(''.join(new_state))
            # 跳跃移动：右侧紧邻位置有棋子，紧接着的下一个位置为空
            if i + 2 < n and state_list[i+1] != '_' and state_list[i+2] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i+2] = 'R'
                neighbors.append(''.join(new_state))
        
        elif piece == 'G':
            # 绿棋只能向左移动
            # 一步移动：当前位置左侧一个位置为空
            if i - 1 >= 0 and state_list[i-1] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i-1] = 'G'
                neighbors.append(''.join(new_state))
            # 跳跃移动：左侧紧邻位置有棋子，紧接着的下一个位置为空
            if i - 2 >= 0 and state_list[i-1] != '_' and state_list[i-2] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i-2] = 'G'
                neighbors.append(''.join(new_state))
    
    return neighbors

def bfs(initial, goal):
    """
    利用广度优先搜索算法，从 initial 状态搜索到 goal 状态，
    返回从初始状态到目标状态的移动序列（包含状态列表）
    """
    queue = deque()
    queue.append((initial, [initial]))  # 每个元素为 (当前状态, 到当前状态的路径)
    visited = set([initial])
    
    while queue:
        current_state, path = queue.popleft()
        if current_state == goal:
            return path  # 找到目标状态，返回路径
        
        for next_state in get_neighbors(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))
    
    return None  # 如果搜索完都没有找到解

def main():
    initial_state = "RRR_GGG"
    goal_state = "GGG_RRR"
    
    solution_path = bfs(initial_state, goal_state)
    
    if solution_path:
        print("找到解，共移动 {} 步：".format(len(solution_path) - 1))
        for idx, state in enumerate(solution_path):
            print("步骤 {}: {}".format(idx, state))
    else:
        print("未找到解！")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
def get_neighbors(state):
    """
    根据当前状态 state，生成所有合法的下一步状态。
    红棋只能向右移动，绿棋只能向左移动，
    棋子可以一步移动或跳跃移动（跳跃时隔一个棋子）。
    """
    neighbors = []
    state_list = list(state)
    n = len(state_list)
    
    for i, piece in enumerate(state_list):
        if piece == 'R':
            # 红棋只能向右移动
            # 一步移动：右侧紧邻位置为空
            if i + 1 < n and state_list[i+1] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i+1] = 'R'
                neighbors.append(''.join(new_state))
            # 跳跃移动：右侧紧邻位置有棋子，且下一个位置为空
            if i + 2 < n and state_list[i+1] != '_' and state_list[i+2] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i+2] = 'R'
                neighbors.append(''.join(new_state))
        
        elif piece == 'G':
            # 绿棋只能向左移动
            # 一步移动：左侧紧邻位置为空
            if i - 1 >= 0 and state_list[i-1] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i-1] = 'G'
                neighbors.append(''.join(new_state))
            # 跳跃移动：左侧紧邻位置有棋子，且再左一个位置为空
            if i - 2 >= 0 and state_list[i-1] != '_' and state_list[i-2] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i-2] = 'G'
                neighbors.append(''.join(new_state))
    
    return neighbors

def dfs(state, goal, path, visited):
    """
    利用深度优先搜索递归查找从 state 到 goal 的路径。
    参数：
      - state: 当前状态（字符串形式）
      - goal: 目标状态
      - path: 从初始状态到当前状态的路径（状态列表）
      - visited: 记录已经访问过的状态，防止重复搜索
    如果找到解，则返回完整路径；否则返回 None。
    """
    if state == goal:
        return path

    for next_state in get_neighbors(state):
        if next_state not in visited:
            visited.add(next_state)
            result = dfs(next_state, goal, path + [next_state], visited)
            if result is not None:
                return result
    return None

def main():
    initial_state = "RRR_GGG"
    goal_state = "GGG_RRR"
    
    # 初始化 visited 集合，记录已经访问的状态，防止陷入循环
    visited = set([initial_state])
    solution_path = dfs(initial_state, goal_state, [initial_state], visited)
    
    if solution_path:
        print("找到解，共移动 {} 步：".format(len(solution_path) - 1))
        for idx, state in enumerate(solution_path):
            print("步骤 {}: {}".format(idx, state))
    else:
        print("未找到解！")

if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
def get_neighbors(state):
    """
    根据当前状态 state，生成所有合法的下一步状态。
    红棋 ('R') 只能向右移动，绿棋 ('G') 只能向左移动。
    棋子可以一步移动，也可以跳跃（前方相邻有棋子，后面空位）。
    """
    neighbors = []
    state_list = list(state)
    n = len(state_list)
    
    for i, piece in enumerate(state_list):
        if piece == 'R':
            # 红棋一步向右：右侧相邻位置为空
            if i + 1 < n and state_list[i+1] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i+1] = 'R'
                neighbors.append(''.join(new_state))
            # 红棋跳跃：右侧紧邻位置有棋子，且再右一位置为空
            if i + 2 < n and state_list[i+1] != '_' and state_list[i+2] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i+2] = 'R'
                neighbors.append(''.join(new_state))
                
        elif piece == 'G':
            # 绿棋一步向左：左侧相邻位置为空
            if i - 1 >= 0 and state_list[i-1] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i-1] = 'G'
                neighbors.append(''.join(new_state))
            # 绿棋跳跃：左侧紧邻位置有棋子，且再左一位置为空
            if i - 2 >= 0 and state_list[i-1] != '_' and state_list[i-2] == '_':
                new_state = state_list.copy()
                new_state[i] = '_'
                new_state[i-2] = 'G'
                neighbors.append(''.join(new_state))
    
    return neighbors

def dp(state, goal, memo):
    """
    动态规划求解从 state 到 goal 的最少步数及其路径。
    使用 memo 记录已计算状态，避免重复计算。
    
    返回值为 (steps, path)：
      - steps：从 state 到 goal 的最少移动步数
      - path：从 state 到 goal 的状态序列列表
    若该状态无解，则返回 None。
    """
    # 如果已达到目标状态，则步数为 0，路径仅包含当前状态
    if state == goal:
        return 0, [state]
    
    # 如果当前状态已经计算过，则直接返回结果
    if state in memo:
        return memo[state]
    
    best = None
    best_path = None
    
    # 遍历所有合法的下一步状态
    for next_state in get_neighbors(state):
        result = dp(next_state, goal, memo)
        # 如果从 next_state 能够达到目标状态
        if result is not None:
            steps, path = result
            # 选择步数最少的方案
            if best is None or steps + 1 < best:
                best = steps + 1
                best_path = [state] + path
    
    # 将当前状态的结果保存到 memo 中
    memo[state] = (best, best_path) if best is not None else None
    return memo[state]

def main():
    initial_state = "RRR_GGG"
    goal_state = "GGG_RRR"
    
    # 使用字典 memo 保存状态对应的 (最少步数, 路径)
    memo = {}
    result = dp(initial_state, goal_state, memo)
    
    if result is not None:
        steps, path = result
        print("找到解，共移动 {} 步：".format(steps))
        for idx, state in enumerate(path):
            print("步骤 {}: {}".format(idx, state))
    else:
        print("未找到解！")

if __name__ == "__main__":
    main()


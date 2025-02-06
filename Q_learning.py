# -*- coding: utf-8 -*-
import random

def get_neighbors(state):
    """
    根据当前状态 state，生成所有合法的下一步状态。
    红棋 ('R') 只能向右移动，绿棋 ('G') 只能向左移动。
    棋子可以一步移动，也可以跳跃移动（前方紧邻有棋子且下一个位置为空）。
    """
    neighbors = []
    state_list = list(state)
    n = len(state_list)
    
    for i, piece in enumerate(state_list):
        if piece == 'R':
            # 红棋一步向右：右侧紧邻位置为空
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
            # 绿棋一步向左：左侧紧邻位置为空
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

def is_terminal(state, goal):
    """
    判断状态是否为终止状态：
      - 到达目标状态；
      - 或无合法移动（失败状态）。
    """
    if state == goal:
        return True
    if not get_neighbors(state):
        return True
    return False

def choose_action(state, Q, epsilon):
    """
    使用 epsilon-greedy 策略选择动作：
      - 以 epsilon 概率随机选动作（探索）；
      - 否则选 Q 值最大的动作（利用）。
    返回选定的下一状态，如果无动作则返回 None。
    """
    actions = get_neighbors(state)
    if not actions:
        return None

    if random.random() < epsilon:
        return random.choice(actions)
    
    # 利用：选择 Q 值最大的动作
    q_vals = [Q.get(state, {}).get(a, 0) for a in actions]
    max_q = max(q_vals)
    best_actions = [a for a in actions if Q.get(state, {}).get(a, 0) == max_q]
    return random.choice(best_actions)

def update_Q(Q, state, action, reward, next_state, alpha, gamma, goal):
    """
    根据 Q-learning 更新公式更新 Q 表：
      Q(s, a) <- Q(s, a) + alpha*(reward + gamma * max_a' Q(s', a') - Q(s,a))
    """
    if state not in Q:
        Q[state] = {}
    if action not in Q[state]:
        Q[state][action] = 0

    # 若 next_state 为终止状态，则后续最大 Q 值为 0
    if is_terminal(next_state, goal):
        max_q_next = 0
    else:
        actions_next = get_neighbors(next_state)
        if not actions_next:
            max_q_next = 0
        else:
            max_q_next = max(Q.get(next_state, {}).get(a, 0) for a in actions_next)
    
    Q[state][action] += alpha * (reward + gamma * max_q_next - Q[state][action])

def q_learning(initial_state, goal_state, episodes=50000, alpha=0.1, gamma=0.9, epsilon=0.5, min_epsilon=0.01, decay_rate=0.999):
    """
    使用 Q-learning 算法训练智能体，返回训练后的 Q 表。
    参数：
      - initial_state: 初始状态（字符串）
      - goal_state: 目标状态（字符串）
      - episodes: 总训练回合数
      - alpha: 学习率
      - gamma: 折扣因子
      - epsilon: 初始 epsilon 值（探索率）
      - min_epsilon: epsilon 的下限
      - decay_rate: 每个回合后 epsilon 的衰减因子
    """
    Q = {}  # Q 表：{ state: { next_state: Q_value, ... }, ... }
    
    for ep in range(episodes):
        state = initial_state
        step = 0
        max_steps = 100  # 增加最大步数
        while not is_terminal(state, goal_state) and step < max_steps:
            action = choose_action(state, Q, epsilon)
            if action is None:
                break
            
            next_state = action
            # 如果达到目标状态，给予正奖励
            reward = 10 if next_state == goal_state else 0

            update_Q(Q, state, action, reward, next_state, alpha, gamma, goal_state)
            
            state = next_state
            step += 1
        
        # 逐渐衰减 epsilon
        epsilon = max(min_epsilon, epsilon * decay_rate)
        
        # 可选：每隔一定回合打印一次进度
        if (ep + 1) % 5000 == 0:
            print(f"Episode {ep+1}, epsilon: {epsilon:.4f}")
    return Q

def extract_policy(Q, initial_state, goal_state):
    """
    根据训练好的 Q 表，从初始状态出发提取最优路径（贪心策略）。
    返回状态序列列表。如果出现循环则终止。
    """
    path = [initial_state]
    state = initial_state
    visited = set([state])
    max_steps = 100  # 设置足够步数避免过早终止
    for _ in range(max_steps):
        if state == goal_state:
            break
        actions = get_neighbors(state)
        if not actions:
            break
        q_vals = [Q.get(state, {}).get(a, -float('inf')) for a in actions]
        max_q = max(q_vals)
        best_actions = [a for a in actions if Q.get(state, {}).get(a, 0) == max_q]
        next_state = random.choice(best_actions)
        if next_state in visited:
            # 如果出现循环，则终止
            break
        path.append(next_state)
        state = next_state
        visited.add(state)
    return path

if __name__ == "__main__":
    initial_state = "RRR_GGG"
    goal_state = "GGG_RRR"
    
    print("开始训练 Q-learning...")
    Q = q_learning(initial_state, goal_state, episodes=50000, alpha=0.1, gamma=0.9,
                   epsilon=0.5, min_epsilon=0.01, decay_rate=0.999)
    
    print("\n提取策略...")
    optimal_path = extract_policy(Q, initial_state, goal_state)
    
    if optimal_path[-1] == goal_state:
        print("找到最优解，共移动 {} 步：".format(len(optimal_path) - 1))
    else:
        print("未能找到完整到达目标状态的路径，当前路径为：")
    for idx, state in enumerate(optimal_path):
        print("步骤 {}: {}".format(idx, state))

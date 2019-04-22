import numpy as np
import pandas as pd


class QLearningTable:
    # 初始化
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.6):
        self.actions = actions  # a list
        self.lr = learning_rate  # 学习率
        self.gamma = reward_decay  # 奖励衰减
        self.epsilon = e_greedy  # 贪婪度
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)  # 初始 q_table

    # 选行为
    def choose_action(self, observation):
        self.check_state_exist(observation)  # 检测本 state 是否在 q_table 中存在
        # 选择 action
        if np.random.uniform() < self.epsilon:  # 选择 Q value 最高的 action
            state_action = self.q_table.loc[observation, :]
            # 同一个 state, 可能会有多个相同的 Q action value, 所以我们乱序一下
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:  # 随机选择 action
            action = np.random.choice(self.actions)
        return action

    # 选行为
    def choose_action_real(self, observation):
        self.check_state_exist(observation)  # 检测本 state 是否在 q_table 中存在
        # 选择 action
        state_action = self.q_table.loc[observation, :]
        # 同一个 state, 可能会有多个相同的 Q action value, 所以我们乱序一下
        action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        return action

    # 学习更新参数
    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)  # 检测 q_table 中是否存在 s_
        q_predict = self.q_table.loc[s, a]
        if s_[6] != '1':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # 下个 state 不是 终止符
        else:
            q_target = r  # 下个 state 是终止符
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # 更新对应的 state-action 值

    # 检测 state 是否存在
    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

from maze_env import Maze
from RL_brain import QLearningTable
from environment import *
from app import *
from brute import *
from baseline import *
import matplotlib.pyplot as plt
import numpy as np
import copy

cloud = Cloud(20, 9999)  # 时延，处理能力
bs = BS(cloud, 10, 50)  # 连接的cloud，时延，处理能力
user = User(bs, 1)  # 连接的bs，处理能力
E = 50000  # 总能量
KE = 0.1  # 能量约束
random = []  # 记录随机试验结果
brute = []  # 记录穷举试验结果
q_learning = []  # 记录强化学习试验结果


def update():
    # 学习 100 回合
    rew = []
    R = 0
    T = 0
    for episode in range(50000):
        # 初始化 state 的观测值
        observation = env.reset()
        stade = copy.deepcopy(observation)
        while True:
            # RL 大脑根据 state 的观测值挑选 action
            action = RL.choose_action(str(observation))
            # 探索者在环境中实施这个 action, 并得到环境返回的下一个 state 观测值, reward 和 done (是否是掉下地狱或者升上天堂)
            observation_, reward, done = env.step(action, user)
            # RL 从这个序列 (state, action, reward, state_) 中学习
            R = (R * T + reward) / (T + 1)
            T += 1
            rew.append(R)
            RL.learn(str(stade), action, reward, str(observation_))
            # 将下一个 state 的值传到下一次循环
            stade = copy.deepcopy(observation_)
            # 如果掉下地狱或者升上天堂, 这回合就结束了
            if done:
                break
    plt.plot(np.arange(len(rew)), rew)
    plt.ylabel('Reward', fontsize=14)
    plt.xlabel('Training steps', fontsize=14)
    plt.show()


if __name__ == "__main__":
    # 定义环境 env 和 RL 方式
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))
    # 开始可视化环境 env
    update()
    for edgeuser in [5, 10, 15, 20, 25, 30, 35, 40, 45]:
        # 随机处理
        t = 0
        for i in range(10):
            G = topology()  # 任务图
            E1 = E
            t += Baseline(user, G, E1, KE, edgeuser)
        random.append(t / 10)

        # 穷举法
        H = topology()  # 任务图
        E2 = E
        t = Brute(user, H, E2, KE, edgeuser)  # (用户，应用，能量，能量限制)
        brute.append(t)

        # Q-learning
        observation = env.reset()
        stade = copy.deepcopy(observation)
        while True:
            # RL 大脑根据 state 的观测值挑选 action
            action = RL.choose_action_real(str(observation))
            # 探索者在环境中实施这个 action, 并得到环境返回的下一个 state 观测值, reward 和 done (是否是掉下地狱或者升上天堂)
            observation_, reward, done = env.step(action, user)
            # RL 从这个序列 (state, action, reward, state_) 中学习
            RL.learn(str(stade), action, reward, str(observation_))
            # 将下一个 state 的值传到下一次循环
            stade = copy.deepcopy(observation_)
            # 如果掉下地狱或者升上天堂, 这回合就结束了
            if done:
                break
        q_learning.append(7000-reward)
        print(reward)

    x = [5, 10, 15, 20, 25, 30, 35, 40, 45]
    plt.plot(x, random, marker='o', label="$Random$", c='b')
    plt.plot(x, brute, marker='x', label="$Brute-force$", c='y')
    plt.plot(x, q_learning, marker='s', label="$Q-learning", c='r')
    # plt.plot(x, c, marker='s', label="$DQN$", c='r')
    # 设置刻度字体大小
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Background task flow of edge server", fontsize=14)
    plt.ylim(0, 5000)
    plt.ylabel("completion  time", fontsize=14)
    plt.legend(loc=0, ncol=2)
    # 图例大小
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize='14')
    plt.grid()
    plt.show()

import scipy.stats as st
import math
import gym

from gym.utils import seeding
from findmax import *
from app import *

# if sys.version_info.major == 2:
#     import Tkinter as tk
# else:
#     import tkinter as tk

action_space = [[[0] * 4] * 4] * 3  # list(np.arange(48))
ENERGY = 50000
KE = 0.07
NUMBER = 1
M = 4  # M = 10 （固定的单个应用）
P = -100
maxrewarf = 7000
rv = st.poisson(2)
taskuser = [100 * rv.pmf(i) for i in range(4)]


class Maze(gym.Env):
    def __init__(self):
        super(Maze, self).__init__()
        self.G = topology()
        self.action_space = action_space
        self.n_actions = 48  # len(self.action_space)
        self.n_features = 4
        self.state = np.zeros(4)
        self.seed()

    def step(self, action, user):
        u = user  # 对应任务的user
        b = u.coonect  # 对应任务的bs
        c = b.coonect  # 对应任务的cloud
        state = self.state
        CTaksQueue = state[0]  # 已完成的task
        n = state[1]  # 序列号
        tasknum = state[2]  # edge user
        self.energy_total = state[3]  # 能量
        ctask = CTaksQueue.astype(int)
        nothingness = 0
        t = int(action / 12) + 1  # 任务节点（1,2,3,4）
        x = int(action / 4) % 3  # 位置(0,1,2)
        e = int(action % 3) + 1  # 四个能量级(1,2,3,4)
        if t == 1 and int(ctask % 10) == 1 and int(ctask / 10 % 10) == 0:
            nothingness = 0
        else:
            for i in G.neighbors(t):  # 判断是否满足依赖关系
                if int((ctask / 10 ** i) % 10) != 1:
                    nothingness = 1
                else:  # 满足依赖，但已执行过
                    if int((CTaksQueue / 10 ** t) % 10) != 0:
                        nothingness = 1
        if nothingness == 0:  # 满足就开始执行
            CTaksQueue += 10 ** t
            if x == 0:  # 本地处理
                k = 100 * e  # 根据能量级分配能量
                self.energy_total = self.energy_total - k
                if self.energy_total > 0:  # 判断电量是否足够
                    time = u.Calculation(G.node[t], k)
                    time = math.ceil(time)  # 取上入整数
                    for j in G.neighbors(t):
                        G.add_weighted_edges_from([(t, j, time)])
                    if CTaksQueue == 11111.0:
                        self.reward = maxrewarf-math.ceil(findmax(self.G, M + 1))  # 按处理时间给奖励
                        done = True
                    else:
                        self.reward = 0
                        done = False
                    kk = ENERGY - self.energy_total
                    if kk >= ENERGY * KE:  # 电量约束，超出部分乘以10
                        self.reward = self.reward - 10 * (kk - ENERGY * KE)
                else:
                    self.reward = P
            elif x == 1:  # offloading到BS
                k = 50 * e
                self.energy_total = self.energy_total - k
                if self.energy_total > 0:
                    time = b.Calculation(G.node[t], tasknum) + b.Transmission(G.node[t], k)
                    time = math.ceil(time)
                    for j in G.neighbors(t):
                        G.add_weighted_edges_from([(t, j, time)])
                    if CTaksQueue == 11111.0:
                        self.reward = maxrewarf-math.ceil(findmax(self.G, M + 1))  # 按处理时间给奖励
                        done = True
                    else:
                        self.reward = 0
                        done = False
                    kk = ENERGY - self.energy_total
                    if kk >= ENERGY * KE:  # 电量约束，超出部分乘以10
                        self.reward = self.reward - 10 * (kk - ENERGY * KE)
                else:
                    self.reward = P
            else:  # offloading到云端
                k = 50 * e
                self.energy_total = self.energy_total - k
                if self.energy_total > 0:
                    time = c.Calculation(G.node[t]) + c.Transmission(G.node[t], k)
                    time = math.ceil(time)
                    for j in G.neighbors(t):
                        G.add_weighted_edges_from([(t, j, time)])
                    if CTaksQueue == 11111.0:
                        self.reward = maxrewarf-math.ceil(findmax(self.G, M + 1))  # 按处理时间给奖励
                        done = True
                    else:
                        self.reward = 0
                        done = False
                    kk = ENERGY - self.energy_total
                    if kk >= ENERGY * KE:  # 电量约束，超出部分乘以10
                        self.reward = self.reward - 10 * (kk - ENERGY * KE)
                else:
                    self.reward = P
        else:  # 不满足依赖关系
            done = True
            self.reward = P
            n -= 1
        state[0] = CTaksQueue  # 已处理序列
        state[1] = n + 1  # 节点编号
        state[2] = 20
        # if n == M:
        #     state[2] = 0
        # else:
        #     state[2] = taskuser[n.astype(int)]  # 其他用户任务数
        state[3] = self.energy_total  # 剩余电量
        return self.state, self.reward, done

    def reset(self):
        self.state[0] = 1  # 已处理序列
        self.state[1] = NUMBER  # 节点编号
        self.state[2] = 20      #taskuser[0]  # 其他用户任务数
        self.state[3] = ENERGY  # 能量
        return self.state

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

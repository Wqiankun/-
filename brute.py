import numpy as np
from itertools import product
from findmax import findmax
import math


# 穷举处理使用者的任务
def Brute(user, H, ener, KE,edgeuser):
    if ener == 0:
        return 99999, 0
    else:
        u = user  # 对应任务的user
        b = u.coonect  # 对应任务的bs
        c = b.coonect  # 对应任务的cloud
        Min = 99999  # 最小值
        brute_force = list(product(np.arange(12).tolist(), repeat=len(H) - 2))
        for i in range(len(brute_force)):  # 穷举所有情况
            e = ener
            t1 = i % 12
            t2 = int(i / 12) % 12
            t3 = int(int(i / 12) / 12) % 12
            t4 = int(int(int(i / 12) / 12) / 12) % 12
            T = [t4, t3, t2, t1]
            for task in range(len(T)):  # 穷举任务
                if T[task] in range(0, 4):  # 在本地处理
                    time = u.Calculation(H.node[task + 1], 100 * (T[task] + 1))
                    for j in H.neighbors(task + 1):  # 将计算时间加为边的权值
                        H.add_weighted_edges_from([(task + 1, j, time)])
                    e = e - 100 * (T[task] + 1)
                elif T[task] in range(4, 8):
                    time = b.Calculation(H.node[task + 1], edgeuser) + b.Transmission(H.node[task + 1],50 * (T[task] - 3))
                    for j in H.neighbors(task + 1):  # 将计算时间加为边的权值
                        H.add_weighted_edges_from([(task + 1, j, time)])
                    e = e - 50 * (T[task] - 3)
                else:
                    time = c.Calculation(H.node[task + 1]) + c.Transmission(H.node[task + 1], 50 * (T[task] - 7))
                    for j in H.neighbors(task + 1):  # 将计算时间加为边的权值
                        H.add_weighted_edges_from([(task + 1, j, time)])
                    e = e - 50 * (T[task] - 7)
            time = math.ceil(findmax(H, len(H) - 1))
            if Min > time and e > ener * (1 - KE):
                Min = time
        return Min

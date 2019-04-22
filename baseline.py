from pylab import *  # 支持中文
import numpy as np
from findmax import findmax

# 随机处理使用者的任务
def Baseline(user, G, ener, KE, edgeuser):
    if ener == 0:
        return 99999, 0
    else:
        u = user  # 对应任务的user
        b = u.coonect  # 对应任务的bs
        c = b.coonect  # 对应任务的cloud

        for i in range(len(G) - 2):
            where = np.random.randint(0, 3)  # 随机位置 0-user   1-bs   2-cloud
            how = np.random.choice([100, 200, 300, 400], 4)  # 随机分配能量
            if where == 0:  # 判断在哪执行
                time = u.Calculation(G.node[i + 1], how[i])
            elif where == 1:
                time = b.Calculation(G.node[i + 1], edgeuser) + b.Transmission(G.node[i + 1], how[i] / 2)
            else:
                time = c.Calculation(G.node[i + 1]) + c.Transmission(G.node[i + 1], how[i] / 2)
            # 将计算时间加为边的权值
            if (ener - how[i]) < ener * (1 - KE):
                time = Baseline(user, G, ener, KE, edgeuser)
                return time
            for j in G.neighbors(i + 1):
                G.add_weighted_edges_from([(i + 1, j, time)])
        time = math.ceil(findmax(G, len(G) - 1))
        return time

import math

# 移动设备处理速率的常量
r = 2
fmax = 20
# 边缘服务器传输功率常量
w1 = 30
Fedge = 50
Pmax = 100
BSRTT = 10
# 云端处理速率
w2 = 80
CLOUDRTT = 100
Fcloud = 15


class BASE(object):
    def __init__(self, Connect, delay=0.01, handle=0.9):
        self.coonect = Connect  # 连接
        self.delay = delay  # 延时
        self.handle = handle  # 处理能力

    # 计算能力
    def Calculation(self, task):
        pass

    # 传输的时延时间
    def Transmission(self, task):
        pass


# user
class User(BASE):
    # 连接的bs ，时延，处理能力（没加能量的）
    def __init__(self, Connect, handle=1):
        super(User, self).__init__(Connect, handle)

    # 计算能力(任务，对应能量的处理效率)
    def Calculation(self, task, energy):
        f = math.sqrt(energy / (r * task['t']))
        if f > fmax:
            f = fmax
        time = task['t'] / f
        return time


# bs
class BS(BASE):
    # 连接的cloud ，时延，处理能力
    def __init__(self, Connect, delay=20, handle=2):
        super(BS, self).__init__(Connect, delay, handle)

    # 计算能力(任务)
    def Calculation(self, task, edgeuser):
        time = 200 / (Fedge-edgeuser)+task['t'] /Fedge
        return time

    # 传输的时延时间
    def Transmission(self, task, energy):
        rj = energy / w1
        # 传输功率不能大于移动设备的最大传输功率
        if rj > Pmax:
            rj = Pmax
        time = task['s'] / rj+BSRTT
        return time


# cloud
class Cloud(BASE):
    # 时延，处理能力
    def __init__(self, delay=20, handle=9999):
        super(Cloud, self).__init__(delay, handle)

    # 计算能力(任务)  云端秒处理
    def Calculation(self, task):
        # time = task['t'] / Fcloud
        time = 0
        return time

    # 传输的时延时间
    def Transmission(self, task, energy):
        rj = energy / w2
        # 传输功率不能大于移动设备的最大传输功率
        if rj > Pmax:
            rj = Pmax
        time = task['s'] / rj+CLOUDRTT
        return time

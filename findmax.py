# 取最长时间线
def findmax(G, n):
    m = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if n == 0:
        return 0
    else:
        for i in G.neighbors(n):
            m[i] = G[n][i]['weight'] + findmax(G, i)
        for s in range(10):
            if m[s] > m[s + 1]:
                m[s + 1] = m[s]
        return m[s + 1]
import numpy as np
import random as rand
import csv

# サーキットの長さ
L = 200.0

# 車の数
N = 100

# 試行回数
max_t = 100

# 車を動かす回数
steps = 1000

# 各車両位置
nx = []

# 各車両速度
nv = []

# 平均車間距離に対応した速度
c = 2.0

# 運転者反応
a = 1.0

# 
dt = 0.005

def mstokmh(ms):
    mh = ms * 3600
    kmh = mh / 1000
    return kmh

def V(dx):
    return np.tanh(dx - c) + np.tanh(c)

def initialize():
    dx = L / N
    x = 0.0
    iv = V(dx)
    for i in range(N):
        nx.append(x)
        nv.append(iv)
        x += dx
        x += (rand.random() - 0.5) * 0.01
    print('success initialize.')

def step():
    for i in range(N):
        dx = 0
        if i != N - 1:
            dx = nx[i+1] - nx[i]
        else:
            dx = nx[0] - nx[i]

        if dx < 0.0:
            dx += L

        if dx > L:
            dx -= L

        nv[i] += a * (V(dx) - nv[i]) * dt
        nx[i] += nv[i] * dt
        if nx[i] > L:
            nx[i] -= L

initialize()
for t in range(max_t):
    for s in range(steps):
        step()
    print('success {0} times.'.format(t+1))
with open('point.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['car_index', 'pos', 'speed', 'time'])
    for t in range(max_t + 1):
        for s in range(steps):
            step()
        for i in range(N):
            writer.writerow([i+1, nx[i], mstokmh(nv[i]), t])
        print('success {0} times.'.format(t))

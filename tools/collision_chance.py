import math

N = 64 ** 9
k = 2000

print(k, 1 - math.exp(-0.5 * k * (k - 1) / N))

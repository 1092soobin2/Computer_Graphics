import numpy

# A
M = numpy.array(range(2, 27))
print(M)
print('\n')
# B
M = M.reshape(5, 5)
print(M)
print('\n')
# C
for i in range(1, M.shape[0] - 1):
    for j in range(1, M.shape[1] - 1):
        M[i, j] = 0
print(M)
print('\n')
# D
M = M @ M
print(M)
print('\n')
# E
v = M [0, ]
v_mag = 0
for i in range(0, v.size):
    v_mag += v[i] * v[i]
v_mag = numpy.sqrt(v_mag)
print(v_mag)
import math, random

def brute_maximum_array(A):
    best_low = None
    best_high = None
    best_sum = None
    c = 0
    for i in range(len(A)):
        s = A[i]
        for j in range(i + 1, len(A)):
            c = c + 1
            s = s + A[j]
            if (i == 0 and j == i + 1) or best_sum < s:
                best_sum = s
                best_high = j
                best_low = i
    print(c)
    return (best_low, best_high, best_sum)

print(brute_maximum_array([1, 2, 3, 4]))

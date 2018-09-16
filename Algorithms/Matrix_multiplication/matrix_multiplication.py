import math

def square_matrix_multiply(A, B):
    # if A == [[]] or B == [[]]:
    #     raise Exception("Empty matrices!")

    (width_A, height_A) = (len(A[0]), len(A))
    (width_B, height_B) = (len(B[0]), len(B))
    if width_A != height_A or width_B != height_B:
        raise Exception("Non square matrices!")
    if (width_A * height_A) != (width_B * height_B):
        raise Exception("Not same size matrices!")

    C = []
    for i in range(height_A):
        # print(i)
        line = []
        for j in range(width_A):
            temp = 0
            for k in range(height_A):
                temp = temp + A[i][k]*B[k][j]
            line.append(temp)
        C.append(line)
    return C

# A = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
# B = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# print(square_matrix_multiply(A, B))

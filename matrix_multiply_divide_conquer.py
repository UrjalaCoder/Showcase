import math, random
from timeit import default_timer as timer
from matrix_multiplication import square_matrix_multiply

STRASSENS_CUTOFF_SIZE = 32

def add_matrices(A, B):
    result = []
    for i in range(len(A)):
        line = []
        for j in range(len(A[i])):
            line.append(A[i][j] + B[i][j])
        result.append(line)
    return result

def subtract_matrices(A, B):
    result = []
    for i in range(len(A)):
        line = []
        for j in range(len(A[i])):
            line.append(A[i][j] - B[i][j])
        result.append(line)
    return result
counter = 0
def strassens_method(A, B):
    """
    A and B are n x n matrices -> lists of lists
    """
    C = []
    n = len(A)
    global counter
    # counter += 1
    # print(counter)
    if n <= STRASSENS_CUTOFF_SIZE:
        return square_matrix_multiply(A, B)
    else:
        # Partitioning of A and B to n/2 x n/2 matrices -->
        # A11 = A[0][1:2]
        mid = int(n / 2)
        top_rows_A = A[0:mid]
        top_rows_B = B[0:mid]

        bottom_rows_A = A[mid:]
        bottom_rows_B = B[mid:]

        # Partioning -->
        A11, B11 = ([a[0:mid] for a in top_rows_A], [a[0:mid] for a in top_rows_B])
        A12, B12 = ([a[mid:] for a in top_rows_A], [a[mid:] for a in top_rows_B])

        A21, B21 = ([a[0:mid] for a in bottom_rows_A], [a[0:mid] for a in bottom_rows_B])
        A22, B22 = ([a[mid:] for a in bottom_rows_A], [a[mid:] for a in bottom_rows_B])

        S1 = subtract_matrices(B12, B22)
        S2 = add_matrices(A11, A12)
        S3 = add_matrices(A21, A22)
        S4 = subtract_matrices(B21, B11)
        S5 = add_matrices(A11, A22)
        S6 = add_matrices(B11, B22)
        S7 = subtract_matrices(A12, A22)
        S8 = add_matrices(B21, B22)
        S9 = subtract_matrices(A11, A21)
        S10 = add_matrices(B11, B12)

        # print(S1)

        P1 = strassens_method(A11, S1)
        P2 = strassens_method(S2, B22)
        P3 = strassens_method(S3, B11)
        P4 = strassens_method(A22, S4)
        P5 = strassens_method(S5, S6)
        P6 = strassens_method(S7, S8)
        P7 = strassens_method(S9, S10)

        C11 = add_matrices(subtract_matrices(add_matrices(P5, P4), P2), P6)
        C12 = add_matrices(P1, P2)
        C21 = add_matrices(P3, P4)
        C22 = subtract_matrices(subtract_matrices(add_matrices(P5, P1), P3), P7)

        # print(C11)
        # print(C12)
        # print(C21)
        # print(C22)

        c_top_rows = []
        c_bottom_rows = []
        for j in range(len(C11)):
            row = C11[j] + C12[j]
            c_top_rows.append(row)
        for j in range(len(C21)):
            row = C21[j] + C22[j]
            c_bottom_rows.append(row)
        c_top_rows += c_bottom_rows
        C = c_top_rows
    return C


def square_matrix_multiply_recursive(A, B):
    """
    A and B are n x n matrices -> lists of lists
    """
    C = []
    n = len(A)
    # print(n)
    if n == 1:
        C.append([A[0][0] * B[0][0]])
    else:
        # Partitioning of A and B to n/2 x n/2 matrices -->
        # A11 = A[0][1:2]
        mid = int(n / 2)
        top_rows_A = A[0:mid]
        top_rows_B = B[0:mid]

        bottom_rows_A = A[mid:]
        bottom_rows_B = B[mid:]

        # Partioning -->
        A11, B11 = ([a[0:mid] for a in top_rows_A], [a[0:mid] for a in top_rows_B])
        A12, B12 = ([a[mid:] for a in top_rows_A], [a[mid:] for a in top_rows_B])

        A21, B21 = ([a[0:mid] for a in bottom_rows_A], [a[0:mid] for a in bottom_rows_B])
        A22, B22 = ([a[mid:] for a in bottom_rows_A], [a[mid:] for a in bottom_rows_B])

        A11_B11 = square_matrix_multiply_recursive(A11, B11)
        A12_B21 = square_matrix_multiply_recursive(A12, B21)
        A11_B12 = square_matrix_multiply_recursive(A11, B12)
        A12_B22 = square_matrix_multiply_recursive(A12, B22)
        A21_B11 = square_matrix_multiply_recursive(A21, B11)
        A22_B21 = square_matrix_multiply_recursive(A22, B21)
        A21_B12 = square_matrix_multiply_recursive(A21, B12)
        A22_B22 = square_matrix_multiply_recursive(A22, B22)

        C11 = add_matrices(A11_B11, A12_B21)
        C12 = add_matrices(A11_B12, A12_B22)

        C21 = add_matrices(A21_B11, A22_B21)
        C22 = add_matrices(A21_B12, A22_B22)

        # Väärin -->
        c_top_rows = []
        c_bottom_rows = []
        for j in range(len(C11)):
            row = C11[j] + C12[j]
            c_top_rows.append(row)
        for j in range(len(C21)):
            row = C21[j] + C22[j]
            c_bottom_rows.append(row)
        c_top_rows += c_bottom_rows
        C = c_top_rows
    return C
def main():
    n = 512
    min = -10
    max = 10
    start = timer()
    a = [[random.randint(min, max) for _ in range(n)] for _ in range(n)]
    b = [[random.randint(min, max) for _ in range(n)] for _ in range(n)]
    end = timer()
    print("Random generation time: " + str(end - start))
    # # print(a)
    # # print(b)
    # a = [[0, 1, 2, 3], [0, 1, 2, 3], [1, 4, 5, 9], [0, 1, 4, 7]]
    # b = [[1, 2, 3, 4], [1, 2, 3, 4], [8, 9, 10, 3], [21, 3, 4, 8]]
    start = timer()
    r_simple = square_matrix_multiply(a, b)
    end = timer()
    print("Simple algorithm time: " + str(end - start))
    # start = timer()
    # r_recursive = square_matrix_multiply_recursive(a, b)
    # end = timer()
    # print("Recursive algorithm time: " + str(end - start))
    start = timer()
    s = strassens_method(a, b)
    end = timer()
    print("strassens_method: " + str(end - start))
if __name__ == "__main__":
    main()

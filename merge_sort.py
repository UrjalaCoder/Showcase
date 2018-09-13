import random, math
def merge(arr, p, q, r):
    n1 = q - p + 1
    n2 = r - q

    L = []
    R = []
    for i in range(n1):
        L.append(arr[p + i])
    for j in range(n2):
        R.append(arr[q + j + 1])

    i = 0
    j = 0
    for k in range(p, r + 1):
        if i < n1 and (j >= n2 or L[i] <= R[j]):
            arr[k] = L[i]
            i = i + 1
        else:
            arr[k] = R[j]
            j = j + 1

def merge_sort(arr, p, r):
    if p < r:
        q = math.floor((p+r) / 2)
        merge_sort(arr, p, q)
        merge_sort(arr, q + 1, r)
        merge(arr, p, q, r)

def main():
    testlist = [random.randint(1, 2048) for _ in range(10)]
    print(testlist)
    merge_sort(testlist, 0, len(testlist) - 1)
    print(testlist)

if __name__ == "__main__":
    main()

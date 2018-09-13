import math, random
def find_max_crossing_subarray(A, low, mid, high):
    # Sums of the left and right sides.
    left_sum = 0
    right_sum = 0
    # Mid is included in left array
    i = mid
    total = 0
    left_max = 0
    while i >= 0:
        total = total + A[i]
        if i == mid or total > left_sum:
            left_sum = total
            left_max = i
        i = i - 1

    j = mid + 1
    total = 0
    right_max = 0
    while j <= high:
        total = total + A[j]
        if j == mid + 1 or total > right_sum:
            right_sum = total
            right_max = j
        j = j + 1
    return (left_max, right_max, left_sum + right_sum)

def find_max_subarray(A, low, high):
    print(str(A[low:(high + 1)]))
    if high == low:
        return (low, high, A[low])
    else:
        mid = math.floor((high + low) / 2)
        # print("low: {} high: {} mid: {}".format(low, high, mid))
        # print("DEBUG")
        (left_low, left_high, left_sum) = find_max_subarray(A, low, mid)
        # print(left_low, left_high, left_sum)
        (right_low, right_high, right_sum) = find_max_subarray(A, mid + 1, high)
        (cross_low, cross_high, cross_sum) = find_max_crossing_subarray(A, low, mid, high)

        if left_sum >= right_sum and left_sum >= cross_sum:
            return (left_low, left_high, left_sum)
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return (right_low, right_high, right_sum)
        else:
            return (cross_low, cross_high, cross_sum)
test_values = [random.randint(-10, 10) for _ in range(5)]
# print(find_max_crossing_subarray(test_values, 0, 2, 5))
print(test_values)
print(find_max_subarray(test_values, 0, len(test_values) - 1))

import random

# Non mutating sorting function.
def insertion_sort(sortable_list):
    # Code modified for 0-based list.
    result_list = sortable_list[:]
    for j in range(1, len(result_list)):
        key = result_list[j]
        i = j - 1
        # Insert key to correct location in sorted "section".
        while i >= 0 and result_list[i] > key:
            result_list[i + 1] = result_list[i]
            i = i - 1
        result_list[i + 1] = key
    return result_list

def generate_random_list(size, min, max):
    result_list = [random.randint(min, max) for _ in range(size)]
    return result_list

def main():
    sortable_sq = generate_random_list(1000, 0, 100)
    print(sortable_sq, "-"*10, "\n")
    print(insertion_sort(sortable_sq))

if __name__ == "__main__":
    main()
else:
    print("Must be main module!")

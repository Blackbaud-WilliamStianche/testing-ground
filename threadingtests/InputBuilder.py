import random


def gen_input(file_handle, count, min_group, max_group, min_value, max_value):
    group_counts = {k:0 for k in range(min_group, max_group+1)}
    print(group_counts)
    for x in range(count):
        group = random.randint(min_group, max_group)
        group_counts[group] += 1
        value = random.randint(min_value, max_value)
        file_handle.write(str(group) + ',' + str(value) + '\n')
    return group_counts

if __name__ == "__main__":
    c = 1200
    mng = 1
    mxg = 8
    mnv = 1
    mxv = 10

    with open("infile.csv", 'w') as file:
        results = gen_input(file, c, mng, mxg, mnv, mxv)

    print(results)
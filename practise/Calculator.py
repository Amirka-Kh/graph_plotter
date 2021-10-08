# mathematical computations

# Find max value ----------------------------------------------
def find_max(array):
    max_v = 0
    for i in range(0, len(array)):
        if max_v < array[i]:
            max_v = array[i]

    return max_v

# Calculate global error --------------------------------------
def global_error(source, result):
    # error array
    err_arr = []

    iterations = len(result)

    for i in range(0, iterations):
        err = abs(float(source[i] - result[i]))
        err_arr.append(err)

    return err_arr

# Calculate local errors --------------------------------------
def local_error(source, result):
    # error array
    err_arr = []

    iterations = len(result)
    err_arr.append(0)

    for i in range(0, iterations-1):
        err = abs(float(source[i+1] - result[i]))
        err_arr.append(err)

    return err_arr


# Differential equation ---------------------------------------
def equation(x, y):
    # 3y - xy^degree
    degree = float(1 / 3)
    result = float(3 * y - x * float(y ** degree))
    return result


# X-array -----------------------------------------------------
def create_array(x, N, X):
    x_arr = []
    h = float((X - x) / N)

    for i in range(0, N):
        x_arr.append(x)
        x += h

    return x_arr

# N-domain ----------------------------------------------------
def create_n_array(n0, N):
    n_dom = []

    for i in range(n0, N):
        n_dom.append(n0+i)

    return n_dom

def func4(sp, stat, n):
    available_seat = sp
    status = []
    rng = []
    min_diff = float('inf')
    most_fitted_car = -1
    for s in stat:
        status.append(int(s))
    for a in available_seat:
        rng.append(abs(a-n))
    i = 0
    for r in rng:
        if status[i] == 0:
            if r < min_diff:
                most_fitted_car = i
                min_diff = r
        i += 1
    print(most_fitted_car)
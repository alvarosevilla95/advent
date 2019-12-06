def check_valid(n):
    c = 0
    c_d = 0
    min_d = 6
    for l in n:
        l = int(l)
        if l < c:
            return False
        if l == c:
            c_d += 1
        else:
            if c_d > 0:
                min_d = min(min_d, c_d)
            c_d = 0
        c = l
    if c_d > 0:
        min_d = min(min_d, c_d)
    return min_d > 0


valid = 0
for n in range(240920,789857):
    valid += 1 if check_valid(str(n)) else 0
print(valid)
    

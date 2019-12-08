def get_primes(n):
    ps = []
    for i in range(2, n):
        if is_prime(ps, i):
            ps.append(i)
    return ps

def is_prime(primes, n):
    for p in primes:
        if n % p == 0:
            return False
        if p**2 > n:
            break
    return True

def compute():
    ans = 0
    primes = get_primes(1000000)
    consecutive = 0
    for i in range(len(primes)):
            sum = primes[i]
            consec = 1
            for j in range(i + 1, len(primes)):
                    sum += primes[j]
                    consec += 1
                    if sum >= len(isprime):
                            break
                    if isprime[sum] and consec > consecutive:
                            ans = sum
                            consecutive = consec
    return str(ans)


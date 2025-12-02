data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

data = open('inputs/day2.txt').read()

ranges = [list(map(int, x.split('-'))) for x in data.split(',')]

p1 = p2 = 0
for r in ranges:
    for n in range(r[0], r[1]+1):
        s = str(n)
        if s[:len(s)//2] == s[len(s)//2:]:
            p1 += n
        for i in range(1, len(s) // 2 + 1):
            if s == s[:i] * (len(s) // i):
                p2 += n
                break

print(p1, p2)

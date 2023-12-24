from common import *

data = r"""
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""".strip().splitlines()

data = open('inputs/day24.txt').read().splitlines()

hail = np.array([[[int(c) for c in line.split(',')] for line in block.split('@')] for block in data])

# part 1
s,e = 200000000000000, 400000000000000

def intersects(a, b):
    (p1,d1), (p2,d2) = a[:2,:2], b[:2,:2]
    try: 
        A, b = np.array([d1, -d2]).T, p2-p1
        t1,t2 = np.linalg.solve(A, b) # type: ignore
        x,y = p1 + d1*t1
        return s<=x<=e and s<=y<=e and t1>0 and t2>0
    except: return False

print(sum(intersects(a, b) for i, a in enumerate(hail) for b in hail[i+1:]))

# part 2
x,y,z,vx,vy,vz,*t = symbols('x y z vx vy vz t0 t1 t2')

def system(rock):
    i, ((xr,yr,zr), (vxr,vyr,vzr)) = rock
    return [(x+vx*t[i]) - (xr+vxr*t[i]), 
            (y+vy*t[i]) - (yr+vyr*t[i]), 
            (z+vz*t[i]) - (zr+vzr*t[i])]

polys = [*chain(*map(system, enumerate(hail[:3])))]
result = solve_poly_system(polys,x,y,z,vx,vy,vz,*t)[0] # type: ignore
print(sum(result[:3])) 

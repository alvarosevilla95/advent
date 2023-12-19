from common import *

data = r"""
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".strip()

data = open('inputs/day19.txt').read()

flows, parts = data.split('\n\n')

def parse_workflow(line):
    name, conds = re.findall(r'(\w+){(.+)}', line)[0]
    *conds, default = conds.split(',')
    conds = [re.findall(r'(\w+)([<>])(\d+):(\w+)', cond)[0] for cond in conds]
    return name, ([(p,o,int(v),t) for p,o,v,t in conds], default)

flows = dict(parse_workflow(line) for line in flows.splitlines())
parts = [{k: int(v) for k,v in re.findall(r'(\w+)=(\d+)', line)} for line in parts.splitlines()]

# part 1
def check_part(part, inst="in"):
    if inst in 'AR': return inst == 'A'
    conds, default = flows[inst]
    check_cond = lambda p: part[p[0]] < p[2] if p[1] == '<' else part[p[0]] > p[2]
    return check_part(part, next((cond[3] for cond in conds if check_cond(cond)), default))

print(sum(value for part in parts if check_part(part) for value in part.values()))

# part 2
def find_ranges(ranges, inst="in"):
    if inst in 'AR': return prod(mx-mn+1 for (mn,mx) in ranges.values()) if inst == 'A' else 0
    total = 0
    conds, default = flows[inst]
    for p,o,v,t in conds:
        mn, mx = ranges[p]
        next_range = (mn, min(mx, v-1)) if o == '<' else (max(mn, v+1), mx)
        total += find_ranges({**ranges, p: next_range}, t)
        ranges[p] = (max(mn, v), mx) if o == '<' else (mn, min(mx, v))
    return total + find_ranges(ranges, default)

print(find_ranges({k: (1, 4000) for k in 'xmas'}))

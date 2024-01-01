import math

data = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip()

data = open('inputs/day7.txt').read()

commands = [c.splitlines() for c in data.split("$ ")[1:]]
commands = [[c[0].split(), c[1:]] for c in commands]

path = []
tree = {}

for c in commands:
    match c[0]:
        case ["cd", "/"]: path = []
        case ["cd", ".."]: path.pop()
        case ["cd", x]: path += [x]
        case ["ls"]: tree[tuple(path)] = c[1]

def object_size(path, obj):
    return get_size((*path, obj.split()[1])) if obj.startswith("dir") else int(obj.split()[0])

def get_size(path):
    return sum(object_size(path, c) for c in tree[path])

# part 1
print(sum(s for d in tree if (s:=get_size(d)) <= 100000))

# part 2
must_free = get_size(tuple()) + 30000000 - 70000000
print(min(s for d in tree if (s:=get_size(d)) >= must_free))

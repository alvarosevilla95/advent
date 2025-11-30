import time
very_start = time.time()
for i in range(1, 25):
    start = time.time()
    print(f"\033[0;32mDay {i}\033[0m")
    exec(f"import day{i:02d}")
    time_taken = time.time() - start
    print(f"\033[0;33m{time_taken*1000:.0f}ms\033[0m")
    print()
print(f"Total time: {time.time() - very_start:.2f}s")

import sys; args = sys.argv[1:]
import time
import cProfile


def constraints(i):
    return {*[i // (N * BLOCK_SIZE) * (N * BLOCK_SIZE) + i % N - i % BLOCK_SIZE + k + j for k in
            range(BLOCK_SIZE) for j in range(0, BLOCK_SIZE * N, N)],
            *[i % N + r * N for r in range(N)],
            *[c + i // N * N for c in range(N)]} - {i}


def is_invalid(pzl, last_filled_pos):
    if last_filled_pos == -1:
        return False
    for i in CONSTRAINTS[last_filled_pos]:
        if pzl[i] == pzl[last_filled_pos]:
            return True
    return False


def choices(pzl):
    min_lst = SYMBOLS
    for i, char in enumerate(pzl):
        if char == '.':
            invalid_symbols = {pzl[c] for c in CONSTRAINTS[i]}
            if N + 1 - len(invalid_symbols) >= len(min_lst):  # +1 to account for period
                continue
            min_lst = [(i, s) for s in SYMBOLS if s not in invalid_symbols]
            if len(min_lst) == 1:
                return min_lst
    return min_lst


# returns a solved pzl or the empty string on failure
def brute_force(pzl, last_filled_pos):
    if is_invalid(pzl, last_filled_pos): return ''
    if '.' not in pzl: return pzl

    for i, char in choices(pzl):
        sub_pzl = pzl[:i] + char + pzl[i + 1:]
        b_f = brute_force(sub_pzl, i)
        if b_f:
            return b_f
    return ''


def grader_print(i, pzl, solution):
    print(f'{i + 1}: ' + (' ' if i < 9 else '') + pzl)
    print(f'    {solution} {checksum(solution)}')


def square_print(pzl):
    for r in range(N):
        for c in range(N):
            print(pzl[r * N + c], end=" ")
            if c + 1 != N and (c + 1) % BLOCK_SIZE == 0:
                print("|", end=" ")
        if r + 1 != N and (r + 1) % BLOCK_SIZE == 0:
            print()
            print("- " * N, end=" ")
        print()


def checksum(pzl):
    min_ascii = ord('1')
    return sum(ord(char) - min_ascii for char in pzl)


def set_globals(pzl):
    # noinspection PyGlobalUndefined
    global N, SYMBOLS, CONSTRAINTS, BLOCK_SIZE

    N = int(len(pzl) ** 0.5)
    BLOCK_SIZE = int(N**0.5)
    SYMBOLS = {str(i + 1) for i in range(N)}
    CONSTRAINTS = [constraints(i) for i in range(N * N)]


def main():
    start = time.process_time()

    with open(args[0]) as f:
        for i, line in enumerate(f):
            puzzle = line.strip()
            if i == 0:
                set_globals(puzzle)
            solution = brute_force(puzzle, -1)
            grader_print(i, puzzle, solution)

    print(time.process_time() - start)


if __name__ == '__main__':  # main()
    cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024

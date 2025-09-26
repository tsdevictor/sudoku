import sys; args = sys.argv[1:]
import time
import cProfile


def constraints(i):
    block_width = int(N ** 0.5)
    return [*({*[i // (N * block_width) * (N * block_width) + i % N - i % block_width + k + j for k in range(block_width) for j in range(0, block_width * N, N)],
            *[i % N + r * N for r in range(N)],
            *[c + i // N * N for c in range(N)]}
           - {i})]


def is_invalid(pzl, pos):
    if pos == -1:
        return False
    for i in CONSTRAINTS[pos]:
        if pzl[i] == pzl[pos]:
            return True
    return False


def is_solved(pzl):
    return '.' not in pzl


def choices(pzl):
    min_len = len(SYMBOLS)
    all_choices = [[] for _ in range(N + 1)]
    for i, char in enumerate(pzl):
        if char == '.':
            invalid_symbols = {pzl[c] for c in CONSTRAINTS[i]}
            if len(SYMBOLS) - len(invalid_symbols) >= min_len:
                continue
            choice_lst = [(i, s) for s in SYMBOLS if s not in invalid_symbols]
            if len(choice_lst) == 1:
                return choice_lst
            if len(choice_lst) < min_len:
                min_len = len(choice_lst)
            all_choices[len(choice_lst)].append(choice_lst)
    for choice_set in all_choices:
        if choice_set:
            return choice_set.pop()


def brute_force(pzl, pos):  # pos is position that was last filled
    # returns a solved pzl or the empty string on failure
    if is_invalid(pzl, pos):
        return ''
    if is_solved(pzl): return pzl

    for i, char in choices(pzl):
        sub_pzl = pzl[:i] + char + pzl[i + 1:]
        b_f = brute_force(sub_pzl, i)
        if b_f:
            return b_f
    return ''


def grader_print(i, pzl, solution):
    print(f'{i + 1}: {pzl}')
    print('   ' + ('' if i < 9 else ' ') + solution, checksum(solution))


def checksum(pzl):
    min_ascii = ord('1')
    check_sum = 0
    for char in pzl:
        check_sum += ord(char) - min_ascii
    return check_sum


def set_globals(pzl):
    # noinspection PyGlobalUndefined
    global N, SYMBOLS, CONSTRAINTS

    N = int(len(pzl) ** 0.5)
    SYMBOLS = [str(i + 1) for i in range(N)]
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

            if i == 60:
                sys.exit()

    print(time.process_time() - start)


if __name__ == '__main__':  # main()
    cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024

import sys; args = sys.argv[1:]
import time
import cProfile


def choices():
    min_len = len(SYMBOLS)
    to_return = 0, []
    for i, choice_lst in enumerate(CHOICES):
        if len(choice_lst) == 1:
            return i, choice_lst
        if choice_lst and len(choice_lst) < min_len:
            min_len = len(choice_lst)
            to_return = i, choice_lst
    return to_return


def brute_force(pzl, pos):  # pos is position that was last filled
    # returns a solved pzl or the empty string on failure
    if is_invalid(pzl, pos):
        return ''
    if '.' not in pzl: return pzl

    update_choices(pzl, pos)

    i, choice_lst = choices()
    global CHOICES
    for char in choice_lst:
        sub_pzl = pzl[:i] + char + pzl[i + 1:]
        choices_copy = [*CHOICES]
        b_f = brute_force(sub_pzl, i)
        if b_f:
            return b_f
        CHOICES = choices_copy

    return ''

def is_invalid(pzl, pos):
    if pos == -1:
        return False
    for i in CONSTRAINTS[pos]:
        if pzl[i] == pzl[pos]:
            return True
    return False

def grader_print(i, pzl, solution):
    print(f'{i + 1}: {pzl}')
    print('   ' + ('' if i < 9 else ' ') + solution, checksum(solution))

def checksum(pzl):
    min_ascii = ord('1')
    check_sum = 0
    for char in pzl:
        check_sum += ord(char) - min_ascii
    return check_sum

def constraints(i):
    block_width = int(N ** 0.5)
    return [*({*[i // (N * block_width) * (N * block_width) + i % N - i % block_width + k + j for k in
                 range(block_width) for j in range(0, block_width * N, N)],
               *[i % N + r * N for r in range(N)],
               *[c + i // N * N for c in range(N)]}
              - {i})]

def set_globals(pzl):
    # noinspection PyGlobalUndefined
    global N, SYMBOLS, CONSTRAINTS, CHOICES

    N = int(len(pzl) ** 0.5)
    SYMBOLS = [str(i + 1) for i in range(N)]
    CONSTRAINTS = [constraints(i) for i in range(N * N)]
    CHOICES = [[] for _ in range(N * N)]

def reset_choices(pzl):
    for i, char in enumerate(pzl):
        if char == '.':
            invalid_symbols = {pzl[c] for c in CONSTRAINTS[i]}
            CHOICES[i] = [s for s in SYMBOLS if s not in invalid_symbols]
        else:
            CHOICES[i] = []

def update_choices(pzl, pos):  # pos: most recently filled position
    if pos == -1:
        return
    CHOICES[pos] = []
    for i in CONSTRAINTS[pos]:
        if pzl[pos] in CHOICES[i]:
            CHOICES[i].remove(pzl[pos])

def square_print(pzl):
    block_size = int(N**0.5)
    for r in range(N):
        for c in range(N):
            print(pzl[r * N + c], end=" ")
            if c + 1 != N and (c+1) % block_size == 0:
                print("|", end=" ")
        if r + 1 != N and (r+1) % block_size == 0:
            print()
            print("- " * N, end=" ")
        print()

def main():
    start = time.process_time()

    with open(args[0]) as f:
        for i, line in enumerate(f):
            puzzle = line.strip()
            if i == 0:
                set_globals(puzzle)

            reset_choices(puzzle)

            solution = brute_force(puzzle, -1)
            grader_print(i, puzzle, solution)

            if i == 60:
                sys.exit()

    print(time.process_time() - start)


if __name__ == '__main__':  # main()
    cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024

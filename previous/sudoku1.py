import sys; args = sys.argv[1:]
import time


def constraints():
    box_size = int(PW ** 0.5)
    constraint_sets = [sorted([n + c + r + i for n in range(box_size) for c in range(0, box_size * PW, PW)]) for r in range(0, PW, box_size) for i in range(0, PW * PW, PW * box_size)]
    constraint_sets += [[col + r * PW for r in range(PW)] for col in range(PW)]
    constraint_sets += [[c + row * PW for c in range(PW)] for row in range(PW)]

    return constraint_sets
def is_invalid(pzl: str, pos: int, constraint_sets: []):
    if pos == -1:
        return False

    for cs in constraint_sets:
        if pos not in cs:
            continue
        for i in cs:
            if i != pos and pzl[i] == pzl[pos]:
                return True

    return False

def is_solved(pzl):
    return '.' not in pzl

def choices(pzl):
    for i in range(len(pzl)):
        if pzl[i] == '.':
            return [(i, s) for s in SYMBOL_SET]
    return []

def brute_force(pzl, pos):  # pos is position that was last filled
    # returns a solved pzl or the empty string on failure
    if is_invalid(pzl, pos, NEIGHBORS):
        return ''
    if is_solved(pzl): return pzl

    for i, char in choices(pzl):
        sub_pzl = pzl[:i] + char + pzl[i+1:]
        b_f = brute_force(sub_pzl, i)
        if b_f:
            return b_f

    return ''

def nice_print(pzl):
    for i in range(PW):
        print(' '.join(pzl[i * PW:i * PW + PW]) + '\n')
    print()

def grader_print(i, pzl, solution):
    print(f'{i+1}: {pzl}')
    print('   ' + ('' if i < 9 else ' ') + solution, checksum(solution))


def checksum(pzl):
    min_ascii = ord('1')
    check_sum = 0
    for char in pzl:
        check_sum += ord(char) - min_ascii
    return check_sum


PW = 9
SYMBOL_SET = [str(i + 1) for i in range(PW)]
NEIGHBORS = constraints()

def main():
    start = time.process_time()

    with open(args[0]) as f:
        for i, line in enumerate(f):
            puzzle = line.strip()
            solution = brute_force(puzzle, -1)
            grader_print(i, puzzle, solution)

    print(time.process_time() - start)


if __name__ == '__main__': main()

# Tristan Devictor, pd. 6, 2024

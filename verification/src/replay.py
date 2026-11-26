"""Exact small tests of the determinant, interpolation, and affine criteria."""

from fractions import Fraction as Q
from itertools import combinations, product


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def det2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def solve2(matrix, values):
    determinant = det2(matrix)
    return ((values[0]*matrix[1][1]-matrix[0][1]*values[1])/determinant,
            (matrix[0][0]*values[1]-values[0]*matrix[1][0])/determinant)


def det3(matrix):
    return sum((-1)**j * matrix[0][j] *
               det2([[matrix[i][l] for l in range(3) if l != j] for i in (1, 2)])
               for j in range(3))


def mix(weight, first, second):
    return (1 - weight) * first + weight * second


def sign(value):
    return (value > 0) - (value < 0)


def check_policy_returns():
    discount = Q(3, 4)
    start = (Q(1, 3), Q(2, 3))
    rewards = (
        ((2, -1), (-3, 5), (7, 2), (1, -3)),
        ((0, 0), (1, -1), (0, 0), (0, 0)),
        ((0, 0), (2, -1), (0, 0), (0, 0)),
        ((0, 0), (1, 0), (0, 0), (0, 0)),
        ((0, 0), (1, 1), (0, 0), (0, 0)),
    )
    count = 0
    for probabilities in product([Q(i, 4) for i in range(5)], repeat=4):
        rows = [tuple(Q(i//2 == j) - discount*v for j, v in enumerate((p, 1-p)))
                for i, p in enumerate(probabilities)]
        baseline = [rows[0], rows[2]]
        denominator = det2(baseline)
        assert denominator > 0
        signs = []
        for reward in rewards:
            immediate = [dot((p, 1-p), values) for p, values in zip(probabilities, reward)]
            base_value = solve2(baseline, [immediate[0], immediate[2]])
            determinants = [det3([(*rows[0], immediate[0]), (*rows[2], immediate[2]),
                                  (*rows[i], immediate[i])]) for i in (1, 3)]
            assert determinants == [denominator*(immediate[i]-dot(rows[i], base_value)) for i in (1, 3)]
            for policy in product((Q(0), Q(1, 2), Q(1)), repeat=2):
                flow = [tuple(mix(policy[s], a, b) for a, b in zip(rows[2*s], rows[2*s+1]))
                        for s in range(2)]
                value = solve2(flow, [mix(policy[s], immediate[2*s], immediate[2*s+1]) for s in range(2)])
                occupancy = solve2(list(zip(*flow)), start)
                alternative_occupancy = [occupancy[s]*policy[s] for s in range(2)]
                assert dot(start, value) == dot(start, base_value) + dot(alternative_occupancy, determinants)/denominator
                count += 1
            signs.append(sign(determinants[0]))
        p = probabilities[1]
        if p in (0, 1):
            assert signs[1] == signs[2]
        if p == Q(1, 2):
            assert signs[1:3] == [0, 1]
        if p == 0:
            assert signs[3:5] == [0, 1]
        else:
            assert signs[3:5] == [1, 1]
    assert (2*Q(2, 5)-1, 3*Q(2, 5)-1) == (Q(-1, 5), Q(1, 5))
    return count


def rank(matrix):
    rows = [list(map(Q, r)) for r in matrix]
    n = 0
    for j in range(len(rows[0])):
        pivot = next((i for i in range(n, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[n], rows[pivot] = rows[pivot], rows[n]
        for i in range(n+1, len(rows)):
            multiplier = rows[i][j]/rows[n][j]
            rows[i] = [a-multiplier*b for a, b in zip(rows[i], rows[n])]
        n += 1
    return n


def check_grids():
    for n in range(1, 8):
        vertices = [tuple(Q(i == j) for j in range(n)) for i in range(n)]
        center = (Q(1, n),)*n
        interior = [center]
        interior += [tuple(z+sign*(a-b)/(2*n) for z, a, b in zip(center, vertices[i], vertices[-1]))
                     for i in range(n-1) for sign in (-1, 1)]
        interior += [tuple(z+(a+b-2*h)/(4*n) for z, a, b, h in
                           zip(center, vertices[i], vertices[j], vertices[-1]))
                     for i, j in combinations(range(n-1), 2)]
        assert all(sum(p) == 1 and all(value > 0 for value in p) for p in interior)
        outer = vertices + [tuple((a+b)/2 for a, b in zip(vertices[i], vertices[j]))
                            for i, j in combinations(range(n), 2)]
        for grid in (interior, outer):
            monomials = [[p[i]*p[j] for i in range(n) for j in range(i, n)] for p in grid]
            assert rank(monomials) == n*(n+1)//2


def ray(vector):
    scale = next((abs(a) for a in vector if a), 1)
    return tuple(Q(a, scale) for a in vector)


def test_signature(reward, states, actions):
    # At gamma=1/2 the baseline value is 2 times its immediate reward.
    def vector(anchor):
        return tuple(
            reward[s*actions+a] +
            reward[(anchor if anchor is not None and a == 1 else s)*actions] -
            2*reward[s*actions]
            for s in range(states) for a in range(1, actions))
    return tuple(ray(vector(anchor)) for anchor in (None, *range(states)))


def check_state_action():
    configs = ((1, 2, (0, 1, 2)), (1, 3, (0, 1, 2)), (2, 2, (0, 1, 2)),
               (2, 3, (0, 1)), (3, 2, (0, 1)))
    count = 0
    for states, actions, alphabet in configs:
        rows = [(test_signature(table, states, actions), ray(tuple(x-table[0] for x in table)))
                for table in product(alphabet, repeat=states*actions)]
        for (test_a, affine_a), (test_b, affine_b) in product(rows, repeat=2):
            assert (test_a == test_b) == (affine_a == affine_b)
            count += 1
    return count


def check_visual():
    for i in range(21):
        p = Q(i, 20)
        strict = (2*p-1, 3*p-1)
        boundary = (p, Q(1))
        assert tuple(map(sign, strict)) == ((i > 10)-(i < 10), (3*i > 20)-(3*i < 20))
        assert tuple(map(sign, boundary)) == (int(i > 0), 1)


if __name__ == "__main__":
    print(f"{check_policy_returns():,} exact occupancy-policy return identities passed.")
    check_grids()
    print("All 14 quadratic interpolation grids passed exact rank and domain checks.")
    print(f"{check_state_action():,} ordered state-action table pairs match the star-kernel test.")
    check_visual()
    print("All 42 illustrated sign tests passed, including an interior reversal and a boundary tie.")

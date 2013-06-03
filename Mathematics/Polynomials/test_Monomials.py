
import unittest
from numpy.random import randint

from .Nomials import Monomial, Polynomial

TEST_COUNT = 3;

def get_pairs_random_monomials(test_count):
    coeffs_A = [randint(-10, 10) for idx in range(test_count)]
    coeffs_B = [randint(-10, 10) for idx in range(test_count)]
    coeffs_C = [randint(-10, 10) for idx in range(test_count)]
    powers_A = [[randint(-10, 10) for idx in range(power_count)] for power_count in range(test_count)]
    powers_B = powers_A
    powers_C = [[this_power + 1 for this_power in A_tuple] for A_tuple in powers_A]
    monos_A = [Monomial(this_coeff, these_powers) for this_coeff, these_powers in zip(coeffs_A, powers_A)]
    monos_B = [Monomial(this_coeff, these_powers) for this_coeff, these_powers in zip(coeffs_B, powers_B)]
    monos_C = [Monomial(this_coeff, these_powers) for this_coeff, these_powers in zip(coeffs_C, powers_C)]
    return (coeffs_A, powers_A, monos_A, coeffs_B, powers_B, monos_B, coeffs_C, powers_C, monos_C)




class IsEqualTest:
    def __init__(self, desc):
        self.description = 'Mathematics.Polynomials.Monomials.' + desc
    def __call__(self, left, right): 
        assert left == right

class IsInstanceTest:
    def __init__(self, desc):
        self.description = 'Mathematics.Polynomials.Monomials.' + desc
    def __call__(self, obj, cls):
        assert isinstance(obj, cls)



def test_equality_zero_generator():
    A_coeffs, A_powers, A_monos, _, _, _, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        A_monos[test_idx].coeff = 0
        yield IsEqualTest('Equality.Zero(%i)' % test_idx), A_monos[test_idx], 0

def test_equality_identity_generator():
    A_coeffs, A_powers, A_monos, _, _, _, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Equality.Identity(%i)' % test_idx), A_monos[test_idx], A_monos[test_idx]

def test_equality_equivalence_generator():
    A_coeffs, A_powers, A_monos, _, _, _, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Equality.Equivalence(%i)' % test_idx), A_monos[test_idx], Monomial(A_coeffs[test_idx], A_powers[test_idx])

def test_unary_positive_generator():
    A_coeffs, A_powers, A_monos, _, _, _, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Unary.Positive(%i)' % test_idx), +A_monos[test_idx], Monomial(A_coeffs[test_idx], A_powers[test_idx])

def test_unary_negative_generator():
    A_coeffs, A_powers, A_monos, _, _, _, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Unary.Negative(%i)' % test_idx), -A_monos[test_idx], Monomial(-1 * A_coeffs[test_idx], A_powers[test_idx])

def test_addition_return_generator():
    A_coeffs, A_powers, A_monos, _, _, _, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsInstanceTest('Addition.ReturnType(%i)' % test_idx), A_monos[test_idx], Monomial

def test_addition_matched_degree_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Addition.MatchedDegree(%i)' % test_idx), A_monos[test_idx] + B_monos[test_idx], Monomial(A_coeffs[test_idx] + B_coeffs[test_idx], A_powers[test_idx])

def test_addition_unmatched_degree_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos, _, _, C_monos = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Addition.UnmatchedDegree(%i)' % test_idx), A_monos[test_idx] + C_monos[test_idx], Polynomial([A_monos[test_idx], C_monos[test_idx]])

def test_subtraction_matched_degree_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Subtraction.MatchedDegree(%i)' % test_idx), A_monos[test_idx] - B_monos[test_idx], Monomial(A_coeffs[test_idx] - B_coeffs[test_idx], A_powers[test_idx])

def test_subtraction_unmatched_degree_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos, _, _, C_monos = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Subtraction.UnmatchedDegree(%i)' % test_idx), A_monos[test_idx] - C_monos[test_idx], Polynomial([A_monos[test_idx], -1 * C_monos[test_idx]])

def test_multiplication_generator():
    for test_idx in range(TEST_COUNT):
        var_count = randint(1, 5)
        M1 = Monomial.random(var_count=var_count)
        M2 = Monomial.random(var_count=var_count)
        yield IsEqualTest('Multiplication(%i)' % test_idx), M1 * M2, Monomial(M1.coeff * M2.coeff, M1.powers + M2.powers)
    assert False

def test_division_generator():    
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Division(%i)' % test_idx), A_monos[test_idx] / B_monos[test_idx], Monomial(A_coeffs[test_idx] / B_coeffs[test_idx], [a - b for a, b in zip(A_powers[test_idx], B_powers[test_idx])])

def test_power_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        int_pwr = randint(-10, 10)
        if A_coeffs[test_idx] == 0:
            assert True 
        yield IsEqualTest('Power(%i)' % test_idx), A_monos[test_idx]**int_pwr, Monomial(A_coeffs[test_idx]**int_pwr, A_powers[test_idx]*int_pwr)

def test_evaluate_zero_value():
    A_coeffs, A_powers, A_monos, _, _, _, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        A_vals = A_powers[test_idx] * 0
        yield IsEqualTest('Evaluate.ZeroValue(%i)' % test_idx), A_mono.evaluate(A_vals), 0

def A_coeffs, A_powers, A_monos, _, _, _, _, _, _ = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        A_monos[test_idx].powers = A_powers[test_idx] * 0
        yield IsEqualTest('Evaluate.ZeroValue(%i)' % test_idx), A_mono.evaluate(A_vals), 0
 
    
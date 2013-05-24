
import unittest
from random import randrange

from .Nomials import Monomial, Polynomial

TEST_COUNT = 3;

def get_pairs_random_monomials(test_count):
    coeffs_A = [randrange(-10, 10) for idx in range(test_count)]
    coeffs_B = [randrange(-10, 10) for idx in range(test_count)]
    powers_A = [[randrange(-10, 10) for idx in range(power_count)] for power_count in range(test_count)]
    powers_B = [[randrange(-10, 10) for idx in range(len(this_tuple))] for this_tuple in powers_A]
    monos_A = [Monomial(this_coeff, these_powers) for this_coeff, these_powers in zip(coeffs_A, powers_A)]
    monos_B = [Monomial(this_coeff, these_powers) for this_coeff, these_powers in zip(coeffs_B, powers_B)]
    return (coeffs_A, powers_A, monos_A, coeffs_B, powers_B, monos_B)




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
        



def test_equality_identity_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Equality.Identity(%i)' % test_idx), A_monos[test_idx], A_monos[test_idx]

def test_equality_equivalence_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Equality.Equivalence(%i)' % test_idx), A_monos[test_idx], Monomial(A_coeffs[test_idx], A_powers[test_idx])

def test_unary_positive_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Unary.Positive(%i)' % test_idx), +A_monos[test_idx], Monomial(A_coeffs[test_idx], A_powers[test_idx])

def test_unary_negative_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Unary.Negative(%i)' % test_idx), -A_monos[test_idx], Monomial(-1 * A_coeffs[test_idx], A_powers[test_idx])

def test_addition_return_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsInstanceTest('Addition.ReturnType(%i)' % test_idx), A_monos[test_idx], Monomial

def test_addition_matched_degree_generator():
    A_coeffs, A_powers, A_monos, B_coeffs, B_powers, B_monos = get_pairs_random_monomials(TEST_COUNT)
    for test_idx in range(TEST_COUNT):
        yield IsEqualTest('Addition.MatchedDegree(%i)' % test_idx), A_monos[test_idx] + B_monos[test_idx], Monomial(A_coeffs[test_idx] + B_coeffs[test_idx], A_powers[test_idx])

    

class TestMonomialAddition(unittest.TestCase):

    def setUp(self):
        self.A = Monomial(1, [1, 2])
        self.B = Monomial(-4, [1, 2])
        self.C = Monomial(3, [0, 1])
        self.D = Monomial(1, [1, 2, 3])

 
    def test_addition_mismatched_degree(self):
        self.assertEqual(self.A + self.C, Polynomial([Monomial(1, [1, 2]), Monomial(3, [0, 1])]))
    def test_addition_mismatched_variables(self):
        self.assertRaises(TypeError, self.A + self.D)


class TestMonomialSubtraction(unittest.TestCase):
    
    def setUp(self):
        self.A = Monomial(1, [1, 2])
        self.B = Monomial(-3, [1, 2])
        self.C = Monomial(3, [0, 1])
        self.D = Monomial(1, [1, 2, 3]) 
        
    def test_subtraction_return_type(self):
        self.assertIsInstance(self.A - self.B, Polynomial)
    def test_subtraction_matched_degree(self):
        self.assertEqual(self.A - self.B, Polynomial([Monomial(4, [1, 2])]))
    def test_subtraction_mismatched_degree(self):
        self.assertEqual(self.A - self.C, Polynomial([Monomial(1, [1, 2]), Monomial(-3, [0, 1])]))
    def test_subtraction_mismatched_variables(self):
        self.assertRaises(TypeError, self.A + self.D)
        

class TestMonomialMultiplication(unittest.TestCase):
    
    def setUp(self):
        self.A = Monomial(1, [1, 2])
        self.B = Monomial(-3, [1, 2])
        self.C = Monomial(3, [0, 1])
        self.D = Monomial(1, [1, 2, 3]) 

    def test_multiplication_return_type(self):
        self.assertIsInstance(self.A * self.B, Monomial)
    def test_multiplication_matched_variables(self):
        self.assertEqual(self.A * self.B, Monomial(-3, [2, 4]))
    def test_multiplication_scalar(self):
        self.assertEqual(self.A * 3, Monomial(3, [1, 2]))

class TestMonomialDivision(unittest.TestCase):
    
    def setUp(self):
        self.A = Monomial(1, [1, 2])
        self.B = Monomial(-3, [1, 2])
        self.C = Monomial(3, [0, 1])
        
#===============================================================================
#             A = Monomial(1, [1, 2])
#     B = Monomial(2, [1, 0])
#     C = Monomial(3, [0, 1])
#     D = Monomial(1, [0, 0])
#     
#     print("A = %s" % str(A))
#     print("B = %s" % str(B))
#     print("C = %s" % str(C))
#     print("D = %s" % str(D))
#     
#     TF_str = lambda b: 'TRUE' if b else 'FALSE'
#     
#     print("A == A:  %s" % TF_str(A==A))
#     print("A == B:  %s" % TF_str(A==B))
#     print("A != A:  %s" % TF_str(A!=A))    
#     
#     P = A + A
#     Q = A + B
#     R = A + C
#     
#     print("P = A + A = %s" % str(P))
#     print("Q = A + B = %s" % str(Q))
#     print("R = A + C = %s" % str(R))
#     print("A + 3 = %s" % str(A + Monomial(3, [0, 0])))
#     print("3 + A = %s" % str(Monomial(3, [0, 0]) + A))
# #     
#     print("A * A = %s" % str(A * A))
#     print("A**2 = %s" % str(A**2))
#     print("A * A == A**2:  %s" % TF_str(A*A == A**2))
#     print("A * B = %s" % str(A * B))
#     print("C * D = %s" % str(C * D))
#     print("3 * A = %s" % str(3 * A))
#     print("A * 5 = %s" % str(A * 5))
#     print("A / A = %s" % str(A / A))
#     print("A / B = %s" % str(A / B))
#     print("B / D = %s" % str(B / D))
#     print("C / 3 = %s" % str(C / 3))
#     print("Q**3 = %s" % str(Q**3))
#     
#     print("\n\n")
#     S = Polynomial([Monomial(1, [0, 1]), Monomial(1, [0, 0])])
#     T = Polynomial([Monomial(1, [0, 1]), Monomial(-1, [0, 0])])
#     U = Polynomial([Monomial(1, [1, 0]), Monomial(1, [0, 1])])
#     
#     print("S = %s" % str(S))
#     print("T = %s" % str(T))
#     print("U = %s" % str(U))
#      
#     print("S * T = %s" % str(S * T))
#     print("S * U = %s" % str(S * U))
#     
#     print("\n")
#     print("Q(a, b) = %s" % str(Q))
#     print("Q(1, 1) = %s" % str(Q.evaluate([1, 1])))
#     print("Q(0, A) = %s" % str(Q.evaluate([0, A])))
#     print("Q(1, A) = %s" % str(Q.evaluate([1, A])))
#     
#     
#     
#     
#     
# #     suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
# #     unittest.TextTestRunner(verbosity=2).run(suite)
#===============================================================================
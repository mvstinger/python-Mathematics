
from numpy import (arange, argmin, array, base_repr, eye, floor, insert, mod, nonzero, prod, roll, sum, transpose, zeros)
from numpy import long as TYPE_INT




from .. import get_prime_factors, nullity



#    CLASSES
class FiniteField(TYPE_INT):
    #    CONSTRUCTOR
    def __new__(cls, idx, p, m, prim_poly=None):
        return super(FiniteField, cls).__new__(cls, idx)
        
    def __init__(self, idx, p, m, prim_poly=None):
        #   Assign members
        self.p = p
        self.m = m
        self.order = p**m
        #    Set idx
        self.idx = idx % (self.p**m)
        #    Get primitive polynomial
        if prim_poly==None:
            self.prim_poly = get_primitive_polynomial(p, m)
        else:
            if is_primitive_polynomial(prim_poly, p, m):
                self.prim_poly = prim_poly
            else:
                raise Exception('Supplied polynomial is not primitive in (p = %i, m = %i)' % (p, m))
        #    Create table of elements
        self.table = self._get_elements();

    #    COMPARISONS
    def __cmp__(self, other):
        raise NotImplemented


    #    ARITHMETIC
    def __add__(self, other):
        coeffs = (self.get_coeffs() + other.get_coeffs()) % self.p
        return FiniteField(self._coeffs_to_idx(coeffs), self.p, self.m, self.prim_poly)
    
    def __sub__(self, other):
        coeffs = (self.get_coeffs() - other.get_coeffs()) % self.p
        return FiniteField(self._coeffs_to_idx(coeffs), self.p, self.m, self.prim_poly)
    
    def __mul__(self, other):
        if self.idx == 0 or other.idx == 0:
            return FiniteField(0, self.p, self.m, self.prim_poly)
        pwr = (self.get_power() + other.get_power()) % self.order
        return FiniteField(self._pwr_to_idx(pwr), self.p, self.m, self.prim_poly)
    
    def __div__(self, other):
        pwr = (self.get_power() - other.get_power()) % self.order
        return FiniteField(self._pwr_to_idx(pwr), self.p, self.m, self.prim_poly)

    def __pow__(self, pow):
        pwr = (self.get_power() * pow) % self.order
        return FiniteField(self._pwr_to_idx(pwr), self.p, self.m, self.prim_poly)
    
    
    #    HELPER FUNCTIONS
    def _idx_to_pwr(self, idx):
        """Return primitive power corresponding to index."""
        return idx - 1
    
    def _pwr_to_idx(self, pwr):
        """Return index corresponding to primitive power."""
        return pwr + 1
    
    def _idx_to_coeffs(self, idx):
        """Return coefficients for polynomial of index."""
        return self.table[idx]
    
    def _pwr_to_coeffs(self, pwr):
        """Return coefficients for primitive power."""
        return self.table(self._pwr_to_idx(pwr))
    
    def _coeffs_to_idx(self, coeffs):
        """Return index of element with coefficients."""
        #    Modulo coefficients
        coeffs = coeffs % self.order
        #    Find coefficients in table
        return argmin(sum((self.table - coeffs)**2, axis=1))
        
    def get_coeffs(self):
        """Return the coeffs of this FiniteField."""
        return self._idx_to_coeffs(self.idx)

    def get_power(self):
        """Return power of this FiniteField."""
        return self._idx_to_pwr(self.idx)
        
                    
    def _get_elements(self):
        """Calculate the table of elements comprising the finite field."""
        #    Predimension variables
        table = zeros((self.order, self.m))
        #    Calculate table
        #        First produce identity matrix
        table[1:(self.m + 1), :] = eye(self.m)
        #        Enter row for primitive polynomial
        table[(self.m + 1), :] = self.prim_poly[0:-1]
        #        Fill in remaining rows
        for row_idx in range(self.m + 2, self.order):
            table[row_idx, :] = roll(table[row_idx - 1, :], 1)
            table[row_idx, 0] = 0
            if table[row_idx - 1, -1] != 0:
                table[row_idx, :] = mod(table[row_idx, :] + mod(table[row_idx - 1, -1] * self.prim_poly[0:-1], self.p), self.p)
        #    Return table
        return table

    def form_mult_table(self):
        elem_cnt = self.order
        #    Produce top row and middle rule
        ret_str = " x |" + "".join([(" %i " % elem) for elem in range(self.order)]) + "\n"
        ret_str += ("---+" + "---" * elem_cnt) + "\n"
        #    Produce rows
        for row_idx in range(self.order):
            these_elems = [FiniteField(elem, self.p, self.m) * FiniteField(row_idx, self.p, self.m) for elem in range(self.order)]
            ret_str += (" %i |" % row_idx) + "".join([" %i " % elem for elem in these_elems]) + "\n"
            
#            print("\n\nrow %i" % row_idx)
#            print(these_elems)
        #    Return string
        return ret_str

    def form_add_table(self):
        elem_cnt = self.order
        #    Produce top row and middle rule
        ret_str = " + |" + "".join([(" %i " % elem) for elem in range(self.order)]) + "\n"
        ret_str += ("---+" + "---" * elem_cnt) + "\n"
        #    Produce rows
        for row_idx in range(self.order):
            these_elems = [FiniteField(elem, self.p, self.m) + FiniteField(row_idx, self.p, self.m) for elem in range(self.order)]
            ret_str += (" %i |" % row_idx) + "".join([" %i " % elem for elem in these_elems]) + "\n"
            
#            print("\n\nrow %i:  %i + ..." % (row_idx, row_idx))
#            print(these_elems)
        #    Return string
        return ret_str

    def form_prim_poly(self):
        ret_list = ["%iX^%i" % (elem, order) for order, elem in enumerate(self.prim_poly)]
        return " + ".join(ret_list)




#    FUNCTIONS        
def get_primitive_polynomial(p, m):
    """Find a primitive polynomial of GF(p^m)."""
    #    Based on algorithm at:
    #    http://www.seanerikoconnor.freeservers.com/Mathematics/AbstractAlgebra/PrimitivePolynomials/theory.html

    #    Generate all p**m possible coefficients
    for coeff_idx in range(p**m, p**(m + 1)):
        #    Calculate all coefficients base p
        #        (Note that base_repr returns numbers with the least significant nit in the last column.)
        coeffs = [int(aux_str) for aux_str in base_repr(coeff_idx, p)]
        coeffs = coeffs[::-1]

        if is_primitive_polynomial(coeffs, p, m):
            return coeffs

    #    If no primitve polynomial is found, return the empty set
    return []


def get_generator_polynomial(p, m):
    """"Find a generator polynomial for GF(p^m)"""
#    http://www.thonky.com/qr-code-tutorial/how-create-generator-polynomial/

def polynomial_division(dividend, divisor, q=None):
    """Polynomial division optionally in GF(q)."""
    #    Get various orders
    dividend_ord = nonzero(dividend)[0][-1]
    divisor_ord = nonzero(divisor)[0][-1]
    max_ord = max((dividend_ord, divisor_ord))
    #    Pad dividend_coeffs and divisor coefficients to same size
    dividend_coeffs = zeros(max_ord + 1, dtype=TYPE_INT)
    dividend_coeffs[0:len(dividend)] = dividend
    divisor_coeffs = zeros(max_ord + 1, dtype=TYPE_INT)
    divisor_coeffs[0:len(divisor)] = divisor
    #    Predimension quotient_coeffs coefficients
    quotient_coeffs = zeros(max_ord + 1, dtype=TYPE_INT)

    #    Count down from order of dividend_coeffs
    for this_ord in range(max_ord, divisor_ord - 1, -1):       
        #    If the current dividend_coeffs order is zero, skip it.
        if dividend_coeffs[this_ord] == 0:
            continue

        #    What is the order of the current idx entered into the quotient_coeffs?
        quotient_ord = this_ord - divisor_ord

        #    If the current divisor_coeffs is zero, the quotient is zero
        quotient_coeffs[quotient_ord] = floor(dividend_coeffs[this_ord] / divisor_coeffs[divisor_ord])

        #    Get the current coefficient for the quotient_coeffs
        aux_divisor_coeffs = insert(divisor_coeffs, [0]*quotient_ord, zeros(quotient_ord, dtype=TYPE_INT))
        dividend_coeffs -= quotient_coeffs[quotient_ord] * aux_divisor_coeffs[0:len(dividend_coeffs)]
        
        #    If division in GF(q), return dividend coefficients modulo q
        if q != None:
            dividend_coeffs = dividend_coeffs % q

        #    Update dividend order
        dividend_ord = nonzero(dividend)[0][-1]
    
    #    Return quotient_coeffs and remainder
    remainder_coeffs = dividend_coeffs
    return quotient_coeffs, remainder_coeffs


def multiplicative_order(n, k):
    """Return the multiplicative order of n base k."""
    MAX_ORD = 20;
    for trial_ord in xrange(2, MAX_ORD):
        if (k**trial_ord) % n == 1:
            return trial_ord
    return None


def is_primitive_root(a, p):
    """Return if a is a primitive root modulo p."""
    #    Check that mod(a**k, p) != 1 for k = 1...p-2 
    aux = a**arange(1, p-1)
    if any(aux % p == 1):
        return False
    #    Check that mod(a**(p-1), p) == 1
    return (a**(p - 1) % p) == 1


def polynomial_has_linear_factor(coeffs, p):
    """Return if a polynomial has any linear factors."""
    for this_x in range(0, p):
        f_of_this_x = mod(sum([(this_coeff * this_x**this_pwr) % p for this_pwr, this_coeff in enumerate(coeffs)]), p)
        if f_of_this_x == 0:
            return True
    return False
    

def is_primitive_polynomial(coeffs, p, m, debug=False):
    """Find a primitive polynomial of GF(p^m)."""
    #    Based on algorithm at:
    #    http://www.seanerikoconnor.freeservers.com/Mathematics/AbstractAlgebra/PrimitivePolynomials/theory.html

    #    Calculate auxilliaries
    if debug: print("Testing polynomial %s of degree n = %s modulo p = %s for primitivity" % (coeffs, m, p))
    
    r = (p**m - 1)/(p - 1)
    primes_to_check = list(set(get_prime_factors(r)))

    if debug: print("Prime factorization: %s" % primes_to_check)


    #    Check that (-1)**n a0 is a primitive root of p
    if not is_primitive_root(coeffs[0] * (-1)**m, p):
        if debug: print(">>>Note primitive:  const coeff a0 fails the primitive root test.")
        return []
    else:
        if debug: print("Const coeff a0 = %s passes primitive root test." % coeffs[0])
    
    
    #    Test for linear coefficients for all a: 1 <= x <= (p - 1)
    if polynomial_has_linear_factor(coeffs, p):
        if debug: print(">>>Not primitive:  contains one or more linear factors.")
        return []
    else:
        if debug: print("No linear factors")


    #    Check if f(x) has two or more irreducible factors
    if debug: print("Powers of x in Q matrix rows = NA")
    QI_mat = zeros((m, m))
    for k in range(m):
        X_kp = array([0] * (k * p) + [1])
        [aux, rem] = polynomial_division(X_kp, coeffs, p)
        QI_mat[k, :] = rem[0:m]
    QI_mat = (QI_mat - eye(m)) % p
    left_nullity = nullity(transpose(QI_mat))
        
    if debug: print("Q - I = %s" % QI_mat)
    if debug: print("Nullity = %i" % left_nullity)
        
    if left_nullity > 1:
        if debug: print(">>>Not primitive:  two or more distinct irreducible factors.")
        return []
    else:
        if debug: print("One (possibly repeated) distinct irreducible factor.")


    #    ** Step 5 **
    X_r = array([0]*r + [1])
    [aux, a] = polynomial_division(X_r, coeffs, p)
    if a[0] != mod(sum(a), p):
        if debug: print(">>>Not primitive:  fails the x^r = a test")
        return []
    else:
        if debug: print("Pass test for x^r = a = integer = %s" % a[0])


    #    ** Step 6 **
    if ((-1)**m * coeffs[0] - a[0]) % p:
        if debug: print(">>>Not primitive:  fails the const coeff test")
        return []
    else:
        if debug: print("Const coeff test passes.")


    #    Test that remainder of X**m / P(X) = a * X**0
    for this_prime in primes_to_check:
        b = r / this_prime
        if ((p - 1) % this_prime) == 0:
            if debug: print("Skipping test for m = %s since pi = %s | p - 1 = %s" % (m, this_prime, p-1))

        [aux, a] = polynomial_division([0] * m + [1], coeffs, p)
        if a[0] == sum(a):
            if debug: print(">>>Not primitive:  failed the a = integer test")
            continue
        else:
            if debug: print("Pass test for x^m = a = %s != integer to m = %s, pi = %s" % (a[0], b, this_prime))


    #    If this point is reached, the polynomial defined by the coefficients coeffs is a
    #        primitive polynomial of degree m, modulo p.
    #    Format and return
    return coeffs
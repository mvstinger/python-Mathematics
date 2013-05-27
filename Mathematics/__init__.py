

from itertools import chain

from numpy import (arange, ceil, compress, floor, log10, insert, ones,
                   sqrt, transpose, zeros)
from numpy.linalg import matrix_rank, svd



def get_primes(n):
    """Return the prime integers up to and including n."""
    #    Handle n = 1 or 2
    if n==1:
        return [1]
    elif n==2:
        return [1, 2]
    #    Handle n > 2
    primes = arange(3, n + 1, 2)
    is_prime = ones((n - 1) / 2, dtype=bool)
    for factor in primes[:int(sqrt(n))]:
        if is_prime[(factor - 2) / 2]:
            is_prime[(factor * 3 - 2) / 2::factor] = 0
    return insert(primes[is_prime], 0, 2)


def get_prime_factors(n):
    """Return the prime factors of an integer."""
    result = []
    # test 2 and all of the odd numbers
    # xrange instead of range avoids constructing the list
    for i in chain([2], xrange(3, n + 1, 2)):
        s = 0
        while n/float(i)==floor(n/float(i)): # is n/i an integer?
            n /= i
            s += 1
            result.extend([i]*s) #avoid another for loop
            if n==1:
                return result


def null(A, eps=1e-15):
    u, s, vh = svd(A)
    null_mask = (s <= eps)
    null_space = compress(null_mask, vh, axis=0)
    return transpose(null_space)


def nullity(A):
    dims = A.shape
    return dims[1] - matrix_rank(transpose(A))


def x_base_b(x, new_base, old_base=10, length=None, big_endian=True):
    """Convert a value into a new base."""
    raise NotImplementedError()
    #    Convert number to decimal
#     if old_base ~= 10:
#         x = sum([coeff * old_base**order for order, coeff in enumerate(x)])
#     #    Get minimum number of digits
#     digit_count = ceil(log10(x) / log10(new_base))
#     y = zeros((1, digit_count))
#     #    Loop over order of new base
#     for order_idx in range(digit_count):
#         this_order = digit_count - order_idx
#         this_power = new_base**order_idx
#         y[order_idx] = x // new_base
#         x = None 
    








    
    
    
    
    







if __name__ == "__main__":
    import nose  # @UnresolvedImport
    nose_tr = nose.core.TextTestRunner(verbosity=3)
    nose.main(testRunner=nose_tr)
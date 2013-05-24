from string import ascii_lowercase



def simplify(nomials):
    """Simplify a list of Mono- and Polynomials."""
    #    Parse inputs
    these_monos = []
    for this_obj in nomials:
        if isinstance(this_obj, Polynomial):
            these_monos += this_obj.monomials
        else:
            these_monos += [this_obj]
    #    Loop over monos, combining like powers
    #    For a list with N monos, compare the first N-1 against those remaining in the list.
    #    While there are more monos in the list,
    #    For each mono in the list,
    #        Compare to all subsequent monos in the list
    #        If there is a match,
    #            Roll new mono into current
    #            Remove the matching mono from the list

    this_mono_idx = 0
    while this_mono_idx <= (len(these_monos) - 2):
        #    Get this mono
        this_mono = these_monos[this_mono_idx]
        #    Compare this_mono to all subsequent monos in list
        for that_mono_idx in range(len(these_monos) - 1, this_mono_idx, -1):
            #    Get comparitor mono
            that_mono = these_monos[that_mono_idx]
            #    If a match is found
            if this_mono.powers == that_mono.powers:
                #    Roll matching mono into current
                this_mono = Monomial(this_mono.coeff + that_mono.coeff, this_mono.powers)
                #    Remove matching mono from list
                these_monos.pop(that_mono_idx)
        #    All matching monos have been rolled into this_mono
        these_monos[this_mono_idx] = this_mono;
        #    Increment this_mono_idx
        this_mono_idx += 1
    #    All monomials have been reconciled
    #    Remove any zeros (unless there is only one term)
    if len(these_monos) > 1:
        for mono_idx, this_mono in enumerate(these_monos):
            if this_mono.coeff == 0:
                these_monos.pop(mono_idx)
    return these_monos








class Monomial(object):
    """Class to implement a monomial."""
    #    CONSTRUCTOR
    def __init__(self, c, P):
        """Constructor for Monomial."""
        self.coeff = c
        self.powers = P
    
    
    #    STRING
    def __str__(self, var_chars=ascii_lowercase):
        #    Write coefficient
        if self.coeff == 0:
            ret = "0"
            return ret
        else:
            ret = "{0.coeff:0.4g}".format(self)
        #    Write list of characters
        for var_idx, this_power in enumerate(self.powers):
            if this_power == 0:
                continue
            elif this_power == 1:
                ret += " {0}".format(var_chars[var_idx])
            else:
                ret += " {0}^{1:0.4g}".format(var_chars[var_idx], this_power)
        #    Return string
        return ret
    
    
    #    COMPARISON
    def __eq__(self, other):
        if isinstance(other, Polynomial) and len(other.monomials)==1:
            other = other.monomials[0]
        if isinstance(other, Monomial):
            if (self.coeff == other.coeff) and (self.powers == other.powers):
                return True
        return False

    def __ne__(self, other):
        return not self==other

    #    UNARY OPERATORS
    def __pos__(self):
        return self
    
    def __neg__(self):
        return Monomial(-1 * self.coeff, self.powers)
   
        
   
    #   ARITHMETIC
    def __add__(self, other):
        return Polynomial([self, other])
    
    def _radd_(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        return Polynomial([self, -other])

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, Monomial):
            return Monomial(self.coeff * other.coeff, [sp + op for sp, op in zip(self.powers, other.powers)])
        else:
            return Monomial(self.coeff * other, self.powers)
       
    def __rmul__(self, other):
        return self.__mul__(other)
       
    def __div__(self, other):
        return self**(-1) * other
     
    def __rdiv__(self, other):
        return self**(-1) * other
    
    def __truediv__(self, other):
        return self * other**(-1)
    
    def __pow__(self, other):
        return Monomial(self.coeff**other, [sp * other for sp in self.powers])


    #    HELPER FUNCTIONS
    def evaluate(self, these_vars):
        new_mono = Monomial(self.coeff, [0]*len(self.powers))
        for var_idx, this_var_pwr in enumerate(self.powers):
            new_mono *= these_vars[var_idx]**this_var_pwr 
        return new_mono














class Polynomial(object):
    
    #   CONSTRUCTOR
    def __init__(self, M):
        """Constructor for Polynomial."""
        self.monomials = simplify(M);
        
    #   STRING
    def __str__(self):
        ret = str(self.monomials[0])
        for mono_idx in range(1, len(self.monomials)):
            ret += ' + ' + str(self.monomials[mono_idx])
        return ret
    
    #    COMPARISON
    
    
    #    ARITHMETIC
    def __add__(self, other):
        return Polynomial([self, other])
    
    def __sub__(self, other):
        return Polynomial([self, -1 * other])
    
    def __mul__(self, other):
        #    Parse inputs
        if isinstance(other, Polynomial):
            other_monos = other.monomials
        else:
            other_monos = [other]
        #    Multiply piecewise
        monos = []
        for this_self_mono in self.monomials:
            for this_other_mono in other_monos:
                monos += [this_self_mono * this_other_mono]
        #    Return Polynomial with monos
        return Polynomial(monos)
    
    def __rmult__(self, other):
        return self.__mult__(other)
    
    def __div__(self, other):
        raise NotImplementedError('Division not implemented for polynomials')
    
    def __rdiv__(self, other):
        raise NotImplementedError('Division not implemented for polynomials')
    
    def __truediv__(self, other):
        raise NotImplementedError('Division not implemented for polynomials')
    
    def __pow__(self, other):
        ret = self
        for power_idx in range(other):
            ret *= self
        return ret
    
    def evaluate(self, vars):
        ret = Monomial(0, [0]*len(self.monomials))
        for M in self.monomials:
            aux = M.evaluate(vars)
            ret = ret + aux
        return ret
        
    
    
    
    
    
    
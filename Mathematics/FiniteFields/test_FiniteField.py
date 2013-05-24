# from .. import FiniteField
from .FiniteField import FiniteField 


class TestFiniteFieldConstructor():
    
    def setUp(self):
        self.obj_A = FiniteField(1, 2, 8)
    
    def test_simple_constructor(self):
        assert isinstance(self.obj_A, FiniteField)
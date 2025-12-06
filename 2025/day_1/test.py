from func import rot_dial, point_at_zero

class TestModFn:
    def test_mod_fn_0(self):
        assert rot_dial(0,0) == 0

    def test_mod_fn_1(self):
        assert rot_dial(10,-20) == 90

    def test_mod_fn_2(self):
        assert rot_dial(10,91) == 1


class TestPointAtZero:
    def test_start_zero(self):
        assert point_at_zero(0,0)==0
        assert point_at_zero(0,1)==0
        assert point_at_zero(0,-1)==0
        assert point_at_zero(0,1000)==10
        assert point_at_zero(0,1005)==10
        assert point_at_zero(0,-999)==9
        assert point_at_zero(0,-1000)==10
        assert point_at_zero(0,-1001)==10
    
    def test_less_one_turn(self):
        assert point_at_zero(10,10)==0
        assert point_at_zero(90,-10)==0
    
    def test_many_turns(self):
        assert point_at_zero(10,191)==2
        assert point_at_zero(10,1901)==19
        assert point_at_zero(80,-3001)==30
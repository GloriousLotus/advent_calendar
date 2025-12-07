from func import is_invalid_id_n, prev_rep, slice_n, next_rep

class TestSlice:
    def test_slice_nice(self):
        x = "123456"
        assert slice_n(x,1) == [x]
        assert slice_n(x,2) == ["123","456"]
        assert slice_n(x,3) == ["12","34","56"]
        assert slice_n(x,6) == ["1","2","3","4","5","6"]

    def test_slice_not_nice(self):
        assert prev_rep("115",2) == "9"
        assert prev_rep("115",3) == "1"
        assert next_rep("99",3) == "1"
        x = "12345678"
        assert slice_n(x,3) == ["12","34","56"]
        assert prev_rep(x,2) == "1234"
        assert next_rep(x,2) == "1235"
        assert prev_rep(x,3) == "99"
        assert next_rep(x,3) == "100"
        assert prev_rep(x,4) == "12"
        assert next_rep(x,4) == "13"
        y = "78134512"
        assert prev_rep(y,4) == "77"
        assert next_rep(y,4) == "78"
        assert next_rep(y,1) == y
        assert next_rep(y,8) == "8"
        assert next_rep("999",1) == "999"
        z = "123456123"
        assert prev_rep(z,3) == "123"
        assert next_rep("1919163519",5) == "19"
        assert prev_rep("1919240770",5) == "19"

    def test_invalid_id(self):
        x = "123123"
        y = x+"4"
        assert is_invalid_id_n(x,1) == False
        assert is_invalid_id_n(x,2) == True
        assert is_invalid_id_n(x,3) == False
        assert is_invalid_id_n(y,2) == False
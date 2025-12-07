from func import is_invalid_id_n, slice_n, next_n

class TestSlice:
    def test_slice_nice(self):
        x = "123456"
        assert slice_n(x,1) == [x]
        assert slice_n(x,2) == ["123","456"]
        assert slice_n(x,3) == ["12","34","56"]
        assert slice_n(x,6) == ["1","2","3","4","5","6"]

    def test_slice_not_nice(self):
        x = "12345678"
        assert slice_n(x,3) == ["12","34","56"]
        assert next_n(x,2) == ["1235","1235"]
        assert next_n(x,3) == ["100","100","100"]
        assert next_n(x,4) == ["13","13","13","13"]
        y = "78134512"
        assert next_n(y,4) == ["78","78","78","78"]
        assert next_n(y,1) == ["8" for _ in y]
        assert next_n("999",1) == ["1","1","1","1"]

    def test_invalid_id(self):
        x = "123123"
        y = x+"4"
        assert is_invalid_id_n(x,1) == False
        assert is_invalid_id_n(x,2) == True
        assert is_invalid_id_n(x,3) == False
        assert is_invalid_id_n(y,2) == False
key_length = (
    # length, expected_result
    (-1, 5),
    (0, 5),
    (5, 5),
    (10, 5),
)

wrong_key_length_type = (
    # invalid key_length
    ("",),
    (1.1,),
    (None,),
    (True,),
    ("test",),
    ([1],),
    ([1, 2, 3, 4, 5],),
)

post_valid_data = (
    # target_url
    ('https://www.google.com/',),
    (
        'https://www.amazon.de/stores/page/'
        'AA21D600-E0B2-4B7C-9068-C5FF5C371702?ingress=2&visitId=7a70c98c-c3c2-4bc1-aa82-c6088c4f67bc&ref_='
        'nav_cs_amazonbasics',),
    (
        'https://www.amazon.de/stores/page/6AB38617-38AD-4F09-8FD7-B8D4B8D9739C?ingress='
        '0&visitId=3226f55c-4175-403f-893e-7d874c7e1c1c&lp_slot=auto-sparkle-hsa-tetris&store_ref='
        'SB_A06017572XE2RAHSM7ENR&ref_=sbx_be_s_sparkle_mcd_hl_Oct_d_odnav_d_300992_1',),
)

post_invalid_data = (
    # invalid target_url
    ('invalid-url',),
    ('postgres://user:pass@localhost:5432/foobar',),
    ('redis://:pass@localhost',),
    ('contact@mail.com',),
    ('',),
    ('✅',),
    ([],),
    (1,),
    (1.2,),
    (None,),
    (True,),
)

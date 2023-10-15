from PyConnect4 import Connect4Board


def test_start_bitboards():
    test = Connect4Board()
    assert test.player0_bitboard == 0b0
    assert test.player1_bitboard == 0b0
    assert test.turn == 0b0
    assert test.bottom_mask == 0b1000000100000010000001000000100000010000001000000
    assert test.top_of_columns == 0b0000001000000100000010000001000000100000010000001

    test = Connect4Board(6, 7)
    assert test.bottom_mask == 0b100000001000000010000000100000001000000010000000
    assert test.top_of_columns == 0b000000010000000100000001000000010000000100000001

    test = Connect4Board(4, 4)
    assert test.bottom_mask == 0b10000100001000010000
    assert test.top_of_columns == 0b00001000010000100001

    test = Connect4Board(10, 10)
    assert test.bottom_mask == 0x2004008010020040080100200400
    assert test.top_of_columns == 0x8010020040080100200400801

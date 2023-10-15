from PyConnect4 import Connect4Board


def test_start_bitboards():
    board = Connect4Board()
    assert board.player0_bitboard == 0b0
    assert board.player1_bitboard == 0b0
    assert board.turn == 0b0
    assert board.bottom_mask == 0b1000000100000010000001000000100000010000001000000
    assert board.top_of_columns == 0b0000001000000100000010000001000000100000010000001

    board = Connect4Board(6, 7)
    assert board.bottom_mask == 0b100000001000000010000000100000001000000010000000
    assert board.top_of_columns == 0b000000010000000100000001000000010000000100000001

    board = Connect4Board(4, 4)
    assert board.bottom_mask == 0b10000100001000010000
    assert board.top_of_columns == 0b00001000010000100001

    board = Connect4Board(10, 10)
    assert board.bottom_mask == 0x2004008010020040080100200400
    assert board.top_of_columns == 0x8010020040080100200400801


def test_setups():
    board = Connect4Board("0123456654321")
    assert board.player0_bitboard == 282591736369216
    assert board.player1_bitboard == 2207747940384
    assert board.turn == 1

    board = Connect4Board("00112233445566")
    assert board.player0_bitboard == 283691315109952
    assert board.player1_bitboard == 141845657554976
    assert board.turn == 0

    board = Connect4Board("66554433221100")
    assert board.player0_bitboard == 283691315109952
    assert board.player1_bitboard == 141845657554976
    assert board.turn == 0

    board = Connect4Board("000000111111222222333333444444555555666666")
    assert board.player0_bitboard == 372344851081812
    assert board.player1_bitboard == 186172425540906
    assert board.turn == 0

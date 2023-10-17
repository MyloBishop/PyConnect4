import pytest

from PyConnect4 import Connect4Board


def test_start_bitboards():
    board = Connect4Board()
    assert board.bottom_mask == 283691315109952
    assert board.top_of_columns == 4432676798593

    board = Connect4Board(6, 7)
    assert board.bottom_mask == 141289400074368
    assert board.top_of_columns == 1103823438081

    board = Connect4Board(4, 4)
    assert board.bottom_mask == 541200
    assert board.top_of_columns == 33825

    board = Connect4Board(10, 10)
    assert board.bottom_mask == 649354174785010196826481221436416
    assert board.top_of_columns == 634134936313486520338360567809


def test_setups():
    board = Connect4Board(position="0123456654321")
    assert board.player0_bitboard == 282591736369216
    assert board.player1_bitboard == 2207747940384
    assert board.turn == 1

    board = Connect4Board(position="00112233445566")
    assert board.player0_bitboard == 283691315109952
    assert board.player1_bitboard == 141845657554976
    assert board.turn == 0

    board = Connect4Board(position="66554433221100")
    assert board.player0_bitboard == 283691315109952
    assert board.player1_bitboard == 141845657554976
    assert board.turn == 0

    board = Connect4Board(position="000000111111222222333333444444555555666666")
    assert board.player0_bitboard == 372344851081812
    assert board.player1_bitboard == 186172425540906
    assert board.turn == 0

    board = Connect4Board(10, 10, position="0123456789")
    assert board.player0_bitboard == 649037262059395257735789917765632
    assert board.player1_bitboard == 316912725614939090691303670784
    assert board.turn == 0

    board = Connect4Board(4, 4, position="0123012301230123")
    assert board.player0_bitboard == 984000
    assert board.player1_bitboard == 30750
    assert board.turn == 0


def test_undo():
    # Test for 6x7 board
    board1 = Connect4Board(6, 7, position="012345543210")
    board2 = Connect4Board(6, 7, position="01234554321")
    board1.undo_move(0)
    assert board1.player0_bitboard == board2.player0_bitboard
    assert board1.player1_bitboard == board2.player1_bitboard
    assert board1.turn == board2.turn

    # Test for 8x8 board
    board1 = Connect4Board(8, 8, position="012345543217")
    board2 = Connect4Board(8, 8, position="01234554321")
    board1.undo_move(7)
    assert board1.player0_bitboard == board2.player0_bitboard
    assert board1.player1_bitboard == board2.player1_bitboard
    assert board1.turn == board2.turn

    # Test for 4x4 board
    board1 = Connect4Board(4, 4, position="0123012301230123")
    board2 = Connect4Board(4, 4, position="012301230123012")
    board1.undo_move(3)
    assert board1.player0_bitboard == board2.player0_bitboard
    assert board1.player1_bitboard == board2.player1_bitboard
    assert board1.turn == board2.turn

    # Test for 10x10 board, double undo
    board1 = Connect4Board(10, 10, position="01234567890")
    board2 = Connect4Board(10, 10, position="012345678")
    board1.undo_move(0)
    board1.undo_move(9)
    assert board1.player0_bitboard == board2.player0_bitboard
    assert board1.player1_bitboard == board2.player1_bitboard
    assert board1.turn == board2.turn


def test_invalid_setup():
    # Test invalid position for a 6x7 board
    with pytest.raises(ValueError):
        Connect4Board(6, 7, position="01234560")

    # Test invalid position for a 8x8 board
    with pytest.raises(ValueError):
        Connect4Board(8, 8, position="01234567842")

    # Test invalid position for a 4x4 board
    with pytest.raises(ValueError):
        Connect4Board(4, 4, position="0123450")

    # Test invalid 11x11 board
    with pytest.raises(ValueError):
        Connect4Board(11, 11, position="0123456789")

    # Test another invalid position for a 6x7 board
    with pytest.raises(ValueError):
        Connect4Board(6, 7, position="01234560")

    # Test another invalid position for a 8x8 board
    with pytest.raises(ValueError):
        Connect4Board(8, 8, position="012345678421")

    # Test another invalid position for a 4x4 board
    with pytest.raises(ValueError):
        Connect4Board(4, 4, position="01234501")

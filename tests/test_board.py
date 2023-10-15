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

def order_moves(moves):
    # Center column first, then head outwards
    center = 3
    moves.sort(key=lambda move: abs(move - center))
    return moves

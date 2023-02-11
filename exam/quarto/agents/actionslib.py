from .quartolib import *
import random
import copy

def random_choose(quarto) -> int:
    return random.randint(0, 15)

def random_place(quarto) -> tuple[int, int]:
    return random.randint(0, 3), random.randint(0, 3)

def pick_piece_with_char(quarto,characteristic,possible_pieces):
    pieces=copy.deepcopy(possible_pieces)
    random.shuffle(pieces)
    for a in pieces:
        piece=quarto.get_piece_charachteristics(a)
        #print(f'Piece {a} with char High {piece.HIGH} Coloured {piece.COLOURED} Solid {piece.SOLID} Square {piece.SQUARE}')
        if (characteristic=='high'and piece.HIGH) or (characteristic=='coloured'and piece.COLOURED) or (characteristic=='solid' and piece.SOLID) or (characteristic=='square' and piece.SQUARE):
            #print(f'Chosen piece {a} with char High {piece.HIGH} Coloured {piece.COLOURED} Solid {piece.SOLID} Square {piece.SQUARE}')
            return a
        if (characteristic=='not_high'and not piece.HIGH) or (characteristic=='not_coloured'and not piece.COLOURED) or (characteristic=='not_solid' and not piece.SOLID) or (characteristic=='not_square' and not piece.SQUARE):
            #print(f'Chosen piece {a} with char High {piece.HIGH} Coloured {piece.COLOURED} Solid {piece.SOLID} Square {piece.SQUARE}')
            return a
    return pieces[0]

def pick_piece_without_char(quarto,characteristic,possible_pieces):
    pieces=copy.deepcopy(possible_pieces)
    random.shuffle(pieces)
    for a in pieces:
        piece=quarto.get_piece_charachteristics(a)
        #print(f'Piece {a} with char High {piece.HIGH} Coloured {piece.COLOURED} Solid {piece.SOLID} Square {piece.SQUARE}')
        if (characteristic=='high'and not piece.HIGH) or (characteristic=='coloured'and not piece.COLOURED) or (characteristic=='solid' and not piece.SOLID) or (characteristic=='square' and not piece.SQUARE):
            #print(f'Chosen piece {a} with char High {piece.HIGH} Coloured {piece.COLOURED} Solid {piece.SOLID} Square {piece.SQUARE}')
            return a
        if (characteristic=='not_high'and piece.HIGH) or (characteristic=='not_coloured'and piece.COLOURED) or (characteristic=='not_solid' and piece.SOLID) or (characteristic=='not_square' and piece.SQUARE):
            #print(f'Chosen piece {a} with char High {piece.HIGH} Coloured {piece.COLOURED} Solid {piece.SOLID} Square {piece.SQUARE}')
            return a
    return pieces[0]

def choose_piece_that_have_most_unique_char(quarto) -> int:
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
    free_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    minval,minchar=None,'high'
    for k,v in placed_pieces_char.items():
        if minval is None or minval>v:
            minval=v
            minchar=k
    #print(f'Placed pieces {placed_pieces} free pieces {free_pieces} chars {placed_pieces_char} min char {minchar}')
    return pick_piece_with_char(quarto,minchar,free_pieces)

def choose_piece_that_have_less_unique_char(quarto) -> int:
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
    free_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    maxval,maxchar=None,'high'
    for k,v in placed_pieces_char.items():
        if maxval is None or maxval<v:
            maxval=v
            maxchar=k
    #print(f'Placed pieces {placed_pieces} free pieces {free_pieces} chars {placed_pieces_char} min char {minchar}')
    return pick_piece_with_char(quarto,maxchar,free_pieces)

def choose_piece_with_random_available_char(quarto) -> int:
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
    free_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
    free_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in free_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        free_pieces_char['high']+=piece_char.HIGH
        free_pieces_char['coloured']+=piece_char.COLOURED
        free_pieces_char['solid']+=piece_char.SOLID
        free_pieces_char['square']+=piece_char.SQUARE
        free_pieces_char['not_high']+=not piece_char.HIGH
        free_pieces_char['not_coloured']+=not piece_char.COLOURED
        free_pieces_char['not_solid']+=not piece_char.SOLID
        free_pieces_char['not_square']+=not piece_char.SQUARE
    #print(f'Placed pieces {placed_pieces} free pieces {free_pieces} chars {placed_pieces_char} min char {minchar}')
    return pick_piece_with_char(quarto,random.choice([k for k,v in free_pieces_char.items() if v>0]),free_pieces)

def choose_piece_with_most_true_chars(quarto) -> int:
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
    free_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
    maxtrues=0
    maxpiece=None
    for piece in free_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        trues=piece_char.HIGH+piece_char.COLOURED+piece_char.SOLID+piece_char.SQUARE
        if trues>=maxtrues:
            maxtrues=trues
            maxpiece=piece
    #print(f'Placed pieces {placed_pieces} free pieces {free_pieces} chars {placed_pieces_char} min char {minchar}')
    return maxpiece

def choose_piece_with_less_true_chars(quarto) -> int:
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
    free_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
    mintrues=None
    minpiece=None
    for piece in free_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        trues=piece_char.HIGH+piece_char.COLOURED+piece_char.SOLID+piece_char.SQUARE
        if mintrues is None or trues<=mintrues:
            mintrues=trues
            minpiece=piece
    #print(f'Placed pieces {placed_pieces} free pieces {free_pieces} chars {placed_pieces_char} min char {minchar}')
    return minpiece

def place_less_used_row(quarto) -> tuple[int, int]:
    return random.randint(0, 3), less_used_row(quarto)

def place_most_used_row(quarto) -> tuple[int, int]:
    return random.randint(0, 3), most_used_row_not_complete(quarto)

def place_less_used_column(quarto) -> tuple[int, int]:
    return less_used_column(quarto), random.randint(0, 3)

def place_most_used_column(quarto) -> tuple[int, int]:
    return most_used_column_not_complete(quarto), random.randint(0, 3)

def place_less_used_row_less_used_column(quarto) -> tuple[int, int]:
    return less_used_column(quarto), less_used_row(quarto)

def place_less_used_row_most_used_column(quarto) -> tuple[int, int]:
    return most_used_column_not_complete(quarto), less_used_row(quarto)

def place_most_used_row_less_used_column(quarto) -> tuple[int, int]:
    return less_used_column(quarto), most_used_row_not_complete(quarto)

def place_most_used_row_most_used_column(quarto) -> tuple[int, int]:
    return most_used_column_not_complete(quarto), most_used_row_not_complete(quarto)

def place_at_diagonal_if_available(quarto) -> tuple[int,int]:
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist()]
    possible_diagonal_placements=[p for p in possible_placements if p[0]==p[1]]
    if len(possible_diagonal_placements)>0:
        return random.choice(possible_diagonal_placements)
    else:
        return random.choice(possible_placements)

def place_at_antidiagonal_if_available(quarto) -> tuple[int,int]:
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist()]
    possible_antidiagonal_placements=[p for p in possible_placements if p[0]+p[1]==NUMROWS-1]
    if len(possible_antidiagonal_placements)>0:
        return random.choice(possible_antidiagonal_placements)
    else:
        return random.choice(possible_placements)

def place_at_corner_if_available(quarto) -> tuple[int,int]:
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist()]
    possible_corner_placements=[p for p in possible_placements if p[0]==0 or p[0]==NUMCOLUMNS-1 or p[1]==0 or p[1]==NUMROWS-1]
    if len(possible_corner_placements)>0:
        return random.choice(possible_corner_placements)
    else:
        return random.choice(possible_placements)

def place_inside_if_available(quarto) -> tuple[int,int]:
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist()]
    possible_inside_placements=[p for p in possible_placements if p[0]!=0 and p[0]!=NUMCOLUMNS-1 or p[1]!=0 and p[1]==NUMROWS-1]
    if len(possible_inside_placements)>0:
        return random.choice(possible_inside_placements)
    else:
        return random.choice(possible_placements)

def place_not_at_diagonal_if_available(quarto) -> tuple[int,int]:
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist()]
    possible_notdiagonal_placements=[p for p in possible_placements if p[0]!=p[1]]
    if len(possible_notdiagonal_placements)>0:
        return random.choice(possible_notdiagonal_placements)
    else:
        return random.choice(possible_placements)

def place_not_at_antidiagonal_if_available(quarto) -> tuple[int,int]:
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist()]
    possible_notantidiagonal_placements=[p for p in possible_placements if p[0]+p[1]!=NUMROWS-1]
    if len(possible_notantidiagonal_placements)>0:
        return random.choice(possible_notantidiagonal_placements)
    else:
        return random.choice(possible_placements)

def get_choose_actions():
    return [choose_piece_with_less_true_chars,choose_piece_with_most_true_chars,choose_piece_with_random_available_char,
                choose_piece_that_have_less_unique_char,choose_piece_that_have_most_unique_char]

def get_place_actions():
    return [place_at_diagonal_if_available,place_at_antidiagonal_if_available,place_at_corner_if_available,place_inside_if_available,
            place_not_at_diagonal_if_available,place_not_at_antidiagonal_if_available,place_less_used_row_less_used_column,
                place_less_used_row_most_used_column,place_most_used_row_less_used_column,place_most_used_row_most_used_column]
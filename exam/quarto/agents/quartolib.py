import numpy as np
import quarto

NUMROWS=4
NUMCOLUMNS=4
def get_placed_pieces(board) :
    return list(board[board!=-1])

def num_pieces_chosen(quarto) -> int:
    return len(get_placed_pieces(quarto.get_board_status()))

def num_pieces_left(quarto) -> int:
    return (NUMROWS*NUMCOLUMNS) - len(get_placed_pieces(quarto.get_board_status()))

def less_used_characteristic(quarto):
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
    return minchar

def most_used_characteristic(quarto):
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
    return maxchar

def most_used_row(quarto):
    return np.argmax(np.count_nonzero(quarto.get_board_status()!=-1,axis=1))

def most_used_column(quarto):
    return np.argmax(np.count_nonzero(quarto.get_board_status()!=-1,axis=0))

def less_used_row(quarto):
    return np.argmin(np.count_nonzero(quarto.get_board_status()!=-1,axis=1))

def less_used_column(quarto):
    return np.argmin(np.count_nonzero(quarto.get_board_status()!=-1,axis=0))

def most_used_column_not_complete(quarto):
    count=np.count_nonzero(quarto.get_board_status()!=-1,axis=0).tolist()
    maxcount=0
    maxcol=0
    for a in range(NUMCOLUMNS):
        if count[a]>=maxcount and count[a]<NUMCOLUMNS:
            maxcount=count[a]
            maxcol=a
    return maxcol

def most_used_row_not_complete(quarto):
    count=np.count_nonzero(quarto.get_board_status()!=-1,axis=1).tolist()
    maxcount=0
    maxrow=0
    for a in range(NUMROWS):
        if count[a]>=maxcount and count[a]<NUMROWS:
            maxcount=count[a]
            maxrow=a
    return maxrow

def num_elements_in_antidiagonal(quarto):
    return np.count_nonzero(np.fliplr(quarto.get_board_status()).diagonal()!=-1)

def num_elements_in_diagonal(quarto):
    return np.count_nonzero(quarto.get_board_status().diagonal()!=-1)

def num_pieces_in_most_used_row(quarto):
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[most_used_row(quarto)]

def num_pieces_in_most_used_column(quarto):
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[most_used_column(quarto)]

def num_pieces_in_most_used_row_not_complete(quarto):
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[most_used_row_not_complete(quarto)]

def num_pieces_in_most_used_column_not_complete(quarto):
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[most_used_column_not_complete(quarto)]

def num_pieces_in_less_used_row(quarto):
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[less_used_column(quarto)]

def num_pieces_in_less_used_column(quarto):
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[less_used_column(quarto)]

def get_choose_functions():
    return [num_elements_in_diagonal,num_elements_in_antidiagonal,num_pieces_in_less_used_column,num_pieces_in_less_used_row,num_pieces_in_most_used_column,
        num_pieces_in_most_used_row,num_pieces_in_most_used_column_not_complete,num_pieces_in_most_used_row_not_complete,
        num_pieces_chosen,num_pieces_left,less_used_characteristic,most_used_characteristic]

def get_place_functions():
    return [num_elements_in_diagonal,num_elements_in_antidiagonal,num_pieces_in_less_used_column,num_pieces_in_less_used_row,num_pieces_in_most_used_column,
        num_pieces_in_most_used_row,num_pieces_in_most_used_column_not_complete,num_pieces_in_most_used_row_not_complete,
        num_pieces_chosen,num_pieces_left,most_used_row,less_used_row,most_used_column,less_used_column,most_used_row_not_complete,most_used_column_not_complete]
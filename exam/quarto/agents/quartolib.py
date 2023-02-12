import numpy as np
import random
import quarto

NUMROWS=4
NUMCOLUMNS=4
POSITIONS=[(a,b) for a in range(4) for b in range(4)]
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

def element_in_less_used_column(quarto):
    column=less_used_column(quarto)
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist() if a[1]==column]
    return random.choice(possible_placements)

def element_in_less_used_row(quarto):
    row=less_used_row(quarto)
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist() if a[0]==row]
    return random.choice(possible_placements)

def element_in_most_used_row_not_complete(quarto):
    row=most_used_row_not_complete(quarto)
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist() if a[0]==row]
    return random.choice(possible_placements)

def element_in_most_used_column_not_complete(quarto):
    column=most_used_column_not_complete(quarto)
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist() if a[1]==column]
    return random.choice(possible_placements)


def element_in_diagonal(quarto):
    return random.choice([a for a in POSITIONS if a[0]==a[1]])

def element_in_antidiagonal(quarto):
    return random.choice([a for a in POSITIONS if a[0]+a[1]==NUMROWS-1])

def element_in_corner(quarto):
    return random.choice([a for a in POSITIONS if a[0]==0 or a[0]==NUMCOLUMNS-1 or a[1]==0 or a[1]==NUMROWS-1])

def element_inside(quarto):
    return random.choice([a for a in POSITIONS if a[0]!=0 and a[0]!=NUMCOLUMNS-1 and a[1]!=0 and a[1]!=NUMROWS-1])

def not_high_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if not quarto.get_piece_charachteristics(a).HIGH])
    
def not_solid_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if not quarto.get_piece_charachteristics(a).SOLID])

def not_coloured_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if not quarto.get_piece_charachteristics(a).COLOURED])

def not_square_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if not quarto.get_piece_charachteristics(a).SQUARE])

def high_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if quarto.get_piece_charachteristics(a).HIGH])

def solid_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if quarto.get_piece_charachteristics(a).SOLID])

def coloured_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if quarto.get_piece_charachteristics(a).COLOURED])

def square_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if quarto.get_piece_charachteristics(a).SQUARE])

def place_possible(quarto,a,b):
    return True if a in [(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist()] else False

def choose_possible(quarto,a,b):
    return True if a in [_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in get_placed_pieces(quarto.get_board_status())] else False

def compare_elements_in_columns(quarto,a,b):
    board=quarto.get_board_status()
    ela,elb=np.count_nonzero(board[:,a]!=-1),np.count_nonzero(board[:,b]!=-1)
    return True if ela>elb and ela!=NUMROWS else False


def compare_elements_in_rows(quarto,a,b):
    board=quarto.get_board_status()
    ela,elb=np.count_nonzero(board[a,:]!=-1),np.count_nonzero(board[b,:]!=-1)
    return True if ela>elb and ela!=NUMCOLUMNS else False

def compare_elements_in_diag(quarto,a,b):
    board=quarto.get_board_status()
    ela,elb=np.count_nonzero(np.diagonal(board,a[0]-a[1])!=-1),np.count_nonzero(np.diagonal(board,b[0]-b[1])!=-1)
    return True if ela>elb else False

def compare_elements_in_antidiag(quarto,a,b):
    board=quarto.get_board_status()
    ela,elb=np.count_nonzero(np.diagonal(np.fliplr(board),a[0]-a[1])!=-1),np.count_nonzero(np.diagonal(np.fliplr(board),b[0]-b[1])!=-1)
    return True if ela>elb else False

def compare_uniqueness(quarto,a,b):
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
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
    aval=placed_pieces_char['high' if apiece.HIGH else 'not_high'] + placed_pieces_char['coloured' if apiece.COLOURED else 'not_coloured'] + placed_pieces_char['solid' if apiece.SOLID else 'not_solid'] +placed_pieces_char['square' if apiece.SQUARE else 'not_square']
    bval=placed_pieces_char['high' if bpiece.HIGH else 'not_high'] + placed_pieces_char['coloured' if bpiece.COLOURED else 'not_coloured'] + placed_pieces_char['solid' if bpiece.SOLID else 'not_solid'] +placed_pieces_char['square' if bpiece.SQUARE else 'not_square']
    return True if aval>bval else False


def get_then_place_functions():
    return [element_in_less_used_row,element_in_less_used_column,element_in_most_used_row_not_complete,element_in_most_used_column_not_complete,element_inside,element_in_diagonal,element_in_antidiagonal,element_in_corner]

def get_then_choose_functions():
    return [high_piece,not_high_piece,solid_piece,not_solid_piece,coloured_piece,not_coloured_piece,square_piece,not_square_piece]

def get_choose_functions():
    return [num_elements_in_diagonal,num_elements_in_antidiagonal,num_pieces_in_less_used_column,num_pieces_in_less_used_row,num_pieces_in_most_used_column,
        num_pieces_in_most_used_row,num_pieces_in_most_used_column_not_complete,num_pieces_in_most_used_row_not_complete,
        num_pieces_chosen,num_pieces_left,less_used_characteristic,most_used_characteristic]

def get_place_functions():
    return [num_elements_in_diagonal,num_elements_in_antidiagonal,num_pieces_in_less_used_column,num_pieces_in_less_used_row,num_pieces_in_most_used_column,
        num_pieces_in_most_used_row,num_pieces_in_most_used_column_not_complete,num_pieces_in_most_used_row_not_complete,
        num_pieces_chosen,num_pieces_left,most_used_row,less_used_row,most_used_column,less_used_column,most_used_row_not_complete,most_used_column_not_complete]
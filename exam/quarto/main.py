# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import quarto
from agents.genetic import GeneticProg as gp
from agents.genome import Genome as myplayer
from agents.genome import RandomPlayer 
import dill as pickle
from os.path import isfile


def main(training,best_player_file,generations):
    mp=None
    if training:
        mp=gp(None,best_player_file,generations)
    else:
        if isfile(best_player_file):
            mp=pickle.load(open(best_player_file,'rb'))
        else:
            print(f'WARNING: Filename provided doesn\'t exists! If you don\'t have a trained player set the --training flag')
    if mp is not None:
        print(f'Game against random player starting, my player is player 1 ...')
        game = quarto.Quarto()
        game.set_players((RandomPlayer(game), mp))
        mp.set_quarto(game)
        winner = game.run()
        print(f"main: Winner: player {winner}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    parser.add_argument('-t','--training', action='store_true',dest='training',
                        help='Training phase done if set to True, otherwise read best player from best_player.p')
    
    parser.add_argument('-f','--filename',dest='filename',type=str,default='best_player.p',
                        help='Provide the filename of the best pickled player already trained or the filename where the best player obtained from training will be pickled, it defaults to best_player.p')

    parser.add_argument('-g','--generations',dest='generations',type=int,default=50,
                        help='If training this represents the number of generations, it defaults to 50')

    args = parser.parse_args()
    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main(args.training,args.filename,args.generations)
"""
mlbscoremap.py - Creates a filterable heat map of Major League Baseball (MLB) scores 
Takes any yearly data from http://www.retrosheet.org/gamelogs/index.html as input

Gathered heatmap creation code from 'joelotz' answer at:
http://stackoverflow.com/questions/14391959/heatmap-in-matplotlib-with-pcolor

Author: Shaun Adkins (shaun.adkins@gmail.com)
"""

from optparse import OptionParser
import matplotlib
matplotlib.use('Agg')   # Causes plots to not be displayed with the $DISPLAY env_var
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import re
import sys

class GameSet:
  
    # Initialize object
    def __init__(self, team):
        self.games = []  # list of games from the data
        self.team = team
    
    # Parse the game logs file
    def parse_file(self, fh):
  
        # Parse out the data from each line, and add to proper category in dictionary
        for line in iter(fh.readline, ''):
            game = Game()   # create new Game object
            data = re.split(',', line, 13)
            game.populate_categories(data)
            
            # Append our newest game data to the stack of games
            if (game.team_in_game(self.team)):
                self.games.append(game)
        return

    # Create the heatmap using our dictionary of games
    def create_heatmap(self, outfile):
    
        # Get labels of runs scored from a range of scores
        ascore_labels = range(get_highest_score('ascore', self.games)+1)    
        hscore_labels = range(get_highest_score('hscore', self.games)+1)
        
        # Get data (x is home scores, y is away scores)
        data = get_scores(self.games, hscore_labels, ascore_labels)
        data = np.array(data)
        # Plot it out
        fig, ax = plt.subplots()
        # Add colors, using a Blue-Purple colormap, with normalization
        heatmap = ax.pcolor(data, cmap=plt.cm.BuPu, norm=LogNorm(), alpha=1)
    
        # Format
        fig = plt.gcf()
        fig.set_size_inches(8, 11)
        
        # Adding labels
        fig.suptitle("Final Score Frequency", fontsize=20)
        
        # turn off the frame
        ax.set_frame_on(False)
        
        # put the major ticks at the middle of each cell
        ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
        ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)    
        
        # Setting labels
        ax.set_xticklabels(hscore_labels, minor=False)
        ax.set_yticklabels(ascore_labels, minor=False)
        ax.set_xlabel("Home team score")
        ax.set_ylabel("Away team score")
        
        # want a more natural, table-like display
        ax.invert_yaxis()
        ax.xaxis.tick_top()     
        ax.xaxis.set_label_position("top")
        
        # Turn off all the ticks
        ax = plt.gca()
        
        for t in ax.xaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        for t in ax.yaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        
        plt.savefig(outfile, bbox_inches='tight')
            
### MATPLOTLIB functions

# Retrieve max score from all data
def get_highest_score(cat, games):
    return int(max(gather_category(cat, games), key=int))

# Retrieve all of the unique game data for a category    
def gather_category(cat, games):
    values = set()
    for game in games:
        values.add(getattr(game, cat))
    return list(values)

# Create a matrix of home and away scores
def get_scores(games, hlabels, alabels):
    # Initialize 2D array of 0's (pythonish way)
    data = [ [0]*len(hlabels) for row in range(len(alabels)) ]
    
    # Normal (longer way)
    # data = []
    # for row in range(len(alabels)):
    #   data.append([])
    #   for col in range(len(hlabels)):
    #       data[row][col] = 0
    
    # Now increment whenever a score combo is found
    for game in games:
        data[int(game.ascore)][int(game.hscore)] += 1
    return data

class Game:
    # Baseball game categories I would like to store, for now
    categories = ['date', 'dblheader', 'weekday', 'ateam', 'aleague', 'agame', 'hteam', 'hleague', 'hgame', 'ascore', 'hscore', 'length', 'daynight']
    
    # Initialize object
    def __init__(self):
        pass
    
    def populate_categories(self, data):
        for i in range(len(self.categories)):
            item = data[i].replace('"', '')
            setattr(self, self.categories[i], item)
            
    def team_in_game(self, team):
        if team == '':
            return True
        elif self.ateam == team or self.hteam == team:
            return True
        else:
            return False

# Filter results by a particular team (eventually adjust to filter by any category
def filter_by_team():
    pass

# Open file
def open_file(file):
    try:
        fh = open(file, "r")
    except IOError:
        sys.stderr.write("Cannot open file " + file + " for reading!\n")
        sys.exit(1)
    else:
        return fh

def main():
    # Set up options parser and help usage statement
    usage = "usage: %prog -i </path/to/schedule/data.txt> [ -o <filename> -t <team initials>]"
    description = "Creates a filterable heatmap of Major League Baseball scores"
    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-i", "--input_file", help="Yearly schedule data .txt file found from http://www.retrosheet.org/gamelogs/index.html")
    parser.add_option("-o", "--output_file", help="(Optional) Filename for output file to be saved in current directory")
    parser.add_option("-t", "--team_filter", help="(Optional) Filter by an individual team's games (use initials)")
    (options, args) = parser.parse_args()
    
    if not options.input_file:
        parser.error("Input data file must be provided")

    if options.output_file:
        outfile = options.output_file
    else:
        outfile = "heatmap.pdf"
        
    if options.team_filter:
        team = options.team_filter
    else:
        team = ''
        
    # Later add option to use urlopen to grab directly from site    
    fh = open_file(options.input_file)
    
    gs = GameSet(team)
    gs.parse_file(fh)
    fh.close()
    gs.create_heatmap(outfile)
    
if __name__ == '__main__':
    main()
    sys.exit(0)
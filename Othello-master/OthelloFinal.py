import random

# Object used to create new boards

class Board:
    def __init__(self, size):
        self.size = size
        self.board = []

    # Used to fill the "board" property with a list with a length equal to the "size" property
    def create_board(self):
        for y_pos in range(self.size):
            for x_pos in range(self.size):
                #  Create a Tile instance  
                
                #  Gives it the coordinates (depending on x_pos and y_pos)
                #  Add it to the board property
                if x_pos != 0 and x_pos != 7 and y_pos != 0 and y_pos != 7:
                    self.board.append(Tile(x_pos, y_pos, "🟩", "🟩"))
                else:
                    self.board.append(Tile(x_pos, y_pos, "X", "🟩"))
        self.place_initial_pawns()

    #  This will print the game board, depending on the data_type
    #  Data types are "Coordinates", "Type" and "Content"
    def draw_board(self, data_type):
        display_board = []
        line_breaker = 0
        print([0, ' 0', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7'])
        for board_index in self.board:
            if (board_index.x_pos == 0):
                display_board.append(board_index.y_pos)
            if data_type == "Coordinates":
                display_board.append([board_index.x_pos, board_index.y_pos])
            elif data_type == "Type":
                display_board.append(board_index.type)
            else:
                display_board.append(board_index.content)
            line_breaker += 1
            if line_breaker > 7:
                print(display_board)
                line_breaker = 0
                display_board = []
        print("\n")

    # Place the 4 initial pawns at the center of the board (2 white and 2 black)
    def place_initial_pawns(self):
        #  We pick the 4 central tiles
        #  And place 2 black pawns and 2 white pawns
        self.board[27].content = "⚪"
        self.board[28].content = "⚫"
        self.board[35].content = "⚫"
        self.board[36].content = "⚪"

    # Check if the position in inside the board
    # Return true or false depending if it is inside or not
    def is_on_board(self, x_pos, y_pos):
        if x_pos < 0 or x_pos > 7 or y_pos < 0 or y_pos > 7:
            return False
        else:
            return True

    # Check if the tile is an empty tile ("🟩")
    # Return true or false depending if it is empty or not
    def is_tile_empty(self, x_pos, y_pos):
        if self.board[(x_pos) + y_pos * 8].content == "🟩":
            return True
        else:
            return False

    # Takes a position (x_pos, y_pos) and a color 
    # Try to simulate the move
    # Returns either false if the move is not valid
    # Or returns which pawns will change color if true
    # The returned list will contain [numbers_of_pawns_to_change, [direction_x, direction_y]]
    def is_legal_move(self, x_pos, y_pos, color):

        # North / Nort-East / East / South-East / South / South-West / West / North-West
        directions = [
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
        ]

        # Opposite of the color of the placed pawn
        if color == "⚪":
            awaited_color = "⚫"
        else:
            awaited_color = "⚪"

        current_x_pos = x_pos
        current_y_pos = y_pos
        is_legal = False
        # [number_of_tile_to_flip, direction]
        # Si on a un pion noir placé en 2,3, on veut:
        # [[1, [1, 0]]
        tiles_to_flip = []

        if (not self.is_tile_empty(current_x_pos, current_y_pos) or not self.is_on_board(current_x_pos, current_y_pos)):
            return False

        # Check for every direction
        for current_dir in directions:
            number_of_tiles_to_flip = 1
            # Get your original coordinates + the direction modifier
            current_x_pos = x_pos + current_dir[0]
            current_y_pos = y_pos + current_dir[1]
            # Check if the new position is on the board and empty
            if self.is_on_board(current_x_pos, current_y_pos):
                #  Get the tile informations
                current_index = self.board[current_x_pos + current_y_pos * 8]
                # If the tile contains a pawn of the opposite color, continue on the line
                while current_index.content == awaited_color:
                    current_x_pos += current_dir[0]
                    current_y_pos += current_dir[1]
                    if self.is_on_board(current_x_pos, current_y_pos):
                        current_index = self.board[current_x_pos +
                                                   current_y_pos * 8]
                        # If the line ends with a pawn of your color, then the move is legal
                        if current_index.content == color:
                            is_legal = True
                            tiles_to_flip.append(
                                [number_of_tiles_to_flip, current_dir])
                            break
                    else:
                        break
                    number_of_tiles_to_flip += 1

        if is_legal:
            return tiles_to_flip
        else:
            return False

    # Takes a position (x_pos, y_pos), an array with a number of tiles to flip and a direction, and a color
    # The array should be obtained with the "is_legal_move" function
    # Doesn't return anything, but will change the color of the tiles selected by "tiles_to_flip"
    def flip_tiles(self, x_pos, y_pos, tiles_to_flip, color):
        # x_pos and y_pos = new pawn position
        # tiles_to_flip = list containing the number of pawn to flip and a direction
        # ex: [
        # [1, [1, 0]],
        # ] means we're changing 1 pawn to the right
        # color = the new color of the pawns to flip
        for current_dir in tiles_to_flip:
            current_x_pos = x_pos + current_dir[1][0]
            current_y_pos = y_pos + current_dir[1][1]
            for nb_tile in range(current_dir[0]):
                current_index = self.board[current_x_pos + current_y_pos * 8]
                current_index.content = color
                current_x_pos += current_dir[1][0]
                current_y_pos += current_dir[1][1]

# Used to create each tile of your board
# Contains a position (x, y), a type to check if it's a boder tile or not, and a content to check if there is a pawn inside the tile


class Tile:
    #   Type is used to check if its an "🟩" empty tile or a "X" border tile
    #   Content is used to check if a pawn is placed o (Empty), B (Black), W (White)
    def __init__(self, x_pos, y_pos, type, content):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        self.content = content

# Used to create new ruleset
# Contains the score, the active player, the game_over check and functions allowing to interact with the game


class Game:
    def __init__(self, jeu):
        self.score_black = 2
        self.score_white = 2
        self.active_player = "⚫"
        self.is_game_over = False
        self.winner = "Noone"

    # Place a pawn on the board (checks if the move is legal before placing it)
    # It takes a position (x, y), a Board object instance and a color
    # The function will automatically check if the move is valid or not
    def place_pawn(self, x_pos, y_pos, board_instance, color):
        if not board_instance.is_on_board(x_pos, y_pos):
            print("Coordinates outside the board")
        else:
            if board_instance.board[(x_pos) + y_pos * 8].content == "🟩":
                tiles_to_flip = board_instance.is_legal_move(
                    x_pos, y_pos, color)
                if not tiles_to_flip:
                    print("Invalid move")
                else:
                    board_instance.board[(x_pos) + y_pos * 8].content = color
                    board_instance.flip_tiles(
                        x_pos, y_pos, tiles_to_flip, color)
                    print(f"Pion placé en {x_pos}, {y_pos}")
                    self.update_score(board_instance)
                    self.change_active_player()
                    self.check_for_valid_moves(board_instance)
                    board_instance.draw_board("Content")
            else:
                print("There is already a pawn here")

    # Change the active player color from black to white or white to black
    def change_active_player(self):
        # Prend self.active_player et change la couleur du joueur actif
        if self.active_player == "⚫":
            self.active_player = "⚪"
            print("C'est au tour du joueur blanc")
        else:
            self.active_player = "⚫"
            print("C'est au tour du joueur bot ")

    # Update the players score after a successful move
    def update_score(self, board_instance):
        # Count all the black & white pawns, and update the scores
        w_score = 0
        b_score = 0
        for tile_index in board_instance.board:
            if tile_index.content == "⚪":
                w_score += 1
            elif tile_index.content == "⚫":
                b_score += 1
        self.score_black = b_score
        self.score_white = w_score

    # Check for a valid move, and end the game if there is none for the current player
    def check_for_valid_moves(self, board_instance):
        is_game_over = True
        for tile_index in board_instance.board:
            move_to_check = board_instance.is_legal_move(
                tile_index.x_pos, tile_index.y_pos, self.active_player)
            if move_to_check != False:
                is_game_over = False

        if is_game_over:
            self.check_for_winner()
            self.is_game_over = True

    # Compare the score, and print the winner's color
    def check_for_winner(self):
        print("Partie terminée !")
        print("Le joueur noir a: " + str(self.score_black) + " points")
        print("Le joueur white a: " + str(self.score_white) + " points")
        if (self.score_black > self.score_white):
            print("Le joueur noir a gagné !")
            self.winner = "⚫"
        elif (self.score_white > self.score_black):
            print("Le joueur blanc a gagné !")
            self.winner = "⚪"
        else:
            print("Égalité !")


class Ma_bot:
    def __init__(self):
        self.bot_name = "name"
        self.counter = 0

    # BOT FUNCTIONS

    def check_valid_moves(self , copy_board , game):

        playable_moves = []
        point_max = 0 
        EMPTY = 0
        mobility = 0
        #for coord in edge_coordinates:
        for my_index in range (len(copy_board.board)) : 
            x_pos = copy_board.board[my_index].x_pos
            y_pos = copy_board.board[my_index].y_pos   
            t_toflip = copy_board.is_legal_move(copy_board.board[my_index].x_pos, copy_board.board[my_index].y_pos, game.active_player) # renvois la liste de mov juable et liste des case gagnable
            if t_toflip != False : # on verifie si on peut jouer
                tile_point = sum([x[0] for x in t_toflip]) # recupere tout les mouvemnt ( somme des directions)
                if self.counter <= 10 :   # on verifie si <= 7 pour jouer strategie debut
                     playable_moves.append([copy_board.board[my_index].x_pos, copy_board.board[my_index].y_pos , tile_point])                      # on ajoute liste des coordonnées et somme de direction                
                else :

                    if point_max < tile_point :     # on verifie pour recuperer le nombre max
                    # point_max = ([copy_board.board[my_index].x_pos, copy_board.board[my_index].y_pos])
                        point_max = tile_point
                        playable_moves = [[copy_board.board[my_index].x_pos, copy_board.board[my_index].y_pos]]     # on recupere les coordonnées de 
                    elif point_max == tile_point : 
                        playable_moves.append([copy_board.board[my_index].x_pos, copy_board.board[my_index].y_pos]) # ajoute les cases jouable, coordonné du liste et nombre des points
                    for coords in playable_moves:
                        if coords[0] == 0 or coords[0] == 7 or coords[1] == 0 or coords[1] == 7:  
                            self.counter += 1  
                            print(self.counter)
                            return coords                
        if len(playable_moves) > 0  and self.counter <= 10 :
                nb_min = min([x[2] for x in playable_moves])      #case qui donne le moin   
                for item in playable_moves : 
                    if item[2] == nb_min : 
                        min_item = item
                        self.counter += 1
                        print(self.counter)
                        return [min_item[0],min_item[1]]      # x_pos = 0 y_pos =1     2 = tile_pointa  
         # Priorité aux mouvements dans le centre     
        elif x_pos in [2, 3, 4, 5] and y_pos in [2, 3, 4, 5]:
            total_flips += 2  # Augmenter le poids pour les cases centrales   

        elif x_pos == 3 and y_pos == 3 or x_pos == 4 and y_pos == 4 or x_pos == 3 and y_pos == 4 or x_pos == 4 and y_pos == 3:
            total_flips += 3  # Ajouter un bonus pour les cases au centre ( proteger le centre)

        # Vérifier les directions adjacentes pour la mobilité
        for x_pos in [-1, 0, 1]:
            for y_pos in [-1, 0, 1]:
                if x_pos == 0 and y_pos == 0:
                    continue  # Ignorer la position actuelle

                x, y = my_index + x_pos, my_index + y_pos

                # Vérifier si la case adjacente est vide
                if 0 <= my_index < 8 and 0 <= my_index < 8 and copy_board.board[x][y] == EMPTY :
                            mobility += 1    

        if self.counter > 10 :
             return random.choice(playable_moves)      
        #elif self.counter => 20 : 


       
                 
                   

        # Si aucun coup n'est possible pour jouer dans le bord, jouer n'importe où
               # return None
                      
        game.check_for_winner() 
        
# Create a new board & a new game instances
        #corto bot
class CrotoBotEz:
    def __init__(self):
        self.coners = [[0, 0], [7, 0], [0, 7], [7, 7]]
        self.avoided_tiles = [[1, 0], [0, 1],  [1, 1], [1, 7], [0, 6], [1, 6], [6, 0], [7, 1], [6, 1], [6, 7], [7, 6], [6, 6]]

    # BOT FUNCTIONS

    def check_valid_moves(self, board, game):
        max_points = -999
        best_moves = []
        current_move = []

        for current_tile in board.board:
            points = 0

            if(board.is_tile_empty):
                current_move = board.is_legal_move(current_tile.x_pos, current_tile.y_pos, game.active_player)
                
                if (current_move != False):
                    for tiles_to_flip in current_move:
                        points += tiles_to_flip[0]
                    
                    points += self.get_tile_weight(current_tile.x_pos, current_tile.y_pos)
                    if(points > max_points):
                        best_moves = [[current_tile.x_pos, current_tile.y_pos]]
                        max_points = points
                    elif(points == max_points):
                        best_moves.append([current_tile.x_pos, current_tile.y_pos])

        return random.choice(best_moves)
                
    def get_tile_weight(self, x, y):
        total_points = 0

        for current_coord in self.coners:
            if x == current_coord[0] and y == current_coord[1]:
                total_points += 100
                break
            
        for current_coord in self.avoided_tiles:
            if x == current_coord[0] and y == current_coord[1]:
                total_points -= 30
                break
        
        return total_points
            
    
      
othello_board = Board(8)
othello_game = Game(100) 


# Fill the board with tiles
othello_board.create_board()

# Draw the board
othello_board.draw_board("Type")

# Create 2 bots
my_bot = Ma_bot()
otherBot = Ma_bot()
croto_bot = CrotoBotEz()

# Loop until the game is over
while not othello_game.is_game_over:
    # First player / bot logic goes here
    if (othello_game.active_player == "⚫"):

    
        move_coordinates = my_bot.check_valid_moves(othello_board , othello_game) 
        # changer ici user par bot pour jouer 

        #move_coordinates[0] = int(input("Coordonnées en X: "))
        #move_coordinates[1] = int(input("Coordonnées en Y: "))    
        othello_game.place_pawn(
            move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)

    # Second player / bot logic goes here
    else:
    
        move_coordinates = my_bot.check_valid_moves(othello_board , othello_game) 
        move_coordinates = croto_bot.check_valid_moves(othello_board, othello_game)
        #move_coordinates[0] = int(input("Coordonnées en X: "))
        #move_coordinates[1] = int(input("Coordonnées en Y: "))
        othello_game.place_pawn(
            move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)

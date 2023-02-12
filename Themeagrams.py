import pygame
import sys
import os
import random
import math
import easygui
from pygame.locals import *
pygame.init()  # initialize pygame
# Sets the frame rate
clock = pygame.time.Clock()
# Sets the start ticks
start_ticks = 0
# Keeps track of which screen the player is on
which_screen = 0
# Stores the words for each level
jungle_words = [
                "Lion", "Tiger", "Elephant", "Giraffe", "Leopard", "Monkey", "Gorilla", "Chimpanzee", "Jaguar", 
                "Crocodile", "Panther", "Hippopotamus", "Koala", "Baboon", "Chameleon", "Sloth", "Toucan", "Flamingo", 
                "Rhinoceros", "Cheetah", "Hyena", "Panda", "Ocelot", "Python", "Gazelle", "Tapir", "Alligator", "Puma",
                "Capybara", "Pangolin"
                ]
famous_cities = [
                "Paris", "London", "Tokyo", "Beijing", "Dubai", "Singapore", "Berlin", "Sydney", "Toronto", 
                "Austin", "Rome", "Seoul", "Mumbai", "Shanghai", "Moscow", "Istanbul", "Barcelona", "Miami"
                "Vienna", "Amsterdam", "Munich", "Milan", "Madrid", "Prague", "Budapest", "Lisbon", 
                "Athens", "Santiago", "Helsinki", "Oslo", "Copenhagen", "Stockholm", "Seattle"
                ]
ocean_words = [
                "Whale", "Shark", "Dolphin", "Squid", "Octopus", "Jellyfish", "Seahorse", "Starfish", "Lobster", 
                "Crab", "Clownfish", "Eel", "Krill", "Plankton", "Turtle", "Stingray", "Seagull", "Manatee", 
                "Narwhal", "Orca", "Walrus", "Tuna", "Salmon", "Sardine", "Penguin", "Seagull", "Swordfish", 
                "Shrimp", "Otter", "Mussel", "Crab", "Scallop", "Clam", "Lobster", "Anchovy"
                ]
words_reset = []
# Stores the theme chosen
theme = "jungle" 
# Keeps track of previous word
prev_word = "."
# Sets text for the game input text box
text = ""
# Stores the anagram created
anagram = ""
# Stores the name inputted
name = ""
# Sets text for the name text box
name_text = ""
# Decides when a new word should be given
keep_word = False
# Decides when the text in the text box should be cleared
reset_text = False
# Decides when to ask the user for a username
need_name = True
# Keeps track of the previous screen
prev_screen = -1
# Keeps track of score
score = 0
# Position value for each screen
home_screen = 0
instruction_screen = 1
leaderboard_screen = 2
add_name_screen = 3
levels_screen = 4
gameover_screen = 5
jungle_screen = 6
ocean_screen = 7
cities_screen = 8
# Load the background images
jungle_bg = pygame.image.load(os.path.join("./", "jungle.jpeg"))
city_bg = pygame.image.load(os.path.join("./", "city.jpeg"))
ocean_bg = pygame.image.load(os.path.join("./", "ocean.jpg"))
home_bg = (35, 206, 235)
# Shows the mouse
pygame.mouse.set_visible(True)

# Sets the caption
pygame.display.set_caption('Themeagrams')

# Set screen size
width, height = jungle_bg.get_size()
screen = pygame.display.set_mode((width, height))

# Keeps track of players and scores during the game
jungle_players = []
jungle_scores = []
ocean_players = []
ocean_scores = []
cities_players = []
cities_scores = []

# Adds any new player and their scores and sorts the leaderboard
def create_leaderboard(players, scores, leaderboard):
    for player, score in zip(players, scores):
        found = False
        for i, (p, s) in enumerate(leaderboard):
            if p == player:
                found = True
                if score > s:
                    leaderboard[i] = (player, score)
                if score < s:
                    leaderboard.append((player, score))
        if not found:
            leaderboard.append((player, score))
    leaderboard = leaderboard[:5]
    return leaderboard

# Writes the leaderboard to the .txt file
def write_leaderboard_to_file(leaderboard, filename):
    with open(filename, 'w') as f:
        for player, score in leaderboard:
            f.write(f'{player}: {score}\n')

# Reads the leaderboard from the .txt file
def read_leaderboard_from_file(filename):
    leaderboard = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                player, score = line.strip().split(': ')
                leaderboard.append((player, int(score)))
    except FileNotFoundError:
        pass
    return leaderboard

# Sorts the leaderboard
def sort_leaderboard(leaderboard):
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    return leaderboard

# Calls the leaderboard functions to update the leaderboard
def update_leaderboard(players, scores, filename):
    leaderboard = read_leaderboard_from_file(filename)
    leaderboard = create_leaderboard(players, scores, leaderboard)
    sort_leaderboard(leaderboard)
    write_leaderboard_to_file(leaderboard, filename)
    return leaderboard

# Updates the leaderboards at the start of the game
jungle_leaderboard = update_leaderboard(jungle_players, jungle_scores, 'jungle_leaderboard.txt')
ocean_leaderboard = update_leaderboard(ocean_players, ocean_scores, 'ocean_leaderboard.txt')
cities_leaderboard = update_leaderboard(cities_players, cities_scores, 'cities_leaderboard.txt')

# Set default leaderboard
theme_leaderboard = "JUNGLE LEADERBOARD"
leaderboard = jungle_leaderboard

# Wraps long text
def split_line(line, font, max_width):
    # Split a line into multiple lines if it is too wide to fit within the max width
    words = line.split()
    lines = []
    current_line = ""
    for word in words:
        current_line += word + " "
        line_width, line_height = font.size(current_line)
        if line_width > max_width:
            lines.append(current_line.strip())
            current_line = ""
    lines.append(current_line.strip())
    return lines

# Creates the home screen
def create_home(screen, mouse_x, mouse_y, mouse_click):
    global home_screen
    global instruction_screen
    global leaderboard_screen
    global add_name_screen
    global levels_screen
    global gameover_screen
    global jungle_screen
    global ocean_screen
    global cities_screen
    global start_ticks
    global which_screen
    global score
    global jungle_leaderboard
    global leaderboard
    global need_name
    
    # Set constants for the buttons and colors
    BUTTON_WIDTH = 275
    BUTTON_HEIGHT = 80
    FILL_COLOR = (238, 108, 77)
    OUTLINE_COLOR = (41, 50, 65)
    HOVER_COLOR = (212, 94, 66)
    OUTLINE_WIDTH = 2

    # Sets fonts
    title_font = pygame.font.Font(None, 75)
    font = pygame.font.Font(None, 40)
     
    # Creates text and buttons for the home screen

    title_text_surface = title_font.render("THEMEAGRAMS", True, OUTLINE_COLOR)
    title_text_rect = title_text_surface.get_rect()
    title_text_rect.center = (width/2, height/7)
    screen.blit(title_text_surface, title_text_rect)

    instruction_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 - BUTTON_HEIGHT * .5, BUTTON_WIDTH, BUTTON_HEIGHT)
    instruction_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 - BUTTON_HEIGHT * .5, BUTTON_WIDTH, BUTTON_HEIGHT)
    if instruction_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        which_screen = instruction_screen
    elif instruction_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, instruction_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, instruction_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, instruction_outline_rect, OUTLINE_WIDTH)
    instruction_text_surface = font.render("INSTRUCTIONS", True, OUTLINE_COLOR)
    instruction_text_rect = instruction_text_surface.get_rect()
    instruction_text_rect.center = instruction_outline_rect.center
    screen.blit(instruction_text_surface, instruction_text_rect)

    leaderboard_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 + BUTTON_HEIGHT * .75, BUTTON_WIDTH, BUTTON_HEIGHT)
    leaderboard_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 + BUTTON_HEIGHT * .75, BUTTON_WIDTH, BUTTON_HEIGHT)
    if leaderboard_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        leaderboard = jungle_leaderboard
        which_screen = leaderboard_screen
    elif leaderboard_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, leaderboard_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, leaderboard_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, leaderboard_outline_rect, OUTLINE_WIDTH)
    leaderboard_text_surface = font.render("LEADERBOARDS", True, OUTLINE_COLOR)
    leaderboard_text_rect = leaderboard_text_surface.get_rect()
    leaderboard_text_rect.center = leaderboard_outline_rect.center
    screen.blit(leaderboard_text_surface, leaderboard_text_rect)

    start_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 - BUTTON_HEIGHT * 1.75, BUTTON_WIDTH, BUTTON_HEIGHT)
    start_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 - BUTTON_HEIGHT * 1.75, BUTTON_WIDTH, BUTTON_HEIGHT)
    if start_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        if need_name == True:
            which_screen = add_name_screen
        else:
            which_screen = levels_screen
    elif start_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, start_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, start_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, start_outline_rect, OUTLINE_WIDTH)
    start_text_surface = font.render("START", True, OUTLINE_COLOR)
    start_text_rect = start_text_surface.get_rect()
    start_text_rect.center = start_outline_rect.center
    screen.blit(start_text_surface, start_text_rect)

    quit_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 + BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 + BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    if quit_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        sys.exit()
    elif quit_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, quit_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, quit_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, quit_button_rect, OUTLINE_WIDTH)
    quit_text_surface = font.render("QUIT", True, OUTLINE_COLOR)
    quit_text_rect = quit_text_surface.get_rect()
    quit_text_rect.center = quit_outline_rect.center
    screen.blit(quit_text_surface, quit_text_rect)

# Creates the screen that asks for the username
def create_add_name(screen, text, mouse_x, mouse_y, mouse_click):
    global home_screen
    global instruction_screen
    global leaderboard_screen
    global add_name_screen
    global levels_screen
    global gameover_screen
    global jungle_screen
    global ocean_screen
    global cities_screen
    global which_screen
    global start_ticks
    global score
    # Sets the constants for the screen
    BUTTON_WIDTH = 125
    BUTTON_HEIGHT = 50
    INPUT_BOX_WIDTH = 450
    INPUT_BOX_HEIGHT = 75
    FILL_COLOR = (238, 108, 77)
    OUTLINE_COLOR = (41, 50, 65)
    HOVER_COLOR = (212, 94, 66)
    OUTLINE_WIDTH = 2
    # Sets the fonts
    title_font = pygame.font.Font(None, 70)
    input_font = pygame.font.Font(None, 60)
    font = pygame.font.Font(None, 35)
    
    # Creates the text and buttons for the add name screen

    instruction_lines = ["PLEASE TYPE IN YOUR USERNAME AND PRESS ENTER"]
    line_height = title_font.get_height()
    y = 50
    for line in instruction_lines:
        # Split the line into multiple lines if it is too wide
        split_lines = []
        split_lines = split_line(line, title_font, width - 200)
        for split_l in split_lines:
            line_surface = title_font.render(split_l, True, OUTLINE_COLOR)
            line_rect = line_surface.get_rect()
            line_rect.centerx = width/2
            line_rect.y = y
            y += line_height
            screen.blit(line_surface, line_rect)
            # Check if the line is within the bounds of the box fill rectangle

    back_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 7/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    back_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 7/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    if back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        which_screen = home_screen
    elif back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, back_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, back_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, back_outline_rect, OUTLINE_WIDTH)
    back_text_surface = font.render("<-BACK", True, OUTLINE_COLOR)
    back_text_rect = back_text_surface.get_rect()
    back_text_rect.center = back_outline_rect.center
    screen.blit(back_text_surface, back_text_rect)

    skip_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 6/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    skip_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 6/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    if skip_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        score = 0
        which_screen = levels_screen
    elif skip_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, skip_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, skip_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, skip_outline_rect, OUTLINE_WIDTH)
    skip_text_surface = font.render("SKIP->", True, OUTLINE_COLOR)
    skip_text_rect = skip_text_surface.get_rect()
    skip_text_rect.center = skip_outline_rect.center
    screen.blit(skip_text_surface, skip_text_rect)

    input_outline_rect = pygame.Rect(width/2 - INPUT_BOX_WIDTH/2, height/2 - INPUT_BOX_HEIGHT, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)
    input_fill_rect = pygame.Rect(width/2 - INPUT_BOX_WIDTH/2 + 2, height/2 - INPUT_BOX_HEIGHT + 2, INPUT_BOX_WIDTH - 4, INPUT_BOX_HEIGHT - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, input_outline_rect)
    pygame.draw.rect(screen, FILL_COLOR, input_fill_rect)
    input_surface = input_font.render(text, True, OUTLINE_COLOR)
    text_rect = input_surface.get_rect()
    text_rect.center = input_outline_rect.center
    screen.blit(input_surface, text_rect)

# Creates the levels menu
def create_levels_menu(screen, mouse_x, mouse_y, mouse_click):
    global home_screen
    global instruction_screen
    global leaderboard_screen
    global add_name_screen
    global levels_screen
    global gameover_screen
    global jungle_screen
    global ocean_screen
    global cities_screen
    global which_screen
    global start_ticks
    global theme
    global score
    # Sets the constants for the game
    BACK_BUTTON_WIDTH = 125
    BACK_BUTTON_HEIGHT = 50
    BUTTON_WIDTH = 275
    BUTTON_HEIGHT = 80
    FILL_COLOR = (238, 108, 77)
    OUTLINE_COLOR = (41, 50, 65)
    HOVER_COLOR = (212, 94, 66)
    OUTLINE_WIDTH = 2
    
    # Creates the fonts for the game
    title_font = pygame.font.Font(None, 75)
    font = pygame.font.Font(None, 35)
    
    # Sets the text and buttons for the menu

    title_text_surface = title_font.render("LEVELS", True, OUTLINE_COLOR)
    title_text_rect = title_text_surface.get_rect()
    title_text_rect.center = (width/2, height/7)
    screen.blit(title_text_surface, title_text_rect)

    jungle_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 - BUTTON_HEIGHT * 1.75, BUTTON_WIDTH, BUTTON_HEIGHT)
    jungle_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 - BUTTON_HEIGHT * 1.75, BUTTON_WIDTH, BUTTON_HEIGHT)
    if jungle_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        start_ticks = pygame.time.get_ticks()
        theme = "jungle"
        score = 0
        which_screen = jungle_screen
    elif jungle_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, jungle_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, jungle_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, jungle_outline_rect, OUTLINE_WIDTH)
    jungle_text_surface = font.render("JUNGLE WORDS", True, OUTLINE_COLOR)
    jungle_text_rect = jungle_text_surface.get_rect()
    jungle_text_rect.center = jungle_outline_rect.center
    screen.blit(jungle_text_surface, jungle_text_rect)

    ocean_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 - BUTTON_HEIGHT * .5, BUTTON_WIDTH, BUTTON_HEIGHT)
    ocean_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 - BUTTON_HEIGHT * .5, BUTTON_WIDTH, BUTTON_HEIGHT)
    if ocean_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        start_ticks = pygame.time.get_ticks()
        theme = "ocean"
        score = 0
        which_screen = ocean_screen
    elif ocean_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, ocean_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, ocean_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, ocean_outline_rect, OUTLINE_WIDTH)
    ocean_text_surface = font.render("OCEAN WORDS", True, OUTLINE_COLOR)
    ocean_text_rect = ocean_text_surface.get_rect()
    ocean_text_rect.center = ocean_outline_rect.center
    screen.blit(ocean_text_surface, ocean_text_rect)

    cities_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 + BUTTON_HEIGHT * .75, BUTTON_WIDTH, BUTTON_HEIGHT)
    cities_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height/2 + BUTTON_HEIGHT * .75, BUTTON_WIDTH, BUTTON_HEIGHT)
    if cities_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        start_ticks = pygame.time.get_ticks()
        theme = "cities"
        score = 0
        which_screen = cities_screen
    elif cities_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, cities_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, cities_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, cities_outline_rect, OUTLINE_WIDTH)
    cities_text_surface = font.render("FAMOUS CITIES", True, OUTLINE_COLOR)
    cities_text_rect = cities_text_surface.get_rect()
    cities_text_rect.center = cities_outline_rect.center
    screen.blit(cities_text_surface, cities_text_rect)

    back_button_rect = pygame.Rect(width/2 - BACK_BUTTON_WIDTH/2, height * 7/8, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)
    back_outline_rect = pygame.Rect(width/2 - BACK_BUTTON_WIDTH/2, height * 7/8, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)
    if back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        which_screen = home_screen
    elif back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, back_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, back_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, back_outline_rect, OUTLINE_WIDTH)
    back_text_surface = font.render("<-BACK", True, OUTLINE_COLOR)
    back_text_rect = back_text_surface.get_rect()
    back_text_rect.center = back_outline_rect.center
    screen.blit(back_text_surface, back_text_rect)

# Creates the instruction screen
def create_instructions(screen, mouse_x, mouse_y, mouse_click):
    global home_screen
    global instruction_screen
    global leaderboard_screen
    global add_name_screen
    global levels_screen
    global gameover_screen
    global jungle_screen
    global ocean_screen
    global cities_screen
    global which_screen
    # Sets the constants for the screen
    BUTTON_WIDTH = 125
    BUTTON_HEIGHT = 50
    BOX_WIDTH = width * 3/4
    BOX_HEIGHT = height * 2/3
    FILL_COLOR = (238, 108, 77)
    OUTLINE_COLOR = (41, 50, 65)
    HOVER_COLOR = (212, 94, 66)
    OUTLINE_WIDTH = 2

    # Sets the fonts
    title_font = pygame.font.Font(None, 75)
    font = pygame.font.Font(None, 35)
    
    # Creates the text and buttons for the instructions screen

    title_text_surface = title_font.render("INSTRUCTIONS", True, OUTLINE_COLOR)
    title_text_rect = title_text_surface.get_rect()
    title_text_rect.center = (width/2, height/7)
    screen.blit(title_text_surface, title_text_rect)

    back_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 7/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    back_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 7/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    if back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        which_screen = home_screen
    elif back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, back_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, back_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, back_outline_rect, OUTLINE_WIDTH)
    back_text_surface = font.render("<-BACK", True, OUTLINE_COLOR)
    back_text_rect = back_text_surface.get_rect()
    back_text_rect.center = back_outline_rect.center
    screen.blit(back_text_surface, back_text_rect)

    # Sets the instruction text and box. Then it wraps the text within the box
    instruction_lines = [
                        "Welcome to Themeagrams!",
                        "",
                        "-The goal of the game is to solve as many anagrams in the time allowed",
                        "",
                        "-Anagrams are decided based on theme of the level",
                        "",
                        "-To guess the word, please type the word and press enter",
                        "",
                        "-Score is added by multiplying the number of letters in the word by 10"
                        ]
    line_height = font.get_height()
    box_outline_rect = pygame.Rect(width/2 - BOX_WIDTH/2, height/2 - BOX_HEIGHT * .47, BOX_WIDTH, BOX_HEIGHT)
    box_fill_rect = pygame.Rect(width/2 - BOX_WIDTH/2 + 2, height/2 - BOX_HEIGHT * .47 + 2, BOX_WIDTH - 4, BOX_HEIGHT - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, box_outline_rect, OUTLINE_WIDTH)
    pygame.draw.rect(screen, FILL_COLOR, box_fill_rect)
    # Render each line of instructions and blit it on the screen
    y = box_fill_rect.y + 20
    for line in instruction_lines:
        # Split the line into multiple lines if it is too wide
        split_lines = []
        split_lines = split_line(line, font, box_fill_rect.width - 100)
        for split_l in split_lines:
            line_surface = font.render(split_l, True, OUTLINE_COLOR)
            line_rect = line_surface.get_rect()
            line_rect.centerx = box_fill_rect.centerx
            line_rect.y = y
            y += line_height
            # Check if the line is within the bounds of the box fill rectangle
            if line_rect.bottom <= box_fill_rect.bottom:
                screen.blit(line_surface, line_rect)

# Creates the leaderboard screen
def create_leaderboard_screen(screen, mouse_x, mouse_y, mouse_click):
    global home_screen
    global instruction_screen
    global leaderboard_screen
    global add_name_screen
    global levels_screen
    global gameover_screen
    global jungle_screen
    global ocean_screen
    global cities_screen
    global which_screen
    global theme_leaderboard
    global leaderboard
    global jungle_leaderboard, ocean_leaderboard, cities_leaderboard
    # Sets the constants for the screen
    BUTTON_WIDTH = 125
    BUTTON_HEIGHT = 50
    BOX_WIDTH = width * 3/4
    BOX_HEIGHT = height * .55
    FILL_COLOR = (238, 108, 77)
    OUTLINE_COLOR = (41, 50, 65)
    HOVER_COLOR = (212, 94, 66)
    OUTLINE_WIDTH = 2

    # Sets the fonts for the screen
    title_font = pygame.font.Font(None, 75)
    theme_font = pygame.font.Font(None, 50)
    font = pygame.font.Font(None, 34)
    
    # Creates the text and buttons for the screen

    title_text_surface = title_font.render("LEADERBOARDS", True, OUTLINE_COLOR)
    title_text_rect = title_text_surface.get_rect()
    title_text_rect.center = (width/2, height/7)
    screen.blit(title_text_surface, title_text_rect)

    back_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 7/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    back_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 7/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    if back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        which_screen = home_screen
    elif back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, back_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, back_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, back_outline_rect, OUTLINE_WIDTH)
    back_text_surface = font.render("<-BACK", True, OUTLINE_COLOR)
    back_text_rect = back_text_surface.get_rect()
    back_text_rect.center = back_outline_rect.center
    screen.blit(back_text_surface, back_text_rect)
    
    jungle_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH * 1.75, height * .19, BUTTON_WIDTH, BUTTON_HEIGHT)
    jungle_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH * 1.75, height * .19, BUTTON_WIDTH, BUTTON_HEIGHT)
    if jungle_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        theme_leaderboard = "JUNGLE LEADERBOARD"
        leaderboard = jungle_leaderboard
    elif jungle_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, jungle_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, jungle_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, jungle_outline_rect, OUTLINE_WIDTH)
    jungle_text_surface = font.render("JUNGLE", True, OUTLINE_COLOR)
    jungle_text_rect = jungle_text_surface.get_rect()
    jungle_text_rect.center = jungle_outline_rect.center
    screen.blit(jungle_text_surface, jungle_text_rect)

    ocean_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH * .5, height * .19, BUTTON_WIDTH, BUTTON_HEIGHT)
    ocean_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH * .5, height * .19, BUTTON_WIDTH, BUTTON_HEIGHT)
    if ocean_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        theme_leaderboard = "OCEAN LEADERBOARD"
        leaderboard = ocean_leaderboard
    elif ocean_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, ocean_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, ocean_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, ocean_outline_rect, OUTLINE_WIDTH)
    ocean_text_surface = font.render("OCEAN", True, OUTLINE_COLOR)
    ocean_text_rect = ocean_text_surface.get_rect()
    ocean_text_rect.center = ocean_outline_rect.center
    screen.blit(ocean_text_surface, ocean_text_rect)

    cities_button_rect = pygame.Rect(width/2 + BUTTON_WIDTH * .75, height * .19, BUTTON_WIDTH, BUTTON_HEIGHT)
    cities_outline_rect = pygame.Rect(width/2 + BUTTON_WIDTH * .75, height * .19, BUTTON_WIDTH, BUTTON_HEIGHT)
    if cities_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        theme_leaderboard = "CITIES LEADERBOARD"
        leaderboard = cities_leaderboard
    elif cities_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, cities_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, cities_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, cities_outline_rect, OUTLINE_WIDTH)
    cities_text_surface = font.render("CITIES", True, OUTLINE_COLOR)
    cities_text_rect = cities_text_surface.get_rect()
    cities_text_rect.center = cities_outline_rect.center
    screen.blit(cities_text_surface, cities_text_rect)

    # Creates the leaderboord box and blits the scores onto the box
    box_outline_rect = pygame.Rect(width/2 - BOX_WIDTH/2, height/2 - BOX_HEIGHT * .38, BOX_WIDTH, BOX_HEIGHT)
    box_fill_rect = pygame.Rect(width/2 - BOX_WIDTH/2 + 2, height/2 - BOX_HEIGHT * .38 + 2, BOX_WIDTH - 4, BOX_HEIGHT - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, box_outline_rect, OUTLINE_WIDTH)
    pygame.draw.rect(screen, FILL_COLOR, box_fill_rect)
    theme_text_surface = theme_font.render(theme_leaderboard, True, OUTLINE_COLOR)
    text_width, text_height = theme_font.size(theme_leaderboard)
    text_x = box_fill_rect.centerx - text_width / 2
    text_y = box_fill_rect.y + 20
    screen.blit(theme_text_surface, (text_x, text_y))
    text = ""
    for i, (player, score) in enumerate(leaderboard):
        if i < 5:
            text = font.render(f'{i + 1}. {player}: {score}', True, OUTLINE_COLOR)
            screen.blit(text, (box_fill_rect.x + 20, box_fill_rect.y + 80 + i * 50))
        elif i < 10:
            text = font.render(f'{i + 1}. {player}: {score}', True, OUTLINE_COLOR)
            screen.blit(text, (BOX_WIDTH * .65, box_fill_rect.y + 80 + (i - 5) * 50))

# Creates the game over screen
def create_gameover(screen, mouse_x, mouse_y, mouse_click, prev_screen):
    global home_screen
    global instruction_screen
    global leaderboard_screen
    global add_name_screen
    global levels_screen
    global gameover_screen
    global jungle_screen
    global ocean_screen
    global cities_screen
    global score
    global start_ticks
    global which_screen
    global keep_word
    global name
    # Sets the constants for the screen
    TITLE_BOX_WIDTH = 400
    TITLE_BOX_HEIGHT = 100
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 75
    # Changes the colors based on which level was just finished
    if prev_screen == jungle_screen:
        FILL_COLOR = (181,255,181)
        OUTLINE_COLOR = (48, 141, 70)
        HOVER_COLOR = (141, 215, 141)
    if prev_screen == ocean_screen:
        FILL_COLOR = (79, 220, 255)
        OUTLINE_COLOR = (0, 111, 138)
        HOVER_COLOR = (51, 180, 212)
    if prev_screen == cities_screen:
        FILL_COLOR = (192,192,192)
        OUTLINE_COLOR = (105,105,105)
        HOVER_COLOR = (128,128,128)
    OUTLINE_WIDTH = 2

    # Sets the fonts
    title_font = pygame.font.Font(None, 75)
    font = pygame.font.Font(None, 35)
    
    # Creates the buttons and text for the screen

    title_outline_rect = pygame.Rect(width/2 - TITLE_BOX_WIDTH/2, height/2 - TITLE_BOX_HEIGHT*2, TITLE_BOX_WIDTH, TITLE_BOX_HEIGHT)
    word_fill_rect = pygame.Rect(width/2 - TITLE_BOX_WIDTH/2 + 2, height/2 - TITLE_BOX_HEIGHT*2 + 2, TITLE_BOX_WIDTH - 4, TITLE_BOX_HEIGHT - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, title_outline_rect, OUTLINE_WIDTH)
    pygame.draw.rect(screen, FILL_COLOR, word_fill_rect)
    title_text_surface = title_font.render("TIME'S UP", True, OUTLINE_COLOR)
    title_text_rect = title_text_surface.get_rect()
    title_text_rect.center = title_outline_rect.center
    screen.blit(title_text_surface, title_text_rect)

    restart_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH*1.1, height*(2/3), BUTTON_WIDTH, BUTTON_HEIGHT)
    restart_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH*1.1, height*(2/3), BUTTON_WIDTH, BUTTON_HEIGHT)
    if restart_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        start_ticks = pygame.time.get_ticks()
        score = 0
        keep_word = False
        which_screen = prev_screen
    elif restart_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, restart_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, restart_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, restart_outline_rect, OUTLINE_WIDTH)
    restart_text_surface = font.render("PLAY AGAIN", True, OUTLINE_COLOR)
    restart_text_rect = restart_text_surface.get_rect()
    restart_text_rect.center = restart_outline_rect.center
    screen.blit(restart_text_surface, restart_text_rect)
    
    home_button_rect = pygame.Rect(width/2 + BUTTON_WIDTH/10, height*(2/3), BUTTON_WIDTH, BUTTON_HEIGHT)
    home_outline_rect = pygame.Rect(width/2 + BUTTON_WIDTH/10, height*(2/3), BUTTON_WIDTH, BUTTON_HEIGHT)
    if home_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        which_screen = home_screen
    elif home_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, home_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, home_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, home_outline_rect, OUTLINE_WIDTH)
    home_text_surface = font.render("HOME", True, OUTLINE_COLOR)
    home_text_rect = home_text_surface.get_rect()
    home_text_rect.center = home_outline_rect.center
    screen.blit(home_text_surface, home_text_rect)

    score_outline_rect = pygame.Rect(title_outline_rect.x, height/2 - TITLE_BOX_HEIGHT*.5, TITLE_BOX_WIDTH, TITLE_BOX_HEIGHT)
    score_fill_rect = pygame.Rect(title_outline_rect.x + 2, height/2 - TITLE_BOX_HEIGHT*.5 + 2, TITLE_BOX_WIDTH - 4, TITLE_BOX_HEIGHT - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, score_outline_rect, OUTLINE_WIDTH)
    pygame.draw.rect(screen, FILL_COLOR, score_fill_rect)
    score_surface = title_font.render(f"{score} PTS", True, OUTLINE_COLOR)
    score_rect = score_surface.get_rect()
    score_rect.center = score_outline_rect.center
    screen.blit(score_surface, score_rect)
    

def create_game(screen, text, word, seconds, score, mouse_x, mouse_y, mouse_click):
    global home_screen
    global instruction_screen
    global leaderboard_screen
    global add_name_screen
    global levels_screen
    global gameover_screen
    global jungle_screen
    global ocean_screen
    global cities_screen
    global which_screen
    global keep_word
    global reset_text
    #Create box widths and heights
    WORD_BOX_WIDTH = 400
    WORD_BOX_HEIGHT = 75
    BUTTON_WIDTH = 125
    BUTTON_HEIGHT = 50
    TIME_BOX_WH = 90
    # Create colors
    FILL_COLOR = (0, 0, 0)
    OUTLINE_COLOR = (0, 0, 0)
    HOVER_COLOR = (0, 0, 0)
    if which_screen == jungle_screen:
        FILL_COLOR = (181,255,181)
        OUTLINE_COLOR = (48, 141, 70)
        HOVER_COLOR = (141, 215, 141)
    if which_screen == ocean_screen:
        FILL_COLOR = (79, 220, 255)
        OUTLINE_COLOR = (0, 111, 138)
        HOVER_COLOR = (51, 180, 212)
    if which_screen == cities_screen:
        FILL_COLOR = (192,192,192)
        OUTLINE_COLOR = (105,105,105)
        HOVER_COLOR = (150,150,150)
    OUTLINE_WIDTH = 2
    # Create fonts
    SCORE_BOX_WIDTH = WORD_BOX_WIDTH - TIME_BOX_WH - 10
    font = pygame.font.Font(None, 60)
    time_font = pygame.font.Font(None, 60)
    back_font = pygame.font.Font(None, 35)

    # Creates the buttons and text for the screen

    input_outline_rect = pygame.Rect(width/2 - WORD_BOX_WIDTH/2, height/2 + WORD_BOX_HEIGHT, WORD_BOX_WIDTH, WORD_BOX_HEIGHT)
    input_fill_rect = pygame.Rect(width/2 - WORD_BOX_WIDTH/2 + 2, height/2 + WORD_BOX_HEIGHT + 2, WORD_BOX_WIDTH - 4, WORD_BOX_HEIGHT - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, input_outline_rect)
    pygame.draw.rect(screen, FILL_COLOR, input_fill_rect)
    input_surface = font.render(text[:14], True, OUTLINE_COLOR)
    text_rect = input_surface.get_rect()
    text_rect.center = input_outline_rect.center
    screen.blit(input_surface, text_rect)

    word_outline_rect = pygame.Rect(width/2 - WORD_BOX_WIDTH/2, height/2 - WORD_BOX_HEIGHT*2, WORD_BOX_WIDTH, WORD_BOX_HEIGHT)
    word_fill_rect = pygame.Rect(width/2 - WORD_BOX_WIDTH/2 + 2, height/2 - WORD_BOX_HEIGHT*2 + 2, WORD_BOX_WIDTH - 4, WORD_BOX_HEIGHT - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, word_outline_rect, OUTLINE_WIDTH)
    pygame.draw.rect(screen, FILL_COLOR, word_fill_rect)
    word_surface = font.render(word, True, OUTLINE_COLOR)
    word_rect = word_surface.get_rect()
    word_rect.center = word_outline_rect.center
    screen.blit(word_surface, word_rect)
    
    time_outline_rect = pygame.Rect(word_outline_rect.x, TIME_BOX_WH/3, TIME_BOX_WH, TIME_BOX_WH)
    time_fill_rect = pygame.Rect(word_outline_rect.x + 2, TIME_BOX_WH/3 + 2, TIME_BOX_WH - 4, TIME_BOX_WH - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, time_outline_rect, OUTLINE_WIDTH)
    pygame.draw.rect(screen, FILL_COLOR, time_fill_rect)
    time_surface = time_font.render(str(30 - math.floor(seconds)), True, OUTLINE_COLOR)
    time_rect = time_surface.get_rect()
    time_rect.center = time_outline_rect.center
    screen.blit(time_surface, time_rect)

    score_outline_rect = pygame.Rect(word_outline_rect.x + WORD_BOX_WIDTH - SCORE_BOX_WIDTH, TIME_BOX_WH/3, SCORE_BOX_WIDTH, TIME_BOX_WH)
    score_fill_rect = pygame.Rect(word_outline_rect.x + WORD_BOX_WIDTH - SCORE_BOX_WIDTH + 2, TIME_BOX_WH/3 + 2, SCORE_BOX_WIDTH - 4, TIME_BOX_WH - 4)
    pygame.draw.rect(screen, OUTLINE_COLOR, score_outline_rect, OUTLINE_WIDTH)
    pygame.draw.rect(screen, FILL_COLOR, score_fill_rect)
    score_surface = time_font.render(f"{score} PTS", True, OUTLINE_COLOR)
    score_rect = score_surface.get_rect()
    score_rect.center = score_outline_rect.center
    screen.blit(score_surface, score_rect)
    
    back_button_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 7/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    back_outline_rect = pygame.Rect(width/2 - BUTTON_WIDTH/2, height * 7/8, BUTTON_WIDTH, BUTTON_HEIGHT)
    if back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == True:
        which_screen = home_screen
        keep_word = False
        reset_text = True
    elif back_button_rect.collidepoint(mouse_x, mouse_y) and mouse_click == False:
        pygame.draw.rect(screen, HOVER_COLOR, back_button_rect)
    else:
        pygame.draw.rect(screen, FILL_COLOR, back_button_rect)
    pygame.draw.rect(screen, OUTLINE_COLOR, back_outline_rect, OUTLINE_WIDTH)
    back_text_surface = back_font.render("<-BACK", True, OUTLINE_COLOR)
    back_text_rect = back_text_surface.get_rect()
    back_text_rect.center = back_outline_rect.center
    screen.blit(back_text_surface, back_text_rect)

# Chooses word based on theme of the level
def choose_word(theme):
    global home_screen
    global instruction_screen
    global leaderboard_screen
    global add_name_screen
    global levels_screen
    global gameover_screen
    global jungle_screen
    global ocean_screen
    global cities_screen
    global keep_word
    global jungle_words
    global ocean_words
    global famous_cities
    global prev_word
    
    # If the game needs a new word, it will choose a word based on theme of the level and then remove the word from the list\
    # If there are no words left, the list will reset

    if theme == "jungle" and keep_word == False:
        rand_word = random.choice(jungle_words)
        keep_word = True
        prev_word = rand_word
        words_reset.append(prev_word)
        if prev_word in jungle_words:
            jungle_words.remove(prev_word)
        if len(jungle_words) == 0:
            jungle_words = words_reset
        return rand_word
    if theme == "ocean" and keep_word == False:
        rand_word = random.choice(ocean_words)
        keep_word = True
        prev_word = rand_word
        words_reset.append(prev_word)
        if prev_word in ocean_words:
            ocean_words.remove(prev_word)
        if len(ocean_words) == 0:
            ocean_words = words_reset
        return rand_word
    if theme == "cities" and keep_word == False:
        rand_word = random.choice(famous_cities)
        keep_word = True
        prev_word = rand_word
        words_reset.append(prev_word)
        if prev_word in famous_cities:
            famous_cities.remove(prev_word)
        if len(famous_cities) == 0:
            famous_cities = words_reset
        return rand_word

# Takes the word chosen, splits it into its characters, shuffles the characters, and then puts the characters back together
def create_anagram(theme):
    word = choose_word(theme).upper()
    charList = list(word)
    random.shuffle(charList)
    anagram = "".join(charList)
    return anagram, word

# Main loop of the game
while True:
    # Retieves mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Sets the frame rate of the game
    clock.tick(60)
    
    # Loop for the home screen
    if which_screen == home_screen:
        # Fills the background
        screen.fill(home_bg)
        # Resets mouse click to false
        mouse_click = False
        # Checks for any events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
                create_home(screen, mouse_x, mouse_y, mouse_click)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        create_home(screen, mouse_x, mouse_y, mouse_click)
        # Updates the screen
        pygame.display.update()

    # Loop for instruction screen
    elif which_screen == instruction_screen:
        screen.fill(home_bg)
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
                create_instructions(screen, mouse_x, mouse_y, mouse_click)
        mouse_click = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        create_instructions(screen, mouse_x, mouse_y, mouse_click)
        pygame.display.update()

    # Loop for leaderboard screen
    elif which_screen == leaderboard_screen:
        screen.fill(home_bg)
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
                create_leaderboard_screen(screen, mouse_x, mouse_y, mouse_click)
        mouse_click = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        create_leaderboard_screen(screen, mouse_x, mouse_y, mouse_click)
        pygame.display.update()

    # Loop for the ask name screen
    elif which_screen == add_name_screen:
        screen.fill(home_bg)
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and (event.unicode.isupper() or event.unicode.islower()):
                    name_text += event.unicode
            if event.type == MOUSEBUTTONDOWN:
                mouse_click = True
                create_add_name(screen, text, mouse_x, mouse_y, mouse_click)
        keys = pygame.key.get_pressed()
        # Adds a space if the space bar is pressed
        if keys[pygame.K_SPACE]:
            name_text += " "
            pygame.time.wait(200)
        # Removes text if the delete key is pressed
        if keys[pygame.K_BACKSPACE]:
                    name_text = name_text[:-1]
                    pygame.time.wait(200)
        # Submits name if return button is pressed
        if keys[pygame.K_RETURN]:
            name = name_text
            pygame.time.wait(250)
            name_text = ""
            start_ticks = pygame.time.get_ticks()
            which_screen = levels_screen
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        mouse_click = False
        create_add_name(screen, name_text, mouse_x, mouse_y, mouse_click)
        pygame.display.update()

    # Loop for levels menu
    elif which_screen == levels_screen:
        screen.fill(home_bg)
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
                create_levels_menu(screen, mouse_x, mouse_y, mouse_click)
        mouse_click = False
        create_levels_menu(screen, mouse_x, mouse_y, mouse_click)
        pygame.display.update()

    # Loop for the jungle level
    elif which_screen == jungle_screen:
        seconds = (pygame.time.get_ticks()-start_ticks)/1000 # Calculate how many seconds have passed
        # Resets the text if it is needed
        if reset_text == True:
            text = ""
            reset_text = False
        screen.blit(jungle_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and (event.unicode.isupper() or event.unicode.islower()):
                    text += event.unicode.upper()
            if event.type == MOUSEBUTTONDOWN:
                mouse_click = True
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
        keys = pygame.key.get_pressed()
        # Keeps removing text if the backspace is held down
        if keys[pygame.K_BACKSPACE]:
                    text = text[:-1]
                    pygame.time.wait(200)
        # Adds a space if the space bar is pressed
        if keys[pygame.K_SPACE]:
            text += ""
            pygame.time.wait(200)
        # If return key is pressed, the game checks to see if the guess is correct
        # If it is correct, it will set keep_word to false so that the game will pick a new word
        if keys[pygame.K_RETURN]:
            if text == word:
                keep_word = False
                text = "CORRECT"
                score += len(word) * 10
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
                pygame.display.update()
                pygame.time.wait(750)
                text = ""
            else:
                text = "WRONG"
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
                pygame.display.update()
                pygame.time.wait(750)
                text = ""
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        if keep_word == False: 
            anagram, word = create_anagram(theme)
        create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
        # If the timer runs out, the game will save the score and add it to the leaderboard, but only if a name was submitted
        # It will then set the screen to the game over screen
        if seconds >= 30:
            keep_word = False
            text = ""
            if name != "":
                jungle_players.append(name)
                jungle_scores.append(score)
                jungle_leaderboard = update_leaderboard(jungle_players, jungle_scores, 'jungle_leaderboard.txt')
            prev_screen = jungle_screen
            which_screen = gameover_screen 
        pygame.display.update()

    elif which_screen == ocean_screen:
        seconds = (pygame.time.get_ticks()-start_ticks)/1000 # Calculate how many seconds have passed
        if reset_text == True:
            text = ""
            reset_text = False
        screen.blit(ocean_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and (event.unicode.isupper() or event.unicode.islower()):
                    text += event.unicode.upper()
            if event.type == MOUSEBUTTONDOWN:
                mouse_click = True
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
        keys = pygame.key.get_pressed()
        # Keeps removing text if the backspace is held down
        if keys[pygame.K_BACKSPACE]:
                    text = text[:-1]
                    pygame.time.wait(200)
        # Adds a space if the space bar is pressed
        if keys[pygame.K_SPACE]:
            text += ""
            pygame.time.wait(200)
        if keys[pygame.K_RETURN]:
            if text == word:
                keep_word = False
                text = "CORRECT"
                score += len(word) * 10
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
                pygame.display.update()
                pygame.time.wait(750)
                text = ""
            else:
                text = "WRONG"
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
                pygame.display.update()
                pygame.time.wait(750)
                text = ""
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        if keep_word == False: 
            anagram, word = create_anagram(theme)
        create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
        if seconds >= 30:
            keep_word = False
            text = ""
            if name != "":
                ocean_players.append(name)
                ocean_scores.append(score)
                ocean_leaderboard = update_leaderboard(ocean_players, ocean_scores, 'ocean_leaderboard.txt')
            prev_screen = ocean_screen
            which_screen = gameover_screen 
        pygame.display.update()

    elif which_screen == cities_screen:
        seconds = (pygame.time.get_ticks()-start_ticks)/1000 # Calculate how many seconds have passed
        if reset_text == True:
            text = ""
            reset_text = False 
        screen.blit(city_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and (event.unicode.isupper() or event.unicode.islower()):
                    text += event.unicode.upper()
            if event.type == MOUSEBUTTONDOWN:
                mouse_click = True
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
        keys = pygame.key.get_pressed()
        # Keeps removing text if the backspace is held down
        if keys[pygame.K_BACKSPACE]:
                    text = text[:-1]
                    pygame.time.wait(200)
        if keys[pygame.K_SPACE]:
            text += ""
            pygame.time.wait(200)
        if keys[pygame.K_RETURN]:
            if text == word:
                keep_word = False
                text = "CORRECT"
                score += len(word) * 10
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
                pygame.display.update()
                pygame.time.wait(750)
                text = ""
            else:
                text = "WRONG"
                create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
                pygame.display.update()
                pygame.time.wait(750)
                text = ""
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        if keep_word == False: 
            anagram, word = create_anagram(theme)
        create_game(screen, text, anagram, seconds, score, mouse_x, mouse_y, mouse_click)
        if seconds >= 30:
            keep_word = False
            text = ""
            if name != "":
                cities_players.append(name)
                cities_scores.append(score)
                cities_leaderboard = update_leaderboard(cities_players, cities_scores, 'cities_leaderboard.txt')
            pygame.time.wait(200)
            prev_screen = cities_screen
            which_screen = gameover_screen
        pygame.display.update()
    
    # Loop for the gameover screen
    elif which_screen == gameover_screen:
        # Decides theme based on which level just ended
        if prev_screen == jungle_screen:
            screen.blit(jungle_bg, (0, 0))
        if prev_screen == ocean_screen:
            screen.blit(ocean_bg, (0, 0))
        if prev_screen == cities_screen:
            screen.blit(city_bg, (0, 0))
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
                create_gameover(screen, mouse_x, mouse_y, mouse_click, prev_screen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        mouse_click = False
        create_gameover(screen, mouse_x, mouse_y, mouse_click, prev_screen)
        pygame.display.update()
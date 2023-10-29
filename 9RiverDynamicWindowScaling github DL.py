# -*- coding: utf-8 -*-
'''
Created on Sat Sep 23 08:53:16 2023
@author: Karl

Acknowledgement:
deck_image pngegg.png by macrovector on Freepik

General notes:
    - Card objects are stored as integers, not strings, and are stored in a
        non-intuitive way. If you need to identify a Card object, either use
        the Card.int_to_str() utility or Card.print_pretty_cards.
    - It isn't clear that it is necessary to include pygame.init() everywhere,
        but the consensus from other pygame developers is that it can't hurt 
        and might help.
    - Drawing or blitting an image **does not** update the display. You need to
        call pygame.display.flip() to update the display.
    - Try not to call pygame.display.flip() more often than necessary.
        Doing so can cause flickering.
    - If pygame encounters an error, it will hang and will need to be stopped.
        Python will probably stop responding. **Freaking save** before you run.
    - The combination of pygame.quit() and sys.exit() seems to close safely.
    - There is no direct way to remove rectangles or text. We just draw over
        them with new felt_color rectangles.
    - The hard-coded numbers for positions can be changed if the size of the
        cards change significantly.
'''

#you will need to install pygame and treys, and maybe PIL
import pygame
import os
from PIL import Image
import sys
import treys
import time
from typing import List, Tuple


pygame.font.init()
'''
Global constants
rank_order: the order of cards as they appear left-to-right in deck image
suit_order: the order of suits as they appear top-to-bottom in deck image
width, height: the width and height of a single card in the card image in px
scale_factor: the amount to scale up or down card images for display in hands
deck_iamge: a single image with all 52 cards;
    update path to local file
screen_width, screen_height: the height and width of the game screen in px
number_of_hands: the number of hands;
    probably fixed at 9
x, y: arrays of the start coordinates for the hands in px;
    len(x), len(y) must equal numer_of_hands
board_x, _y: the x and y coordinates where the game displays top left corner
    of the first flop cards
felt_color: the rgb code for the background color of the screen
button_color: the rgb code for the color of the buttons
font_color: the rgb code for the font used on buttons and for results
winning_color: the rgb code for the box put around the winning hand(s)
selected_color: the rgb code for the box put around the selected hand
box_width: the width of the box around winning/selected hands in px
font: the font used for button and message text
starting_bet: the initial amount bet. make sure that this is divisible by all
    bet modifications
'''
SCALE = 1
rank_order = {'A':0, '2':1, '3': 2, '4':3, '5':4, '6':5, '7':6, '8':7,
              '9':8, 'T':9, 'J':10, 'Q':11, 'K':12}
suit_order = {'h':0, 's':1, 'd':2, 'c':3}
width = int(225/SCALE)
height = int(315/SCALE)
scale_factor = 0.5/SCALE
deck_image = Image.open(r"D:\9totheRiver\pngegg.png")
screen_width = int(1600/SCALE)
screen_height = int(1200/SCALE)
number_of_hands = 9
x = [int(val / SCALE) for val in [100, 100, 100, 400, 700, 1000, 1300, 1300, 1300]]
y = [int(val / SCALE) for val in [700, 400, 100, 100, 100, 100, 100, 400, 700]]
board_x = int(500/SCALE)
board_y = int(550/SCALE)
felt_color = (53, 101, 77)
button_color = (255, 0, 0)
font_color = (255, 255, 255)
winning_color = (255, 0, 0)
selected_color = (0, 0, 255)
box_width = int(5/SCALE)
font = pygame.font.Font(None, 36)
starting_bet = 2
player_score = 0

def card_to_rank_and_suit(card: int) -> Tuple[int, int]:
    """
    Return the rank order and suit order of a card to locate in image.
    
    card: the integer representing the card to be ranked.
    
    NB: if not behaving as expected, make sure global rank_order and
    suit_order dictionaries reflect the deck image being used.
    """
    str_card = treys.Card.int_to_str(card)
    return((rank_order[str_card[0]], suit_order[str_card[1]]))

def display_card(card: int, card_x: int, card_y: int, scale: bool = True) -> None:
    """
    Identifies the part of the deck images that contains the card pass, and
        displays the card at a specific location.
    
    card: the integer representing the card to be displayed
    card_x, _y: the x and y positions of the top left corner of the card
    scale: should the card be scaled? currently, there is no use of False
    """
    pygame.init()
    (ro, so) = card_to_rank_and_suit(card)
    left, right = width * ro, width * (ro + 1)
    top, bottom = height * so, height * (so + 1)
    card_image = deck_image.crop((left, top, right, bottom))
    if scale:
        card_image = card_image.resize((int(width * scale_factor), 
                                    int(height * scale_factor)))
    str_card_image = card_image.tobytes()
    window.blit(pygame.image.fromstring(str_card_image, card_image.size, 
                                        card_image.mode), (card_x, card_y))
    pygame.display.flip()
    pass

def display_hand(hand: List[int], hand_x: int, hand_y: int) -> None:
    """
    Displays an entire hand at a specified location, one card at a time.
    
    hand: a list of two cards to display
    hand_x, _y: the coordinates of the top left corner of the hand
    """
    display_card(hand[0], hand_x, hand_y)
    display_card(hand[1], int(hand_x + width * scale_factor), hand_y)
    pass

def display_text(text: str, text_x: int, text_y: int) -> None:
    """
    Displays the specified text.
    
    text: the text to be displayed
    text_x, _y: the coorindates of the top left corner of the text render
    """
    pygame.init()
    text_image = font.render(text, True, font_color)
    window.blit(text_image, (text_x, text_y))
    pygame.display.flip()
    pass

def draw_button(text: str, button_x: int, button_y: int, 
                button_width: int, button_height: int) -> None:
    """
    Draw a button with specified text at a given location.
    
    text: the text of the button
    button_x, _y: the coordinates of the top left corner of the button
    button_width, _height: the width and height of the button
    
    NB: the button does not do anything
    """
    pygame.init()
    pygame.draw.rect(window, button_color, (button_x, button_y, 
                                            button_width, button_height))
    text_surface = font.render(text, True, font_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (button_x + button_width // 2, 
                        button_y + button_height // 2)  
    window.blit(text_surface, text_rect)
    pygame.display.flip()
    pass

def draw_rectangle(box_x: int, box_y: int, color: Tuple[int, int, int],
                   width: int, height: int) -> None:
    """
    Draw a rectangle at the specified location
    
    box_x, _y: the coordinates of the top left corner of the rectangle
    color: the rgb code for the desired color of the rectangle
    width, height: the width and height of the rectangle
    """
    pygame.init()
    pygame.draw.rect(window, color, (box_x, box_y, width, height))
    pygame.display.flip()

def draw_rectangle_box(box_x: int, box_y: int, color: Tuple[int, int, int]) -> None:
    """"
    Draw an empty rectangular box around a hand with specified location
    
    box_x, _y: the coordinates of the top left corner of the hand to be boxed
    color: the rgb code for the color of the box
    
    NB: this is designed to draw around a two card hand. It will always draw
        in that size, since there is no other need for a box like this.
    """
    pygame.init()
    pygame.draw.rect(window, color, (box_x - box_width, box_y - box_width, 
                                     (width * scale_factor + box_width) * 2,
                                     height * scale_factor + box_width * 2),
                     width = box_width)
    pygame.display.flip()
    
def make_selection() -> int:
    """
    Allows the player to select a hand. The game waits for the player to click.
    If that click is within the known coordinates of a hand, return the index
    of that hand. Otherwise, continue to wait.
    
    i: the index of the hand selected. The hands are arranged graphically in
        the same order they appear in the list hands.
    """
    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(number_of_hands):
                    if (x[i] <= mouse_x <= x[i] + width * 2 * scale_factor 
                        and y[i] <= mouse_y <= y[i] + height * scale_factor):
                        draw_rectangle_box(x[i], y[i], selected_color)
                        return i

def display_bet() -> None:
    """"
    Erase the current bet and draw the new bet in its place.
    """
    draw_rectangle(int(150/SCALE), int(1000/SCALE), felt_color, int(300/SCALE), int(200/SCALE))
    display_text(f'Current bet: {bet}', int(150/SCALE), int(1000/SCALE))
    
def display_eligible() -> None:
    """
    Erase the current eligibility status and draw the new one it its place.
    Note that eligibility is equivalent to (not switched).
    """
    draw_rectangle(int(1300/SCALE), int(1000/SCALE), felt_color, int(300/SCALE), int(200/SCALE))
    if switched:
        display_text('Bonus ineligible', int(1300/SCALE), int(1000/SCALE))
    else:
        display_text('Bonus eligible!', int(1300/SCALE), int(1000/SCALE))
                    
def deal_flop() -> Tuple[int, int, bool]:
    """
    Display the flop, then display three buttons. Wait for the user to click to
    either double the bet, switch hands, or stand pat. The order of the ifs 
    follows the order of the button texts; that is where to modify the behavior
    if needed.
    
    (bet, selected, switched) is returned, updating the bet amount, hand that
        is selected, and whether or not the hand has been switched.
    """
    pygame.init()
    draw_rectangle(board_x, board_y, felt_color, width * 5 * scale_factor, 
                   height)
    for i in range(3):
        display_card(board[i], board_x + width * i * scale_factor + 5 * i, board_y)
    button_texts = ['Double', 'Switch', 'Pat']
    for i in range(3):
        draw_button(button_texts[i], int(500 / SCALE + 200 * i / SCALE), int(1000 / SCALE), int(150 / SCALE), int(100 / SCALE))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if int(500 / SCALE) <= mouse_x <= int(650 / SCALE) and int(1000 / SCALE) <= mouse_y <= int(1100 / SCALE):                    
                    return (bet * 2, selected, False)
                elif int(700 / SCALE) <= mouse_x <= int(850 / SCALE) and int(1000 / SCALE) <= mouse_y <= int(1100 / SCALE):
                    draw_rectangle_box(int(x[selected] / SCALE), int(y[selected] / SCALE), felt_color)
                    draw_rectangle(int(500 / SCALE), int(1000 / SCALE), felt_color, int(600 / SCALE), int(100 / SCALE))
                    display_text('Please select a new hand', int(680 / SCALE), int(1000 / SCALE))
                    return (bet, make_selection(), True)
                elif int(900 / SCALE) <= mouse_x <= int(1050 / SCALE) and int(1000 / SCALE) <= mouse_y <= int(1100 / SCALE):
                    return (bet, selected, False)
                
def deal_turn() -> int:
    """
    Display the turn, then display three buttons. Wait for the user to click to
    either double the bet, halve the bet, or stand pat. The order of the ifs 
    follows the order of the button texts; that is where to modify the behavior
    if needed.
    
    bet is returned, updating the amount being wagered. Nothing else can change
    on the turn as presently designed.
    
    NB: the turn has 20 px of space between it and the flop, instead of the 
    5 px between flop cards.
    """
    pygame.init()
    draw_rectangle(int(500 / SCALE), int(1000 / SCALE), felt_color, int(600 / SCALE), int(300 / SCALE))
    display_card(board[3], board_x + width * 3 * scale_factor + 30, board_y)
    button_texts = ['Double', 'Halve', 'Pat']
    for i in range(3):
        draw_button(button_texts[i], int((500 + 200 * i) / SCALE), int(1000 / SCALE), int(150 / SCALE), int(100 / SCALE))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if int(500 / SCALE) <= mouse_x <= int(650 / SCALE) and int(1000 / SCALE) <= mouse_y <= int(1100 / SCALE):                    
                    return bet * 2
                elif int(700 / SCALE) <= mouse_x <= int(850 / SCALE) and int(1000 / SCALE) <= mouse_y <= int(1100 / SCALE):
                    return bet // 2
                elif int(900 / SCALE) <= mouse_x <= int(1050 / SCALE) and int(1000 / SCALE) <= mouse_y <= int(1100 / SCALE):
                    return bet
    
def deal_river() -> None:
    """
    Currently, there is nothing to do on the river but display the river card.
    If that changes, make those modifications here.
    
    NB: the river has 20 px of space between it and the turn, instead of the
    5 px between flop cards.
    """
    display_card(board[4], board_x + width * 4 * scale_factor + 50, board_y)

def bonus(hand) -> int:
    """
    Determines what, if any, bonus should be applied to a hand. Currently, the
    hands that are eligible for bonuses are quads+, TT-, AA, and 72, but *only*
    if switched is False.
    
    hand: the selected and sole winning hand    
    
    return either 1 or the bonus amount, so that this can always be multiplied
    by the amount bet.
    """
    if switched:
        return 1
    evaluator = treys.Evaluator()
    best_class = evaluator.get_rank_class(evaluator.evaluate(hand, board))
    if best_class in (0, 1, 2):
        return 2
    if 4205 < evaluator.evaluate(hand, board) < 6185:
        return 2
    if {treys.Card.int_to_str(hand[0]), 
           treys.Card.int_to_str(hand[0])} == {'A'}:
        return 2
    if {treys.Card.int_to_str(hand[0]), 
            treys.Card.int_to_str(hand[0])} == {'7', '2'}:
        return 2
    return 1
    
def who_wins() -> None:
    global player_score
    print(f"Player score at start of who_wins: {player_score}")
    """
    Finds the winning hand(s), boxes them, and tells the player of the result.
    Currently, a loss can have a tied winner but a win cannot.
    """
    draw_rectangle(int(500 / SCALE), int(1000 / SCALE), felt_color, int(600 / SCALE), int(300 / SCALE))
    evaluator = treys.Evaluator()
    hand_values = [evaluator.evaluate(hand, board) for hand in hands]
    best_hand = min(hand_values)
    for i, value in enumerate(hand_values):
        if value == best_hand:
            draw_rectangle_box(x[i], y[i], winning_color)
    if hand_values[selected] > best_hand:
        player_score -= bet  # Deduct the bet from the player's score
        display_text(f'You lose {bet}', int(680 / SCALE), int(1000 / SCALE))
    else:
        if hand_values.count(best_hand) > 1:
            display_text('You tie and win 0', int(680 / SCALE), int(1000 / SCALE))
        else:
            win_amount = bet * bonus(hands[selected])
            player_score += win_amount
            display_text(f'You win {win_amount}!', int(680 / SCALE), int(1000 / SCALE))

    # Display the running total of the player's score
    draw_rectangle(50, 50, felt_color, 300, 50)  # Clear previous score display
    display_text(f'Total Score: {player_score}', int(50 / SCALE), int(50 / SCALE))
    print(f"Player score at end of who_wins: {player_score}")
""""
Initialize the screen, deck, hands, board, and other variables
"""
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1366 + 100, 1)
bet = starting_bet
switched = False
selected = 0
pygame.init()
window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
deck = treys.Deck()
hands = []
for i in range(number_of_hands):
    hands.append(deck.draw(2))
board = deck.draw(5)
window.fill(felt_color)
for i, hand in enumerate(hands):
    display_hand(hand, x[i], y[i])

"""
Prompt the user to select a hand
"""
display_bet()
display_eligible()
display_text('Please select a hand', int(680 / SCALE), int(600 / SCALE))
selected = make_selection()

"""
Display the flop and adjust bet, selected hand, and bonus eligibility as needed
"""
(bet, selected, switched) = deal_flop()
display_bet()
display_eligible()
time.sleep(0.5)

"""
Display the turn and update the bet.
"""
bet = deal_turn()
display_bet()
time.sleep(0.5)

"""
Display the river, determine the winner, and tell the player the result
"""
deal_river()

who_wins()

time.sleep(3)

##Run loop again here##

pygame.quit()
sys.exit()

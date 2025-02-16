"""Attempt at a pygame window view
tutorial based on g4g :")
+ https://youtu.be/Rvcyf4HsWiw?si=WK7eG4Km0GI3Qrc7 for text input
"""
import random
import re
import time
from copy import deepcopy

import pygame

import pygame_entities as p_ent
import game_entities as g_ent
import word_chain as wc

pygame.init()
assert pygame.get_init()

# hold to duplicate keyboard input
pygame.key.set_repeat(500, 100)

# display set up
width = p_ent.WIDTH
height = p_ent.HEIGHT
window = p_ent.WINDOW

# update display
pygame.display.set_caption("Word chain!")
pygame.display.update()

# overlay
overlay = pygame.Surface((width, height))
overlay.fill((255, 255, 255))
overlay.set_alpha(165)

# other
clock = pygame.time.Clock()
bg_color = (238, 238, 228)
font = "Cochin, Times New Roman"

pygame.time.set_timer(pygame.USEREVENT, 1000)


# RENDERING BASIC TEXT
def render_text(user_text: str, input_rectangle: pygame.Rect, input_font: pygame.font, textbox: bool = False):
    """

    :param user_text:
    :param input_rectangle:
    :param input_font:
    """
    if textbox:
        pygame.draw.rect(window, "black", input_rectangle, 2)
    else:
        # pygame.draw.rect(window, bg_color, input_rectangle, 0)
        pass

    if "P1" in user_text:
        color = "red"
    elif "P2" in user_text:
        color = "blue"
    else:
        color = "black"
    text_surface = input_font.render(user_text, False, color)
    # w = text_surface.get_width()
    window.blit(text_surface, (input_rectangle.x + 12, input_rectangle.y + 12.5))
    input_rectangle.w = max(text_surface.get_width() + 12, 200) + 12


# RENDERING MAIN WINDOW
def render_main_text(turn_text: dict[str, str], input_rects: dict[str, pygame.rect],
                     last_word_rects: dict[str, pygame.rect], input_font: pygame.font, scores: list):
    """

    :param turn_text:
    :param input_rects:
    :param last_word_rects:
    :param input_font:
    """
    sp_font = pygame.font.SysFont(font, 40)
    issue_font = pygame.font.SysFont(font, 30)

    # TEXT INPUT GROUP
    render_text(turn_text["enter_word_cap"], input_rects["caption"], input_font)
    render_text(turn_text["input_text"], input_rects["text_box"], input_font, True)
    render_text(turn_text["issue"], input_rects["issue"], issue_font)

    # LAST WORD GROUP
    render_text(turn_text["last_word_cap"], last_word_rects["caption"], input_font)
    render_text(turn_text["last_word"], last_word_rects["last_word"], sp_font)

    # SCORES
    p1_rec = pygame.Rect(200, 2 * height / 3, 240, 50)
    p2_rec = pygame.Rect((width - 200) - 12 * 15, 2 * height / 3, 240, 50)
    render_text(f'P1 score: {str(scores[0])}', p1_rec, input_font)
    render_text(f'P2 score: {str(scores[1])}', p2_rec, input_font)


def setup_window():
    """set up"""
    base_font = pygame.font.SysFont(font, 32)
    user_text = ''

    curr_game_setup = {"players": 0, "bot_first": 0, "time_limit": 60}
    questions = ["How many players are playing? [1 or 2]",
                 "Enter 1 for bot to play first, 2 if you want to play first.",
                 "How many seconds do you wish to take? (5-60 seconds)"]
    q_id = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                elif event.key == pygame.K_RETURN:
                    if q_id == 0 and user_text in ["1", "2"]:
                        curr_game_setup["players"] = int(user_text)
                        if user_text == "2":
                            user_text = ''
                            q_id = 2
                        elif user_text == "1":
                            user_text = ''
                            q_id += 1
                    elif q_id == 1 and user_text in ["1", "2"]:
                        curr_game_setup["bot_first"] = int(user_text)
                        user_text = ''
                        q_id += 1
                    elif q_id == 2 and user_text.isnumeric() and 5 <= int(user_text) <= 60:
                        curr_game_setup["time_limit"] = int(user_text)
                        return curr_game_setup
                else:
                    user_text += event.unicode

        # window.fill(bg_color)
        window.blit(p_ent.bg.image, p_ent.bg.rect)
        window.blit(overlay, (0, 0))
        clock.tick(60)

        text_rect = pygame.Rect(width / 2 - 6 * len(questions[q_id]), height / 3, 240, 50)
        input_rect = pygame.Rect(width / 2 - 145, height / 3 + 75, 240, 50)

        render_text(questions[q_id], text_rect, base_font)
        render_text(user_text, input_rect, base_font, True)
        pygame.display.update()


def trigger_win(winner: int, scores) -> bool:
    """

    :param winner:
    :param scores:
    """
    # TODO: TEMP

    # WIN/LOSE
    win_font = pygame.font.SysFont(font, 100)
    lose_font = pygame.font.SysFont(font, 50)
    win_rec = pygame.Rect(width / 2 - 350, height / 3, 240, 100)
    lose_rec = pygame.Rect(width / 2 - 350, height / 3 + 100, 240, 75)

    # RETRY TEXTBOX
    text_rect = pygame.Rect(width / 2 - 250, 2 * height / 3, 240, 50)
    input_rect = pygame.Rect(width / 2 - 105, 2 * height / 3, 240, 50)
    try_again = pygame.font.SysFont(font, 32)
    user_inp = ''

    if winner == 0:
        print("Player 2 wins")
        win_st = f"Player 2 wins with {scores[1]}!"
        lose_st = f"Player 1 wins with {scores[0]}!"
    else:
        print("Player 1 wins")
        win_st = f"Player 1 wins with {scores[0]}!"
        lose_st = f"Player 2 wins with {scores[1]}!"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_inp = user_inp[0:-1]
                elif event.key == pygame.K_RETURN:
                    clean_txt = re.sub(r'[^a-zA-Z0-9]', '', user_inp)
                    if clean_txt.lower() in ["tryagain", "yes", "y"]:
                        return True
                    else:
                        return False
                else:
                    user_inp += event.unicode

        # window.fill(bg_color)
        window.blit(p_ent.bg.image, p_ent.bg.rect)
        clock.tick(60)

        render_text(win_st, win_rec, win_font)
        render_text(lose_st, lose_rec, lose_font)

        render_text("Try again?", text_rect, try_again)
        render_text(user_inp, input_rect, try_again, True)

        pygame.display.update()


def main_game_window(game_obj: g_ent.WordChain, time_limit: int):
    """main game"""
    time_left = time_limit

    # USER INPUT
    base_font = pygame.font.SysFont(font, 32)
    word = ''

    # text rects
    last_word_rects = {
        "caption": pygame.Rect(width / 2 - 220, height / 5, 240, 50),
        "last_word": pygame.Rect(width / 2 - 220, height / 5 + 50, 240, 50)
    }
    input_rects = {
        "caption": pygame.Rect(width / 2 - 220, height / 3, 240, 50),
        "text_box": pygame.Rect(width / 3, height / 3 + 50, 240, 50),
        "issue": pygame.Rect(width / 3, height / 3 + 100, 240, 50)
    }
    time_rect = pygame.Rect(width / 2 - 150, 2 * height / 3, 240, 50)

    # game text
    current = ["P2 turn", "P1 turn"]
    last_word = '...'
    issue = ''
    last_letter = random.choice('nesgjwdombiuhpycltarqkfv'.lower())

    running = True
    rounds = 1
    og_game_state = deepcopy(game_obj)
    while running:
        # curr player
        pygame.display.update()

        if rounds % 2 != 0:
            curr_player = game_obj.player1
        else:
            curr_player = game_obj.player2

        # IF BOT'S TURN
        if isinstance(curr_player, g_ent.Bot):
            tmp = wc.get_bot_input(last_letter, curr_player.word_bank, game_obj.words_used)
            print("Bot is thinking...")
            pygame.event.set_blocked([pygame.KEYDOWN])
            time.sleep(1.5)
            pygame.event.set_allowed([pygame.KEYDOWN])

            if tmp is None:  # todo
                running = trigger_win((rounds + 1) % 2, [game_obj.player1.score, game_obj.player2.score])
                issue, time_left, last_word = '', time_limit, '...'
                last_letter = random.choice('nesgjwdombiuhpycltarqkfv'.lower())
                game_obj = og_game_state
            else:
                word = tmp
                wc.update_game_data(curr_player, game_obj, word)
                print(f"{current[rounds % 2]}: {curr_player.score}")
                last_word, last_letter, word, issue = word, word[len(word) - 1], '', ''
                rounds += 1
                time_left = time_limit + 1

        # IF USER TURN
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    word = word[0:-1]
                elif event.key == pygame.K_RETURN:
                    if word in game_obj.word_dictionary and word not in game_obj.words_used and word[0] == last_letter:
                        wc.update_game_data(curr_player, game_obj, word)
                        print(f"{current[rounds % 2]}: {curr_player.score}")
                        last_word, last_letter, word, issue = word, word[len(word) - 1], '', ''
                        rounds += 1
                        time_left = time_limit + 1
                    elif word not in game_obj.word_dictionary:
                        issue = "That is not a word!"
                    elif word in game_obj.words_used:
                        issue = "A player sent that word!"
                    elif word[0] != last_letter:
                        issue = f"Word doesn't start with the letter {last_letter}"
                else:
                    word += event.unicode

            if event.type == pygame.USEREVENT:
                time_left -= 1

            if time_left <= 0:
                running = trigger_win((rounds + 1) % 2, [game_obj.player1.score, game_obj.player2.score])
                issue, time_left, last_word = '', time_limit, '...'
                last_letter = random.choice('nesgjwdombiuhpycltarqkfv'.lower())
                game_obj = og_game_state

        # window.fill(bg_color)
        window.blit(p_ent.bg.image, p_ent.bg.rect)
        window.blit(overlay, (0, 0))
        clock.tick(60)

        if ((rounds % 2 == 0 and isinstance(game_obj.player2, wc.Bot))
                or rounds % 2 == 1 and isinstance(game_obj.player1, wc.Bot)):
            enter_word_cap = f"{current[rounds % 2]}: Bot is thinking..."
        else:
            enter_word_cap = f"{current[rounds % 2]}: Enter a word starting with the letter {last_letter}"

        texts = {
            "input_text": word,
            "last_word": last_word,
            "last_word_cap": "The most recent word:",
            "enter_word_cap": enter_word_cap,
            "issue": issue
        }
        render_main_text(texts, input_rects, last_word_rects, base_font,
                         [game_obj.player1.score, game_obj.player2.score])

        render_text(f"Seconds left: {time_left}", time_rect, base_font)

        # pygame.display.update()


if __name__ == "__main__":
    game_setup = setup_window()
    game = wc.setup_game(game_setup)

    print(f"P1: {type(game.player1)}")
    print(f"P2: {type(game.player2)}")

    main_game_window(game, game_setup["time_limit"])

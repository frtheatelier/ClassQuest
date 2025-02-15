"""Attempt at a pygame window view
tutorial based on g4g :")
+ https://youtu.be/Rvcyf4HsWiw?si=WK7eG4Km0GI3Qrc7 for text input
"""
import random
import time

import pygame

import pygame_entities as p_ent
import game_entities as g_ent
import word_chain as wc

pygame.init()
assert pygame.get_init()

pygame.key.set_repeat(500, 100)

# display set up
width = p_ent.WIDTH
height = p_ent.HEIGHT
window = p_ent.WINDOW
pygame.display.set_caption("Word chain!")
pygame.display.update()

# other
clock = pygame.time.Clock()
bg_color = (238, 238, 228)


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
        pygame.draw.rect(window, bg_color, input_rectangle, 0)

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


# RENDERING SCORE POSITION
# def render_score(p1_rec: pygame.Rect, input_font: pygame.font, score: list):
#     pygame.draw.rect(window, bg_color, p1_rec, 0)
#     text_surface = input_font.render(score, False, "black")
#     # w = text_surface.get_width()
#     window.blit(text_surface, (p1_rec.x + 12, p1_rec.y + 12.5))
#     p1_rec.w = max(text_surface.get_width() + 12, 200) + 12


# RENDERING MAIN WINDOW
def render_main_text(turn_text: dict[str, str], input_rects: dict[str, pygame.rect],
                     last_word_rects: dict[str, pygame.rect], input_font: pygame.font, scores: list):
    """

    :param turn_text:
    :param input_rects:
    :param last_word_rects:
    :param input_font:
    """
    # TEXT INPUT GROUP
    render_text(turn_text["enter_word_cap"], input_rects["caption"], input_font)
    render_text(turn_text["input_text"], input_rects["text_box"], input_font, True)

    # LAST WORD GROUP
    render_text(turn_text["last_word_cap"], last_word_rects["caption"], input_font)
    render_text(turn_text["last_word"], last_word_rects["last_word"], input_font)

    # SCORES
    p1_rec = pygame.Rect(200, 2*height / 3, 240, 50)
    p2_rec = pygame.Rect((width - 200) - 12*15, 2*height / 3, 240, 50)
    render_text(f'P1 score: {str(scores[0])}', p1_rec, input_font)
    render_text(f'P2 score: {str(scores[1])}', p2_rec, input_font)


def setup_window():
    """set up"""
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    text_rect = pygame.Rect(width / 2 - 220, height / 3 - 25, 240, 50)
    input_rect = pygame.Rect(width / 2 - 105, height / 3 + 50, 240, 50)

    curr_game_setup = {"players": 0, "bot_first": 0}
    questions = ["How many players are playing? [1 or 2]",
                 "Enter 1 for bot to play first, 2 if you want to play first"]
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
                        if user_text == 2:
                            return curr_game_setup
                        else:
                            user_text = ''
                            q_id += 1
                    elif q_id == 1 and user_text in ["1", "2"]:
                        curr_game_setup["bot_first"] = int(user_text)
                        return curr_game_setup
                else:
                    user_text += event.unicode

        window.fill(bg_color)
        clock.tick(60)

        render_text(questions[q_id], text_rect, base_font)
        render_text(user_text, input_rect, base_font, True)
        pygame.display.update()


def trigger_win(winner: int, scores):
    """

    :param winner:
    :param scores:
    """
    # TODO: TEMP

    win_font = pygame.font.Font(None, 32)
    lose_font = pygame.font.Font(None, 24)

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

        window.fill(bg_color)
        clock.tick(60)

        win_rec = pygame.Rect(width/2, height/2, 240, 50)
        lose_rec = pygame.Rect(width/2, height/2+20, 240, 32)
        render_text(win_st, win_rec, win_font)
        render_text(win_st, win_rec, lose_font)

        pygame.display.update()


def main_game_window(game_obj: g_ent.WordChain):
    """main game"""
    # USER INPUT
    base_font = pygame.font.Font(None, 32)
    word = ''

    # text rects
    last_word_rects = {
        "caption": pygame.Rect(width / 2 - 220, height / 5, 240, 50),
        "last_word": pygame.Rect(width / 2 - 220, height / 5 + 50, 240, 50)
    }
    input_rects = {
        "caption": pygame.Rect(width / 2 - 220, height / 3, 240, 50),
        "text_box": pygame.Rect(width / 3, height / 3 + 50, 240, 50)
    }

    # game text
    current = ["P2 turn", "P1 turn"]
    last_word = '...'
    last_letter = random.choice('nesgjwdombiuhpycltarqkfv'.lower())

    running = True
    rounds = 1
    while running:
        # curr player
        if rounds % 2 != 0:
            curr_player = game_obj.player1
        else:
            curr_player = game_obj.player2

        # IF BOT'S TURN
        if isinstance(curr_player, g_ent.Bot):
            tmp = wc.get_bot_input(last_letter, curr_player.word_bank, game_obj.words_used)
            print("Bot is thinking...")
            pygame.event.set_blocked([pygame.KEYDOWN])
            for _ in range(3):
                pygame.display.update()
                time.sleep(0.8)
            pygame.event.set_allowed([pygame.KEYDOWN])

            if tmp is None:  # todo
                trigger_win((rounds+1) % 2, [game_obj.player1.score, game_obj.player2.score])
            else:
                word = tmp
                wc.update_game_data(curr_player, game_obj, word)
                print(f"{current[rounds % 2]}: {curr_player.score}")
                last_word, last_letter, word = word, word[len(word) - 1], ''
                rounds += 1

        # IF USER TURN
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    word = word[0:-1]
                elif event.key == pygame.K_RETURN:
                    # todo
                    if word in game_obj.word_dictionary and word not in game_obj.words_used and word[0] == last_letter:
                        wc.update_game_data(curr_player, game_obj, word)
                        print(f"{current[rounds % 2]}: {curr_player.score}")
                        last_word, last_letter, word = word, word[len(word) - 1], ''
                        rounds += 1
                else:
                    word += event.unicode

        window.fill(bg_color)
        clock.tick(60)

        if ((rounds % 2 == 0 and isinstance(game_obj.player2, wc.Bot))
                or rounds % 2 == 1 and isinstance(game_obj.player1, wc.Bot)):
            enter_word_cap = f"{current[rounds % 2]}: Bot is thinking..."
        else:
            enter_word_cap = f"{current[rounds % 2]}: Enter a word starting with the letter {last_letter}"

        # todo add render func
        texts = {
            "input_text": word,
            "last_word": last_word,
            "last_word_cap": "The most recent word:",
            "enter_word_cap": enter_word_cap
        }
        render_main_text(texts, input_rects, last_word_rects, base_font,
                         [game_obj.player1.score, game_obj.player2.score])

        pygame.display.update()


if __name__ == "__main__":
    game_setup = setup_window()
    game = wc.setup_game(game_setup)

    print(f"P1: {type(game.player1)}")
    print(f"P2: {type(game.player2)}")

    main_game_window(game)

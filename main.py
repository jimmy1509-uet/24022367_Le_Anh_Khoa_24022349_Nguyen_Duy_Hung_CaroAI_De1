import sys
import pygame
from constants import *
from game import Game, check_win, is_full
import ai
import renderer


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Caro — Minimax AI")
    clock = pygame.time.Clock()

    fn_big = pygame.font.Font(None, 15)
    fn_med = pygame.font.Font(None, 13)
    fn_sm = pygame.font.Font(None, 11)
    fn_mono = pygame.font.Font(None, 11)
    fonts = (fn_big, fn_med, fn_sm, fn_mono)

    game = Game()
    ai_pending = False
    slider_x = MARGIN + BOARD_W + MARGIN + 14
    slider_w = PANEL_W - 28
    slider_y, slider_y2 = renderer.get_slider_y(fonts)
    dragging_slider = False
    dragging_slider_algo = False

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    ai_pending = False
                if event.key == pygame.K_u:
                    game.undo_last_moves()
                    ai_pending = False
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    game.depth = int(event.unicode)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Depth slider
                fill_w = int(slider_w * (game.depth - 1) / 3)
                tx = slider_x + fill_w
                ty = slider_y + 8
                if abs(mx - tx) <= 14 and abs(my - ty) <= 14:
                    dragging_slider = True
                # Algorithm slider
                fill_w2 = int(slider_w * game.algorithm / 2)
                tx2 = slider_x + fill_w2
                ty2 = slider_y2 + 8
                if abs(mx - tx2) <= 14 and abs(my - ty2) <= 14:
                    dragging_slider_algo = True

            if event.type == pygame.MOUSEBUTTONUP:
                dragging_slider = False
                mx, my = event.pos

                if not game.game_over and game.player_turn and not ai_pending:
                    bx = mx - MARGIN
                    by = my - MARGIN
                    if 0 <= bx < BOARD_W and 0 <= by < BOARD_H:
                        c = bx // CELL
                        r = by // CELL
                        if 0 <= r < ROWS and 0 <= c < COLS and game.grid[r][c] == EMPTY:
                            game.grid[r][c] = HUMAN
                            game.history.append((r, c, HUMAN))
                            game.move_log.append(("Người", r, c, None, None, None, None))
                            wc = check_win(game.grid, HUMAN)
                            if wc:
                                game.win_cells = wc
                                game.game_over = True
                                game.status_msg = "Bạn thắng!  Nhấn 'Ván mới' để chơi lại."
                            elif is_full(game.grid):
                                game.game_over = True
                                game.status_msg = "Hòa!  Bàn cờ đầy."
                            else:
                                game.player_turn = False
                                game.thinking = True
                                game.status_msg = "AI đang suy nghĩ..."
                                ai_pending = True

                if hasattr(game, '_btn_new') and game._btn_new.collidepoint(mx, my):
                    game.reset()
                    ai_pending = False
                if hasattr(game, '_btn_undo') and game._btn_undo.collidepoint(mx, my):
                    game.undo_last_moves()
                    ai_pending = False
                # Nút "Thoát"
                if hasattr(game, '_btn_exit') and game._btn_exit.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

                if slider_x <= mx <= slider_x + slider_w and abs(my - (slider_y + 8)) <= 14:
                    raw = (mx - slider_x) / slider_w
                    game.depth = max(1, min(4, round(raw * 3) + 1))
                # Click on algorithm slider track
                if slider_x <= mx <= slider_x + slider_w and abs(my - (slider_y2 + 8)) <= 14:
                    raw = (mx - slider_x) / slider_w
                    game.algorithm = max(0, min(2, round(raw * 2)))

            if event.type == pygame.MOUSEMOTION and dragging_slider:
                mx, _ = event.pos
                raw = (mx - slider_x) / slider_w
                game.depth = max(1, min(4, round(raw * 3) + 1))
            if event.type == pygame.MOUSEMOTION and dragging_slider_algo:
                mx, _ = event.pos
                raw = (mx - slider_x) / slider_w
                game.algorithm = max(0, min(2, round(raw * 2)))

        if ai_pending:
            renderer.draw_board(screen, game, fonts)
            pygame.display.flip()
            pygame.time.delay(60)
            ai.do_ai_move(game)
            game.thinking = False
            ai_pending = False

        renderer.draw_board(screen, game, fonts)
        pygame.display.flip()


if __name__ == "__main__":
    main()

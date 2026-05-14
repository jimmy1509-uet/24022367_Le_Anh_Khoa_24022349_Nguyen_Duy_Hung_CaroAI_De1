import sys
import pygame
from constants import *
from game import Game, check_win, is_full
from src.ai.game_logic import do_ai_move
from src.ui.board import draw_board
from src.ui.menu import draw_menu, get_slider_y
from src.ui.statistics import draw_statistics


def load_unicode_font(size: int) -> pygame.font.Font:
    """Load a system font that supports Unicode/Vietnamese."""
    for name in ["Segoe UI", "Arial", "Tahoma", "Verdana", "DejaVu Sans"]:
        path = pygame.font.match_font(name)
        if path:
            return pygame.font.Font(path, size)
    return pygame.font.SysFont(None, size)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Caro — Minimax AI")
    clock = pygame.time.Clock()

    fn_big = load_unicode_font(15)
    fn_med = load_unicode_font(13)
    fn_sm = load_unicode_font(11)
    fn_mono = load_unicode_font(11)
    fonts = (fn_big, fn_med, fn_sm, fn_mono)

    game = Game()
    ai_pending = game.mode == "PvAI" and game.ai_first
    dragging_slider = False

    while True:
        clock.tick(60)

        slider_x = MARGIN + BOARD_W + MARGIN + 14
        slider_w = PANEL_W - 28
        slider_y, _ = get_slider_y(fonts)

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

            if event.type == pygame.MOUSEBUTTONUP:
                dragging_slider = False
                mx, my = event.pos

                if not game.game_over and not ai_pending:
                    bx = mx - MARGIN
                    by = my - MARGIN
                    if 0 <= bx < BOARD_W and 0 <= by < BOARD_H:
                        c = bx // CELL
                        r = by // CELL
                        if 0 <= r < ROWS and 0 <= c < COLS and game.grid[r][c] == EMPTY:
                            if game.mode == "PvAI" and not game.player_turn:
                                pass
                            else:
                                piece = HUMAN if game.player_turn else AI
                                player_name = "Người" if game.mode == "PvAI" else ("Người 1" if game.player_turn else "Người 2")
                                game.grid[r][c] = piece
                                game.history.append((r, c, piece))
                                game.move_log.append((player_name, r, c, None, None, None, None))
                                wc = check_win(game.grid, piece)
                                if wc:
                                    game.win_cells = wc
                                    game.game_over = True
                                    game.status_msg = f"{player_name} thắng!  Nhấn 'Ván mới' để chơi lại."
                                elif is_full(game.grid):
                                    game.game_over = True
                                    game.status_msg = "Hòa!  Bàn cờ đầy."
                                else:
                                    if game.mode == "PvAI":
                                        game.player_turn = False
                                        game.thinking = True
                                        game.status_msg = "AI đang suy nghĩ..."
                                        ai_pending = True
                                    else:
                                        game.player_turn = not game.player_turn
                                        next_label = "Người 1" if game.player_turn else "Người 2"
                                        game.status_msg = f"Lượt {next_label} — nhấp vào ô trống"

                if hasattr(game, '_btn_mode_pvp') and game._btn_mode_pvp.collidepoint(mx, my):
                    game.reset(mode="PvP", ai_first=False)
                    ai_pending = False
                if hasattr(game, '_btn_mode_pvai') and game._btn_mode_pvai.collidepoint(mx, my):
                    game.reset(mode="PvAI", ai_first=game.ai_first)
                    ai_pending = game.ai_first
                if hasattr(game, '_btn_first_human') and game._btn_first_human.collidepoint(mx, my):
                    if game.mode == "PvAI":
                        game.reset(mode="PvAI", ai_first=False)
                        ai_pending = False
                if hasattr(game, '_btn_first_ai') and game._btn_first_ai.collidepoint(mx, my):
                    if game.mode == "PvAI":
                        game.reset(mode="PvAI", ai_first=True)
                        ai_pending = True
                if hasattr(game, '_btn_algo_minimax') and game._btn_algo_minimax.collidepoint(mx, my):
                    game.algorithm = 0
                if hasattr(game, '_btn_algo_ab') and game._btn_algo_ab.collidepoint(mx, my):
                    game.algorithm = 1

                if hasattr(game, '_btn_new') and game._btn_new.collidepoint(mx, my):
                    game.reset(mode=game.mode, ai_first=game.ai_first)
                    ai_pending = game.mode == "PvAI" and game.ai_first
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

            if event.type == pygame.MOUSEMOTION and dragging_slider:
                mx, _ = event.pos
                raw = (mx - slider_x) / slider_w
                game.depth = max(1, min(4, round(raw * 3) + 1))

        screen.fill(BG)

        if ai_pending:
            draw_board(screen, game, fonts)
            draw_menu(screen, game, fonts)
            draw_statistics(screen, game, fonts)
            pygame.display.flip()
            pygame.time.delay(60)
            do_ai_move(game)
            game.thinking = False
            ai_pending = False

        screen.fill(BG)

        draw_board(screen, game, fonts)
        draw_menu(screen, game, fonts)
        draw_statistics(screen, game, fonts)
        pygame.display.flip()


if __name__ == "__main__":
    main()
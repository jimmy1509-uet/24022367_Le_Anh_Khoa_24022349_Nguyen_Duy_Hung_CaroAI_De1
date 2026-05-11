import pygame
from constants import *


def draw_board(surface, game, fonts):
    fn_big, fn_med, fn_sm, fn_mono = fonts
    ox, oy = MARGIN, MARGIN

    surface.fill(BG)

    # Nền bàn cờ
    pygame.draw.rect(surface, (250, 248, 240),
                     (ox, oy, BOARD_W, BOARD_H))

    # Lưới
    for r in range(ROWS + 1):
        pygame.draw.line(surface, GRID_COL,
                         (ox, oy + r * CELL), (ox + BOARD_W, oy + r * CELL), 1)
    for c in range(COLS + 1):
        pygame.draw.line(surface, GRID_COL,
                         (ox + c * CELL, oy), (ox + c * CELL, oy + BOARD_H), 1)

    # Nhãn cột (A–N cho 14 cột)
    for c in range(COLS):
        lbl = fn_sm.render(chr(ord('A') + c), True, TEXT_SUB)
        surface.blit(lbl, (ox + c * CELL + CELL // 2 - lbl.get_width() // 2, oy - 22))
    # Nhãn hàng (1–14)
    for r in range(ROWS):
        lbl = fn_sm.render(str(r + 1), True, TEXT_SUB)
        surface.blit(lbl, (ox - 22, oy + r * CELL + CELL // 2 - lbl.get_height() // 2))

    # Tô ô thắng
    win_set = set(game.win_cells)
    for r, c in win_set:
        pygame.draw.rect(surface, WIN_HL,
                         (ox + c * CELL + 2, oy + r * CELL + 2, CELL - 4, CELL - 4))

    # Quân cờ
    for r in range(ROWS):
        for c in range(COLS):
            if game.grid[r][c] == EMPTY:
                continue
            cx = ox + c * CELL + CELL // 2
            cy = oy + r * CELL + CELL // 2
            is_win = (r, c) in win_set
            lw = 3 if is_win else 2

            if game.grid[r][c] == HUMAN:
                pad = int(CELL * 0.27)
                pygame.draw.line(surface, X_COL,
                                 (ox + c * CELL + pad, oy + r * CELL + pad),
                                 (ox + c * CELL + CELL - pad, oy + r * CELL + CELL - pad), lw)
                pygame.draw.line(surface, X_COL,
                                 (ox + c * CELL + CELL - pad, oy + r * CELL + pad),
                                 (ox + c * CELL + pad, oy + r * CELL + CELL - pad), lw)
            else:
                pygame.draw.circle(surface, O_COL, (cx, cy), int(CELL * 0.3), lw)

    # Gạch chân nước AI cuối
    if game.last_move and not win_set:
        r, c = game.last_move
        pygame.draw.rect(surface, (200, 180, 100),
                         (ox + c * CELL + 2, oy + r * CELL + 2, CELL - 4, CELL - 4), 2)
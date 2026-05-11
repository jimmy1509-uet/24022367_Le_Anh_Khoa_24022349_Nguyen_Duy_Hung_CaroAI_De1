import pygame
from constants import *


def draw_statistics(surface, game, fonts):
    fn_big, fn_med, fn_sm, fn_mono = fonts
    # ── THANH TRẠNG THÁI ──
    sy = MARGIN + BOARD_H + 10
    pygame.draw.rect(surface, STATUS_BG,
                     (MARGIN, sy, BOARD_W, 40), border_radius=8)
    # Đèn trạng thái
    dot_col = (226, 75, 74) if game.game_over else \
              (239, 159, 39) if game.thinking else \
              (29, 158, 117)
    pygame.draw.circle(surface, dot_col, (MARGIN + 18, sy + 20), 6)
    st = fn_med.render(game.status_msg, True, TEXT_MAIN)
    surface.blit(st, (MARGIN + 34, sy + 20 - st.get_height() // 2))
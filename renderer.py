import pygame
from constants import *


def get_slider_y(fonts):
    fn_big, fn_med, fn_sm, fn_mono = fonts
    # Depth slider
    depth_y = (MARGIN + 16 + fn_big.get_height() + 6 + 1 + 10 +
               (fn_sm.get_height() + 5) * 5 + 4 + 1 + 10 +
               fn_sm.get_height() + 6 + 8)
    # Algorithm slider below depth
    algo_y = depth_y + 28 + fn_sm.get_height() + 12 + 10 + fn_sm.get_height() + 6 + 8
    return depth_y, algo_y


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

    # ── PANEL PHẢI ────────────────────────────────
    px = MARGIN + BOARD_W + MARGIN
    py = MARGIN

    pygame.draw.rect(surface, PANEL_BG,
                     (px, py, PANEL_W, BOARD_H), border_radius=10)
    pygame.draw.rect(surface, PANEL_BORD,
                     (px, py, PANEL_W, BOARD_H), 1, border_radius=10)

    cy_panel = py + 16

    # Tiêu đề
    title = fn_big.render("Caro — Minimax AI", True, TEXT_MAIN)
    surface.blit(title, (px + (PANEL_W - title.get_width()) // 2, cy_panel))
    cy_panel += title.get_height() + 6

    pygame.draw.line(surface, PANEL_BORD, (px + 12, cy_panel), (px + PANEL_W - 12, cy_panel), 1)
    cy_panel += 10

    # Nước đi cuối + điểm đánh giá
    def info_row(label, value, val_color=TEXT_MAIN):
        lbl = fn_sm.render(label, True, TEXT_SUB)
        val = fn_mono.render(str(value), True, val_color)
        surface.blit(lbl, (px + 14, cy_panel))
        surface.blit(val, (px + PANEL_W - val.get_width() - 14, cy_panel))
        return lbl.get_height() + 5

    mv_str = f"{chr(ord('A') + game.last_move[1])}{game.last_move[0] + 1}" if game.last_move else "—"
    cy_panel += info_row("Nước đi (Máy):", mv_str, O_COL)
    sc_str = str(game.last_score) if game.last_score is not None else "—"
    cy_panel += info_row("Đánh giá:", sc_str)
    cy_panel += info_row("Độ sâu:", str(game.depth))
    st_str = f"{game.last_states:,}" if game.last_states else "0"
    cy_panel += info_row("Trạng thái xét:", st_str)
    t_str = f"{int(game.last_time)} ms" if game.last_time else "0 ms"
    cy_panel += info_row("Thời gian:", t_str)

    cy_panel += 4
    pygame.draw.line(surface, PANEL_BORD, (px + 12, cy_panel), (px + PANEL_W - 12, cy_panel), 1)
    cy_panel += 10

    # ── Thanh độ sâu ──
    lbl = fn_sm.render(f"Độ sâu tìm kiếm: {game.depth}", True, TEXT_SUB)
    surface.blit(lbl, (px + 14, cy_panel))
    cy_panel += lbl.get_height() + 6

    bar_x, bar_y = px + 14, cy_panel
    bar_w = PANEL_W - 28
    # Track
    pygame.draw.rect(surface, PANEL_BORD, (bar_x, bar_y + 6, bar_w, 4), border_radius=2)
    # Fill
    fill_w = int(bar_w * (game.depth - 1) / 3)
    pygame.draw.rect(surface, GREEN, (bar_x, bar_y + 6, fill_w, 4), border_radius=2)
    # Thumb
    tx = bar_x + fill_w
    pygame.draw.circle(surface, GREEN, (tx, bar_y + 8), 8)
    pygame.draw.circle(surface, (255, 255, 255), (tx, bar_y + 8), 5)
    cy_panel += 28

    # Nhãn 1–4
    for i in range(4):
        xp = bar_x + int(bar_w * i / 3)
        n = fn_sm.render(str(i + 1), True, TEXT_SUB)
        surface.blit(n, (xp - n.get_width() // 2, cy_panel))
    cy_panel += fn_sm.get_height() + 12

    pygame.draw.line(surface, PANEL_BORD, (px + 12, cy_panel), (px + PANEL_W - 12, cy_panel), 1)
    cy_panel += 10

    # ── Thanh thuật toán ──
    lbl = fn_sm.render(f"Thuật toán: {game.algorithm}", True, TEXT_SUB)
    surface.blit(lbl, (px + 14, cy_panel))
    cy_panel += lbl.get_height() + 6

    bar_x2, bar_y2 = px + 14, cy_panel
    bar_w2 = PANEL_W - 28
    pygame.draw.rect(surface, PANEL_BORD, (bar_x2, bar_y2 + 6, bar_w2, 4), border_radius=2)
    fill_w2 = int(bar_w2 * game.algorithm / 2)
    pygame.draw.rect(surface, GREEN, (bar_x2, bar_y2 + 6, fill_w2, 4), border_radius=2)
    tx2 = bar_x2 + fill_w2
    pygame.draw.circle(surface, GREEN, (tx2, bar_y2 + 8), 8)
    pygame.draw.circle(surface, (255, 255, 255), (tx2, bar_y2 + 8), 5)
    cy_panel += 28

    # Nhãn 0–2
    for i in range(3):
        xp = bar_x2 + int(bar_w2 * i / 2)
        labels = ["Minimax", "Alpha-Beta", "So sánh"]
        n = fn_sm.render(labels[i], True, TEXT_SUB)
        surface.blit(n, (xp - n.get_width() // 2, cy_panel))
    cy_panel += fn_sm.get_height() + 12

    pygame.draw.line(surface, PANEL_BORD, (px + 12, cy_panel), (px + PANEL_W - 12, cy_panel), 1)
    cy_panel += 10

    # ── Nút ──
    btn_w, btn_h = PANEL_W - 28, 34
    # Nút "Ván mới"
    new_rect = pygame.Rect(px + 14, cy_panel, btn_w, btn_h)
    game._btn_new = new_rect
    pygame.draw.rect(surface, BTN_BG, new_rect, border_radius=7)
    pygame.draw.rect(surface, GREEN, new_rect, 1, border_radius=7)
    t = fn_med.render("⟳  Ván mới", True, GREEN)
    surface.blit(t, (new_rect.centerx - t.get_width() // 2,
                     new_rect.centery - t.get_height() // 2))
    cy_panel += btn_h + 8

    # Nút "Đi lại"
    undo_rect = pygame.Rect(px + 14, cy_panel, btn_w, btn_h)
    game._btn_undo = undo_rect
    pygame.draw.rect(surface, BTN_BG, undo_rect, border_radius=7)
    pygame.draw.rect(surface, PANEL_BORD, undo_rect, 1, border_radius=7)
    t = fn_med.render("←  Đi lại", True, TEXT_MAIN)
    surface.blit(t, (undo_rect.centerx - t.get_width() // 2,
                     undo_rect.centery - t.get_height() // 2))
    cy_panel += btn_h + 8

    # Nút "Thoát"
    exit_rect = pygame.Rect(px + 14, cy_panel, btn_w, btn_h)
    game._btn_exit = exit_rect
    pygame.draw.rect(surface, (200, 50, 50), exit_rect, border_radius=7)  # Màu đỏ
    pygame.draw.rect(surface, PANEL_BORD, exit_rect, 1, border_radius=7)
    t = fn_med.render("Thoát", True, (255, 255, 255))  # Chữ trắng
    surface.blit(t, (exit_rect.centerx - t.get_width() // 2,
                     exit_rect.centery - t.get_height() // 2))
    cy_panel += btn_h + 12

    pygame.draw.line(surface, PANEL_BORD, (px + 12, cy_panel), (px + PANEL_W - 12, cy_panel), 1)
    cy_panel += 8

    # ── Lịch sử nước đi ──
    lbl = fn_sm.render("Lịch sử nước đi", True, TEXT_SUB)
    surface.blit(lbl, (px + 14, cy_panel))
    cy_panel += lbl.get_height() + 4

    log_area_h = (py + BOARD_H) - cy_panel - 10
    clip_rect = pygame.Rect(px + 10, cy_panel, PANEL_W - 20, log_area_h)
    surface.set_clip(clip_rect)
    log_y = cy_panel
    for entry in reversed(game.move_log[-12:]):
        who, mr, mc, sc, dep, sta, ms = entry
        who_col = O_COL if who == "Máy" else X_COL
        t1 = fn_mono.render(f"{who}→{chr(ord('A') + mc)}{mr + 1}", True, who_col)
        surface.blit(t1, (px + 12, log_y))
        if sc is not None:
            t2 = fn_mono.render(f"val:{sc} d:{dep} n:{sta} {ms}ms", True, TEXT_SUB)
            surface.blit(t2, (px + 12, log_y + t1.get_height()))
            log_y += t1.get_height() + t2.get_height() + 3
        else:
            log_y += t1.get_height() + 4
    surface.set_clip(None)

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

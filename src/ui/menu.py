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


def draw_menu(surface, game, fonts):
    fn_big, fn_med, fn_sm, fn_mono = fonts
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

    # Chọn chế độ chơi
    lbl = fn_sm.render("Chế độ chơi:", True, TEXT_SUB)
    surface.blit(lbl, (px + 14, cy_panel))
    cy_panel += lbl.get_height() + 6

    mode_btn_w = (PANEL_W - 42) // 2
    mode_btn_h = 28
    pvp_rect = pygame.Rect(px + 14, cy_panel, mode_btn_w, mode_btn_h)
    pvai_rect = pygame.Rect(px + 28 + mode_btn_w, cy_panel, mode_btn_w, mode_btn_h)
    game._btn_mode_pvp = pvp_rect
    game._btn_mode_pvai = pvai_rect

    active_color = GREEN
    pygame.draw.rect(surface, active_color if game.mode == "PvP" else BTN_BG, pvp_rect, border_radius=7)
    pygame.draw.rect(surface, PANEL_BORD, pvp_rect, 1, border_radius=7)
    t = fn_sm.render("Người vs Người", True, (255, 255, 255) if game.mode == "PvP" else TEXT_MAIN)
    surface.blit(t, (pvp_rect.centerx - t.get_width() // 2,
                     pvp_rect.centery - t.get_height() // 2))

    pygame.draw.rect(surface, active_color if game.mode == "PvAI" else BTN_BG, pvai_rect, border_radius=7)
    pygame.draw.rect(surface, PANEL_BORD, pvai_rect, 1, border_radius=7)
    t = fn_sm.render("Người vs AI", True, (255, 255, 255) if game.mode == "PvAI" else TEXT_MAIN)
    surface.blit(t, (pvai_rect.centerx - t.get_width() // 2,
                     pvai_rect.centery - t.get_height() // 2))
    cy_panel += mode_btn_h + 10

    if game.mode == "PvAI":
        lbl = fn_sm.render("Ai đi trước:", True, TEXT_SUB)
        surface.blit(lbl, (px + 14, cy_panel))
        cy_panel += lbl.get_height() + 6

        first_btn_w = (PANEL_W - 42) // 2
        first_btn_h = 28
        human_first_rect = pygame.Rect(px + 14, cy_panel, first_btn_w, first_btn_h)
        ai_first_rect = pygame.Rect(px + 28 + first_btn_w, cy_panel, first_btn_w, first_btn_h)
        game._btn_first_human = human_first_rect
        game._btn_first_ai = ai_first_rect

        pygame.draw.rect(surface, active_color if not game.ai_first else BTN_BG, human_first_rect, border_radius=7)
        pygame.draw.rect(surface, PANEL_BORD, human_first_rect, 1, border_radius=7)
        t = fn_sm.render("Người", True, (255, 255, 255) if not game.ai_first else TEXT_MAIN)
        surface.blit(t, (human_first_rect.centerx - t.get_width() // 2,
                         human_first_rect.centery - t.get_height() // 2))

        pygame.draw.rect(surface, active_color if game.ai_first else BTN_BG, ai_first_rect, border_radius=7)
        pygame.draw.rect(surface, PANEL_BORD, ai_first_rect, 1, border_radius=7)
        t = fn_sm.render("AI", True, (255, 255, 255) if game.ai_first else TEXT_MAIN)
        surface.blit(t, (ai_first_rect.centerx - t.get_width() // 2,
                         ai_first_rect.centery - t.get_height() // 2))
        cy_panel += first_btn_h + 10

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
    fill_w = int(bar_w * (game.depth - 1) / 5)
    pygame.draw.rect(surface, GREEN, (bar_x, bar_y + 6, fill_w, 4), border_radius=2)
    # Thumb
    tx = bar_x + fill_w
    pygame.draw.circle(surface, GREEN, (tx, bar_y + 8), 8)
    pygame.draw.circle(surface, (255, 255, 255), (tx, bar_y + 8), 5)
    cy_panel += 28

    # Nhãn 1–6
    for i in range(6):
        xp = bar_x + int(bar_w * i / 5)
        n = fn_sm.render(str(i + 1), True, TEXT_SUB)
        surface.blit(n, (xp - n.get_width() // 2, cy_panel))
    cy_panel += fn_sm.get_height() + 12

    pygame.draw.line(surface, PANEL_BORD, (px + 12, cy_panel), (px + PANEL_W - 12, cy_panel), 1)
    cy_panel += 10

    # ── Chọn thuật toán ──
    lbl = fn_sm.render("Thuật toán:", True, TEXT_SUB)
    surface.blit(lbl, (px + 14, cy_panel))
    cy_panel += lbl.get_height() + 6

    algo_btn_w = (PANEL_W - 42) // 2
    algo_btn_h = 30
    algo_min_rect = pygame.Rect(px + 14, cy_panel, algo_btn_w, algo_btn_h)
    algo_ab_rect = pygame.Rect(px + 28 + algo_btn_w, cy_panel, algo_btn_w, algo_btn_h)
    game._btn_algo_minimax = algo_min_rect
    game._btn_algo_ab = algo_ab_rect

    pygame.draw.rect(surface, GREEN if game.algorithm == 0 else BTN_BG, algo_min_rect, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORD, algo_min_rect, 1, border_radius=8)
    t = fn_sm.render("Minimax", True, (255, 255, 255) if game.algorithm == 0 else TEXT_MAIN)
    surface.blit(t, (algo_min_rect.centerx - t.get_width() // 2,
                     algo_min_rect.centery - t.get_height() // 2))

    pygame.draw.rect(surface, GREEN if game.algorithm == 1 else BTN_BG, algo_ab_rect, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORD, algo_ab_rect, 1, border_radius=8)
    t = fn_sm.render("Alpha-Beta", True, (255, 255, 255) if game.algorithm == 1 else TEXT_MAIN)
    surface.blit(t, (algo_ab_rect.centerx - t.get_width() // 2,
                     algo_ab_rect.centery - t.get_height() // 2))
    cy_panel += algo_btn_h + 12

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
    pygame.draw.rect(surface, (200, 50, 50), exit_rect, border_radius=7)
    pygame.draw.rect(surface, PANEL_BORD, exit_rect, 1, border_radius=7)
    t = fn_med.render("Thoát", True, (255, 255, 255))
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
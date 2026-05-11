import math
import time
from constants import *
from game import check_win, is_full
from .evaluate import evaluate

states_visited = [0]

def get_candidates(grid):
    cands = set()
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == EMPTY:
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
                        cands.add((nr, nc))
    if not cands:
        mid = ROWS // 2
        cands.add((mid, mid))
    return list(cands)


def find_immediate_win(grid, player):
    """
    Tìm nước đi thắng ngay lập tức cho player.
    """
    for r, c in get_candidates(grid):
        grid[r][c] = player
        if check_win(grid, player):
            grid[r][c] = EMPTY
            return r, c
        grid[r][c] = EMPTY
    return None


def do_ai_move(game):
    # Clear transposition tables mỗi nước đi mới để tránh memory leak
    from .alphabeta import transposition_table
    from .minimax import minimax_tt
    transposition_table.clear()
    minimax_tt.clear()

    states_visited[0] = 0

    # Nước đi thắng hoặc chặn nếu có
    win_move = find_immediate_win(game.grid, AI)
    if win_move:
        r, c = win_move
        game.grid[r][c] = AI
        game.history.append((r, c, AI))
        game.last_move = (r, c)
        game.last_score = 0
        game.last_states = states_visited[0]
        game.last_time = 0
        game.move_log.append(("Máy", r, c, 0, game.depth, states_visited[0], 0))
        game.win_cells = check_win(game.grid, AI)
        game.game_over = True
        game.status_msg = "Máy thắng!  Nhấn 'Ván mới' để chơi lại."
        return

    block_move = find_immediate_win(game.grid, HUMAN)
    if block_move:
        r, c = block_move
        game.grid[r][c] = AI
        game.history.append((r, c, AI))
        game.last_move = (r, c)
        game.last_score = 0
        game.last_states = states_visited[0]
        game.last_time = 0
        game.move_log.append(("Máy", r, c, 0, game.depth, states_visited[0], 0))
        if check_win(game.grid, AI):
            game.win_cells = check_win(game.grid, AI)
            game.game_over = True
            game.status_msg = "Máy thắng!  Nhấn 'Ván mới' để chơi lại."
            return
        if is_full(game.grid):
            game.game_over = True
            game.status_msg = "Hòa!  Bàn cờ đầy."
            return
        game.player_turn = True
        game.status_msg = "Lượt của bạn — nhấp vào ô trống"
        return

    t0 = time.time()

    # Iterative deepening: tăng dần độ sâu từ 1 đến game.depth
    best_move = None
    best_score = None
    best_states = 0
    best_time = 0
    for depth in range(1, game.depth + 1):
        if game.algorithm == 0:  # Minimax
            from .minimax import minimax
            score, move = minimax(game.grid, depth, True)
        elif game.algorithm == 1:  # Alpha-Beta
            from .alphabeta import alpha_beta
            score, move = alpha_beta(game.grid, depth, True, -math.inf, math.inf)
        elif game.algorithm == 2:  # Compare
            # Chạy cả hai và ghi log
            from .minimax import minimax
            from .alphabeta import alpha_beta
            states_visited[0] = 0
            score_minimax, move_minimax = minimax(game.grid, depth, True)
            states_minimax = states_visited[0]
            time_minimax = (time.time() - t0) * 1000

            states_visited[0] = 0
            t1 = time.time()
            score_ab, move_ab = alpha_beta(game.grid, depth, True, -math.inf, math.inf)
            states_ab = states_visited[0]
            time_ab = (time.time() - t1) * 1000

            # Sử dụng kết quả alpha-beta
            score, move = score_ab, move_ab

            # Ghi log cả hai
            game.move_log.append(("Minimax", move_minimax[0] if move_minimax else None, move_minimax[1] if move_minimax else None, score_minimax, depth, states_minimax, int(time_minimax)))
            game.move_log.append(("Alpha-Beta", move_ab[0] if move_ab else None, move_ab[1] if move_ab else None, score_ab, depth, states_ab, int(time_ab)))
        else:
            from .alphabeta import alpha_beta
            score, move = alpha_beta(game.grid, depth, True, -math.inf, math.inf)

        # Cập nhật nước đi tốt nhất từ độ sâu hiện tại
        if move:
            best_move = move
            best_score = score
            best_states = states_visited[0]
            best_time = (time.time() - t0) * 1000

    if not best_move:
        return

    r, c = best_move
    game.grid[r][c] = AI
    game.history.append((r, c, AI))

    if game.algorithm != 2:
        game.last_move = (r, c)
        game.last_score = best_score
        game.last_states = best_states
        game.last_time = best_time
        game.move_log.append(("Máy", r, c, best_score, game.depth, best_states, int(best_time)))

    wc = check_win(game.grid, AI)
    if wc:
        game.win_cells = wc
        game.game_over = True
        game.status_msg = "Máy thắng!  Nhấn 'Ván mới' để chơi lại."
        return

    if is_full(game.grid):
        game.game_over = True
        game.status_msg = "Hòa!  Bàn cờ đầy."
        return

    # Tiếp tục trò chơi - quay lại lượt người chơi
    game.player_turn = True
    game.status_msg = "Lượt của bạn — nhấp vào ô trống"
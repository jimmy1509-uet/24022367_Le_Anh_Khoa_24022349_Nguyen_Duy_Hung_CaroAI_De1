import math
import time
from constants import *
from game import check_win, is_full

states_visited = 0


def eval_line(count, open_ends, player):
    if count >= WIN:
        return 100_000 if player == AI else -100_000
    if count == WIN - 1:
        if open_ends == 2:
            return 5_000 if player == AI else -5_000
        if open_ends == 1:
            return 1_000 if player == AI else -1_000
    if count == WIN - 2:
        if open_ends == 2:
            return 200 if player == AI else -200
        if open_ends == 1:
            return 50 if player == AI else -50
    if count == WIN - 3 and open_ends == 2:
        return 10 if player == AI else -10
    return 0


def evaluate(grid):
    score = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in dirs:
                for player in (HUMAN, AI):
                    if grid[r][c] != player:
                        continue
                    pr, pc = r - dr, c - dc
                    if 0 <= pr < ROWS and 0 <= pc < COLS and grid[pr][pc] == player:
                        continue
                    cnt, nr, nc = 0, r, c
                    while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == player:
                        cnt += 1
                        nr += dr
                        nc += dc
                    open_ends = 0
                    if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
                        open_ends += 1
                    if 0 <= pr < ROWS and 0 <= pc < COLS and grid[pr][pc] == EMPTY:
                        open_ends += 1
                    score += eval_line(cnt, open_ends, player)
    return score


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


def minimax(grid, depth, is_max):
    """
    Minimax thuần túy, không pruning.
    """
    global states_visited
    states_visited += 1

    if check_win(grid, AI):
        return 100_000 + depth, None
    if check_win(grid, HUMAN):
        return -100_000 - depth, None
    if is_full(grid) or depth == 0:
        return evaluate(grid), None

    cands = get_candidates(grid)
    best_score = -math.inf if is_max else math.inf
    best_move = None

    for r, c in cands:
        grid[r][c] = AI if is_max else HUMAN
        score, _ = minimax(grid, depth - 1, not is_max)
        grid[r][c] = EMPTY

        if is_max:
            if score > best_score:
                best_score, best_move = score, (r, c)
        else:
            if score < best_score:
                best_score, best_move = score, (r, c)

    return best_score, best_move


def alpha_beta(grid, depth, is_max, alpha, beta):
    """
    Alpha-Beta pruning.
    """
    global states_visited
    states_visited += 1

    if check_win(grid, AI):
        return 100_000 + depth, None
    if check_win(grid, HUMAN):
        return -100_000 - depth, None
    if is_full(grid) or depth == 0:
        return evaluate(grid), None

    cands = get_candidates(grid)
    best_score = -math.inf if is_max else math.inf
    best_move = None

    for r, c in cands:
        grid[r][c] = AI if is_max else HUMAN
        score, _ = alpha_beta(grid, depth - 1, not is_max, alpha, beta)
        grid[r][c] = EMPTY

        if is_max:
            if score > best_score:
                best_score, best_move = score, (r, c)
            alpha = max(alpha, best_score)
        else:
            if score < best_score:
                best_score, best_move = score, (r, c)
            beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score, best_move


def do_ai_move(game):
    global states_visited
    states_visited = 0

    t0 = time.time()

    if game.algorithm == 0:  # Minimax
        score, move = minimax(game.grid, game.depth, True)
    elif game.algorithm == 1:  # Alpha-Beta
        score, move = alpha_beta(game.grid, game.depth, True, -math.inf, math.inf)
    elif game.algorithm == 2:  # Compare
        # Run both and log both
        states_visited = 0
        score_minimax, move_minimax = minimax(game.grid, game.depth, True)
        states_minimax = states_visited
        time_minimax = (time.time() - t0) * 1000

        states_visited = 0
        t1 = time.time()
        score_ab, move_ab = alpha_beta(game.grid, game.depth, True, -math.inf, math.inf)
        states_ab = states_visited
        time_ab = (time.time() - t1) * 1000

        # Use alpha-beta result
        score, move = score_ab, move_ab

        # Log both
        game.move_log.append(("Minimax", move_minimax[0] if move_minimax else None, move_minimax[1] if move_minimax else None, score_minimax, game.depth, states_minimax, int(time_minimax)))
        game.move_log.append(("Alpha-Beta", move_ab[0] if move_ab else None, move_ab[1] if move_ab else None, score_ab, game.depth, states_ab, int(time_ab)))
    else:
        score, move = alpha_beta(game.grid, game.depth, True, -math.inf, math.inf)

    elapsed_ms = (time.time() - t0) * 1000

    if move is None:
        return

    r, c = move
    game.grid[r][c] = AI
    game.history.append((r, c, AI))

    if game.algorithm != 2:
        game.last_move = (r, c)
        game.last_score = score
        game.last_states = states_visited
        game.last_time = elapsed_ms
        game.move_log.append(("Máy", r, c, score, game.depth, states_visited, int(elapsed_ms)))

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

    game.player_turn = True
    game.status_msg = "Lượt của bạn — nhấp vào ô trống"

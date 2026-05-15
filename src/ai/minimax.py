import math

from matplotlib.pyplot import grid
from constants import *
from game import check_win, is_full
from .evaluate import LOSING, WINNING, evaluate
from .game_logic import get_candidates

# Bảng transposition cho minimax
minimax_tt = {}

def minimax(grid, depth, is_max):
    """
    Thuật toán Minimax thuần túy với sắp xếp nước đi và bảng transposition.
    """
    from .game_logic import states_visited
    states_visited[0] += 1

    board_hash = (
        tuple(tuple(row) for row in grid),
        is_max
    )

    # Kiểm tra TT
    if board_hash in minimax_tt and minimax_tt[board_hash][0] >= depth:
        return minimax_tt[board_hash][1], minimax_tt[board_hash][2]

    if check_win(grid, AI):
        score = WINNING - depth
        minimax_tt[board_hash] = (depth, score, None)
        return score, None

    if check_win(grid, HUMAN):
        score = LOSING + depth
        minimax_tt[board_hash] = (depth, score, None)
        return score, None
    if is_full(grid) or depth == 0:
        score = evaluate(grid)
        minimax_tt[board_hash] = (depth, score, None)
        return score, None

    cands = get_candidates(grid)
    # Sắp xếp
    player = AI if is_max else HUMAN
    cands = sort_moves_minimax(grid, cands, player)
    # Giới hạn
    if len(cands) > BEAM_WIDTH:
        cands = cands[:BEAM_WIDTH]

    best_score = -math.inf if is_max else math.inf
    best_move = None

    for r, c in cands:
        grid[r][c] = player

        # Thắng ngay
        if check_win(grid, player):
            if player == AI:
                score = WINNING - depth
            else:
                score = LOSING + depth
        else:
            score, _ = minimax(grid, depth - 1, not is_max)

        grid[r][c] = EMPTY

        if is_max:
            if score > best_score:
                best_score, best_move = score, (r, c)
        else:
            if score < best_score:
                best_score, best_move = score, (r, c)

    minimax_tt[board_hash] = (depth, best_score, best_move)
    return best_score, best_move

def quick_move_score_minimax(grid, r, c, player):
    """
    Đánh giá nhanh cho minimax.
    """
    score = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
        cnt = 1
        open_ends = 0
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == player:
            cnt += 1
            nr += dr
            nc += dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
            open_ends += 1
        nr, nc = r - dr, c - dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == player:
            cnt += 1
            nr -= dr
            nc -= dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
            open_ends += 1
        if cnt >= WIN:
            score += 1_000_000

        elif cnt == WIN - 1:
            if open_ends == 2:
                score += 80_000
            elif open_ends == 1:
                score += 20_000

        elif cnt == WIN - 2:
            if open_ends == 2:
                score += 3_000
    # Ưu tiên center
    center_r, center_c = ROWS // 2, COLS // 2
    dist = abs(r - center_r) + abs(c - center_c)
    score += (ROWS + COLS - dist) * 2
    return score

def blocking_score_minimax(grid, r, c, player):
    """
    Tính điểm chặn cho minimax.
    """
    opponent = HUMAN if player == AI else AI
    score = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
        cnt = 0
        open_ends = 0
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == opponent:
            cnt += 1
            nr += dr
            nc += dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
            open_ends += 1
        nr, nc = r - dr, c - dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == opponent:
            cnt += 1
            nr -= dr
            nc -= dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
            open_ends += 1
        if cnt == WIN - 1 and open_ends >= 1:
            score += 120_000

        elif cnt == WIN - 2 and open_ends == 2:
            score += 5_000
    return score

def sort_moves_minimax(grid, moves, player):
    scored = []

    for r, c in moves:

        # Giả lập nước đi
        grid[r][c] = player
        score = quick_move_score_minimax(grid, r, c, player)
        score += blocking_score_minimax(grid, r, c, player)

        # Undo
        grid[r][c] = EMPTY

        scored.append((score, (r, c)))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [move for _, move in scored]
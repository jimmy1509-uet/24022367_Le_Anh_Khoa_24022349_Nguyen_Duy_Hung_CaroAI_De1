import math
from constants import *
from game import check_win, is_full
from .evaluate import LOSING, evaluate, WINNING
from .game_logic import get_candidates

# Bảng transposition để lưu kết quả đã tính
transposition_table = {}

def quick_move_score(grid, r, c, player):
    """
    Đánh giá nhanh một nước đi dựa trên các đường thẳng cục bộ và vị trí.
    Trả về điểm số để sắp xếp nước đi.
    """
    score = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
        cnt = 1
        open_ends = 0
        # Đếm về phía trước
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == player:
            cnt += 1
            nr += dr
            nc += dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
            open_ends += 1
        # Đếm về phía sau
        nr, nc = r - dr, c - dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == player:
            cnt += 1
            nr -= dr
            nc -= dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
            open_ends += 1
        # Tính điểm đơn giản
        if cnt >= WIN:
            score += 1000000
        elif cnt == WIN - 1:
            if open_ends == 2:
                score += 80000
            elif open_ends == 1:
                score += 20000
        elif cnt == WIN - 2:
            if open_ends == 2:
                score += 3000
    # Thêm điểm cho vị trí gần center
    center_r, center_c = ROWS // 2, COLS // 2
    dist = abs(r - center_r) + abs(c - center_c)
    score += (ROWS + COLS - dist) * 2  # Ưu tiên center
    return score

def blocking_score(grid, r, c, player):
    """
    Tính điểm cho việc chặn đối thủ.
    """
    opponent = HUMAN if player == AI else AI
    score = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
        cnt = 0
        open_ends = 0
        # Đếm về phía trước cho đối thủ
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == opponent:
            cnt += 1
            nr += dr
            nc += dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
            open_ends += 1
        # Đếm về phía sau
        nr, nc = r - dr, c - dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == opponent:
            cnt += 1
            nr -= dr
            nc -= dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
            open_ends += 1
        # Nếu là mối đe dọa, chặn được thì điểm cao
        if cnt == WIN - 1 and open_ends >= 1:
            score += 120000# Chặn 3 liên tiếp
        elif cnt == WIN - 2 and open_ends == 2:
            score += 5000# Chặn 2 với 2 đầu hở
    return score

def sort_moves(grid, moves, player):
    scored = []

    for r, c in moves:

        # Giả lập nước đi
        grid[r][c] = player

        score = quick_move_score(grid, r, c, player)
        score += blocking_score(grid, r, c, player)

        # Undo
        grid[r][c] = EMPTY

        scored.append((score, (r, c)))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [move for _, move in scored]

def alpha_beta(grid, depth, is_max, alpha, beta):
    """
    Thuật toán Alpha-Beta với cắt tỉa, sắp xếp nước đi và bảng transposition.
    """
    from .game_logic import states_visited
    states_visited[0] += 1

    # Tạo hash cho bảng cờ (đơn giản: tuple của grid)
    board_hash = (
    tuple(tuple(row) for row in grid),
    is_max
    )
    # Kiểm tra bảng transposition
    if board_hash in transposition_table:
        tt_depth, tt_score, tt_flag, tt_move = transposition_table[board_hash]
        if tt_depth >= depth:
            if tt_flag == 'exact':
                return tt_score, tt_move
            elif tt_flag == 'lower' and tt_score >= beta:
                return tt_score, tt_move
            elif tt_flag == 'upper' and tt_score <= alpha:
                return tt_score, tt_move

    if check_win(grid, AI):
        score = WINNING - depth  # Thắng sớm hơn thì điểm cao hơn
        transposition_table[board_hash] = (depth, score, 'exact', None)
        return score, None
    if check_win(grid, HUMAN):
        score = LOSING + depth
        transposition_table[board_hash] = (depth, score, 'exact', None)
        return score, None
    if is_full(grid) or depth == 0:
        score = evaluate(grid)
        transposition_table[board_hash] = (depth, score, 'exact', None)
        return score, None

    cands = get_candidates(grid)
    # Sắp xếp nước đi
    player = AI if is_max else HUMAN
    cands = sort_moves(grid, cands, player)
    # Giới hạn số nước đi (beam search)
    if len(cands) > BEAM_WIDTH:
        cands = cands[:BEAM_WIDTH]

    best_score = -math.inf if is_max else math.inf
    best_move = None
   

    for r, c in cands:
        grid[r][c] = player
        score, _ = alpha_beta(grid, depth - 1, not is_max, alpha, beta)
        grid[r][c] = EMPTY

        if is_max:
            if score > best_score:
                best_score, best_move = score, (r, c)
            alpha = max(alpha, best_score)
            if best_score >= beta:
                break
        else:
            if score < best_score:
                best_score, best_move = score, (r, c)
            beta = min(beta, best_score)
            if best_score <= alpha:
                break

    # Lưu vào bảng transposition
    transposition_table[board_hash] = (
    depth,
    best_score,
    'exact',
    best_move
    )

    return best_score, best_move
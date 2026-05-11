from constants import *

# Điểm số cho các mẫu đường thẳng
TWO = 100          # Hai quân liên tiếp
TWO_OBSTACLE = 50  # Hai quân bị chặn một đầu
THREE = 10000      # Ba quân liên tiếp
THREE_OBSTACLE = 5000  # Ba quân bị chặn
FOUR = 100000000   # Bốn quân liên tiếp
FOUR_OBSTACLE = 50000000  # Bốn quân bị chặn
WINNING = 2000000000  # Năm quân thắng

# Điểm số cho đối thủ
TWO_OPPONENT = -200
TWO_OBSTACLE_OPPONENT = -30
THREE_OPPONENT = -20000
THREE_OBSTACLE_OPPONENT = -7500
FOUR_OPPONENT = -200000000
FOUR_OBSTACLE_OPPONENT = -100000000
LOSING = -1000000000

def eval_pattern(count, open_ends, player):
    """
    Đánh giá một chuỗi liên tiếp theo số quân và đầu mở.
    """
    if player == AI:
        if count >= WIN:
            return WINNING
        if count == WIN - 1:
            if open_ends == 2:
                return FOUR
            if open_ends == 1:
                return FOUR_OBSTACLE
        if count == WIN - 2:
            if open_ends == 2:
                return THREE
            if open_ends == 1:
                return THREE_OBSTACLE
        if count == WIN - 3:
            if open_ends == 2:
                return TWO
            if open_ends == 1:
                return TWO_OBSTACLE
    else:
        if count >= WIN:
            return LOSING
        if count == WIN - 1:
            if open_ends == 2:
                return FOUR_OPPONENT
            if open_ends == 1:
                return FOUR_OBSTACLE_OPPONENT
        if count == WIN - 2:
            if open_ends == 2:
                return THREE_OPPONENT
            if open_ends == 1:
                return THREE_OBSTACLE_OPPONENT
        if count == WIN - 3:
            if open_ends == 2:
                return TWO_OPPONENT
            if open_ends == 1:
                return TWO_OBSTACLE_OPPONENT
    return 0

def evaluate(grid):
    """
    Đánh giá toàn bộ bảng cờ.
    Tính điểm cho tất cả các chuỗi liên tiếp của AI và người chơi.
    """
    score = 0
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(ROWS):
        for c in range(COLS):
            player = grid[r][c]
            if player not in (HUMAN, AI):
                continue
            for dr, dc in dirs:
                pr, pc = r - dr, c - dc
                if 0 <= pr < ROWS and 0 <= pc < COLS and grid[pr][pc] == player:
                    continue

                count = 0
                open_ends = 0
                nr, nc = r, c
                while 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == player:
                    count += 1
                    nr += dr
                    nc += dc

                if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == EMPTY:
                    open_ends += 1
                if 0 <= pr < ROWS and 0 <= pc < COLS and grid[pr][pc] == EMPTY:
                    open_ends += 1

                score += eval_pattern(count, open_ends, player)

    return score
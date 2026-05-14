from constants import *

# Điểm số cho các mẫu đường thẳng
THREE = 100000000         # Ba quân liên tiếp hở 2 đầu (Rất nguy hiểm)
THREE_OBSTACLE = 50000000 # Ba quân bị chặn một đầu
TWO = 10000               # Hai quân liên tiếp hở 2 đầu
TWO_OBSTACLE = 5000       # Hai quân bị chặn một đầu
WINNING = 2000000000      # Đạt 4 quân (Thắng)

# Điểm số cho đối thủ (Ưu tiên chặn)
THREE_OPPONENT = -200000000
THREE_OBSTACLE_OPPONENT = -100000000
TWO_OPPONENT = -20000
TWO_OBSTACLE_OPPONENT = -7500
LOSING = -1000000000

def eval_pattern(count, open_ends, player):
    """
    Đánh giá chuỗi liên tiếp cho luật 4 quân thắng.
    WIN = 4 (từ constants)
    """
    if player == AI:
        # Trường hợp thắng ngay lập tức
        if count >= WIN:
            return WINNING
        
        # Trường hợp có 3 quân (WIN - 1)
        if count == WIN - 1:
            if open_ends == 2:
                return THREE # Hở 2 đầu là chắc chắn thắng
            if open_ends == 1:
                return THREE_OBSTACLE
        
        # Trường hợp có 2 quân (WIN - 2)
        if count == WIN - 2:
            if open_ends == 2:
                return TWO
            if open_ends == 1:
                return TWO_OBSTACLE
                
    else: # Đánh giá phía Người chơi (Đối thủ)
        if count >= WIN:
            return LOSING
        
        if count == WIN - 1:
            if open_ends == 2:
                return THREE_OPPONENT
            if open_ends == 1:
                return THREE_OBSTACLE_OPPONENT
        
        if count == WIN - 2:
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
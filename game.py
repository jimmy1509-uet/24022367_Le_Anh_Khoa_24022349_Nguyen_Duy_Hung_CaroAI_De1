from constants import *

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [[EMPTY] * COLS for _ in range(ROWS)]
        self.history = []
        self.game_over = False
        self.player_turn = True
        self.win_cells = []
        self.depth = MAX_DEPTH
        self.algorithm = 1  # 0: minimax, 1: alpha-beta, 2: compare
        self.last_move = None
        self.last_score = None
        self.last_states = 0
        self.last_time = 0.0
        self.move_log = []
        self.status_msg = "Lượt của bạn — nhấp vào ô trống"
        self.thinking = False

    def undo_last_moves(self, count=2):
        undone = 0
        while undone < count and self.history:
            r, c, _ = self.history.pop()
            self.grid[r][c] = EMPTY
            undone += 1

        if self.move_log:
            for _ in range(min(undone, len(self.move_log))):
                self.move_log.pop()

        self.game_over = False
        self.player_turn = True
        self.win_cells = []
        self.last_move = None
        self.status_msg = "Đã hoàn tác — lượt của bạn"
        self.thinking = False


def check_win(grid, player):
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != player:
                continue
            for dr, dc in dirs:
                cells = [(r, c)]
                for k in range(1, WIN):
                    nr, nc = r + dr * k, c + dc * k
                    if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == player:
                        cells.append((nr, nc))
                    else:
                        break
                if len(cells) == WIN:
                    return cells
    return None


def is_full(grid):
    return all(grid[r][c] != EMPTY for r in range(ROWS) for c in range(COLS))

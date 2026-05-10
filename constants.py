from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT.parent / "assets"

ROWS = 9
COLS = 9
WIN = 4
CELL = 50  # Giảm từ 60 xuống 50 để cửa sổ nhỏ hơn
MARGIN = 30  # Giảm margin
PANEL_W = 250  # Giảm panel width

BOARD_W = COLS * CELL
BOARD_H = ROWS * CELL
WIN_W = MARGIN + BOARD_W + MARGIN + PANEL_W + MARGIN
WIN_H = MARGIN + BOARD_H + MARGIN + 60

MAX_DEPTH = 2

BG = (245, 243, 235)
GRID_COL = (200, 195, 180)
LINE_COL = (160, 155, 140)
X_COL = (55, 138, 221)
O_COL = (226, 75, 74)
WIN_HL = (255, 220, 80)
PANEL_BG = (255, 253, 248)
PANEL_BORD = (210, 205, 190)
TEXT_MAIN = (0, 0, 0)  # Đen đậm để nổi bật
TEXT_SUB = (100, 100, 100)  # Xám đậm hơn
BTN_BG = (235, 230, 218)
BTN_HOV = (215, 210, 198)
BTN_BORD = (190, 185, 170)
GREEN = (29, 158, 117)
STATUS_BG = (238, 236, 226)

EMPTY = 0
HUMAN = 1
AI = 2

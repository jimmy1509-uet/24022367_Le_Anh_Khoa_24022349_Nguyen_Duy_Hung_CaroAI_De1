import sys
import os
import time
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.ai.alphabeta import alpha_beta
from src.ai.evaluate import evaluate
from constants import AI, HUMAN

# Import các trạng thái bàn cờ
from board_state1 import grid as grid1
from board_state2 import grid as grid2
from board_state3 import grid as grid3

def run_benchmark(grid, state_name):
    print(f"\n--- Benchmark cho {state_name} ---")
    print("Bàn cờ:")
    for row in grid:
        print(' '.join(str(cell) for cell in row))

    # Tìm nước đi tốt nhất cho AI
    start_time = time.time()
    score, best_move = alpha_beta(grid, 4, True, -math.inf, math.inf)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Nước đi tốt nhất: {best_move}")
    print(f"Điểm số: {score}")
    print(".4f")

    # Đánh giá trạng thái hiện tại
    current_score = evaluate(grid)
    print(f"Đánh giá trạng thái hiện tại: {current_score}")

    return best_move, score, elapsed_time

if __name__ == "__main__":
    # Chạy benchmark cho 3 trạng thái
    states = [
        (grid1, "Trạng thái 1: Bàn cờ trống"),
        (grid2, "Trạng thái 2: Giữa game"),
        (grid3, "Trạng thái 3: Gần thắng")
    ]

    for grid, name in states:
        run_benchmark(grid, name)
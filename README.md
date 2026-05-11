# Trò Chơi Caro AI

Một triển khai Python của trò chơi Caro (Gomoku) với đối thủ AI sử dụng thuật toán Minimax và Alpha-Beta pruning.

## Tính năng

- **Chơi với người vs AI**: Chơi với đối thủ AI thông minh
- **Nhiều thuật toán AI**:
  - Thuật toán Minimax
  - Alpha-Beta pruning (phiên bản tối ưu)
  - Chế độ so sánh để xem cả hai thuật toán hoạt động
- **Điều chỉnh độ khó**: Thay đổi độ sâu tìm kiếm (1-4 cấp)
- **Giao diện tương tác**: Được xây dựng với Pygame
  - Bàn cờ trực quan với tọa độ được đánh dấu
  - Bảng điều khiển với thống kê trò chơi
  - Lịch sử nước đi và chỉ số hiệu suất
  - Thanh trượt để chọn thuật toán và điều chỉnh độ sâu
- **Điều khiển trò chơi**:
  - Nhấp chuột trái để đặt quân cờ
  - 'R' để đặt lại trò chơi
  - 'U' để hoàn tác hai nước đi cuối
  - '1'-'4' để thay đổi độ sâu
  - 'ESC' để thoát

## Cấu trúc dự án

```
├── ai/                    # Thuật toán và logic AI
│   ├── alphabeta.py      # Triển khai Alpha-Beta pruning
│   ├── evaluate.py       # Các hàm đánh giá bàn cờ
│   ├── game_logic.py     # Logic trò chơi và thực hiện nước đi AI
│   └── minimax.py        # Triển khai thuật toán Minimax
├── ui/                    # Các thành phần giao diện người dùng
│   ├── board.py          # Vẽ bàn cờ
│   ├── main.py           # Vòng lặp trò chơi chính
│   ├── menu.py           # Bảng điều khiển và các nút
│   └── statistics.py     # Hiển thị trạng thái
├── constants.py          # Hằng số và cấu hình trò chơi
├── game.py               # Quản lý trạng thái trò chơi
├── play.py               # Tập lệnh điểm vào
└── requirements.txt      # Các phụ thuộc Python
```

## Cài đặt

1. Sao chép hoặc tải xuống dự án
2. Cài đặt các phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

## Chạy trò chơi

```bash
python play.py
```

## Cách chơi

1. Trò chơi được chơi trên bàn cờ 9x9
2. Người chơi lần lượt đặt quân cờ (X cho người, O cho AI)
3. Có 4 quân cờ liên tiếp (ngang, dọc hoặc chéo) để thắng
4. AI sử dụng thuật toán nâng cao để cung cấp lối chơi đầy thách thức

## Chi tiết thuật toán

- **Minimax**: Khám phá tất cả các trạng thái trò chơi có thể để tìm nước đi tối ưu
- **Alpha-Beta**: Phiên bản tối ưu cắt tỉa các nhánh không cần thiết, nhanh hơn đáng kể
- **Đánh giá**: Sử dụng nhận dạng mẫu để chấm điểm vị trí bàn cờ dựa trên các hình thành quân cờ

## Điều khiển

- **Chuột**: Nhấp vào ô trống để đặt quân cờ
- **R**: Đặt lại trò chơi
- **U**: Hoàn tác hai nước đi cuối
- **1-4**: Thay đổi độ sâu AI
- **ESC**: Thoát trò chơi

## Tác giả

- Lê Anh Khoa (24022367)
- Nguyễn Duy Hưng (24022349)

## Giấy phép

Dự án này dành cho mục đích giáo dục.
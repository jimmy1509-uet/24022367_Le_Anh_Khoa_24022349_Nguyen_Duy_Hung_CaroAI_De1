# Trò Chơi Caro AI 🏆

Một triển khai Python hoàn chỉnh của trò chơi Caro (Gomoku) với đối thủ AI thông minh sử dụng thuật toán Minimax và Alpha-Beta pruning. Dự án này được phát triển như một phần của môn học Trí Tuệ Nhân Tạo.

## 📋 Mô tả

Trò chơi Caro là một trò chơi chiến lược cổ điển nơi hai người chơi lần lượt đặt quân cờ trên bàn cờ vuông. Người đầu tiên tạo được một đường thẳng với số quân cờ quy định sẽ thắng. Trong phiên bản này, AI sử dụng các thuật toán tìm kiếm nâng cao để cung cấp trải nghiệm chơi đầy thách thức.

## ✨ Tính năng chính

- **🎮 Chế độ chơi đa dạng**:
  - Người vs AI: Thách đấu với máy thông minh
  - Người vs Người: Chơi với bạn bè
- **🤖 Thuật toán AI tiên tiến**:
  - Thuật toán Minimax thuần túy
  - Alpha-Beta pruning với cắt tỉa tối ưu
  - Beam search để giới hạn không gian tìm kiếm
  - Bảng transposition để tăng hiệu suất
- **⚙️ Điều chỉnh độ khó linh hoạt**: Độ sâu tìm kiếm từ 1-4 cấp
- **🎨 Giao diện người dùng trực quan** (Pygame):
  - Bàn cờ 15x15 với lưới rõ ràng
  - Bảng điều khiển hiển thị thống kê real-time
  - Lịch sử nước đi và hiệu suất AI
  - Thanh trượt điều chỉnh tham số
- **🎯 Tính năng nâng cao**:
  - Phát hiện nước đi thắng/chặn ngay lập tức
  - Iterative deepening cho độ sâu động
  - Đánh giá heuristic thông minh

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.7+
- Pygame 2.0+

### Các bước cài đặt
1. **Sao chép dự án**:
   ```bash
   git clone <repository-url>
   cd BTB-CSAI
   ```

2. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy trò chơi**:
   ```bash
   python play.py
   ```

## 🎲 Cách chơi

### Luật cơ bản
- **Bàn cờ**: 15x15 ô vuông
- **Mục tiêu**: Tạo đường thẳng 4 quân cờ liên tiếp (ngang, dọc hoặc chéo)
- **Luân phiên**: Người chơi (X) và AI (O) lần lượt đặt quân

### Điều khiển
- **🖱️ Chuột trái**: Nhấp vào ô trống để đặt quân cờ
- **🔄 R**: Đặt lại ván chơi mới
- **↶ U**: Hoàn tác 2 nước đi cuối cùng
- **🔢 1-4**: Thay đổi độ sâu AI (1=dễ, 4=khó)
- **🚪 ESC**: Thoát trò chơi

### Giao diện
- **Bàn cờ**: Khu vực chính hiển thị trạng thái trò chơi
- **Bảng điều khiển**: Hiển thị lượt chơi, điểm số, thời gian suy nghĩ
- **Thanh trượt**: Điều chỉnh thuật toán và độ sâu

## 🧠 Thuật toán AI

### Minimax
Thuật toán cổ điển khám phá toàn bộ cây trạng thái trò chơi để tìm nước đi tối ưu. Tuy hiệu quả về mặt lý thuyết nhưng chậm với độ sâu lớn.

### Alpha-Beta Pruning
Phiên bản tối ưu của Minimax với kỹ thuật cắt tỉa nhánh không cần thiết, giảm đáng kể không gian tìm kiếm mà vẫn đảm bảo kết quả tối ưu.

### Tối ưu hóa bổ sung
- **Beam Search**: Giới hạn số nước đi xem xét tại mỗi nút (BEAM_WIDTH=20)
- **Transposition Table**: Lưu trữ kết quả đã tính để tránh tính lại
- **Move Ordering**: Sắp xếp nước đi theo heuristic để cắt tỉa hiệu quả hơn
- **Iterative Deepening**: Tăng dần độ sâu để tận dụng thời gian tốt hơn

### Hàm đánh giá
Sử dụng nhận dạng mẫu để chấm điểm dựa trên:
- Số quân liên tiếp và đầu hở
- Vị trí trên bàn cờ (ưu tiên center)
- Mối đe dọa từ đối thủ

## 📁 Cấu trúc dự án

```
├── 📂 ai/                    # 🔍 Thuật toán và logic AI
│   ├── alphabeta.py         # ⚡ Alpha-Beta pruning implementation
│   ├── evaluate.py          # 📊 Hàm đánh giá bàn cờ
│   ├── game_logic.py        # 🎮 Logic trò chơi và AI moves
│   └── minimax.py           # 🌳 Minimax algorithm
├── 📂 ui/                    # 🎨 Giao diện người dùng
│   ├── board.py             # 📋 Vẽ bàn cờ
│   ├── main.py              # 🎯 Vòng lặp chính
│   ├── menu.py              # 🎛️ Bảng điều khiển
│   └── statistics.py        # 📈 Thống kê
├── 📂 benchmark/            # 🧪 Test và benchmark
│   ├── benchmark.py         # 📊 Script benchmark
│   ├── board_state1.py      # 🎯 Trạng thái test 1
│   ├── board_state2.py      # 🎯 Trạng thái test 2
│   └── board_state3.py      # 🎯 Trạng thái test 3
├── constants.py             # ⚙️ Hằng số cấu hình
├── game.py                  # 🎲 Quản lý trạng thái
├── play.py                  # 🚀 Entry point
├── requirements.txt         # 📦 Dependencies
└── README.md               # 📖 Tài liệu này
```

## 🧪 Benchmark và Test

Dự án bao gồm hệ thống benchmark để đánh giá hiệu suất AI:

```bash
python src/benchmark/benchmark.py
```

Bao gồm 3 trạng thái test:
- **Trạng thái 1**: Bàn cờ trống - Test nước đi đầu
- **Trạng thái 2**: Giữa ván - Test chiến lược
- **Trạng thái 3**: Gần thắng - Test phát hiện thắng

## 👥 Tác giả

- **Lê Anh Khoa** (24022367) - Phát triển thuật toán AI
- **Nguyễn Duy Hưng** (24022349) - Thiết kế giao diện và tích hợp

---

**🎉 Chúc bạn chơi vui! Nếu có góp ý hoặc câu hỏi, hãy liên hệ với tác giả.**
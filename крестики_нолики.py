
### Игра Крестики-нолики ################################################

def print_board(board):
    """Выводит игровое поле в консоль."""
    for row in board:
        print(" | ".join(row))
        if row != board[-1]:
            print("---------")

def check_winner(board, player):
    """Проверяет, выиграл ли игрок."""
    # Проверка строк
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Проверка столбцов
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Проверка диагоналей
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    """Проверяет, заполнено ли поле."""
    return all(cell != " " for row in board for cell in row)


def main():
    # Инициализация пустого поля 3x3
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"  # Первый игрок — X

    print("Крестики‑нолики!\n")
    print_board(board)

    while True:
        # Ввод хода
        try:
            row = int(input(f"Игрок {current_player}, введите номер строки (1–3): ")) - 1
            col = int(input(f"Игрок {current_player}, введите номер столбца (1–3): ")) - 1
        except ValueError:
            print("Введите числа от 1 до 3.")
            continue

        # Проверка корректности ввода
        if not (0 <= row <= 2 and 0 <= col <= 2):
            print("Координаты должны быть от 1 до 3.")
            continue
        if board[row][col] != " ":
            print("Эта клетка уже занята!")
            continue

        # Делаем ход
        board[row][col] = current_player
        print_board(board)

        # Проверяем победу
        if check_winner(board, current_player):
            print(f"Игрок {current_player} победил!")
            break

        # Проверяем ничью
        if is_full(board):
            print("Ничья!")
            break

        # Смена игрока
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
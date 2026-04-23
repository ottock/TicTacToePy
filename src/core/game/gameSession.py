class Game:
    def __init__(self):
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', ''],
        ]
        self.turn = 'o'
        self.result = ''


    # functions
    def start_game(self) -> None:
        running = True
        while running:
            self._on_turn()
            self.result = self._check_board()
            match(self.result):
                case('o'):
                    running = False
                case('x'):
                    running = False
                case("draw"):
                    running = False


    def play_move(self, row: int, col: int) -> bool:
        if self.result:
            return False

        if not (0 <= row < 3 and 0 <= col < 3):
            return False

        if self.board[row][col] != '':
            return False

        self.board[row][col] = self.turn
        self.result = self._check_board()

        if not self.result:
            self._pass_turn()

        return True


    def _reset(self) -> None:
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', ''],
        ]
        self.turn = 'o'
        self.result = ''


    def _pass_turn(self) -> None:
        self.turn = 'x' if self.turn == 'o' else 'o'


    def _check_board(self) -> str:
        def _check_draw():
            for row in self.board:
                if '' in row:
                    return False
            return True


        def _check_horizontal() -> str:
            for row in self.board:
                if row[0] != '' and row.count(row[0]) == 3:
                    return row[0]
            return ''


        def _check_vertical() -> str:
            for col in range(3):
                if (
                    self.board[0][col] != '' and
                    self.board[0][col] == self.board[1][col] == self.board[2][col]
                ):
                    return self.board[0][col]
            return ''


        def _check_diagonal() -> str:
            if (
                self.board[0][0] != '' and
                self.board[0][0] == self.board[1][1] == self.board[2][2]
            ):
                return self.board[0][0]

            if (
                self.board[0][2] != '' and
                self.board[0][2] == self.board[1][1] == self.board[2][0]
            ):
                return self.board[0][2]
            return ''

        result = _check_horizontal()
        if result:
            return result
        result = _check_vertical()
        if result:
            return result
        result = _check_diagonal()
        if result:
            return result
        if _check_draw():
            return "draw"
        return ''
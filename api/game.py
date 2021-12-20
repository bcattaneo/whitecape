import subprocess
import sys
import time
import chess

MOVEMENT_PREFIX = "position startpos move"


class Game:
    def __init__(self, stockfish_path, starting_position=[]):
        self.board = chess.Board()
        self.position = starting_position
        self.stockfish_path = stockfish_path
        self.__init_board()  # throws exception on first bad move in starting position

    def sanToUciSteps(steps):
        temp_board = chess.Board()
        return list(map(lambda step: str(temp_board.push_san(step)), steps))

    def move(self, movement):
        self.board.push_uci(movement)  # throws exception if bad move
        self.position.append(movement)

    def display(self):
        return "\n".join(self.__run_stockfish("d").split("\n")[2:20])

    def best_move(self):
        # TODO: include ponder in the API response?
        output = self.__run_stockfish("go depth 20").split("\n")[-1]
        return "" if "bestmove (none)" in output else output[9:13]

    def apply_best_move(self):
        new_best_move = self.best_move()
        self.move(new_best_move)
        return new_best_move

    def __run_stockfish(self, command):
        commands = [self.__get_position(), command]
        process = subprocess.Popen([self.__get_stockfish_path()],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        for c in commands:
            time.sleep(0.5)
            print(c, file=process.stdin, flush=True)

        time.sleep(5)

        output = process.communicate()[0]
        # print(output)
        return output.strip()

    def __init_board(self):
        for move in self.position:
            self.board.push_uci(move)

    def __get_stockfish_path(self):
        return self.stockfish_path

    def __get_position(self):
        return f"{MOVEMENT_PREFIX} {' '.join(self.position)}"

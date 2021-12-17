import subprocess

STOCKFISH_PATH = "stockfish/stockfish.exe"
MOVEMENT_PREFIX = "position startpos move"


class Game:
    def __init__(self, starting_position=[], stockfish_path=STOCKFISH_PATH):
        # TODO: validate starting position
        # starting_position = list of position strings
        self.position = starting_position
        self.stockfish_path = stockfish_path

    def move(self, movement):
        new_position = list(self.position)
        new_position.append(movement)
        # TODO: validate here new position is valid
        # otherwise return false (or throw exception)
        if True:
            self.position = new_position
            return True
        else:
            return False

    def display(self):
        return "\n".join(self.__run_stockfish("d").split("\n")[2:20])

    def best_move(self):
        return self.__run_stockfish("go depth 25").split("\n")[2].replace("bestmove ", "")

    def apply_best_move(self):
        new_best_move = self.best_move()
        self.move(new_best_move)
        return new_best_move

    def __run_stockfish(self, command):
        commands = [self.__get_position(), command]
        # program = subprocess.Popen([self.__get_stockfish_path(), "\n".join(commands)],
        program = subprocess.Popen(self.__get_stockfish_path(),
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        [out, err] = program.communicate(
            ("\n".join(commands)).encode(), timeout=50)
        # program.wait(timeout=10)

        # TODO: throw exception when there are errors
        # print(err.decode(), file=sys.stderr)
        # print(program.stdout.readlines())
        # return program.stdout
        return out.decode().strip()

    def __get_stockfish_path(self):
        return self.stockfish_path

    def __get_position(self):
        return f"{MOVEMENT_PREFIX} {' '.join(self.position)}"

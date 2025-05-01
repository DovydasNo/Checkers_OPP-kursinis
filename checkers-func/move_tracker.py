def log_move(self, from_row, from_col, to_row, to_col, jumped):
    log = f"{self.turn.capitalize()} moved from ({from_row}, {from_col}) to ({to_row}, {to_col})"
    
    if jumped:
        log += f" capturing {[f'({Piece.row}, {Piece.col})' for Piece in jumped]}"
    self.move_log.append(log)

    with open("move_log.txt", "a") as f:
        f.write(log + "\n")

def read_move_log(filename="move_log.txt"):
    with open(filename, "r") as f:
        return f.readlines()
        
def clear_move_log(filename="move_log.txt"):
    open(filename, "w").close()
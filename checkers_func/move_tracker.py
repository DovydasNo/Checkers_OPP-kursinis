def log_move(turn, from_row, from_col, to_row, to_col, jumped):
    log = f"{turn.capitalize()} moved from ({from_row},{from_col}) to ({to_row},{to_col})"
    if jumped:
        log += f" capturing {[f'({p.row}, {p.col})' for p in jumped]}"
    with open("move_log.txt", "a") as f:
        f.write(log + "\n")

def read_move_log(filename="move_log.txt"):
    with open(filename, "r") as f:
        return f.readlines()
        
def clear_move_log(filename="move_log.txt"):
    open(filename, "w").close()
# Checkers_OPP-kursinis

Kursinis darbas - Šaškės (Checkers)

Sistemos reikalavimai *(minimum)*:
- OS: Ką turi, tas veiks (tikriausiai)
- Procesorius: Truputį geresnis už bulvę
- Atmintis: 512 MB
- Grafikų plokštė: Jei perskaitai, vadinas turėtu užtekti
- Internetas: Kam, ne Fortnite žaidi
- Vieta: 20 MB užteks
- Garso plokštė: Kažkas dar tokias naudoja?
- "Mayonnaise overconsumption may be hazardous to your health"

Paleisti žaidimą galima nustačius teisingą direktyvą ir komandos lauke įvedus `python main.py`. Žaidimo metu galioja Amerikietiškos standartinės šaškių taisyklės (žr. https://www.hasbro.com/common/instruct/Checkers.PDF). Visi ėjimai yra išsaugomi iki kito žaidimo pradžios arba atstatymo. Žaidimo metu galima pradėti žaidimą iš naujo nuspaudus `R` mygtuką. Šis žaidimas neturi nei AI žaidėjo, nei neveikia pagal minmax algoritmą - žaisk vienas arba su draugu.

## Žaidimo kodas

Pačio žaidimo stuktūra yra paskirstyta per 6 failus ir juos visus suriša `main.py`: 
- Daugiausia žaidimo logikos yra apdorojama `game.py` (žaidimo procesas ir laimėjimas)
- Kartu su `board.py` (su lentos ribomis ir judėjimu susiję skaičiavimai)
- `piece.py` yra atsakingas už detalių piešimą ir jų būseną
- `constants.py` yra nusakytos visos šiame žaidime naudojamos nesikeičiačios vertės
- `move_tracker.py` seka ir išsaugo žaidėjo atliktus veiksmus ir juos įrašo į `move_log.txt`

Šiam projektui panaudoti buvo 

## **4 Objektinio programavimo principai**:

### Polimorfizmas
Iš `board.py`:
    
    def draw(self, win):
        <...>
        piece.draw(win)

Iš `piece.py`:

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(win, BLACK, (self.__x, self.__y), radius + OUTLINE)
        pygame.draw.circle(win, self.__colour, (self.__x, self.__y), radius)
        if self.__queen:
            win.blit(CROWN, (self.__x - CROWN.get_width() // 2, self.__y - CROWN.get_height() // 2))

Čia yra du pavyzdžiai polimorfizmo mano kode: 
  1) `Board` klasėje metodas `draw` kviečia `Piece` klasėje esantį metoda;
  2) `Piece` klasėje naudojamas tas pats `draw` metodas, nepriklausomai ar tai paprasta figūra, ar karalienė.

 
### Abstrakcija

Iš `move_tracker.py`:

    def log_move(turn, from_row, from_col, to_row, to_col, jumped):
        log = f"{turn.capitalize()} moved from ({from_row},{from_col}) to ({to_row},{to_col})"
        if jumped:
            log += f" capturing {[f'({p.row}, {p.col})' for p in jumped]}"
        with open("move_log.txt", "a") as f:
            f.write(log + "\n")

Kodo paskirstymas po kelis failus ir yra abstrakcija. Geriausias jos pavyzdys yra `move_tracker.py` failas. Visas šio failo darbas yra įrašyti, perskaityti ir ištrinti informaciją. Kitose klasėse jį reikia tik iškviesti ir tai palengvina kodą "ant akių".

 
### Paveldėjimas

Iš `piece.py`:

    class QueenPiece(Piece):
    def __init__(self, row, col, colour_name):
        super().__init__(row, col, colour_name)
        self._is_queen = True

Šiuo atveju, `Piece` klasė yra tėvinė, `QueenPiece` kaip dukterinė ima argumentus ir prideda viena savo. Tai bendru atvėju sumažina kodo ir pasikartojančių argumentų apimtį.

 
### Inkapsuliacija

Iš `piece.py`:

    def __init__(self, row, col, colour_name):
        self.__row = row
        self.__col = col
        self.__colour_name = colour_name
        self.__colour = WHITE if colour_name == "white" else BLACK
        self.__queen = False
        self.__x = 0
        self.__y = 0
        self.__position()

    @property
    def row(self):
        return self.__row

Inkapsuliacija šiame kode labiausiai naudojama `Piece` klasėje, kadangi dauguma figūrų veiksmų yra atliekami šioje klasėje. Jei reikia perduoti duomenis kitoms klasėms, privatūs duomenys yra perduodami kaip @property atributai.

 
## Panaudoti dizaino modeliai (Design patterns):

### Decorator

Iš `constants.py`:

    def make_my_text_pretty(func):
    def wrapper(*args, **kwargs):
        print("\n°º¤ø,__,ø¤º°`°º¤ø,__,ø¤°º¤ø,__,ø¤º°`°º¤ø,\n\n")
        result = func(*args, **kwargs)
        print("\n\n°º¤ø,__,ø¤º°`°º¤ø,__,ø¤°º¤ø,__,ø¤º°`°º¤ø,\n")
        return result
    return wrapper

Iš `game.py`:

    @make_my_text_pretty
    def reset(self):
        self._init()
        clear_move_log()
        print('             Game restarted')

Dekoratorius naudojamas konsolėje išskirti vietą ir parodyti žinutę: šiuo atvėju kai žaidimas yra perkrautas ir kai kažkas laimi. Kaip pavadinimas nusako, šis dizaino modelis labiausiai tiko pagražinti tekstą.

 
### Factory method

Iš `piece.py`:

    class PieceFactory:
    @staticmethod
    def create_piece(row, col, colour_name, is_queen=False):
        piece = Piece(row, col, colour_name)
        if is_queen:
            piece.make_queen()
        return piece

Iš `board.py`:

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 != 0:
                    if row < 3:
                        self.board[row].append(PieceFactory.create_piece(row, col, "black"))
                    elif row > 4:
                        self.board[row].append(PieceFactory.create_piece(row, col, "white"))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

Detalių fabrikas, skirtas gaminti figūras. Ką daugiau pasakyt. Pasirinktas pagal pavadinimą.


## Kompozicija ir agregacija:

Iš `game.py`:

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = "white"
        self.valid_moves = {}

Šiame kode agregacijos beveik nėra - viskas buvo daryta kompozicijos principu. Šiame pavyzdyje kompozicija pasireiškia kaip '`Game` klasė viduje turi `Board`' ir jei nebebus, arba bus atstatyta `Game` klasė, `Board` klasė su savyje esančiais `Piece` klasės elementais bus atstatyta.


## Darbas su failu:

Iš `move_tracker.py`:

    def log_move(turn, from_row, from_col, to_row, to_col, jumped):
        log = f"{turn.capitalize()} moved from ({from_row},{from_col}) to ({to_row},{to_col})"
        if jumped:
            log += f" capturing {[f'({p.row}, {p.col})' for p in jumped]}"
        with open("move_log.txt", "a") as f:
            f.write(log + "\n")

    def clear_move_log(filename="move_log.txt"):
        open(filename, "w").close()

Visa šio failo esmė yra įrašyti žaidėjo ėjimus, juos sugebėt perskaityti ir prasidėjus naujam žaidimui arba jį atstačius ištrinti informaciją.


## Unit'u testavimas:

Iš `test_piece,py`:

    class TestPiece(unittest.TestCase):
    def test_initial_position(self):
        piece = Piece(2, 3, 'white')
        self.assertEqual(piece.get_possition(), (2, 3))

Visoms klasėms buvo atlikti testai, visi pavyko.


## Išvados:

- Žaidimas veikia;
- Projektas ne toks sunkus kokio tikėjausi, ypač kai neturiu daug programavimo patirties;
- Jį tikrai galima pagerinti, gal net panaudosiu gyvenime žinias, įgytas darant šitą žaidimą.

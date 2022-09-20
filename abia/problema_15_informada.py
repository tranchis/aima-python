from __future__ import annotations
from typing import List, Generator, Dict

from search import Problem, breadth_first_graph_search, depth_first_graph_search, depth_limited_search, \
    iterative_deepening_search, uniform_cost_search, breadth_first_tree_search, recursive_best_first_search, Node, \
    greedy_best_first_graph_search

"""
Possible sol·lució al Problema 15 de Cerca Heurística
"""

PIECE_COLORS = ['B', 'N', ' ']  # Constant: colors possibles en el tauler


def count_elems(list_elems: List[str], value: str) -> int:
    """
    Funció d'utilitat per comptar els elements d'una llista iguals al valor d'entrada.
    S'utilitzarà més endavant per guardar en l'estat el número de peces de cada color.
    """
    return len(list(filter(lambda elem: elem == value, list_elems)))


class Problema15Board(object):
    """
    Classe de representació de l'estat pel Problema 15

    Defineix estructures de dades internes i conté les funcions
    necessàries per manipular i fer consultes en aquestes estructures.
    """

    def __init__(self, pieces_list: List[str], color_counts: Dict[str, int] = None):
        """
        Constructora. Rep com a mínim una llista que representa les caselles del joc.
        A més, pot rebre un diccionari amb les freqüències dels colors en aquestes caselles.
        Si no es rep aquest diccionari, es crea en base a la llista de les caselles.
        """
        self.pieces_list = pieces_list
        self.board_length = len(self.pieces_list)  # També guardem la mida del tauler, que serà fixe
        if color_counts is None:
            # Creació del diccionari amb les freqüències dels colors.
            # Implica un augment constant del cost però permet estalviar temps en la
            # comprovació d'estat final, que seria lineal sense aquesta estructura.
            self.color_counts = {color: count_elems(pieces_list, color) for color in PIECE_COLORS}
        else:
            self.color_counts = color_counts
        if self.color_counts[' '] != 1:
            raise Exception("Incorrect board configuration")

    def copy(self) -> Problema15Board:
        """
        Funció de còpia que permet treballar amb còpies de les estructures
        internes de dades
        """
        return Problema15Board(self.pieces_list.copy(), self.color_counts.copy())

    def is_goal(self) -> bool:
        """
        Comprovació d'estat final: totes les peces negres menys una buida.
        Cost constant gràcies a l'estructura de freqüències de colors.
        """
        return self.color_counts['N'] == (self.board_length - 1) and self.color_counts[' '] == 1

    def move_piece(self, initial_position: int, final_position: int) -> Problema15Board:
        """
        Retorna un tauler a on la peça initial_position es mou a final_position.
        No hi ha canvis de color i per tant no cal modificar l'estructura de freqüències.
        IMPORTANT: no modificar l'estat i retornar una versió nova
        """
        new_problem = self.copy()
        new_problem.pieces_list[final_position] = new_problem.pieces_list[initial_position]
        new_problem.pieces_list[initial_position] = ' '
        return new_problem

    def jump_over_piece(self, initial_position: int, middle_position: int) -> Problema15Board:
        """
        Retorna un tauler a on la peça initial_position salta per sobre de middle_position.
        Cal comprovar si la peça a middle_position ha de canviar de color, i en cas positiu
        caldrà modificar l'estructura de freqüències.
        IMPORTANT: no modificar l'estat i retornar una versió nova
        """
        distance = middle_position - initial_position
        final_position = middle_position + distance  # Es podria haver passat com a paràmetre de la funció
        jumping_color = self.pieces_list[initial_position]
        jumped_color = self.pieces_list[middle_position]
        must_switch_color = jumping_color != jumped_color

        new_problem = self.copy()
        if must_switch_color:
            new_problem.pieces_list[middle_position] = jumping_color  # Canvi de color
            # Modificació de l'estructura de freqüències:
            new_problem.color_counts[jumped_color] = new_problem.color_counts[jumped_color] - 1
            new_problem.color_counts[jumping_color] = new_problem.color_counts[jumping_color] + 1

        # En qualsevol cas, intercanvi: initial_position amb final_position
        new_problem.pieces_list[final_position] = jumping_color
        new_problem.pieces_list[initial_position] = ' '
        return new_problem

    """
    Funcions auxiliars per saber quins operadors seran aplicables
    """

    def can_move_right(self, pos: int) -> bool:
        return 0 <= pos <= self.board_length - 2 \
               and self.pieces_list[pos] != ' ' and self.pieces_list[pos + 1] == ' '

    def can_move_left(self, pos: int) -> bool:
        return 1 <= pos <= self.board_length - 1 \
               and self.pieces_list[pos] != ' ' and self.pieces_list[pos - 1] == ' '

    def can_jump_right(self, pos: int) -> bool:
        return 0 <= pos <= self.board_length - 3 \
               and self.pieces_list[pos] != ' ' and self.pieces_list[pos + 1] != ' ' \
               and self.pieces_list[pos + 2] == ' '

    def can_jump_left(self, pos: int) -> bool:
        return 2 <= pos <= self.board_length - 1 \
               and self.pieces_list[pos] != ' ' and self.pieces_list[pos - 1] != ' ' \
               and self.pieces_list[pos - 2] == ' '

    def heuristic(self) -> float:
        return self.color_counts['B']

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()


class Problema15Action(object):
    """
    Classe abstracta que representa una acció possible al Problema 15
    """
    pass


class MovePiece(Problema15Action):
    """
    Classe per representar l'acció de moure una peça a una casella contígua
    """
    def __init__(self, initial_position: int, final_position: int):
        self.initial_position = initial_position
        self.final_position = final_position

    def __repr__(self):
        return f"Move Piece {self.initial_position} to {self.final_position}"


class JumpOverPiece(Problema15Action):
    """
    Classe per representar l'acció de saltar una peça per sobre d'una altra
    """
    def __init__(self, initial_position: int, middle_position: int):
        self.initial_position = initial_position
        self.middle_position = middle_position

    def __repr__(self):
        return f"Jump Piece {self.initial_position} over {self.middle_position}"


class Problema15(Problem):
    """
    Classe que implementa el problema. Aquesta classe hereda de Problem i per tant
    es podrà aplicar a tots els algoritmes de cerca no informada i informada.
    """
    def __init__(self, initial_state: List[str] = None):
        """
        Constructora. El problema té un estat inicial i no té estat final.
        Com que la nostra representació de l'estat és la classe Problema15Board,
        hem de crear un objecte d'aquesta classe passant la llista de les caselles
        com a paràmetre.
        """
        if initial_state is None:
            self.initial_state = Problema15Board(['N', 'N', 'B', 'B', ' '])
            self.board_length = 5
        else:
            self.initial_state = Problema15Board(initial_state)
            self.board_length = len(initial_state)
        self.expanded_nodes = 0  # Variable que utilitzarem per comparar algoritmes
        super().__init__(self.initial_state, None)

    def actions(self, current_state: Problema15Board) -> Generator[Problema15Action, None, None]:
        """
        Funció que calcula els operadors aplicables des de l'estat, parametritzats.
        Com en aquesta implementació, és recomanable fer-ho amb generadors per estalviar memòria.
        L'ús de yield permet retornar automàticament un generador sense haver d'usar return.
        """
        self.expanded_nodes = self.expanded_nodes + 1  # actions() es crida quan s'obre un node
        board_length = current_state.board_length
        for pos in range(board_length):
            if current_state.can_move_right(pos):
                yield MovePiece(pos, pos + 1)
            if current_state.can_move_left(pos):
                yield MovePiece(pos, pos - 1)
            if current_state.can_jump_right(pos):
                yield JumpOverPiece(pos, pos + 1)
            if current_state.can_jump_left(pos):
                yield JumpOverPiece(pos, pos - 1)

    def result(self, current_state: Problema15Board, next_action: Problema15Action) -> Problema15Board:
        """
        Funció que retorna el nou estat resultant d'aplicar l'operador parametritzat
        next_action a partir de l'estat current_state.
        """
        if isinstance(next_action, MovePiece):
            return current_state.move_piece(next_action.initial_position, next_action.final_position)
        elif isinstance(next_action, JumpOverPiece):
            return current_state.jump_over_piece(next_action.initial_position, next_action.middle_position)

    def goal_test(self, state: Problema15Board) -> bool:
        """
        Funció que retorna si l'estat state és final.
        """
        return state.is_goal()

    def path_cost(self, c, state1, action, state2):
        return c + 1


if __name__ == '__main__':
    problema = Problema15()
    n = breadth_first_graph_search(problema)
    # [Move Piece 3 to 4, Jump Piece 1 over 2, Jump Piece 3 over 2, Move Piece 4 to 3, Jump Piece 2 over 3]
    print("BFS solution: " + str(n.solution()))
    print(f"Expanded nodes: {problema.expanded_nodes}")

    # problema = Problema15()
    # n = depth_first_graph_search(problema)
    # No acaba. Per què?
    # print("DFS solution: " + n.solution())
    # print(f"Expanded nodes: {problema.expanded_nodes}")

    problema = Problema15()
    n = depth_limited_search(problema)
    # Molt ineficient. La profunditat per defecte és 50, podeu provar altres valors? 1000? 100?
    print("Depth limited solution: " + str(n.solution()))
    print(f"Expanded nodes: {problema.expanded_nodes}")

    problema = Problema15()
    n = iterative_deepening_search(problema)
    print("IDS solution: " + str(n.solution()))
    print(f"Expanded nodes: {problema.expanded_nodes}")

    problema = Problema15()
    n = uniform_cost_search(problema)
    print("B&B: " + str(n.solution()))
    print(f"Expanded nodes: {problema.expanded_nodes}")

    problema = Problema15()
    n = recursive_best_first_search(problema, h=lambda node: node.state.heuristic())
    print("RBFS: " + str(n.solution()))
    print(f"Expanded nodes: {problema.expanded_nodes}")

    problema = Problema15()
    n = greedy_best_first_graph_search(problema, f=lambda node: node.state.heuristic())
    print("GBS: " + str(n.solution()))
    print(f"Expanded nodes: {problema.expanded_nodes}")

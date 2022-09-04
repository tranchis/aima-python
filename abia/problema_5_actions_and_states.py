from __future__ import annotations
from typing import List, Generator

from search import Problem, breadth_first_tree_search


class Flip(object):
    def __init__(self, pos_1: int, pos_2: int):
        self.pos_1 = pos_1
        self.pos_2 = pos_2

    def __repr__(self):
        return f"Flip coins: {self.pos_1} and {self.pos_2}"


class ImmutableCoinsState(object):
    def __init__(self, coins_state: List[str]):
        self.coins_state = coins_state

    def generate_actions(self):
        total_coins = len(self.coins_state)
        return (Flip(x, (x + 1) % total_coins) for x in range(total_coins))

    def apply_action(self, next_action: Flip) -> ImmutableCoinsState:
        new_state = self.coins_state.copy()

        new_state[next_action.pos_1] = self.flip_coin(self.coins_state[next_action.pos_1])
        new_state[next_action.pos_2] = self.flip_coin(self.coins_state[next_action.pos_2])

        return ImmutableCoinsState(new_state)

    @staticmethod
    def flip_coin(coin: str):
        if coin == 'A':
            return 'R'
        elif coin == 'R':
            return 'A'
        else:
            raise Exception("Coin is not valid, should be A or R")

    def length(self):
        return len(self.coins_state)

    def __eq__(self, other):
        return isinstance(other, ImmutableCoinsState) and self.coins_state == other.coins_state

    def __repr__(self):
        return str.join("", self.coins_state)


class Problema5ActionsAndStates(Problem):
    def __init__(self, initial_state=None, goal_state=None):
        if initial_state is None:
            initial_state = ImmutableCoinsState(['A', 'R', 'A', 'R', 'A'])
        if goal_state is None:
            goal_state = ImmutableCoinsState(['R', 'R', 'R', 'A', 'R'])

        if initial_state.length() != goal_state.length():
            raise Exception("Length of arguments should be equal")

        super().__init__(initial_state)
        self.goal_state = goal_state

    def actions(self, current_state: ImmutableCoinsState) -> Generator[Flip, None, None]:
        return current_state.generate_actions()

    def result(self, current_state: ImmutableCoinsState, next_action: Flip) -> ImmutableCoinsState:
        return current_state.apply_action(next_action)

    def value(self, current_state):
        return None  # Not yet applicable until local search algorithms

    def goal_test(self, current_state):
        return current_state == self.goal_state


if __name__ == '__main__':
    example_initial_state = ImmutableCoinsState(['A', 'R', 'A', 'R', 'A'])
    example_goal_state = ImmutableCoinsState(['R', 'R', 'R', 'A', 'R'])

    problem = Problema5ActionsAndStates(example_initial_state, example_goal_state)
    node = breadth_first_tree_search(problem)

    print(node.solution())

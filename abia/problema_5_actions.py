from typing import List, Generator

from search import Problem, breadth_first_tree_search


class Flip(object):
    def __init__(self, pos_1: int, pos_2: int):
        self.pos_1 = pos_1
        self.pos_2 = pos_2

    def __repr__(self):
        return f"Flip coins: {self.pos_1} and {self.pos_2}"


class Problema5Actions(Problem):
    def __init__(self, initial_state=None, goal_state=None):
        if initial_state is None:
            initial_state = ['A', 'R', 'A', 'R', 'A']
        if goal_state is None:
            goal_state = ['R', 'R', 'R', 'A', 'R']

        if len(initial_state) != len(goal_state):
            raise Exception("Length of arguments should be equal")

        super().__init__(initial_state)
        self.goal_state = goal_state

    @staticmethod
    def flip_coin(coin: str):
        if coin == 'A':
            return 'R'
        elif coin == 'R':
            return 'A'
        else:
            raise Exception("Coin is not valid, should be A or R")

    def actions(self, current_state: List[str]) -> Generator[Flip, None, None]:
        total_coins = len(current_state)
        return (Flip(x, (x + 1) % total_coins) for x in range(total_coins))

    def result(self, current_state: List[str], next_action: Flip) -> List[str]:
        new_state = current_state.copy()

        new_state[next_action.pos_1] = self.flip_coin(current_state[next_action.pos_1])
        new_state[next_action.pos_2] = self.flip_coin(current_state[next_action.pos_2])

        return new_state

    def value(self, current_state):
        return None  # Not yet applicable until local search algorithms

    def goal_test(self, current_state):
        return current_state == self.goal_state


if __name__ == '__main__':
    example_initial_state = ['A', 'R', 'A', 'R', 'A']
    example_goal_state = ['R', 'R', 'R', 'A', 'R']

    problem = Problema5Actions(example_initial_state, example_goal_state)
    node = breadth_first_tree_search(problem)

    print(node.solution())

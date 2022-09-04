from typing import List

from search import Problem, breadth_first_tree_search


class Problema5(Problem):
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

    def actions(self, current_state: List[str]) -> range:
        return range(len(current_state))

    def result(self, current_state: List[str], next_action: int) -> List[str]:
        new_state = current_state.copy()
        pos_1 = next_action
        pos_2 = (next_action + 1) % len(current_state)

        new_state[pos_1] = self.flip_coin(current_state[pos_1])
        new_state[pos_2] = self.flip_coin(current_state[pos_2])

        return new_state

    def value(self, current_state):
        return None  # Not yet applicable until local search algorithms

    def goal_test(self, current_state):
        return current_state == self.goal_state


if __name__ == '__main__':
    example_initial_state = ['A', 'R', 'A', 'R', 'A']
    example_goal_state = ['R', 'R', 'R', 'A', 'R']

    problem = Problema5(example_initial_state, example_goal_state)
    node = breadth_first_tree_search(problem)

    print(node.solution())

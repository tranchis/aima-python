from search import GraphProblem, UndirectedGraph, depth_first_graph_search

if __name__ == '__main__':
  g = UndirectedGraph({'1': {'2': 1, '3': 1},
                       '2': {'3': 1},
                       '3': {'4': 1}})

  p = GraphProblem('1', '4', g)
  n = depth_first_graph_search(p)
  print(n.solution())  # ['3', '4']

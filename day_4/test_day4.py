import unittest
from day4 import Graph
class TestAssumptions(unittest.TestCase):
    def test_x_mas_cross_correct(self):
        graph = Graph(3, 3)
        test_data = [['M','X','M'],
                     ['X','A','X'],
                     ['S','X','S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()

        self.assertEqual(count_mas, 1)

        graph = Graph(3, 3)
        test_data = [['M','X','S'],
                     ['X','A','X'],
                     ['M','X','S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()

        self.assertEqual(count_mas, 1)

        graph = Graph(3, 3)
        test_data = [['S','X','M'],
                     ['X','A','X'],
                     ['S','X','M']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()

        self.assertEqual(count_mas, 1)

        graph = Graph(3, 3)
        test_data = [['S','X','S'],
                     ['X','A','X'],
                     ['M','X','M']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()

        self.assertEqual(count_mas, 1)

        graph = Graph(6, 4)
        test_data = [['M', 'X', 'M', 'X'],
                     ['X', 'A', 'X', 'A'],
                     ['S', 'X', 'S', 'X'],
                     ['X', 'M', 'X', 'M'],
                     ['X', 'X', 'A', 'X'],
                     ['X', 'S', 'X', 'S']]
        
        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()

        self.assertEqual(count_mas, 2)

    def test_xmas_cross_wrong(self):
        graph = Graph(3, 3)
        test_data = [['M','X','M'],
                     ['X','A','X'],
                     ['M','X','M']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()

        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['M','X','M'],
                     ['X','A','X'],
                     ['S','X','M']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['M','X','M'],
                     ['X','A','X'],
                     ['M','X','S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['M','X','S'],
                     ['X','A','X'],
                     ['M','X','M']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['S','X','M'],
                     ['X','A','X'],
                     ['M','X','M']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['S','X','S'],
                     ['X','A','X'],
                     ['S','X','S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['M','X','S'],
                     ['X','A','X'],
                     ['S','X','S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['S','X','M'],
                     ['X','A','X'],
                     ['S','X','S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['S','X','S'],
                     ['X','A','X'],
                     ['S','X','M']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 3)
        test_data = [['S','X','S'],
                     ['X','A','X'],
                     ['M','X','S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(3, 1)
        test_data = [['M'],
                     ['A'],
                     ['S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

        graph = Graph(1, 3)
        test_data = [['M', 'A', 'S']]

        graph.generate_graph(test_data)
        count_xmas, count_mas = graph.check_adjacencies()
        
        self.assertEqual(count_mas, 0)

if __name__ == "__main__":
    unittest.main()
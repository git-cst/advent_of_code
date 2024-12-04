import unittest
from day2 import safe

class TestAssumptions(unittest.TestCase):
    def test_breadth_of_changes_greater_than_0_less_than_3_ASC_and_DESC(self):
        asc_matrix = [1, 2, 3, 4, 5, 7]
        complies_with_logic = safe(asc_matrix)

        self.assertEqual(complies_with_logic, True)

        desc_matrix = [7, 5, 4, 3, 2, 1]
        complies_with_logic = safe(desc_matrix)

        self.assertEqual(complies_with_logic, True)

    def test_asc_to_desc(self):
        matrix = [1, 2, 3, 2, 5, 7]
        complies_with_logic = safe(matrix)
        
        self.assertNotEqual(complies_with_logic, True)

    def test_desc_to_asc(self):
        matrix = [7, 5, 7, 3, 2, 1]
        complies_with_logic = safe(matrix)
        
        self.assertNotEqual(complies_with_logic, True)

    def test_breadth_of_changes_equal_to_0(self):
        matrix = [1, 2, 3, 3, 4, 5, 7]
        complies_with_logic = safe(matrix)
        
        self.assertNotEqual(complies_with_logic, True)

    def test_breadth_of_changes_greater_than_3_ASC_and_DESC(self):
        matrix = [1, 2, 3, 4, 5, 8, 15]
        complies_with_logic = safe(matrix)

        self.assertNotEqual(complies_with_logic, True)

        desc_matrix = [15, 13, 10, 4, 2, 1]
        complies_with_logic = safe(desc_matrix)

        self.assertNotEqual(complies_with_logic, True)

if __name__ == "__main__":
    unittest.main()
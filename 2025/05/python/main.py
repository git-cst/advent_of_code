from pathlib import Path
import sys
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution

class IngredientRange:
    def __init__(self, lbound: int, ubound: int):
        self.lbound: int = lbound
        self.ubound: int = ubound

    def update_range(self, lbound: int, ubound: int) -> bool:
        lbound_lte_lbound = lbound <= self.lbound
        ubound_gte_ubound = ubound >= self.ubound

        if lbound_lte_lbound and ubound_gte_ubound:
            self.lbound = lbound
            self.ubound = ubound
            return True
        
        ubound_lte_ubound = ubound <= self.ubound
        ubound_gte_lbound = ubound >= self.lbound

        if lbound_lte_lbound and ubound_lte_ubound and ubound_gte_lbound:
            self.lbound = lbound
            return True
        
        lbound_gte_lbound = lbound >= self.lbound
        lbound_lte_ubound = lbound <= self.ubound
        
        if ubound_gte_ubound and lbound_gte_lbound and lbound_lte_ubound:
            self.ubound = ubound
            return True
        
        if lbound_gte_lbound and ubound_lte_ubound:
            return True # Don't create a new one just skip
        
        return False
    
    def check_if_in_range(self, ingredient_id: int) -> bool:
        return ingredient_id >= self.lbound and ingredient_id <= self.ubound
    
    def possible_fresh_ingredients_in_range(self) -> int:
        return self.ubound - self.lbound + 1

@time_execution
def solve_part_1(ingredient_ranges: list[str], available_ingredients: list[str]) -> int:
    spoiled_ingredients = 0

    ingredient_ranges = sorted(ingredient_ranges, key=lambda x: int(x.split("-")[0]))
    possible_ranges: list[IngredientRange] = []
    for ingredient_range in ingredient_ranges:
        lbound, ubound = ingredient_range.split("-")
        updated = False
        for possible_range in possible_ranges:
            updated = possible_range.update_range(int(lbound), int(ubound))
            if updated:
                break

        if not updated:
            possible_ranges.append(IngredientRange(int(lbound), int(ubound)))

    for ingredient_id in available_ingredients:
        for possible_range in possible_ranges:
            if possible_range.check_if_in_range(int(ingredient_id)):
                spoiled_ingredients += 1
                break

    return spoiled_ingredients

@time_execution
def solve_part_2(ingredient_ranges: list[str]) -> int:
    ingredient_ranges = sorted(ingredient_ranges, key=lambda x: int(x.split("-")[0]))
    possible_ranges: list[IngredientRange] = []
    for ingredient_range in ingredient_ranges:
        lbound, ubound = ingredient_range.split("-")
        updated = False
        for possible_range in possible_ranges:
            updated = possible_range.update_range(int(lbound), int(ubound))
            if updated:
                break

        if not updated:
            possible_ranges.append(IngredientRange(int(lbound), int(ubound)))

    possible_fresh_ingredients = 0
    for ingredient_range in possible_ranges:
        possible_fresh_ingredients += ingredient_range.possible_fresh_ingredients_in_range()

    return possible_fresh_ingredients

if __name__ == '__main__':
    ingredient_range_data_path = Path(__file__).parent.parent / 'data_ingredient_ranges.csv'
    available_ingredient_data_path = Path(__file__).parent.parent / 'data_available_ingredients.csv'

    ingredient_ranges = get_data(ingredient_range_data_path).splitlines()
    available_ingredients = get_data(available_ingredient_data_path).splitlines()

    print(solve_part_1(ingredient_ranges, available_ingredients))
    print(solve_part_2(ingredient_ranges))
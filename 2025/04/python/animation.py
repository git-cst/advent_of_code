from tkinter import Tk, BOTH, Canvas
import sys
import os
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from helper_functions.import_data import get_data
from helper_functions.time_execution import time_execution
from main import Warehouse

class Window():
    def __init__(self, window_size: tuple[int, int]):
        self.__root_widget = Tk()
        self.__root_widget.title("Warehouse Visualization")
        self.__root_widget.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas_widget = Canvas(
            master=self.__root_widget, 
            bg="gray8", 
            width=window_size[0], 
            height=window_size[1]
        )
        self.__canvas_widget.pack(fill=BOTH, expand=1)

        self.__running = False
        self.canvas_width = window_size[0]
        self.canvas_height = window_size[1]

    def draw_cell(self, row: int, col: int, cell_size: float, colour: str) -> None:
        """Draw a filled circle for a grid cell"""
        # Calculate center point of the cell
        center_x = col * cell_size + cell_size / 2
        center_y = row * cell_size + cell_size / 2
        
        # Define radius (slightly smaller than cell to avoid overlap)
        radius = cell_size * 0.4  # Adjust this factor (0.3-0.45 works well)
        
        # Create oval (circle) using bounding box
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius
        
        self.__canvas_widget.create_oval(x1, y1, x2, y2, fill=colour, outline="")

    def clear_canvas(self) -> None:
        self.__canvas_widget.delete("all")

    def redraw(self) -> None:
        self.__root_widget.update_idletasks()
        self.__root_widget.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self) -> None:
        self.__running = False

if __name__ == '__main__':
    win = Window((800, 800))
    
    input_data_path = Path(__file__).parent.parent / 'data.csv'
    warehouse_layout = get_data(input_data_path).splitlines()

    wh = Warehouse()
    wh.generate_grid(warehouse_layout)
    wh.count_valid_adjacencies()
    
    num_rows = wh._num_rows
    num_cols = wh._num_cols
    cell_size = min(win.canvas_width / num_cols, win.canvas_height / num_rows)
    
    win.redraw()

    i = 0
    for (row, col), _ in wh._active_cells.items():          
        win.draw_cell(row, col, cell_size, "grey")
        if i % 10 == 0:
            win.redraw()
        i += 1

    while wh.num_valid_paper_rolls > 0:
        i = 0
        cells_to_animate = set(wh._valid_paper_rolls.items())
        for (row, col), _ in cells_to_animate:
            win.draw_cell(row, col, cell_size, "orange")
            time.sleep(0.001)
            if i % 10 == 0:
                win.redraw()
            i += 1

        win.redraw()
        
        i = 0
        cells_to_animate = set(wh._valid_paper_rolls.items())
        for (row, col), _ in cells_to_animate:
            win.draw_cell(row, col, cell_size, "grey8")
            time.sleep(0.001)
            if i % 10 == 0:
                win.redraw()
            i += 1
        
        win.redraw()
        
        wh.remove_valid_paper_rolls()
        wh.count_valid_adjacencies()

    win.wait_for_close()



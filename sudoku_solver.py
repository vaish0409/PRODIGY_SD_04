import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        # Create a 9x9 grid of Entry widgets
        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(root, width=2, font=("Arial", 18), justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Create buttons for Solve and Clear actions
        solve_button = tk.Button(root, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, column=0, columnspan=4, padx=5, pady=5)

        clear_button = tk.Button(root, text="Clear", command=self.clear_grid)
        clear_button.grid(row=9, column=5, columnspan=4, padx=5, pady=5)

    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)

    def get_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                if value == "":
                    row.append(0)
                else:
                    row.append(int(value))
            grid.append(row)
        return grid

    def set_grid(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(grid[i][j]))

    def solve_sudoku(self):
        grid = self.get_grid()
        if self.solve(grid):
            self.set_grid(grid)
        else:
            messagebox.showerror("Error", "Sudoku puzzle is unsolvable.")

    def solve(self, grid):
        empty = self.find_empty_location(grid)
        if not empty:
            return True  # Puzzle solved

        row, col = empty
        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num

                if self.solve(grid):
                    return True

                grid[row][col] = 0  # Backtrack

        return False

    def find_empty_location(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, grid, row, col, num):
        return self.is_row_safe(grid, row, num) and \
               self.is_col_safe(grid, col, num) and \
               self.is_box_safe(grid, row - row % 3, col - col % 3, num)

    def is_row_safe(self, grid, row, num):
        return num not in grid[row]

    def is_col_safe(self, grid, col, num):
        return num not in [grid[i][col] for i in range(9)]

    def is_box_safe(self, grid, box_start_row, box_start_col, num):
        for i in range(3):
            for j in range(3):
                if grid[i + box_start_row][j + box_start_col] == num:
                    return False
        return True

# Create the main window and start the Sudoku Solver
root = tk.Tk()
app = SudokuSolver(root)
root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from dataclasses import dataclass


@dataclass
class Item:
    value: int
    weight: int
    
    @property
    def ratio(self) -> float:
        return self.value / self.weight if self.weight != 0 else 0


class IntegerKnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Integer Knapsack Solver")
        self.root.geometry("800x600")
        
        self.items: List[Item] = []
        
        self.create_input_frame()
        self.create_items_frame()
        self.create_solution_frame()
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Add New Item", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        # Weight input
        ttk.Label(input_frame, text="Weight (integer):").grid(row=0, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var)
        self.weight_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Value input
        ttk.Label(input_frame, text="Value (integer):").grid(row=0, column=2, padx=5, pady=5)
        self.value_var = tk.StringVar()
        self.value_entry = ttk.Entry(input_frame, textvariable=self.value_var)
        self.value_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Add item button
        self.add_button = ttk.Button(input_frame, text="Add Item", command=self.add_item)
        self.add_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Clear all button
        self.clear_button = ttk.Button(input_frame, text="Clear All", command=self.clear_all)
        self.clear_button.grid(row=0, column=5, padx=5, pady=5)
        
        # Capacity input
        ttk.Label(input_frame, text="Knapsack Capacity (integer):").grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.capacity_var = tk.StringVar()
        self.capacity_entry = ttk.Entry(input_frame, textvariable=self.capacity_var)
        self.capacity_entry.grid(row=1, column=2, padx=5, pady=5)
        
        # Solve button
        self.solve_button = ttk.Button(input_frame, text="Solve Knapsack", command=self.solve_knapsack)
        self.solve_button.grid(row=1, column=3, columnspan=2, padx=5, pady=5)
        
    def create_items_frame(self):
        items_frame = ttk.LabelFrame(self.root, text="Items List", padding="10")
        items_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.tree = ttk.Treeview(items_frame, columns=("Index", "Weight", "Value", "Ratio"), show="headings")
        self.tree.heading("Index", text="Index")
        self.tree.heading("Weight", text="Weight")
        self.tree.heading("Value", text="Value")
        self.tree.heading("Ratio", text="Value/Weight Ratio")
        
        self.tree.column("Index", width=50)
        self.tree.column("Weight", width=100)
        self.tree.column("Value", width=100)
        self.tree.column("Ratio", width=150)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
    def create_solution_frame(self):
        solution_frame = ttk.LabelFrame(self.root, text="Solution", padding="10")
        solution_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.solution_text = tk.Text(solution_frame, height=10, wrap="word")
        self.solution_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(solution_frame, orient=tk.VERTICAL, command=self.solution_text.yview)
        self.solution_text.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
    def add_item(self):
        try:
            weight = int(self.weight_var.get())
            value = int(self.value_var.get())
            if weight <= 0 or value <= 0:
                raise ValueError("Weight and Value must be positive integers.")
            self.items.append(Item(value=value, weight=weight))
            self.update_items_list()
            self.weight_var.set("")
            self.value_var.set("")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
    
    def clear_all(self):
        self.items.clear()
        self.update_items_list()
        self.solution_text.delete("1.0", tk.END)
    
    def update_items_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for index, item in enumerate(self.items):
            self.tree.insert("", "end", values=(index + 1, item.weight, item.value, f"{item.ratio:.2f}"))
    
    def solve_knapsack(self):
        try:
            capacity = int(self.capacity_var.get())
            if capacity <= 0:
                raise ValueError("Capacity must be a positive integer.")
            
            n = len(self.items)
            W = capacity
            dp = [[0] * (W + 1) for _ in range(n + 1)]
            
            for i in range(1, n + 1):
                for w in range(W + 1):
                    if self.items[i - 1].weight <= w:
                        dp[i][w] = max(dp[i - 1][w],
                                       dp[i - 1][w - self.items[i - 1].weight] + self.items[i - 1].value)
                    else:
                        dp[i][w] = dp[i - 1][w]
            
            selected_items = []
            w = W
            for i in range(n, 0, -1):
                if dp[i][w] != dp[i - 1][w]:
                    selected_items.append(self.items[i - 1])
                    w -= self.items[i - 1].weight
            
            solution = f"Maximum value achievable: {dp[n][W]}\n\nSelected Items:\n"
            for item in selected_items:
                solution += f"Weight: {item.weight}, Value: {item.value}, Ratio: {item.ratio:.2f}\n"
            
            self.solution_text.delete("1.0", tk.END)
            self.solution_text.insert(tk.END, solution)
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = IntegerKnapsackGUI(root)
    root.mainloop()

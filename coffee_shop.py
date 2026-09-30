import tkinter as tk
from tkinter import ttk, messagebox

class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class CoffeeOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Ordering App")
        self.root.geometry("600x500")
        self.root.configure(bg="#8B4513")
        
        # Coffee menu
        self.menu = [
            Coffee("Espresso", 2.50),
            Coffee("Latte", 3.50),
            Coffee("Cappuccino", 3.00),
            Coffee("Americano", 2.00),
            Coffee("Mocha", 4.00),
            Coffee("Macchiato", 3.25),
            Coffee("Frappuccino", 4.50),
            Coffee("Black Coffee", 1.50)
        ]
        
        self.order_items = []
        self.total_price = 0.0
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="☕ Coffee Shop ☕", 
                              font=("Arial", 24, "bold"), 
                              fg="white", bg="#8B4513")
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#8B4513")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left frame for menu
        left_frame = tk.Frame(main_frame, bg="#D2691E", relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        menu_label = tk.Label(left_frame, text="Menu", 
                             font=("Arial", 16, "bold"), 
                             fg="white", bg="#D2691E")
        menu_label.pack(pady=10)
        
        # Coffee selection frame
        coffee_frame = tk.Frame(left_frame, bg="#D2691E")
        coffee_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create coffee buttons
        for i, coffee in enumerate(self.menu):
            row = i // 2
            col = i % 2
            
            coffee_btn = tk.Button(coffee_frame, 
                                 text=f"{coffee.name}\n${coffee.price:.2f}",
                                 font=("Arial", 10, "bold"),
                                 bg="#F4A460",
                                 fg="black",
                                 width=15,
                                 height=3,
                                 command=lambda c=coffee: self.add_to_order(c))
            coffee_btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Right frame for order
        right_frame = tk.Frame(main_frame, bg="#DEB887", relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        order_label = tk.Label(right_frame, text="Your Order", 
                              font=("Arial", 16, "bold"), 
                              fg="black", bg="#DEB887")
        order_label.pack(pady=10)
        
        # Order listbox with scrollbar
        listbox_frame = tk.Frame(right_frame, bg="#DEB887")
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.order_listbox = tk.Listbox(listbox_frame, 
                                       font=("Arial", 10),
                                       bg="white",
                                       selectmode=tk.SINGLE)
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        
        self.order_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.order_listbox.yview)
        
        self.order_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Total price label
        self.total_label = tk.Label(right_frame, text="Total: $0.00", 
                                   font=("Arial", 14, "bold"), 
                                   fg="red", bg="#DEB887")
        self.total_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(right_frame, bg="#DEB887")
        button_frame.pack(pady=10)
        
        # Remove item button
        remove_btn = tk.Button(button_frame, text="Remove Selected", 
                              font=("Arial", 10, "bold"),
                              bg="#CD853F", fg="white",
                              command=self.remove_from_order)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear order button
        clear_btn = tk.Button(button_frame, text="Clear Order", 
                             font=("Arial", 10, "bold"),
                             bg="#A0522D", fg="white",
                             command=self.clear_order)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Checkout button
        checkout_btn = tk.Button(right_frame, text="🛒 Checkout", 
                                font=("Arial", 12, "bold"),
                                bg="#228B22", fg="white",
                                width=20, height=2,
                                command=self.checkout)
        checkout_btn.pack(pady=10)
    
    def add_to_order(self, coffee):
        self.order_items.append(coffee)
        self.update_order_display()
        
    def remove_from_order(self):
        selected_index = self.order_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.order_items.pop(index)
            self.update_order_display()
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
    
    def clear_order(self):
        if self.order_items:
            result = messagebox.askyesno("Clear Order", "Are you sure you want to clear your order?")
            if result:
                self.order_items.clear()
                self.update_order_display()
        else:
            messagebox.showinfo("Empty Order", "Your order is already empty.")
    
    def update_order_display(self):
        self.order_listbox.delete(0, tk.END)
        self.total_price = 0.0
        
        item_count = {}
        for item in self.order_items:
            if item.name in item_count:
                item_count[item.name] += 1
            else:
                item_count[item.name] = 1
        
        for coffee_name, count in item_count.items():
            coffee = next(c for c in self.menu if c.name == coffee_name)
            item_total = coffee.price * count
            self.total_price += item_total
            
            display_text = f"{count}x {coffee_name} - ${item_total:.2f}"
            self.order_listbox.insert(tk.END, display_text)
        
        self.total_label.config(text=f"Total: ${self.total_price:.2f}")
    
    def checkout(self):
        if not self.order_items:
            messagebox.showwarning("Empty Order", "Please add items to your order before checkout.")
            return
        
        # Create checkout summary
        summary = "Order Summary:\n\n"
        item_count = {}
        for item in self.order_items:
            if item.name in item_count:
                item_count[item.name] += 1
            else:
                item_count[item.name] = 1
        
        for coffee_name, count in item_count.items():
            coffee = next(c for c in self.menu if c.name == coffee_name)
            item_total = coffee.price * count
            summary += f"{count}x {coffee_name} - ${item_total:.2f}\n"
        
        summary += f"\nTotal: ${self.total_price:.2f}"
        
        result = messagebox.askyesno("Checkout", f"{summary}\n\nProceed with payment?")
        
        if result:
            messagebox.showinfo("Order Confirmed", 
                               "Thank you for your order!\n"
                               "Your coffee will be ready in 5-10 minutes.")
            self.order_items.clear()
            self.update_order_display()

def main():
    root = tk.Tk()
    app = CoffeeOrderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

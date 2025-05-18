import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import os

# Load stock data
stock_data = pd.read_excel("stock.xlsx", index_col=[0, 1, 2])
catalog = {}
for (category, item, attr), value in stock_data.itertuples():
    catalog.setdefault(category, {}).setdefault(item, {})[attr] = value

order = {}

def get_discount(cost): return cost * 0.1 if cost > 500 else 0

class FreshMartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FreshMart App")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")

        self.create_header()
        self.create_catalog()

    def create_header(self):
        header = tk.Frame(self.root, bg="#2424A0", height=60)
        header.pack(fill="x")

        tk.Label(header, text="🛒 FreshMart", font=("Arial", 20, "bold"), bg="#232f3e", fg="white").pack(side="left", padx=20)
        tk.Button(header, text="View Cart", command=self.show_cart, bg="#febd69", fg="black").pack(side="right", padx=20)

    def create_catalog(self):
        cat_frame = tk.Frame(self.root, bg="#f5f5f5")
        cat_frame.pack(pady=50)

        tk.Label(cat_frame, text="Choose a Category", font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=10)

        tk.Button(cat_frame, text=" Browse Fruits", font=("Arial", 14), width=20,
                  bg="#ff6f61", fg="white", command=lambda: self.open_category("fruits")).pack(pady=10)

        tk.Button(cat_frame, text=" Browse Vegetables", font=("Arial", 14), width=20,
                  bg="#81c784", fg="white", command=lambda: self.open_category("vegetables")).pack(pady=10)

    def open_category(self, category_name):
        win = tk.Toplevel(self.root)
        win.title(f"{category_name.capitalize()} Catalog")
        win.geometry("700x600")
        win.configure(bg="blue")

        tk.Label(win, text=f"{category_name.capitalize()} ", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        wrapper = tk.Frame(win, bg="#f0f0f0")
        wrapper.pack(fill="both", expand=True)

        canvas = tk.Canvas(wrapper, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        cat_frame = tk.Frame(canvas, bg="#f0f0f0")

        cat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=cat_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        row, col = 0, 0
        for item, details in catalog.get(category_name, {}).items():
            self.create_product_card_in_frame(item, details, cat_frame, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def create_product_card_in_frame(self, item, details, frame, row, col):
        card = tk.Frame(frame, bg="white", width=260, height=300, bd=1, relief="solid")
        card.grid(row=row, column=col, padx=20, pady=20)

        img_path = f"images/{item.lower()}.jpg"
        if os.path.exists(img_path):
            img = Image.open(img_path).resize((120, 120))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(card, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(pady=10)
        else:
            tk.Label(card, text="[Image]", bg="white").pack()

        tk.Label(card, text=item, font=("Arial", 12, "bold"), bg="white").pack()
        tk.Label(card, text=f"₹{details['price']} per {details['unit']}", bg="white", fg="green").pack()
        stock_text = f"Stock: {details['stock']}"
        color = "red" if details['stock'] < 10 else "gray"
        tk.Label(card, text=stock_text, bg="white", fg=color).pack()

        qty_var = tk.StringVar()
        tk.Entry(card, textvariable=qty_var, width=5).pack(pady=5)

        def add():
            try:
                qty = float(qty_var.get())
                if qty > details['stock']:
                    messagebox.showwarning("Stock Error", "Insufficient stock.")
                    return
                cost = details['price'] * qty
                if item in order:
                    order[item]["quantity"] += qty
                    order[item]["cost"] += cost
                else:
                    order[item] = {"quantity": qty, "unit": details['unit'], "cost": cost}
                messagebox.showinfo("Added", f"{item} added to cart.")
            except:
                messagebox.showerror("Input Error", "Enter a valid quantity.")

        tk.Button(card, text="Add to Cart", command=add, bg="#ff9900", fg="black").pack(pady=5)

    def populate_catalog(self):
        row = 0
        col = 0
        for category in catalog:
            for item, details in catalog[category].items():
                self.create_product_card(item, details, row, col)
                col += 1
                if col >= 4:
                    col = 0
                    row += 1

    def create_product_card(self, item, details, row, col):
        frame = tk.Frame(self.catalog_frame, bg="white", width=280, height=300, bd=1, relief="solid")
        frame.grid(row=row, column=col, padx=20, pady=20)

        image_path = f"images/{item.lower()}.png"
        if os.path.exists(image_path):
            img = Image.open(image_path).resize((120, 120))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(pady=10)
        else:
            tk.Label(frame, text="[Image]", bg="white").pack()

        tk.Label(frame, text=item, font=("Arial", 12, "bold"), bg="white").pack()
        tk.Label(frame, text=f"₹{details['price']} per {details['unit']}", bg="white", fg="green").pack()

        qty_var = tk.StringVar()
        qty_entry = tk.Entry(frame, textvariable=qty_var, width=5)
        qty_entry.pack(pady=5)

        def add():
            try:
                qty = float(qty_var.get())
                if qty > details['stock']:
                    messagebox.showwarning("Stock Error", "Insufficient stock.")
                    return
                cost = details['price'] * qty
                order[item] = {
                    "quantity": qty,
                    "unit": details['unit'],
                    "cost": cost
                }
                messagebox.showinfo("Added", f"{item} added to cart.")
            except:
                messagebox.showerror("Input Error", "Enter a valid quantity.")

        tk.Button(frame, text="Add to Cart", command=add, bg="#ff9900", fg="black").pack(pady=5)

    def show_cart(self):
        win = tk.Toplevel(self.root)
        win.title("Your Cart")
        win.geometry("500x600")
        win.configure(bg="white")

        tk.Label(win, text="🛒 Your Cart", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        if not order:
            tk.Label(win, text="Cart is empty!", bg="white").pack(pady=20)
            return

        total = 0
        for item, details in order.items():
            line = f"{item} - {details['quantity']} {details['unit']} - ₹{details['cost']:.2f}"
            tk.Label(win, text=line, bg="white").pack(anchor="w", padx=20, pady=5)
            total += details["cost"]

        discount = get_discount(total)
        payable = total - discount

        summary = f"\nTotal: ₹{total:.2f}\nDiscount: ₹{discount:.2f}\nAmount Payable: ₹{payable:.2f}"
        tk.Label(win, text=summary, font=("Arial", 12, "bold"), fg="green", bg="white").pack(pady=20)

        tk.Button(win, text="Enter Delivery Address", command=self.address_popup, bg="#ffa500", fg="white").pack(pady=5)
        tk.Button(win, text="Submit Feedback", command=self.feedback_popup, bg="#6a1b9a", fg="white").pack(pady=5)

    def address_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Delivery Address")
        win.geometry("400x300")
        tk.Label(win, text="Enter your address:", font=("Arial", 14)).pack(pady=10)
        text = tk.Text(win, height=6, width=40)
        text.pack(pady=10)
        tk.Button(
            win,
            text="Confirm",
            command=lambda: [
                self.reduce_stock(),
                messagebox.showinfo("Confirmed", "Thanks! Your order will be delivered."),
                win.destroy(),
                order.clear()
            ],
            bg="green",
            fg="white"
        ).pack()

    def feedback_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Feedback")
        win.geometry("400x250")
        tk.Label(win, text="Rate your experience:", font=("Arial", 14)).pack(pady=10)
        text = tk.Text(win, height=6, width=40)
        text.pack(pady=10)
        tk.Button(win, text="Submit", command=lambda: [messagebox.showinfo("Thanks", "Feedback submitted!"), win.destroy()], bg="blue", fg="white").pack()

    def reduce_stock(self):
        for item, details in order.items():
            for (category, item_name, attr), value in stock_data.itertuples():
                if item_name == item and attr == "stock":
                    new_value = value - details["quantity"]
                    stock_data.loc[(category, item_name, "stock"), :] = new_value

        stock_data.to_excel("stock.xlsx")
        messagebox.showinfo("Stock Updated", "Inventory has been updated in stock.xlsx")

# Run the app
root = tk.Tk()
app = FreshMartApp(root)
root.mainloop()

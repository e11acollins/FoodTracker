from tkinter import *
import sqlite3
from datetime import datetime


class FoodDatabase:
    # This initializes the database and creates the table
    def __init__(self, db_name="food_tracker.db"):
        self.con = sqlite3.connect(db_name)
        self.cursor = self.con.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food TEXT NOT NULL,
                expiry_date TEXT NOT NULL
            )
        """)
        self.con.commit()
        

    def add_food(self, food, expiry_date):
        self.cursor.execute(
            "INSERT INTO foods (food, expiry_date) VALUES (?, ?)",
            (food, expiry_date)
        )
        self.con.commit()

    # This retrieves all food entries from the database
    def get_all_foods(self):
        self.cursor.execute("SELECT food, expiry_date FROM foods")
        return self.cursor.fetchall()

    def close(self):
        self.con.close()


class FoodCategorizer:
    def __init__(self, food_entries):
        self.food_entries = food_entries  # list of (food, expiry_date) tuples

    def categorize(self):
        today = datetime.today()
        expired = []
        expiring_today = []
        expiring_soon = []
        others = []

        # This categorizes the food based on expiration dates
        for food, expiry in self.food_entries:
            try:
                expiry_date = datetime.strptime(expiry, "%d/%m/%y")
                days_left = (expiry_date.date() - today.date()).days
                if days_left < 0:
                    expired.append((food, expiry, abs(days_left)))
                elif days_left == 0:
                    expiring_today.append((food, expiry))
                elif 1 <= days_left <= 3:
                    expiring_soon.append((food, expiry, days_left))
                elif days_left > 3:
                    others.append((food, expiry, days_left))
            except ValueError:
                continue
        return expired, expiring_today, expiring_soon, others


class App_EnterFood:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Tracker")
        self.db = FoodDatabase()  # Use the database class
        self.food_data = []  # Add this line to define food_data

        # Widgets made before packing
        self.open_label = Label(root, text="Please enter your food details below.")
        self.food = Label(root, text="Food:")
        self.expiry_date = Label(root, text="Expiry Date (DD/MM/YY):")
        self.food_entry = Entry(root)
        self.date_entry = Entry(root)
        self.correct_label = Label(root, text="Is this correct?")
        self.result_label = Label(root, text="")
        self.btn_yes = Button(root, text="Yes", command=self.on_yes)
        self.btn_no = Button(root, text="No", command=self.on_no)
        self.enter_button = Button(root, text="Enter", command=self.on_enter)
        self.food_summary = Button(root, text="Show Food Summary", command=self.on_second_no)
        self.ask_again_label = Label(root, text="Please enter your food details again.")
        self.more_food_label = Label(root, text="Do you have more food to enter? Yes/No")
        self.btn_second_yes = Button(root, text="Yes", command=self.on_second_yes)
        self.btn_second_no = Button(root, text="No", command=self.on_second_no)

        # Start the entry loop
        self.show_entry_form()

    # This creates the loop to enter food data
    def show_entry_form(self):
        for widget in [self.ask_again_label, self.more_food_label, self.btn_second_yes, self.btn_second_no,
                       self.open_label, self.food, self.food_entry, self.expiry_date, self.date_entry, self.enter_button]:
            widget.pack_forget()
        self.open_label.pack()
        self.food.pack()
        self.food_entry.pack()
        self.expiry_date.pack()
        self.date_entry.pack()
        self.enter_button.pack()
        self.food_summary.pack()


    # This is what happens when you press enter
    def on_enter(self):
        # This stores the food data
        food = self.food_entry.get()
        date = self.date_entry.get()
        self.food_data.append({"food": food, "expiry_date": date})
        # Store the data in SQLite using the database class
        self.db.add_food(food, date)
        self.result_label.config(text=f"Food entered: {food}\nExpiry date: {date}")
        # This is asking if the data is correct
        self.correct_label.pack()
        self.result_label.pack()
        self.btn_yes.pack()
        self.btn_no.pack()
 

    # This is what happens when you press no, data is incorrect
    def on_no(self):
        self.food_entry.delete(0, END)
        self.date_entry.delete(0, END)
        # Hide widgets 
        self.correct_label.pack_forget()
        self.result_label.pack_forget()
        self.btn_yes.pack_forget()
        self.btn_no.pack_forget()
        self.more_food_label.pack_forget()
        self.ask_again_label.pack()

    # This is what happens when you press yes, data is correct
    def on_yes(self):
        # Hide all widgets and clear Entry fields
        for widget in self.root.pack_slaves():
            widget.pack_forget()
            if isinstance(widget, Entry):
                widget.delete(0, END)
        # This asks if there is more food to enter
        self.more_food_label.pack()
        self.btn_second_yes.pack()
        self.btn_second_no.pack()
        self.root.update_idletasks()  # This ensures the UI updates immediately (otherwise it lags)
   

    # This is what happens when you press yes to more food (restarts the loop)
    def on_second_yes(self):
        self.show_entry_form()

    # This is what happens when you press no to more food
    def on_second_no(self):
        # Instead of closing, open the summary window
        self.root.destroy()  # Close current window
        summary_root = Tk()
        App_FoodSummary(summary_root)
        summary_root.geometry("400x400")
        summary_root.mainloop()


# This is the summary window that appears after finishing food entry
class App_FoodSummary:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Summary")

        # Load and categorize food data
        db = FoodDatabase()
        foods = db.get_all_foods()
        db.close()
        categorizer = FoodCategorizer(foods)
        expired, exp_today, exp_soon, others = categorizer.categorize()

        # Save categories as attributes
        self.expired = expired
        self.exp_today = exp_today
        self.exp_soon = exp_soon
        self.others = others        

        # Display categorized food summary
        summary_text = "Expired Foods:\n"
        for food, expiry, days in expired:
            summary_text += f"- {food} (Expired {days} days ago)\n"

        summary_text += "\nExpiring Today:\n"
        for food, expiry in exp_today:
            summary_text += f"- {food} (Expires today)\n"

        summary_text += "\nExpiring Soon:\n"
        for food, expiry, days in exp_soon:
            summary_text += f"- {food} (Expires in {days} days)\n"

        summary_text += "\nOther Foods:\n"
        for food, expiry, days in others:
            summary_text += f"- {food} (Expires in {days} days)\n"

        self.summary_label = Label(root, text=summary_text, justify=LEFT)
        self.summary_label.pack()

        # Buttons to exit, enter more food or remove items
        self.exit_button = Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack()
        self.enter_more_button = Button(root, text="Enter More Food", command=self.enter_more_food)
        self.enter_more_button.pack()
        self.remove_items_button = Button(root, text="Remove Food Items", command=self.remove_items)
        self.remove_items_button.pack()
        self.clear_all_button = Button(root, text="Clear All Items", command=self.clear_all_items)

   
    def remove_items(self):
        # Open the remove items window without destroying the summary window
        remove_root = Toplevel(self.root)
        App_RemoveFood(remove_root, self.expired, self.exp_today, self.exp_soon, self.others)
        remove_root.geometry("400x400")


    def refresh_summary(self):
        # Reload and categorize food data
        db = FoodDatabase()
        foods = db.get_all_foods()
        db.close()
        categorizer = FoodCategorizer(foods)
        expired, exp_today, exp_soon, others = categorizer.categorize()

        # Update attributes
        self.expired = expired
        self.exp_today = exp_today
        self.exp_soon = exp_soon
        self.others = others

        # Rebuild summary text
        summary_text = "Expired Foods:\n"
        for food, expiry, days in expired:
            summary_text += f"- {food} (Expired {days} days ago)\n"

        summary_text += "\nExpiring Today:\n"
        for food, expiry in exp_today:
           summary_text += f"- {food} (Expires today)\n"

        summary_text += "\nExpiring Soon:\n"
        for food, expiry, days in exp_soon:
           summary_text += f"- {food} (Expires in {days} days)\n"

        summary_text += "\nOther Foods:\n"
        for food, expiry, days in others:
           summary_text += f"- {food} (Expires in {days} days)\n"

        # Update label on the summary window
        self.summary_label.config(text=summary_text)
        self.root.update_idletasks()


    def remove_items(self):
        remove_root = Toplevel(self.root)
        App_RemoveFood(
            remove_root,
            self.expired, self.exp_today, self.exp_soon, self.others,
            refresh_callback=self.refresh_summary
        )
        remove_root.geometry("400x400")


    def clear_all_items(self):
        db = FoodDatabase()
        db.cursor.execute("DELETE FROM foods")
        db.con.commit()
        db.close()
        # Optionally update UI here

    def enter_more_food(self):
        self.root.destroy()
        new_root = Tk()
        app = App_EnterFood(new_root)
        new_root.geometry("400x300")
        new_root.mainloop()

    def exit_app(self):
        self.root.destroy()


class App_RemoveFood:
    def __init__(self, root, expired, exp_today, exp_soon, others, refresh_callback=None):
        self.root = root
        self.root.title("Remove Food Items")
        self.refresh_callback = refresh_callback

        # Flatten all items into a single list
        self.all_items = []
        for food, expiry, days in expired:
            self.all_items.append((food, expiry))
        for food, expiry in exp_today:
            self.all_items.append((food, expiry))
        for food, expiry, days in exp_soon:
            self.all_items.append((food, expiry))
        for food, expiry, days in others:
            self.all_items.append((food, expiry))

        # Listbox for selection
        self.listbox = Listbox(root, width=50)
        for item in self.all_items:
            self.listbox.insert(END, f"{item[0]} | {item[1]}")
        self.listbox.pack()

        # Button to remove selected
        self.remove_button = Button(root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack()
        self.return_button = Button(root, text="Return to Summary", command=self.root.destroy)
        self.return_button.pack()

    def remove_selected(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            item = self.all_items.pop(idx)
            db = FoodDatabase()
            db.cursor.execute("DELETE FROM foods WHERE food=? AND expiry_date=?", (item[0], item[1]))
            db.con.commit()
            db.close()
            self.listbox.delete(idx)
            # Refresh summary in parent window
            if self.refresh_callback:
              self.refresh_callback()


# Opens the window
myroot = Tk()
app = App_EnterFood(myroot)
# Sets the window size
geometry = "400x300"
myroot.geometry(geometry)


myroot.mainloop()
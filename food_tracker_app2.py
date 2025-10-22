from tkinter import *
import sqlite3
from datetime import datetime

# This is a food tracker app using Tkinter and SQLite
# It allows users to enter food items with expiration dates,
# categorizes them based on how soon they expire,
# displays a summary, and lets users remove items from the database.

# There are five classes here: FoodDatabase, FoodCategorizer, App_EnterFood, App_FoodSummary, and App_RemoveFood
# FoodDatabase handles all database operations
# FoodCategorizer categorizes food based on expiration dates
# App_EnterFood is the Tkinter app for entering food data
# App_FoodSummary displays the categorized food summary
# App_RemoveFood allows users to remove food items from the database


class FoodDatabase:
    # This initializes the database and creates a table for food and expiry dates
    # It uses SQLite for storage
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
        

    # This adds a food entry to the database
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
    # This constructs the categorizer with food entries
    def __init__(self, food_entries):
        self.food_entries = food_entries  # list of (food, expiry_date) tuples

    # This helps categorize food based on expiration dates
    def categorize(self):
        today = datetime.today()
        expired = []
        expiring_today = []
        expiring_soon = []
        others = []

        # This categorizes the food based on expiration dates
        # There are four categories: expired, expiring today, expiring soon (within 3 days), and others
        # It uses try and except to handle invalid date formats
        # It also uses if statements to sort food into the correct category
        for food, expiry in self.food_entries:
            try:
                expiry_date = datetime.strptime(expiry, "%d/%m/%y") # This matches the input format DD/MM/YY
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

    # This sorts food items by expiration date
    def sort_by_date(food_list):
        return sorted(food_list, key=lambda x: datetime.strptime(x[1], "%d/%m/%y")) 


class App_EnterFood:
    # This is the Tkinter app for entering food data
    def __init__(self, root):
        self.root = root
        self.root.title("Food Tracker")
        self.db = FoodDatabase()  # Use the database class
        self.food_data = []  # To temporarily store food data

        # All the widgets made before packing (labels, buttons, entries)
        # This makes it neater to manage the UI and pack them later
        self.open_label = Label(root, text="Please enter your food details below.")
        self.food = Label(root, text="Food:")
        self.expiry_date = Label(root, text="Expiry Date (DD/MM/YY):")
        self.food_entry = Entry(root)
        self.date_entry = Entry(root)
        self.error_label = Label(root, text="", fg="red")
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

        # This starts the entry loop
        self.show_entry_form()

    # This is the code for the loop above
    # This loop goes between the entry form and the confirmation form, 
    # letting you keep entering food data for as long as you want
    def show_entry_form(self):
        for widget in [self.ask_again_label, self.more_food_label, self.btn_second_yes, self.btn_second_no,
                       self.open_label, self.food, self.food_entry, self.expiry_date, self.date_entry, self.enter_button]:
            widget.pack_forget() # Hide all widgets first so when we repack, there are no duplicates
        self.open_label.pack()
        self.food.pack()
        self.food_entry.pack()
        self.expiry_date.pack()
        self.date_entry.pack()
        self.enter_button.pack()
        self.food_summary.pack()


    # This is what happens when you press enter to store food data
    def on_enter(self):
        # get() retrieves the text from the Entry widgets
        food = self.food_entry.get()
        date = self.date_entry.get()
        try:
            # This checks if the date format is correct
            datetime.strptime(date, "%d/%m/%y")
            self.error_label.config(text="")
            self.food_data.append({"food": food, "expiry_date": date})
            self.db.add_food(food, date)
            self.result_label.config(text=f"Food entered: {food}\nExpiry date: {date}")
            self.correct_label.pack()
            self.result_label.pack()
            self.btn_yes.pack()
            self.btn_no.pack()
        except ValueError:
            # This handles the case where the date format is incorrect
            self.error_label.config(text="Error: Please enter the expiry date as DD/MM/YY")
            self.error_label.pack()
            self.date_entry.delete(0, END)
 

    # This is what happens when you press no, data is incorrect
    def on_no(self):
        # This deletes the incorrect data
        self.food_entry.delete(0, END)
        self.date_entry.delete(0, END)
        # This hides the widgets
        self.correct_label.pack_forget()
        self.result_label.pack_forget()
        self.btn_yes.pack_forget()
        self.btn_no.pack_forget()
        self.more_food_label.pack_forget()
        # This asks to enter food details again
        self.ask_again_label.pack()


    # This is what happens when you press yes, data is correct
    def on_yes(self):
        # This hides all widgets and clears Entry fields
        for widget in self.root.pack_slaves():
            widget.pack_forget()
            # 'isinstance' checks to see if the widget is an Entry, then it clears the entry from start to finish (0-END)
            if isinstance(widget, Entry):
                widget.delete(0, END)
        # This asks if there is more food to enter
        self.more_food_label.pack()
        self.btn_second_yes.pack()
        self.btn_second_no.pack()
        self.root.update_idletasks()  # This ensures the UI updates immediately (otherwise it lags)
   

    # This is what happens when you press yes, add more food 
    # It restarts the loop from above 
    def on_second_yes(self):
        self.show_entry_form()


    # This is what happens when you press no to more food
    def on_second_no(self):
        # Hide the entry window
        self.root.withdraw()
        # Create summary window
        summary_win = Toplevel(self.root)
        summary_win.geometry("500x400")
        App_FoodSummary(summary_win)


class App_FoodSummary: 
    def __init__(self, root):
        self.root = root
        self.root.title("Food Summary")

        # This loads and categorizes food data
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

        # This displays categorized food summary
        # sort_by_date will sort food items by expiration date
        summary_text = "Expired Foods:\n"
        for food, expiry, days in FoodCategorizer.sort_by_date(expired):
            summary_text += f"- {food} (Expired {days} days ago)\n"

        summary_text += "\nExpiring Today:\n"
        for food, expiry in FoodCategorizer.sort_by_date(exp_today):
            summary_text += f"- {food} (Expires today)\n"

        summary_text += "\nExpiring Soon:\n"
        for food, expiry, days in FoodCategorizer.sort_by_date(exp_soon):
         summary_text += f"- {food} (Expires in {days} days)\n"

        summary_text += "\nOther Foods:\n"
        for food, expiry, days in FoodCategorizer.sort_by_date(others):
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


    # This takes you to the remove items window
    def remove_items(self):
        remove_root = Toplevel(self.root)
        App_RemoveFood(
            remove_root,
            self.expired, self.exp_today, self.exp_soon, self.others,
            refresh_callback=self.refresh_summary
        )
        remove_root.geometry("400x400")


    # This refreshes the summary after items are removed
    # This makes the food disappear immediately rather than having to restart the app
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

        # Rebuild summary text without the deleted items
        summary_text = "Expired Foods:\n"
        for food, expiry, days in FoodCategorizer.sort_by_date(expired):
            summary_text += f"- {food} (Expired {days} days ago)\n"

        summary_text += "\nExpiring Today:\n"
        for food, expiry in FoodCategorizer.sort_by_date(exp_today):
            summary_text += f"- {food} (Expires today)\n"

        summary_text += "\nExpiring Soon:\n"
        for food, expiry, days in FoodCategorizer.sort_by_date(exp_soon):
         summary_text += f"- {food} (Expires in {days} days)\n"

        summary_text += "\nOther Foods:\n"
        for food, expiry, days in FoodCategorizer.sort_by_date(others):
          summary_text += f"- {food} (Expires in {days} days)\n"

        # Update label on the summary window
        self.summary_label.config(text=summary_text)
        self.root.update_idletasks()

    # This takes you back to the start to enter more food
    def enter_more_food(self):
        self.root.destroy()  # Destroys summary window
        # Show the entry window again
        self.root.master.deiconify()

    # This exits the app
    def exit_app(self):
        self.root.destroy()


class App_RemoveFood:
    def __init__(self, root, expired, exp_today, exp_soon, others, refresh_callback=None):
        self.root = root
        self.root.title("Remove Food Items")
        self.root.geometry("500x400")
        self.refresh_callback = refresh_callback
        self.expired = expired

        # This puts all food items into a single list for display
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

        # Buttons for removing items
        self.remove_button = Button(root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack()
        self.remove_expired_button = Button(root, text="Remove All Expired Items", command=self.remove_expired)
        self.remove_expired_button.pack()
        self.return_button = Button(root, text="Return to Summary", command=self.root.destroy)
        self.return_button.pack()


    # This removes the selected item from the database and listbox
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


    # This removes all expired items from the database and listbox
    def remove_expired(self):
        db = FoodDatabase()
        to_remove = [item for item in self.all_items if item in [(food, expiry) for food, expiry, days in self.expired]]
        for item in to_remove:
            db.cursor.execute("DELETE FROM foods WHERE food=? AND expiry_date=?", (item[0], item[1]))
            self.all_items.remove(item)
        db.con.commit()
        db.close()
        # Refresh listbox
        self.listbox.delete(0, END)
        for item in self.all_items:
            self.listbox.insert(END, f"{item[0]} | {item[1]}")
        # Refresh summary in parent window
        if self.refresh_callback:
            self.refresh_callback()


if __name__ == "__main__":
    myroot = Tk()
    myroot.geometry("500x400")
    app = App_EnterFood(myroot)
    myroot.mainloop()
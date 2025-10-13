from tkinter import *

myroot = Tk()
myroot.title("Food Tracker")
#add geometry, title, etc. later

# This creates the initial labels and entry fields
Label(myroot, text="Please enter your food details below.").pack()

Label(myroot, text="Food:").pack()
food_entry = Entry(myroot)
food_entry.pack()

Label(myroot, text="Expiry Date (DD/MM/YY):").pack()
date_entry = Entry(myroot)
date_entry.pack()


# This creates the labels but doesn't display them yet
correct_label = Label(myroot, text="Is this correct?")
result_label = Label(myroot, text="")
btn_yes = Button(myroot, text="Yes")
btn_no = Button(myroot, text="No")


def on_enter():
    food = food_entry.get()
    date = date_entry.get()

    # Show what was entered
    result_label.config(text=f"Food entered: {food}\nExpiry date: {date}")

    # Pack the confirmation items when "Enter" is pressed
    correct_label.pack()
    result_label.pack()
    btn_yes.pack()
    btn_no.pack()

# --- Enter Button ---
Button(myroot, text="Enter", command=on_enter).pack()

myroot.mainloop()
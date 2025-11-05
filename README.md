# FoodTracker

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project status](#project-status)
* [Room for improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)

## General info
This project is a food expiry date tracker that allows users to input a food item they have bought and its corresponding expiry date. The application will then provide a categorised list based on when their food is going to expire in hopes to reduce household waste. 
	
## Technologies
This project is created with 
- Python
- Visual Studio Code
- SQLite3
- Tkinter
- Datetime

## Features 
The best features in my project are;
- The seamless transitions between windows
- The categorisation of food items
- The ability to remove food items without any UI lag

## Screenshots 
<img width="497" height="423" alt="Screenshot 2025-11-05 at 11 38 13 pm" src="https://github.com/user-attachments/assets/fe7eb9d8-2481-441e-98ef-9ab0583f82b2" />
<img width="495" height="426" alt="Screenshot 2025-11-05 at 11 38 32 pm" src="https://github.com/user-attachments/assets/f22ef013-defc-4904-b0e7-35dfba58ad27" />

## Setup
No external dependencies required
Uses only Python standard library modules: tkinter, sqlite3, datetime

You will need Python 3 installed and Tkinter but this is often included 


## Usage 
This Food Tracker app lets you log food items with their expiration dates, view categorized food summaries, and remove food items, all through a simple graphical interface.  
It uses Tkinter for the GUI and SQLite for persistent storage.

### 1. Running the App

To start the application, run:

```bash
python food_tracker_app2.py
```

### 2. Enter Food Items

- Enter the food name and its expiry date (format **DD/MM/YY**).
- Confirm the correct entry or re-enter details if needed.
- You can continually add more food items or move directly to the summary.

### 3. View Food Summary

After entering foods, the summary window displays your foods grouped as:
- **Expired Foods** – already past expiration date
- **Expiring Today** – expiring today
- **Expiring Soon** – expiring within 3 days
- **Other Foods** – anything expiring after three days

### 4. Remove Food Items

From the summary window, you can:
- Select and remove individual food items.
- Remove all expired items in one click.
- Return to the summary or enter more items as needed.

### 5. Example

```python
# To start the app, simply run:
python food_tracker_app2.py

# When prompted, enter:
# Food: Milk
# Expiry Date (DD/MM/YY): 10/11/25

# Continue entering more foods or proceed to view the summary.

# In the summary window, you can:
# - See all your items categorized.
# - Remove single or all expired items.
# - Add more foods or exit.
```

**Note:**  
- Make sure you enter expiry dates in the **DD/MM/YY** format.
- The app stores food data in a local SQLite database file (`food_tracker.db`) which persists across sessions.

---

For any issues or customizations, feel free to explore and modify the classes:
- `FoodDatabase` (handles storage)
- `FoodCategorizer` (groups foods)
- `App_EnterFood` (entry UI)
- `App_FoodSummary` (summary UI)
- `App_RemoveFood` (removal UI)


## Project status
My project is finished and no longer being worked on


## Room for improvement 
To improve on my project, I could develop a way to scan expiry dates rather than having to enter them manually 
I could also develop it further so that my application suggests recipes that use up foods that are close to expiring. 


## Acknowledgements 
This project was based on _Code Nust's_YouTube video 'CREATE WASTE FOOD MANAGMENT SYSTEM USING PYTHON && LEARN PYTHON BY BUILDING SIMPLE PROJECTS' https://www.youtube.com/watch?v=fiqG0ZkhuEQ&t=17s 

import tkinter as tk
from tkinter import messagebox
import random
import os

# the constants
WINDOW_WIDTH = 500  # the width of the application window
WINDOW_HEIGHT = 400  # the height of the application window
SCORE_FILE = "scores.txt"  # file to store all user scores
LEADERBOARD_FILE = "leaderboard.txt"  # file to store the leaderboard
LEADERBOARD_LIMIT = 5  # max # of entries in the leaderboard
MIN_PASSWORD_LENGTH = 8  # min password length for registration

# colors for buttons
BUTTON_BG = "#4CAF50"  # makes green background
BUTTON_FG = "white"  # white text button
BUTTON_ACTIVE_BG = "#45a049"

# questions for the IGCSE Quiz
questions = [
    ("What does CPU stand for?",
     ["Central Processing Unit", "Computer Personal Unit", "Central Process Unit", "Control Processing Unit"], 0, 1),
    ("Which of these is an example of secondary storage?", ["RAM", "Cache", "SSD", "Register"], 2, 1),
    ("What does RAM stand for?",
     ["Random Access Memory", "Read Access Memory", "Run Access Memory", "Remote Access Memory"], 0, 1),
    ("Which of these is NOT an input device?", ["Keyboard", "Mouse", "Monitor", "Microphone"], 2, 1),
    ("What is the binary equivalent of decimal 10?", ["1001", "1010", "1100", "1000"], 1, 2),
    ("Which data type would store a whole number?", ["String", "Float", "Integer", "Boolean"], 2, 1),
    ("Which logic gate outputs true only if both inputs are true?", ["OR", "AND", "NOT", "NAND"], 1, 1),
    ("What does HTTP stand for?",
     ["HyperText Transfer Protocol", "Hyperlink Transfer Protocol", "Hyper Text Transmission Protocol",
      "Hyper Tool Transfer Protocol"], 0, 1),
    ("What is the purpose of an operating system?",
     ["Manage hardware", "Run software", "Provide UI", "All of the above"], 3, 2),
    ("What is phishing?", ["A network attack", "A social engineering attack", "A virus", "A type of encryption"], 1, 1)
]


class QuizApp:
    def __init__(self, root):
        self.root = root  # initializes the root window
        self.root.title("iGCSE Computer Science Quiz")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")  # sets the window size
        self.username = ""  # stores current username of user
        self.score = 0  # stores current scores
        self.current_question = 0  # track the current question indexs
        self.user_data = {}  # dictionary to store user credentials

        self.initialize_files()  # creates necessary files if they do not already exist
        self.load_users()  # loads existing users from file
        self.show_login_screen()  # displays the login screen

    def initialize_files(self):
        """create score and leaderboard files if they don't exist."""
        for file in [SCORE_FILE, LEADERBOARD_FILE]:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    f.write("")

    def load_users(self):
        """loads user credentials from 'users.txt'."""
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as file:
                for line in file:
                    user, pwd = line.strip().split(",")  # splits username and password
                    self.user_data[user] = pwd  # then stores in dictionary

    def save_users(self):
        """save user credentials to 'users.txt'."""
        with open("users.txt", "w") as file:
            for user, pwd in self.user_data.items():
                file.write(f"{user},{pwd}\n")  # puts username and password to the file

    def show_login_screen(self):
        """displays the login screen."""
        self.clear_screen()
        self.create_label("Login", font=("Arial", 18))  # title label
        self.create_label("Username:")  # username label
        self.username_entry = self.create_entry()  # username entry field
        self.create_label("Password:")  # password label
        self.password_entry = self.create_entry(show="*")  # password entry field (hidden)

        # colors with buttons
        self.create_button("Login", self.login)
        self.create_button("Register", self.show_register_screen)
        self.create_button("View Leaderboard", self.show_leaderboard)
        self.create_button("Quit", self.root.quit, bg="red", active_bg="darkred")  # red for quit button

    def show_register_screen(self):
        """displays the registration screen."""
        self.clear_screen()
        self.create_label("Register", font=("Arial", 18))  # Title label
        self.create_label("Username:")  # username label
        self.reg_username_entry = self.create_entry()  # sername entry field
        self.create_label(f"Password ({MIN_PASSWORD_LENGTH}+ chars):")  # password label
        self.reg_password_entry = self.create_entry(show="*")  # password entry field (hidden)

        # colors with buttons
        self.create_button("Register", self.register)
        self.create_button("Back", self.show_login_screen)

    def create_label(self, text, **kwargs):
        """helper function to create a label."""
        label = tk.Label(self.root, text=text, **kwargs) # helper function = small, reusable function designed to perform a specific task and support the main logic of a program
        label.pack()
        return label

    def create_entry(self, **kwargs):
        """helper function to create an entry field."""
        entry = tk.Entry(self.root, **kwargs)
        entry.pack()
        return entry

    def create_button(self, text, command, bg=BUTTON_BG, fg=BUTTON_FG, active_bg=BUTTON_ACTIVE_BG, **kwargs):
        """helper function to create a styled button."""
        button = tk.Button(
            self.root,
            text=text,
            command=command,
            bg=bg,  # background color
            fg=fg,  # text color
            activebackground=active_bg,  # background color when clicked
            font=("Arial", 12),
            padx=10,
            pady=5,
            **kwargs
        )
        button.pack(pady=5)
        return button

    def register(self):
        """registers a new user to the program."""
        username = self.reg_username_entry.get()  # get entered username
        password = self.reg_password_entry.get()  # get entered password

        if len(password) < MIN_PASSWORD_LENGTH:  # validates password length
            messagebox.showerror("Error", f"Password must be at least {MIN_PASSWORD_LENGTH} characters long")
            return

        if username in self.user_data:  # checks if username already exists
            messagebox.showerror("Error", "Username already exists")
            return

        self.user_data[username] = password  # adds new user to dictionary
        self.save_users()  # sAve updated user data to file

        #  creates a text file for the new user
        with open(f"{username}.txt", "w") as file:
            file.write(f"User: {username}\n")

        messagebox.showinfo("Success", "Registration successful!")  # show success message when registering
        self.show_login_screen()  # return to the login screen

    def login(self):
        """handle user login."""
        username = self.username_entry.get()  # get entered username
        password = self.password_entry.get()  #  get entered password

        if username in self.user_data and self.user_data[username] == password:  # validate credentials for user
            self.username = username  # set current username
            self.start_quiz()  # start the quiz
        else:
            messagebox.showerror("Error", "Invalid login credentials")  # show error message if invalid login details

    def start_quiz(self):
        """start the quiz by resetting the score and shuffling questions."""
        self.score = 0  # reset score
        self.current_question = 0  # reset question index
        random.shuffle(questions)  # shuffle questions
        self.show_question()  # displays the first question

    def show_question(self):
        """display the current question and options."""
        self.clear_screen()
        if self.current_question < len(questions):  # check if there are any more questions
            question, options, correct_index, points = questions[self.current_question]  # get current question
            self.create_label(question, wraplength=400, font=("Arial", 14))  # display question

            for i, option in enumerate(options):  # loop through options
                self.create_button(option, lambda i=i: self.check_answer(i))  # add option buttons

            self.create_label(f"Score: {self.score}", font=("Arial", 12))  # display current score
        else:
            self.show_result()  # if no more questions are left then, show the result

    def check_answer(self, selected_index):
        """check if the selected answer is correct and then update the score of the user."""
        question, options, correct_index, points = questions[self.current_question]  # get current question
        if selected_index == correct_index:  # check if selected answer is correct
            self.score += points  # add points to score
        else:
            self.score -= 1  # remove points if incorrect answer
        self.current_question += 1  # move on to next question
        self.show_question()  # display the next question

    def show_result(self):
        """displays the final score and update the leaderboard."""
        self.clear_screen()
        self.create_label(f"{self.username}, your final score: {self.score}", font=("Arial", 16))  # display final score

        # write the score to the scores file
        with open(SCORE_FILE, "a") as file:
            file.write(f"{self.username}: {self.score}\n")

        # update the leaderboard
        self.update_leaderboard()

        # colors with buttons
        self.create_button("Play Again", self.start_quiz)
        self.create_button("Exit", self.root.quit, bg="red", active_bg="darkred")  # red color for exit button

    def update_leaderboard(self):
        """update the leaderboard with the current score."""
        leaderboard = []
        if os.path.exists(LEADERBOARD_FILE):  # check if leaderboard file exists
            with open(LEADERBOARD_FILE, "r") as file:
                leaderboard = [line.strip() for line in file.readlines()]  # read existing entries

        # add the current score
        leaderboard.append(f"{self.username}: {self.score}")

        # remove duplicates/same names and sort by score (descending)
        leaderboard = list(set(leaderboard))  # remove duplicates
        leaderboard.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)  # sort by score - will put top scores first

        # keep only the top entries
        leaderboard = leaderboard[:LEADERBOARD_LIMIT]

        # write the updated leaderboard to the file
        with open(LEADERBOARD_FILE, "w") as file:
            for entry in leaderboard:
                file.write(f"{entry}\n")

    def show_leaderboard(self):
        """display the leaderboard."""
        self.clear_screen()
        self.create_label("Leaderboard", font=("Arial", 18))  # title label

        if os.path.exists(LEADERBOARD_FILE):  # check if leaderboard file exists
            with open(LEADERBOARD_FILE, "r") as file:
                leaderboard = [line.strip() for line in file.readlines()]  # read leaderboard entries

            if not leaderboard:  # check if leaderboard is empty
                self.create_label("No entries yet!", font=("Arial", 12))
            else:
                for i, entry in enumerate(leaderboard):  # display top entries
                    self.create_label(f"{i + 1}. {entry}", font=("Arial", 12))
        else:
            self.create_label("Leaderboard is empty!", font=("Arial", 12))

        # back button with color
        self.create_button("Back", self.show_login_screen)

    def clear_screen(self):
        """clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()


# the main application loop
if __name__ == "__main__":
    root = tk.Tk()  # create the main window
    app = QuizApp(root)  # initializes the QuizApp class
    root.mainloop()  # start the application loop
import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import pygame
import requests
import json
import os

# Initialize pygame mixer
pygame.mixer.init()

quiz_data = []
current_question = 0
score = 0
player_name = ""


# Function to fetch questions
def fetch_questions():
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/CodingCSmith/Questions/main/CQuestions.json"
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching questions: {e}")
        return []


# Function to show the question
def show_question():
    global current_question
    if 0 <= current_question < len(quiz_data):
        question = quiz_data[current_question]
        qs_label.config(text=question["question"])

        # Display the choices on the buttons with different colors in a row
        for i in range(3):
            choice_btns[i].config(
                text=question["choices"][i],
                state="normal",
                style=question["colors"][i],  # Set the color style
            )

        # Clear the feedback label
        feedback_label.config(text="")

        # Display the score label
        update_score_label()

    else:
        show_result_page()


# Function to update the score label
def update_score_label():
    global score
    score_label.config(text=f"Score: {score}/{len(quiz_data)}")


# Function to check the answer
def check_answer(choice):
    global current_question, score
    if 0 <= current_question < len(quiz_data):
        question = quiz_data[current_question]
        selected_choice = choice_btns[choice].cget("text")

        # Check if the selected choice matches the correct answer
        if selected_choice == question["answer"]:
            # Update the score and display it
            score += 1
            feedback_label.config(text="Correct!", foreground="green")
            update_score_label()  # Update the score label
        else:
            feedback_label.config(text="Incorrect!", foreground="red")

        # Disable all choice buttons
        for button in choice_btns:
            button.config(state="disabled")

        # Schedule the next question after a delay
        root.after(1, next_question_auto)

        # Disable the keyboard input during the cooldown
        root.unbind("<Key>")
    else:
        show_result_page()


# Function to move to the next question automatically
def next_question_auto():
    global current_question
    current_question += 1
    show_question()

    # Re-enable the keyboard input after the cooldown
    root.bind("<Key>", handle_keyboard)

    # Re-enable all choice buttons
    for button in choice_btns:
        button.config(state="normal")


# Function to restart the game
def restart_game():
    global score, current_question
    score = 0
    current_question = 0

    # Hide the result page frame and show the username entry frame
    result_frame.pack_forget()
    username_frame.pack()


# Function to show the result page (final score and leaderboard)
def show_result_page():
    global score

    if player_name:  # Check if a valid player name exists
        # Add player score to leaderboard only if a valid name is provided
        add_to_leaderboard(player_name, score)

    # Hide the quiz frame and show the result page frame
    quiz_frame.pack_forget()
    result_frame.pack()

    # Display final score and leaderboard
    display_final_score()
    display_leaderboard()


# Function to add player to leaderboard
def add_to_leaderboard(name, score):
    if name and isinstance(name, str):  # Check if name is a non-empty string
        leaderboard_file = "leaderboard.json"

        if os.path.exists(leaderboard_file) and os.path.getsize(leaderboard_file) > 0:
            try:
                with open(leaderboard_file, "r") as f:
                    leaderboard_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                leaderboard_data = []
        else:
            leaderboard_data = []

        leaderboard_data.append({"name": name, "score": score})

        with open(leaderboard_file, "w") as f:
            json.dump(leaderboard_data, f)


# Function to display final score
def display_final_score():
    global score
    print(f"Final Score: {score}/{len(quiz_data)}")
    final_score_label.config(text=f"Final Score: {score}/{len(quiz_data)}")


# Function to display the leaderboard
def display_leaderboard():
    leaderboard_file = "leaderboard.json"
    try:
        with open(leaderboard_file, "r") as f:
            leaderboard_data = json.load(f)

        # Sort leaderboard data by score in descending order
        sorted_leaderboard = sorted(
            leaderboard_data, key=lambda x: x["score"], reverse=True
        )

        # Display the leaderboard in the result frame
        leaderboard_text = "Leaderboard:\n"
        for idx, entry in enumerate(sorted_leaderboard[:10], start=1):
            leaderboard_text += f"{idx}. {entry['name']} - {entry['score']}\n"

        leaderboard_label.config(text=leaderboard_text)
    except FileNotFoundError:
        messagebox.showwarning("Leaderboard", "Leaderboard file not found.")
    except json.JSONDecodeError:
        messagebox.showerror("Leaderboard", "Error loading leaderboard data.")


# Function to start the quiz
def start_quiz():
    global quiz_data, player_name

    # Get player name from entry widget
    player_name = name_entry.get().strip()
    if not player_name:
        messagebox.showerror("Error", "Please enter your name.")
        return

    # Fetch questions and initialize quiz
    quiz_data = fetch_questions()
    show_question()

    # Hide username entry frame and show quiz frame
    username_frame.pack_forget()
    quiz_frame.pack()

    # Focus on the first choice button for keyboard input
    choice_btns[0].focus_set()


# Function to handle keyboard input
def handle_keyboard(event):
    key = event.keysym
    if key in {"1", "2", "3"}:
        check_answer(int(key) - 1)  # Convert key to index (0-based)
    elif key == "Return":  # Use "Return" (Enter key) to restart the game
        restart_game()


# Create the main window
root = tk.Tk()
root.style = Style(theme="darkly")
root.title("Quiz App")
root.geometry("1920x1080")
style = Style(theme="darkly")

style.configure("TLabel", font=("Helvetica", 40))
style.configure("TButton", font=("Helvetica", 32))

# Username entry frame
username_frame = ttk.Frame(root)

name_label = ttk.Label(username_frame, text="Enter your name:")
name_label.grid(row=0, column=0, padx=10)

name_entry = ttk.Entry(username_frame, font=("Helvetica", 30))
name_entry.grid(row=0, column=1, padx=10)

start_button = ttk.Button(username_frame, text="Start Quiz", command=start_quiz)
start_button.grid(row=1, columnspan=2, pady=20)

# Quiz frame (for displaying questions)
quiz_frame = ttk.Frame(root)

qs_label = ttk.Label(quiz_frame, anchor="center", wraplength=1600, padding=10)
qs_label.pack(pady=20)

choice_btns = []
for i in range(3):
    button = ttk.Button(
        quiz_frame,
        command=lambda i=i: check_answer(i),
        style="TButton",
    )
    button.pack(side="top", pady=10)
    choice_btns.append(button)

feedback_label = ttk.Label(quiz_frame, anchor="center", padding=10)
feedback_label.pack(pady=10)

score_label = ttk.Label(quiz_frame, text="Score: 0/0", anchor="center", padding=10)
score_label.pack(pady=100)

# Result page frame (for displaying final score and leaderboard)
result_frame = ttk.Frame(root)

final_score_label = ttk.Label(result_frame, text="", font=("Helvetica", 40))
final_score_label.pack(pady=50)

leaderboard_label = ttk.Label(result_frame, text="", font=("Helvetica", 32))
leaderboard_label.pack(pady=20)

# Button to go back to username entry
restart_button = ttk.Button(result_frame, text="Restart Quiz", command=restart_game)
restart_button.pack(pady=20)

# Bind keyboard events
root.bind("<Return>", lambda event: start_quiz())
root.bind("<Key>", handle_keyboard)

# Initially show the username entry frame
username_frame.pack(pady=100)

# Start the main event loop
root.mainloop()

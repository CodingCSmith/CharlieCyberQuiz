import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quiz_data import quiz_data
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load audio files
correct_sound = pygame.mixer.Sound("Sounds/CheeringEffect.mp3")
incorrect_sound = pygame.mixer.Sound("Sounds/WompWompWompEffect.mp3")


# Function to display the current question and choices
def show_question():
    # Get the current question from the quiz_data list
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
    score_label.config(text="Score: {}/{}".format(score, len(quiz_data)))


# Function to check the selected answer and provide feedback
def check_answer(choice):
    # Get the current question from the quiz_data list
    question = quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")

    # Check if the selected choice matches the correct answer
    if selected_choice == question["answer"]:
        # Update the score and display it
        global score
        score += 1
        feedback_label.config(text="Correct!", foreground="green")
        correct_sound.play()
    else:
        feedback_label.config(text="Incorrect!", foreground="red")
        incorrect_sound.play()

    # Disable all choice buttons
    for button in choice_btns:
        button.config(state="disabled")

    # Schedule the next question after a delay
    root.after(5000, next_question_auto)

    # Disable the keyboard input during the cooldown
    root.unbind("<Key>")


# Function to move to the next question automatically
def next_question_auto():
    global current_question
    current_question += 1

    if current_question < len(quiz_data):
        # If there are more questions, show the next question
        show_question()
    else:
        # If all questions have been answered, display the final score and end the quiz
        messagebox.showinfo(
            "Quiz Completed",
            "Quiz Completed! Final score: {}/{}".format(score, len(quiz_data)),
        )
        root.destroy()

    # Re-enable the keyboard input after the cooldown
    root.bind("<Key>", handle_keyboard)

    # Re-enable all choice buttons
    for button in choice_btns:
        button.config(state="normal")


# Function to handle keyboard input
def handle_keyboard(event):
    key = event.char
    if key in {"1", "2", "3"}:
        check_answer(int(key) - 1)  # Convert key to index (0-based)


# Create the main window
root = tk.Tk()
root.style = Style(theme="darkly")
root.title("Quiz App")
root.geometry("600x500")
style = Style(theme="darkly")

# Configure the font size for the question and choice buttons
style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

# Create the question label
qs_label = ttk.Label(root, anchor="center", wraplength=500, padding=10)
qs_label.pack(pady=10)

# Create the choice buttons horizontally with different colors and rounded edges in a row
choice_btns = []
for i in range(3):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i),
        style="success.Outline.TButton",  # Default style for the button
    )
    button.pack(side="top", pady=5)
    choice_btns.append(button)

# Create the feedback label
feedback_label = ttk.Label(root, anchor="center", padding=10)
feedback_label.pack(pady=10)

# Create the score label
score_label = ttk.Label(
    root, text="Score: 0/{}".format(len(quiz_data)), anchor="center", padding=10
)
score_label.pack(pady=10)

# Initialize the score
score = 0

# Initialize the current question index
current_question = 0

# Show the first question
show_question()

# Bind the keyboard input to the handle_keyboard function
root.bind("<Key>", handle_keyboard)

# Start the main event loop
root.mainloop()

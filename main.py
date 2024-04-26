import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import pygame
import requests
import json
import os

pygame.mixer.init()
correct_sound = pygame.mixer.Sound("Sounds/CheeringEffect.mp3")
incorrect_sound = pygame.mixer.Sound("Sounds/WompWompWompEffect.mp3")


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App")
        self.geometry("1920x1080")

        self.style = Style(theme="darkly")
        self.style.configure("TLabel", font=("Helvetica", 40))
        self.style.configure("TButton", font=("Helvetica", 32))

        self.quiz_data = []
        self.current_question = 0
        self.score = 0
        self.player_name = ""

        self.create_widgets()
        self.bind("<Key>", self.handle_keyboard)

    def create_widgets(self):
        self.username_frame = ttk.Frame(self)

        name_label = ttk.Label(self.username_frame, text="Enter your name:")
        name_label.grid(row=0, column=0, padx=10)

        self.name_entry = ttk.Entry(self.username_frame, font=("Helvetica", 30))
        self.name_entry.grid(row=0, column=1, padx=10)

        start_button = ttk.Button(
            self.username_frame, text="Start Quiz", command=self.start_quiz
        )
        start_button.grid(row=1, columnspan=2, pady=20)

        self.quiz_frame = ttk.Frame(self)

        self.qs_label = ttk.Label(
            self.quiz_frame, anchor="center", wraplength=1600, padding=10
        )
        self.qs_label.pack(pady=20)

        self.choice_btns = []
        for i in range(3):
            button = ttk.Button(
                self.quiz_frame,
                command=lambda i=i: self.check_answer(i),
                style="TButton",
            )
            button.pack(side="top", pady=10)
            self.choice_btns.append(button)

        self.feedback_label = ttk.Label(self.quiz_frame, anchor="center", padding=10)
        self.feedback_label.pack(pady=10)

        self.score_label = ttk.Label(
            self.quiz_frame, text="Score: 0/0", anchor="center", padding=10
        )
        self.score_label.pack(pady=100)

        self.result_frame = ttk.Frame(self)

        self.final_score_label = ttk.Label(
            self.result_frame, text="", font=("Helvetica", 40)
        )
        self.final_score_label.pack(pady=50)

        self.leaderboard_label = ttk.Label(
            self.result_frame, text="", font=("Helvetica", 32)
        )
        self.leaderboard_label.pack(pady=20)

        restart_button = ttk.Button(
            self.result_frame, text="Restart Quiz", command=self.restart_game
        )
        restart_button.pack(pady=20)

        self.username_frame.pack(pady=100)

    def start_quiz(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        self.quiz_data = self.fetch_questions()
        self.show_question()
        self.username_frame.pack_forget()
        self.quiz_frame.pack()
        self.choice_btns[0].focus_set()
        self.bind("<Key>", self.handle_keyboard)

    def fetch_questions(self):
        try:
            response = requests.get(
                "https://raw.githubusercontent.com/CodingCSmith/Questions/main/CQuestions.json"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching questions: {e}")
            return []

    def show_question(self):
        if 0 <= self.current_question < len(self.quiz_data):
            question = self.quiz_data[self.current_question]
            self.qs_label.config(text=question["question"])

            for i in range(3):
                self.choice_btns[i].config(
                    text=question["choices"][i],
                    state="normal",
                    style=question["colors"][i],
                )

            self.feedback_label.config(text="")
            self.update_score_label()

        else:
            self.show_result_page()

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}/{len(self.quiz_data)}")

    def check_answer(self, choice):
        if 0 <= self.current_question < len(self.quiz_data):
            question = self.quiz_data[self.current_question]
            selected_choice = self.choice_btns[choice].cget("text")

            if selected_choice == question["answer"]:
                self.score += 1
                self.feedback_label.config(text="Correct!", foreground="green")
                self.update_score_label()
                correct_sound.play()
            else:
                self.feedback_label.config(text="Incorrect!", foreground="red")
                incorrect_sound.play()

            for button in self.choice_btns:
                button.config(state="disabled")

            self.after(1000, self.next_question_auto)

            self.unbind("<Key>")
        else:
            self.show_result_page()

    def next_question_auto(self):
        self.current_question += 1
        self.show_question()

        self.bind("<Key>", self.handle_keyboard)

        for button in self.choice_btns:
            button.config(state="normal")

    def restart_game(self):
        messagebox.showerror("Restart", "Error going back to the start of the game.")

    def show_result_page(self):
        if self.player_name:
            self.add_to_leaderboard(self.player_name, self.score)

        self.quiz_frame.pack_forget()
        self.result_frame.pack()

        self.display_final_score()
        self.display_leaderboard()

    def add_to_leaderboard(self, name, score):
        if name and isinstance(name, str):
            leaderboard_file = "leaderboard.json"

            if (
                os.path.exists(leaderboard_file)
                and os.path.getsize(leaderboard_file) > 0
            ):
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

    def display_final_score(self):
        self.final_score_label.config(
            text=f"{self.player_name} Your Final Score is: {self.score}/{len(self.quiz_data)}"
        )

    def display_leaderboard(self):
        leaderboard_file = "leaderboard.json"
        try:
            with open(leaderboard_file, "r") as f:
                leaderboard_data = json.load(f)

            sorted_leaderboard = sorted(
                leaderboard_data, key=lambda x: x["score"], reverse=True
            )

            leaderboard_text = "Leaderboard:\n"
            for idx, entry in enumerate(sorted_leaderboard[:10], start=1):
                leaderboard_text += f"{idx}. {entry['name']} - {entry['score']}\n"

            self.leaderboard_label.config(text=leaderboard_text)
        except FileNotFoundError:
            messagebox.showwarning("Leaderboard", "Leaderboard file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Leaderboard", "Error loading leaderboard data.")

    def handle_keyboard(self, event):
        key = event.keysym
        if key in {"1", "2", "3"}:
            self.check_answer(int(key) - 1)
        elif key == "4":
            self.restart_game()


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()

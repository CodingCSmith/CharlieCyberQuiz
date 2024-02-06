# Quiz Application

This is a simple quiz application built using Python and Tkinter, designed to test your knowledge on various IT and computer-related topics. The program presents a series of multiple-choice questions and allows users to answer them by clicking on buttons or using keyboard shortcuts.

## Notes For Charlies Group

- **Make More/New IT/Cyber Questions:** Dont use the ones i have already dont this is because they are done by ChatGTP and dont want to get you in trouble. Format the questions like how i have shown bellow.

  ```json
    {
        "question": "Q1: Enter Your IT/Cyber Question Here?",
        "choices": ["Answer 1", "Answer 2", "Answer 3"],
        "answer": "Correct Answer Here",
        "colors": ["success.TButton", "info.TButton", "warning.TButton"] // Copy Paste This Line Aswell But Dont Change Them
    },
  ```

- **If You Need Any Help Ask Charlie Or Callum And We Help**

## Features

- **Interactive Interface:** The application provides an interactive graphical user interface (GUI) using Tkinter, making it easy and intuitive to navigate.

- **Sound Effects:** Enjoy sound effects for correct and incorrect answers, enhancing the overall user experience. Cheer for correct answers and hear a "womp womp" sound for incorrect ones.

- **Keyboard Input:** Users can answer questions using keyboard shortcuts (1, 2, 3) in addition to clicking on the buttons. This feature adds flexibility and convenience.

- **Cooldown Period:** To prevent spamming, there is a 5-second cooldown after each answer is selected. During this time, both buttons and keyboard input are disabled.

## Prerequisites

Before running the application, make sure you have the required libraries installed:

```bash
pip install tkinter ttkbootstrap pygame
```

## How to Use Git and Download the Repository

1. **Clone the repository using Git:**

   - Open your terminal or command prompt.
   - Navigate to the directory where you want to clone the repository.
   - Run the following command:

     ```bash
     git clone https://github.com/CodingCSmith/CharlieCyberQuiz.git
     ```

2. **Download the repository:**
   - If you prefer not to use Git, you can download the repository as a ZIP file.
   - Visit the GitHub repository page at [https://github.com/CodingCSmith/CharlieCyberQuiz.git](https://github.com/CodingCSmith/CharlieCyberQuiz.git).
   - Click on the "Code" button.
   - Select "Download ZIP."

## How to Run

1. Ensure that you have the necessary audio files (`CheeringEffect.mp3` and `WompWompWompEffect.mp3`) in a folder named `Sounds`.

2. Run the `quiz.py` file using the following command:

   ```bash
   python quiz.py
   ```

3. Answer the questions by clicking on the buttons or using keyboard shortcuts (1, 2, 3) this is so we can add buttons to click for you.

4. Enjoy the sound effects and test your knowledge!

## Question Data

The quiz questions and answer choices are stored in the `quiz_data.py` file. Feel free to customize the questions and add more to suit your preferences.

```python
# quiz_data.py file
quiz_data = [
    {
        "question": "Q1: What does URL stand for?",
        "choices": ["Uniform Resource Locator", "Universal Resource Locator", "Ultimate Resource Locator", "Uniform Retrieval Locator"],
        "answer": "Uniform Resource Locator",
        "colors": ["success.TButton", "info.TButton", "warning.TButton"]
    },
]
```

Modify the `quiz_data` list to include your own set of questions.

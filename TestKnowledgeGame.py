# A fun way to test your knowledge
import json
import os

import tkinter as tk
import random
from tkinter import messagebox

# load questions
def load_questions_from_json():
    path = os.path.join("data", "questions.json")
    with open(path, "r") as f:
        return json.load(f)

all_questions = load_questions_from_json()


# Define quiz levels

# GUI setup
root = tk.Tk()
root.title("NLP Quiz Level Selector")
root.geometry("400x300")

level_var = tk.IntVar()

def start_quiz():
    level = level_var.get()
    level=str(level)
    if level not in all_questions:
        messagebox.showerror("Invalid Level", "Please select a valid quiz level.")
        return
    root.destroy()
    questions=all_questions[level]
    launch_quiz(questions)

title = tk.Label(root, text="Select Your NLP Quiz Level", font=("Arial", 16))
title.pack(pady=20)

levels = ["Level 1: Tokenization", "Level 2: + Stemming & Lemma", "Level 3: + Stopwords", "Level 4: Final Boss"]
for idx, name in enumerate(levels, start=1):
    tk.Radiobutton(root, text=name, variable=level_var, value=idx, font=("Arial", 12)).pack(anchor="w", padx=40)

tk.Button(root, text="Start Quiz", command=start_quiz, font=("Arial", 12), bg="green", fg="white").pack(pady=20)

# Quiz launcher function
def launch_quiz(questions):
    score = 0
    question_index = 0
    hearts = 5

    quiz = tk.Tk()
    quiz.title("NLP Quiz Master")
    quiz.geometry("600x400")

    question_label = tk.Label(quiz, text="", font=("Arial", 14), wraplength=500, justify="center")
    question_label.pack(pady=20)

    options_var = tk.StringVar()
    option_buttons = []
    for _ in range(4):
        btn = tk.Radiobutton(quiz, text="", variable=options_var, value="", font=("Arial", 12))
        btn.pack(anchor="w", padx=100)
        option_buttons.append(btn)

    feedback_label = tk.Label(quiz, text="", font=("Arial", 12), fg="green")
    feedback_label.pack()

    hearts_label = tk.Label(quiz, text="❤️❤️❤️❤️❤️", font=("Arial", 16), fg="red")
    hearts_label.pack()

    def update_hearts():
        hearts_label.config(text="❤️" * hearts + " " * (5 - hearts))

    def display_question():
        nonlocal question_index
        if question_index < len(questions):
            q = questions[question_index]
            question_label.config(text=f"Q{question_index+1}: {q['question']}")
            options_var.set("")
            for i in range(4):
                option_buttons[i].config(text=q['options'][i], value=q['options'][i])
            update_hearts()
        else:
            show_result()

    def check_answer():
        nonlocal score, question_index, hearts
        selected = options_var.get()
        
        if selected == "":
            messagebox.showwarning("No selection", "Please choose an answer before submitting.")
            return
        correct = questions[question_index]['answer']
        if selected == correct:
            score += 1
            feedback_label.config(text="✅ Correct!", fg="green")
        else:
            hearts -= 1
            feedback_label.config(text=f"❌ Wrong! Correct: {correct}", fg="red")
            update_hearts()
            if hearts == 0:
                show_result()
                return
       
        feedback_label.after(2000,lambda:feedback_label.config(text=""))
        question_index += 1
        quiz.after(1000, display_question)

    def show_result():
        for widget in quiz.winfo_children():
            widget.destroy()

        emoji = ""
        message = ""
        final_score = int((score / len(questions)) * 100)

        if final_score >= 90:
            emoji = "🧙‍♂️✨"
            message = "Are you a wizard so cool? Oh wow, maybe you should try teaching next time!"
        elif final_score < 40:
            emoji = "😔📚"
            message = "You gave it a try and that matters. Don't stop now—next time you'll ace it!"
        elif final_score<60 and final_score>=50:
            emoji = "😍🤘 "
            message = "You're half up there! Just half more."
        else:
            emoji = "😎👍"
            message = "Great effort! You're on the path to mastering NLP. Keep it up!"

        result_label = tk.Label(quiz, text=f"Your Score: {final_score}%", font=("Arial", 20))
        result_label.pack(pady=20)

        emoji_label = tk.Label(quiz, text=emoji, font=("Arial", 50))
        emoji_label.pack()

        message_label = tk.Label(quiz, text=message, font=("Arial", 14), wraplength=500, justify="center")
        message_label.pack(pady=10)

    submit_btn = tk.Button(quiz, text="Submit", command=check_answer, font=("Arial", 12), bg="#4CAF50", fg="white")
    submit_btn.pack(pady=10)

    random.shuffle(questions)
    display_question()
    quiz.mainloop()

root.mainloop()
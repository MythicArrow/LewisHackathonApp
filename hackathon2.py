import random
import pygame
import sys
import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter import messagebox
from time import sleep

TF_ENABLE_ONEDNN_OPTS = 0

class RockPaperScissorsAI:
    def __init__(self):
        self.move_history = []
        self.labels = {'R': 0, 'P': 1, 'S': 2}
        self.moves = ['R', 'P', 'S']
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(6,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(3, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def get_ai_move(self):
        if len(self.move_history) < 3:
            return random.choice(self.moves)

        input_data = np.array(self.move_history[-3:]).flatten().reshape(1, 6)
        prediction = self.model.predict(input_data, verbose=0)
        predicted_move = np.argmax(prediction)
        counter_move = (predicted_move + 1) % 3
        return self.moves[counter_move]

    def update_history(self, user_move, ai_move):
        user_move_encoded = self.labels[user_move]
        ai_move_encoded = self.labels[ai_move]
        self.move_history.append([user_move_encoded, ai_move_encoded])

        if len(self.move_history) > 100:
            self.move_history.pop(0)

    def train_model(self):
        if len(self.move_history) < 4:
            return

        X = np.array([np.array(self.move_history[i:i+3]).flatten() for i in range(len(self.move_history) - 3)])
        y = np.array([self.move_history[i + 3][0] for i in range(len(self.move_history) - 3)])

        self.model.fit(X, y, epochs=10, verbose=0)

def play_rps_ai():
    ai = RockPaperScissorsAI()
    ai_wins = 0
    user_wins = 0
    total_games = 0
    required_wins = 3


    while user_wins < required_wins:
        user_move = input("Choose Rock (R), Paper (P), or Scissors (S): ").upper()
        if user_move not in ['R', 'P', 'S']:
            print("Invalid move! Please choose R, P, or S.")
            continue

        ai_move = ai.get_ai_move()

        if (ai_move == 'R' and user_move == 'S') or (ai_move == 'P' and user_move == 'R') or (ai_move == 'S' and user_move == 'P'):
            print(f"AI chose {ai_move}. AI wins this round!")
            ai_wins += 1
        elif ai_move == user_move:
            print(f"AI chose {ai_move}. It's a tie!")
        else:
            print(f"AI chose {ai_move}. You win this round!")
            user_wins += 1

        total_games += 1
        ai.update_history(user_move, ai_move)
        ai.train_model()

        print(f"Score: AI Wins - {ai_wins}, Your Wins - {user_wins}, Total Games - {total_games}")

        if ai_wins >= required_wins:
            print("AI wins the match! You must try again.")
            return False

    print("You won against the AI! You can guess again!")
    return True

def final_challenge():
    class QuizApp:
        def __init__(self, master):
            self.master = master
            self.master.title("Programming Quiz")

            self.questions = [
                {"question": "What does 'HTML' stand for?", "options": ["HyperText Markup Language", "HyperText Machine Language", "HyperText Modeling Language"], "answer": "HyperText Markup Language"},
                {"question": "Which language is known as the language of the web?", "options": ["Python", "JavaScript", "C++"], "answer": "JavaScript"},
                {"question": "What is the correct file extension for Python files?", "options": [".py", ".java", ".c"], "answer": ".py"},
                {"question": "What does 'IDE' stand for?", "options": ["Integrated Development Environment", "Integrated Design Environment", "Internal Development Environment"], "answer": "Integrated Development Environment"},
                {"question": "Which company developed Java?", "options": ["Microsoft", "Sun Microsystems", "Apple"], "answer": "Sun Microsystems"},
                {"question": "What is the default value of an uninitialized variable in Java?", "options": ["0", "null", "undefined"], "answer": "null"},
                {"question": "Which keyword is used to define a function in Python?", "options": ["def", "function", "func"], "answer": "def"},
                {"question": "What is the main purpose of a version control system?", "options": ["Manage code changes", "Manage file storage", "Manage network traffic"], "answer": "Manage code changes"},
                {"question": "Which of the following is a Python web framework?", "options": ["Django", "React", "Angular"], "answer": "Django"},
                {"question": "What does 'SQL' stand for?", "options": ["Structured Query Language", "Standard Query Language", "Sequential Query Language"], "answer": "Structured Query Language"}
            ]
            self.current_question = 0
            self.correct_answers = 0

            self.question_label = tk.Label(master, text="", wraplength=400)
            self.question_label.pack(pady=20)

            self.option_var = tk.StringVar()
            self.option_buttons = []
            for _ in range(3):
                button = tk.Radiobutton(master, text="", variable=self.option_var, value="", command=self.check_answer)
                button.pack(anchor='w')
                self.option_buttons.append(button)

            self.next_button = tk.Button(master, text="Next", command=self.next_question)
            self.next_button.pack(pady=20)

            self.show_question()

        def show_question(self):
            question = self.questions[self.current_question]
            self.question_label.config(text=question["question"])
            for i, option in enumerate(question["options"]):
                self.option_buttons[i].config(text=option, value=option)
            self.option_var.set(None)

        def check_answer(self):
            selected_option = self.option_var.get()
            correct_answer = self.questions[self.current_question]["answer"]
            if selected_option == correct_answer:
                self.correct_answers += 1

        def next_question(self):
            if self.current_question < len(self.questions) - 1:
                self.current_question += 1
                self.show_question()
            else:
                self.end_quiz()

        def end_quiz(self):
            if self.correct_answers >= 3:
                messagebox.showinfo("Quiz Finished", "Congratulations! You've passed the quiz.")
                self.master.quit()
                self.passed = True
            else:
                messagebox.showinfo("Quiz Finished", "Sorry, you didn't pass the quiz. Better luck next time!")
                self.master.quit()
                self.passed = False

    while True:
        root = tk.Tk()
        app = QuizApp(root)
        root.mainloop()

        if app.passed:
            break  # Exit the loop if the player passed
        else:
            print("You didn't pass the quiz. You will get a new number to guess.")
            return  # Restart the guessing game with a new random number

def play_snake_game():
    pygame.init()
    back = (192, 192, 192)
    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Classic Snake Game')
    gameDisplay.fill(back)
    clock = pygame.time.Clock()
    running = True
    tail = [[200, 100], [180, 100], [160, 100], [140, 100], [120, 100], [100, 100]]
    rotation = "right"
    random_apple = lambda: [random.randint(0, 39) * 20, random.randint(0, 29) * 20]
    apple = random_apple()
    score = 0
    tick_speed = 10
    required_score = 5  # Set the required score to 5

    while running:
        gameDisplay.fill(back)
        _event = pygame.event.get()
        for event in _event:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    rotation = "up"
                elif event.key == pygame.K_s:
                    rotation = "down"
                elif event.key == pygame.K_a:
                    rotation = "left"
                elif event.key == pygame.K_d:
                    rotation = "right"

        # Snake movement
        if rotation == "right":
            tail.insert(0, [tail[0][0] + 20, tail[0][1]])
        elif rotation == "left":
            tail.insert(0, [tail[0][0] - 20, tail[0][1]])
        elif rotation == "up":
            tail.insert(0, [tail[0][0], tail[0][1] - 20])
        elif rotation == "down":
            tail.insert(0, [tail[0][0], tail[0][1] + 20])

        tail.pop()

        # Check collision with apple
        if tail[0] == apple:
            apple = random_apple()
            tail.append([0, 0])
            score += 1

        # Draw snake and apple
        for i in tail:
            pygame.draw.rect(gameDisplay, (0, 255, 0) if i == tail[0] else (11, 11, 11), pygame.Rect(i[0], i[1], 20, 20))
        pygame.draw.rect(gameDisplay, (255, 0, 0), pygame.Rect(apple[0], apple[1], 20, 20))

        pygame.display.set_caption(f"Score - {score:_>3}  Length - {len(tail)}")
        pygame.display.update()
        clock.tick(tick_speed)

        # Check for game over conditions
        if not 0 <= tail[0][0] < 800 or not 0 <= tail[0][1] < 600:
            print(f"Game Over\nScore - {score}\nLength - {len(tail)}")
            running = False

        # Check if score requirement is met
        if score >= required_score:
            print("Nice play! You can guess again!")
            break  # Exit the game loop and allow the player to guess again

    pygame.quit()

def main():
    while True:
        randint = random.randint(1, 100)
        guess = int(input("Guess a number between 1 and 100: "))
        guessNumber = 0

        while guess != randint:
            guessNumber += 1
            if guess > randint:
                print("Uh oh, your guess was too high. You must play a game to guess again!")

                play_snake_game()

            elif guess < randint:
                print("Uh oh, your guess was too small. You must beat a Rock-Paper-Scissors AI 3 times before guessing again!")
                if not play_rps_ai():
                    continue  # If the player loses to the AI, they must try to guess again

            guess = int(input("Guess a number between 1 and 100: "))
            if guess == randint:
                print("Nice, you guessed the number but you must do one more final challenge to win!")
                sleep(2)
                print("You are going to take a programming quiz!")

                final_challenge()  # Call the final quiz challenge

                if app.passed:
                    print(f"Congratulations! You've guessed the number {randint} in {guessNumber} tries.")
                    return  # Exit the main guessing loop if the player passed the final challenge
                else:
                    # If failed, loop continues to get a new number
                    print("You didn't pass the quiz. You will get a new number to guess.")

if __name__ == "__main__":
    main()












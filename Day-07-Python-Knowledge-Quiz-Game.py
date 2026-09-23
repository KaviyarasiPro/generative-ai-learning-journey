# Day 7 - Python Knowledge Quiz Game

questions = [
    ["Which keyword is used to create a function in Python?", "def"],
    ["Which method adds an item to a list?", "append"],
    ['What is the output of len("Python")?', "6"],
    ["Which loop is commonly used to iterate through a list?", "for"],
    ["Which symbol is used for comments in Python?", "#"]
]

score = 0

print("==============================")
print("       PYTHON QUIZ GAME")
print("==============================")

for question in questions:

    print("\n", question[0])
    answer = input("Your answer: ")

    if answer.lower() == question[1].lower():
        print("Correct!")
        score = score + 1

    else:
        print("Wrong!")
        print("Correct answer:", question[1])


percentage = (score / len(questions)) * 100

if percentage >= 90:
    performance = "Excellent"

elif percentage >= 75:
    performance = "Very Good"

elif percentage >= 60:
    performance = "Good"

else:
    performance = "Keep Practicing"


print("\n==============================")
print("          QUIZ RESULT")
print("==============================")
print("Score       :", score, "/", len(questions))
print("Percentage  :", round(percentage, 2), "%")
print("Performance :", performance)
print("==============================")








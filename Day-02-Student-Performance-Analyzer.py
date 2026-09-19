"""
Day 2 - Student Performance Analyzer

Write a Python program to:
1. Get the student's name.
2. Get marks for Tamil, English, Maths, Science and Social Science.
3. Calculate the average mark.
4. Display the student's performance based on the average.
"""

def calculate_average(marks):
   total = 0

   for mark in marks:
       total += mark
   return total / len(marks)

def get_performance(average):
    if average >= 90:
        return "Excellent"
    elif average >= 75:
        return "Very Good"
    elif average >= 60:
        return "Good"
    elif average >= 50:
        return "Average"
    else:
        return "Need Improvement"
    
name = input("Enter student name :")

subjects = ["Tamil","English","Maths","Science","Social Science"]
marks = []

for subject in subjects :
    mark = float(input(f"Enter {subject} mark :"))
    marks.append(mark)

average = calculate_average(marks)
performance = get_performance(average)

print("\n---Student Performance Report")
print("Student :",name)
print("Average :",round(average,2))
print("Performance :",performance)




































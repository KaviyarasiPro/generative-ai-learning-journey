# Day 16 - Customer Support Chatbot
print("-"*50)
print("  CUSTOMER SUPPORT CHATBOT")
print("-"*50)
print("Hello! Welcome to our customer support chatbot. How can I assist you today?")

while True:
    message = input("You: ")
    message = message.lower()
    if "bye" in message or "exit" in message or "quit" in message:
     print("Chatbot: Thank you for using our customer support chatbot. Have a great day!")
     break
    if "order" in message or "track" in message:
        print("Chatbot: you can track your order using the tracking link sent to your email.")
    elif "refund" in message or "return" in message:
        print("Chatbot: you can return your order within 30 days of purchase.")
    elif "payment" in message or "pay" in message:
        print("Chatbot: please check our payment methods and try again. if the issue continues, contact our support team.")
    elif "refund" in message :
        print("Chatbot: your refund will be processed within 5-7 business days.")
    elif "exit" in message or "quit" in message:
        print("Chatbot: Thank you for using our customer support chatbot. Have a great day!")
        break
    else :
        print("Chatbot: I'm sorry, I didn't understand your request. Please contact our support team for further assistance.")


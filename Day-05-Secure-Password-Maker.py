# Day 5 - Secure Password Maker
# Generate a random password based on user preferences

import random
import string

def generate_password(length,include_symbols):
    
    characters = string.ascii_letters + string.digits

    if include_symbols == "yes" :
        characters = characters + string.punctuation

    password = ""

    for i in range(length):
        password = password + random.choice(characters)

    return password

def check_strength(length):

    if length >= 12 :
        return "Strong"
    elif length >= 8 :
        return "Medium"
    else :
        return "weak"
        
print("================================")
print("     🔐 SECURE PASSWORD MAKER")
print("================================")

name = input("Enter your name : ")
length = int(input("Enter password length : "))
include_symbols = input("Include symbols? (yes/no) :").lower()

password = generate_password(length,include_symbols)

strength = check_strength(length)

print("\nGenerating your secure password...")

print("\n--------------------------------")
print("👤 User       :", name)
print("🔑 Password   :", password)
print("📏 Length     :", length)
print("🛡️ Strength   :", strength)
print("--------------------------------")

print("\n✅ Your password is ready!")









string = input()
result = ""
for letter in string:
    if letter.isupper() and letter.isalpha():
        letter = letter.lower()
    elif letter.islower() and letter.isalpha():
        letter = letter.upper()
    result += letter
print(result)
import requests
from random import random
from collections import Counter


# Calculating Pi

""" precision = int(input("Enter number of decimal places: "))

hits, total = 0, 0
for i in range(10_000_000):
    x, y = random(), random()
    
    if (x - 0.5)**2 + (y - 0.5)**2 <= 0.25:
        hits += 1
    total += 1

print(round((hits/total)*4, precision)) """


################################################################################


# Breaking Caesar's Cipher

def validate(word):
    if word:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}") #can occasionally error pointlessly
        return 'title' not in response.json()
    else: return False


def shifter(ciphertext, shift):
    decrypted_text = []
    for char in ciphertext:
        if char.isalpha():
            shifted_index = (ord(char) - 97 - shift) % 26
            decrypted_text.append(chr(shifted_index + 97))
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)


def freq_analysis(ciphertext):
    ranked_shifts = []
    
    for shift in range(1, 27):
        score = 0
        letter_counts = Counter([letter for letter in shifter(ciphertext, shift) if letter.isalpha()])
        shifted_freq = [letter for letter, count in letter_counts.most_common()] #list of letters sorted by freq
        
        for i, letter in enumerate(shifted_freq):
            if letter.isalpha():
              score += abs('etaoinshrdlcumwfgypbvkjxqz'.index(letter) - i) #difference between letter placements
        ranked_shifts.append((shift, score))
    
    #lower score = better match
    ranked_shifts.sort(key=lambda x: x[1])
    return [shift for shift, _ in ranked_shifts]


def word_split(decrypted_text):
    i = 0

    while i < len(decrypted_text):
        found_word = False
        for j in range(len(decrypted_text), i, -1):  #start from longest possible word
            word_candidate = decrypted_text[i:j]
            if validate(word_candidate):
                i = j
                found_word = True
                break

        if not found_word:
            return None

    return decrypted_text


def break_cipher(ciphertext):
    ciphertext = ciphertext.lower() 
    ranked_shifts = freq_analysis(ciphertext)
    
    for shift in ranked_shifts:
        shifted_text = shifter(ciphertext, shift)
        
        segmented_text = word_split(shifted_text)
        
        if segmented_text: #if all valid words
            return f'Decrypted text with a shift of {shift}:\n{segmented_text}'
    
    return "Decryption failed; could not find valid text."


ciphertext = input('Ciphertext: ')
print(break_cipher(ciphertext))
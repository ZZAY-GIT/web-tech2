with open("example.txt", encoding='utf-8') as f:
    text = f.read()

clean_text = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text)
words = clean_text.split()

if not words:
    exit()

max_length = max(map(len, words))
longest_words = []

seen = set()
for word in words:
    if len(word) == max_length and word not in seen:
        seen.add(word)
        longest_words.append(word)

print('\n'.join(longest_words))
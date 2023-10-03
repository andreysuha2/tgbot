import spacy
nlp = spacy.load("uk_core_news_lg")
print("test")

while True:
    message1 = nlp(input(">>> "))
    message2 = nlp(input(">>> "))

    similarity = message1.similarity(message2)

    print(similarity)
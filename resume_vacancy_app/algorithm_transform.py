import requests
import pandas as pd
import numpy as np
import random
import re
import nltk
import asyncio
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from pymystem3 import Mystem
from nltk.corpus import stopwords
from gensim.models import Word2Vec

# Обработка текста
def processing(text):
    # Регулярные выражения
    pattern = r"[^\w]"
    text = re.sub(pattern, " ", text)

    # Лемматезация
    m = Mystem()
    lemmas = m.lemmatize(text)
    text = "".join(lemmas).strip()

    # Токенизация
    text = nltk.sent_tokenize(text)
    text = [nltk.word_tokenize(sentence) for sentence in text]

    # Стоп-слова
    stop_words = set(stopwords.words("russian"))
    for i in range(len(text)):
        text[i] = [word for word in text[i] if not word in stop_words]

    return text

def count_similar_word(resume, vacancy):
  sentences = resume + vacancy
  model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
  model.train(sentences, total_examples=model.corpus_count, epochs=10)
  count = 0
  resume_text = resume[0]
  vacancy_text = vacancy[0]
  for word in resume_text:
    # Получение вектора слова
    vector = model.wv[word]
    # Поиск похожих слов
    similar_words = model.wv.most_similar(word)
    for similar_word in similar_words:
      if similar_word[0] in vacancy_text and similar_word[1] >= 0.15:
        count += 1

  return count
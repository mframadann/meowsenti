import nltk
import pickle
import re
import os
import pandas as pd
from enum import Enum
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class MfModelOption(Enum):
    MFNb = "model_nb.pkl"
    MFSvc = "model_svc.pkl"

class MFSentimentAnalyzer:
    def __init__(self, df: pd.DataFrame, model: MfModelOption):
        self.__df = df
        self.__df_origin = self.__df.copy()
        self.__df_origin["alg_type"] = "Naive Bayes" if model == MfModelOption.MFNb else "Support Vector Machine"
        
        base_path = os.getcwd()
        self.__libsPath = os.path.join(base_path, "src/libs")
        self.__picklesPath = os.path.join(base_path, "src/model")
        
        model_path = os.path.join(self.__picklesPath, model.value)
        with open(model_path, "rb") as file:
            self.__model = pickle.load(file)


    def __text_cleaning(self, text: str) -> str:
        text = text.lower()
        text = re.sub("[^a-z]", " ", text)
        text = re.sub("\\s+", " ", text).strip()
        return text


    def __correct_spelling(self, text: str) -> str:
        dictionaries = {}
        spell_file = os.path.join(self.__libsPath, "addons_spelling.txt")
        
        with open(spell_file, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    dictionaries[parts[0].strip()] = parts[1].strip()
        
        for word, replacement in dictionaries.items():
            text = re.sub(rf"\b{re.escape(word)}\b", replacement, text, flags=re.IGNORECASE)
        return text


    def __remove_stopword(self, text: str) -> str:
        factory = StopWordRemoverFactory()
        sastrawi_stopwords = set(factory.get_stop_words())
        nltk_stopwords = set(stopwords.words("indonesian"))
        
        stopword_file = os.path.join(self.__libsPath, "addons_stopwords.txt")
        with open(stopword_file, "r") as file:
            additional_stopwords = set(file.read().splitlines())
        
        all_stopwords = sastrawi_stopwords | nltk_stopwords | additional_stopwords
        
        words = text.split()
        filtered_text = " ".join(word for word in words if word not in all_stopwords)
        return filtered_text


    def __stemm_text(self, text: str) -> str:
        stemmer = StemmerFactory().create_stemmer()
        return stemmer.stem(text)


    def Analyze(self) -> pd.DataFrame:
        self.__df["review"] = self.__df["review"].apply(self.__text_cleaning)
        self.__df["review"] = self.__df["review"].apply(self.__correct_spelling)
        self.__df["review"] = self.__df["review"].apply(self.__remove_stopword)
        self.__df["review"] = self.__df["review"].apply(self.__stemm_text)
        
        vectorizer_path = os.path.join(self.__picklesPath, "vectorizer_tfidf.pkl")
        with open(vectorizer_path, "rb") as file:
            vectorizer = pickle.load(file)
        
        self.__df_origin["kind_of_sentiment"] = self.__model.predict(vectorizer.transform(self.__df["review"]))
        self.__df_origin["kind_of_sentiment"] = self.__df_origin["kind_of_sentiment"].replace({
              0: "Negative",
              1: "Positive",
              2: "Neutral"
        })

        return self.__df_origin


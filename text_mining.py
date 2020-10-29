import pandas as pd
from string import digits
import re
import os


class TextCleaner:


    def __get_stop_words(self):
        stopwords = pd.read_csv(f"stopwords.txt", names=['words'])
        return stopwords

    def __get_text_df(self, text):
        text_df = pd.DataFrame(data=text.split(), columns=['words'])
        return text_df

    def __cleaning_text(self, text):

        def remove_emoji(text):
            emoji_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F"  # emoticons
                                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       u"\U00002702-\U000027B0"
                                       u"\U000024C2-\U0001F251"
                                       "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)

        text = text.lower().strip()

        # remove url
        text = re.sub(r"http\S+", "", text)

        text = remove_emoji(text=text)
        text = re.sub(r'[^\w\s]', '', text)

        # remove digits
        remove_digits = str.maketrans('', '', digits)
        text = text.translate(remove_digits)


        return text

    def get_clean_text(self, text):
        text = self.__cleaning_text(text)
        text_df = self.__get_text_df(text)
        stopwords = self.__get_stop_words()

        clean_text_df = text_df[~text_df.words.isin(stopwords.words)].reset_index(drop=True)
        clean_text_df = clean_text_df.words.value_counts().\
            reset_index().\
            rename(columns={'index': 'word', 'words': 'count'}).\
            sort_values(by=['count'], ascending=False).\
            reset_index(drop=True)

        return clean_text_df

    # insert new stopword(s) into stopwords.txt
    def insert_new_word(self, new_word):
        stop_words = self.__get_stop_words()

        if type(new_word) == list:
            new_word = [i.strip().lower() for i in new_word]
        else:
            new_word = [new_word.lower().strip()]

        words = []

        for word in new_word:
            if word not in list(stop_words.words):
                words.append(word)
                print(f"insert_new_word: {word} has been inserted")
            else:
                print(f"insert_new_word: {word} already exists")

        if words:
            new_stopwords_df = pd.concat([stop_words, pd.DataFrame(data=words, columns=['words'])])
            new_stopwords_df.to_csv('stopwords.txt', index=False, header=False)

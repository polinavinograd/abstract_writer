import nltk
from nltk.corpus import wordnet
from nltk import WordNetLemmatizer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

from pymorphy2 import MorphAnalyzer


try:
    from nltk.corpus import stopwords
except ImportError:
    nltk.download("stopwords")

LEMMATIZER = WordNetLemmatizer()
morph = MorphAnalyzer()
stop_words_rus = set(stopwords.words('russian'))
stop_words_eng = set(stopwords.words("english"))


class NaturalLanguageUtils:
    @staticmethod
    def normalize(tokenized_text: 'list[str]') -> list:
        part_of_speech_tags = nltk.pos_tag(tokenized_text)
        new_part_of_speech_tags = []
        for tag in part_of_speech_tags:
            wn_part_of_speech = wordnet.ADJ
            if tag[1].startswith('N'):
                wn_part_of_speech = wordnet.NOUN
            elif tag[1].startswith('V'):
                wn_part_of_speech = wordnet.VERB
            elif tag[1].startswith('R'):
                wn_part_of_speech = wordnet.ADV
            new_tag = tuple([LEMMATIZER.lemmatize(tag[0], wn_part_of_speech), tag[1]])
            new_part_of_speech_tags.append(new_tag)
        return new_part_of_speech_tags

    def normalize_tokens_only(self, tokenized_text: 'list[str]') -> 'list[str]':
        return self.normalize_russian_text(list(map(lambda tag: tag[0], NaturalLanguageUtils.normalize(tokenized_text))))

    @staticmethod
    def normalize_russian_text(tokenized_text: 'list[str]') -> 'list[str]':
        normalized_words = [morph.parse(word)[0].normal_form for word in tokenized_text if
                            word.isalpha() and word not in stop_words_rus and word not in stop_words_eng]
        return normalized_words

    @staticmethod
    def get_most_common_collocations(normalized_words: list[str]) -> list:
        bigram_measures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(normalized_words)

        finder.apply_freq_filter(2)
        return finder.nbest(bigram_measures.raw_freq, 100)

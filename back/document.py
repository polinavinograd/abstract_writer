import nltk
from natural_language_utils import NaturalLanguageUtils


class Document:
    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text.lower()

    def tokenized(self) -> 'list[str]':
        return nltk.word_tokenize(self.text)

    def normalized(self) -> 'list[str]':
        return NaturalLanguageUtils().normalize_tokens_only(self.tokenized())

    def split_by_paragraphs(self) -> 'list[str]':
        return self.text.split(".\n")

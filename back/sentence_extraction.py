import os.path
import math
import numpy as np
import json

from document import Document
from natural_language_utils import NaturalLanguageUtils
import utils
from path import LOCAL_PATH


class SentenceExtractor:
    def __init__(self, number_of_sentences=10):
        self.__number_of_sentences = number_of_sentences

        with open('texts_scores.json', 'r+', encoding="utf-8") as file:
            try:
                self.__texts_scores = json.load(file)
            except json.JSONDecodeError:
                self.__texts_scores = {}
                documents = utils.get_all_documents_in_folder(os.path.join(LOCAL_PATH, "docs"))
                for document in documents:
                    self.__texts_scores[document.name] = self.__get_sentences_score(document)
                json.dump(self.__texts_scores, file, indent=4, ensure_ascii=False)

    def __calculate_document_position(self, document: Document, paragraph_index: int, sentence_index: int) -> float:
        symbols_before = 0
        paragraphs = document.split_by_paragraphs()
        for paragraph in paragraphs[:paragraph_index]:
            symbols_before += len(paragraph)

        symbols_before += self.__get_count_symbols_before(paragraphs[paragraph_index], sentence_index)
        position = 1 - symbols_before / len(document.text)
        return position

    def __get_count_symbols_before(self, paragraph: str, sentence_index: int) -> int:
        sentences = NaturalLanguageUtils.sentence_tokenize(paragraph)
        symbols_before = 0
        for sentence in sentences[:sentence_index]:
            symbols_before += len(sentence)
        return symbols_before

    def __calculate_paragraph_position(self, paragraph: str, sentence_index: int) -> float:
        symbols_before = self.__get_count_symbols_before(paragraph, sentence_index)
        position = 1 - symbols_before / len(paragraph)
        return position

    def __number_of_documents_containing_term(self, word: str) -> int:
        num_docs_with_word = 0
        for document in utils.get_all_documents_in_folder(os.path.join(LOCAL_PATH, "docs")):
            if word in document.tokenized():
                num_docs_with_word += 1
        return num_docs_with_word

    def __get_sentences_score(self, document: Document) -> dict[int, float]:
        sentences = NaturalLanguageUtils.sentence_tokenize(document.text)
        sentences_score = {}
        for i in range(len(sentences)):
            sentence_score = []
            tokenized_sentence = NaturalLanguageUtils.extract_stop_words(sentences[i])
            for word in tokenized_sentence:
                frequency_in_sen = NaturalLanguageUtils.get_word_frequency(word, sentences[i])
                frequency_in_doc = NaturalLanguageUtils.get_word_frequency(word, document.text)
                max_frequency = NaturalLanguageUtils.get_max_word_frequency(document.text)
                word_score = 0.5 * (1 + frequency_in_doc / max_frequency) * \
                             math.log(len(utils.get_all_documents_in_folder(os.path.join(LOCAL_PATH, "docs"))) /
                                      self.__number_of_documents_containing_term(word))
                score = frequency_in_sen * word_score
                sentence_score.append(score)

            sentences_score[i] = sum(sentence_score)
        return sentences_score

    def summarize_document(self, document: Document) -> str:
        sentences = NaturalLanguageUtils.sentence_tokenize(document.text)
        sentences_score = np.array(list(self.__texts_scores[document.name].values()))

        top_indices = np.argpartition(sentences_score, -self.__number_of_sentences)[-self.__number_of_sentences:]
        sorted_indices = np.sort(top_indices)
        summarized_doc = ' '.join(np.array(sentences)[sorted_indices])
        return summarized_doc


from document import Document
from natural_language_utils import NaturalLanguageUtils
import utils
import json
import os


class KeywordsBasedAbstract:
    def __init__(self):
        with open('word_frequency.json', 'r+', encoding="utf-8") as file:
            try:
                self.__word_frequency = json.load(file)
            except json.JSONDecodeError:
                self.__word_frequency = {}

                for root, dirs, files in os.walk("..\\docs"):
                    for file_name in files:
                        document = Document(file_name, utils.get_file_contents(os.path.join(root, file_name)))
                        local_word_amount = self.__count_local_word_amount(document)
                        self.__word_frequency[file_name] = self.__calculate_word_frequency(local_word_amount)
                json.dump(self.__word_frequency, file, indent=4, ensure_ascii=False)

    @staticmethod
    def __count_local_word_amount(document: Document) -> 'dict[str: float]':
        local_word_amount = {}
        for word in document.normalized():
            if word not in local_word_amount:
                local_word_amount[word] = 0
            local_word_amount[word] += 1
        return local_word_amount

    @staticmethod
    def __calculate_word_frequency(word_amount: 'dict[str, int]') -> 'dict[str, float]':
        for word, frequency in word_amount.items():
            word_amount[word] /= sum(word_amount.values())
        return word_amount

    def find_most_common_words_from_document(self, document: Document) -> 'dict[str, float]':
        sorted_dict = dict(sorted(self.__word_frequency[document.name].items(), key=lambda item: item[1], reverse=True)
                           [:20])
        return sorted_dict

    def find_hierarchy(self, document: Document) -> 'dict[str: list[str]]':
        collocations = NaturalLanguageUtils.get_most_common_collocations(document.normalized())
        most_common_words = self.find_most_common_words_from_document(document)
        result_dict = {}
        for key in most_common_words.keys():
            result_dict[key] = []
            for collocation in collocations:
                if key in collocation:
                    result_dict[key].append(collocation)
        return result_dict

    def get_hierarchy_abstract(self, document: Document):
        hierarchy_dict = self.find_hierarchy(document)
        result_string = ""
        for key, values in hierarchy_dict.items():
            result_string += f"{key}\n"
            for value in values:
                result_string += f"    {' '.join(value)}\n"
        return result_string


if __name__ == "__main__":
    document = utils.get_document_by_name('eng_computer_science.html')
    abstractor = KeywordsBasedAbstract()
    print(abstractor.get_hierarchy_abstract(document))

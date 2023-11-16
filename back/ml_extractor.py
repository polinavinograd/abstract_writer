from transformers import pipeline, AutoTokenizer
import sentencepiece
import math
from langdetect import detect_langs

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer

from natural_language_utils import stop_words_rus, stop_words_eng
from document import Document
import utils

stop_words = stop_words_rus.union(stop_words_eng)


def get_abstract_summary(document: Document):
    scores = detect_langs(document.text)
    model_name = 'IlyaGusev/mbart_ru_sum_gazeta' if scores[0].lang == 'ru' else 'sshleifer/distilbart-cnn-12-6'

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model_name)

    max_token_count = 250  # Model's token limit
    tokens = tokenizer(document.text, truncation=True, padding='longest', return_tensors="pt")['input_ids'][0]

    summary_text_full = ''
    num_segments = math.ceil(len(tokens) / max_token_count)

    for i in range(num_segments):
        segment_tokens = tokens[i * max_token_count:(i + 1) * max_token_count]
        segment_text = tokenizer.decode(segment_tokens, skip_special_tokens=True)
        summary = summarizer(segment_text, max_length=250, min_length=10, do_sample=False)
        summary_text = summary[0]['summary_text']
        summary_text_full += summary_text

    return summary_text_full

# эта функция использует LSA, о принадлежности которого к машинному обучению можно поспорить
# https://cyberleninka.ru/article/n/sravnenie-nekotoryh-metodov-mashinnogo-obucheniya-dlya-analiza-tekstovyh-dokumentov/viewer -
# стр 4 сразу под рисунком - подтверждение, что LSA - метод машинного обучения
# https://ru.wikipedia.org/wiki/%D0%92%D0%B5%D1%80%D0%BE%D1%8F%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%BD%D1%8B%D0%B9_%D0%BB%D0%B0%D1%82%D0%B5%D0%BD%D1%82%D0%BD%D0%BE-%D1%81%D0%B5%D0%BC%D0%B0%D0%BD%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7
# ВЛСА - наследник ЛСА - применяется в машинном обучении
def summary_extraction(document: Document) -> str:
    parser = PlaintextParser.from_string(document.text, Tokenizer("english"))
    stemmer = Stemmer("english")

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = stop_words

    summary = summarizer(parser.document, 10)
    return ' '.join([str(sentence) for sentence in summary])


if __name__ == "__main__":
    document = utils.get_document_by_name('rus_literature.html')

    print(get_abstract_summary(document))
from transformers import pipeline
import sentencepiece
import math
from langdetect import detect_langs

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer

from natural_language_utils import stop_words_rus, stop_words_eng
from document import Document

stop_words = stop_words_rus.union(stop_words_eng)


def get_abstract_summary(document: Document):
    scores = detect_langs(document.text)
    if scores[0].lang == 'ru':
        summarizer = pipeline("summarization", model='IlyaGusev/mbart_ru_sum_gazeta')
    else:
        summarizer = pipeline("summarization")

    max_embedding = 1024*3

    summary_text_full = ''
    num = math.ceil(len(document.text) / max_embedding)
    for i in range(num):
        start = i*max_embedding
        end = (i+1)*max_embedding

        summary_text = summarizer(document.text[start:end][:1024], max_length=1024, min_length=10, do_sample=False)
        summary_text = summary_text[0]['summary_text']
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


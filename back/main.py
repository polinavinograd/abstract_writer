from sentence_extraction import SentenceExtractor
from ml_extractor import summary_extraction, get_abstract_summary

from document import Document


class ResumeFactory:
    _extractors = {}

    @staticmethod
    def get_extractor(method_type):
        if method_type not in ResumeFactory._extractors:
            if method_type == 'sentence_extraction':
                ResumeFactory._extractors[method_type] = SentenceExtractor()
            else:
                raise ValueError("Unsupported method type")

        return ResumeFactory._extractors[method_type]


def keyword_based_abstract(document: Document) -> str:
    RESUME_CREATOR = ResumeFactory.get_extractor(method_type='sentence_extraction')
    return RESUME_CREATOR.summarize_document(document)


def machine_learning_abstract(document: Document) -> str:
    return get_abstract_summary(document)

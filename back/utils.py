import os
from document import Document
from path import LOCAL_PATH


def get_file_contents(file_path: str) -> str:
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_contents = f.read()
                return file_contents
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}")


def get_document_by_name(doc_name: str) -> Document:
    for document in get_all_documents_in_folder(LOCAL_PATH + "\\docs"):
        if document.name == doc_name:
            return document


def get_subfolders_list(folder_path: str) -> 'list[str]':
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]


def get_all_documents_in_folder(path: str) -> 'list[Document]':
    documents = []
    for root, directories, files in os.walk(path):
        for filename in files:
            documents.append(Document(filename, get_file_contents(os.path.join(root, filename))))
    return documents


def save_result_to_file(result: str) -> None:
    try:
        with open("recognition_results.txt", "r+", encoding="utf-8") as f:
            f.write(result)
    except Exception as e:
        print(f"Ошибка при обработке файла: {str(e)}")



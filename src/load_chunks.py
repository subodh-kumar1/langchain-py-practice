from typing import List
from langchain.schema import Document
from langchain.text_splitter import Language
from langchain.document_loaders.parsers import LanguageParser
from langchain.document_loaders.generic import GenericLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Iterable

from const import GIT_LOCAL_DIR


####################################################################################################
# Load the code from the file path passed
####################################################################################################
def load_code(code_path, language=Language.PYTHON) -> List[Document]:
    """
    Load text from Code file
    """
    # Prepare Loader
    loader = GenericLoader.from_filesystem(
        code_path,
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser(language=language)
    )

    # Load the code files
    documents = loader.load()
    return documents


###################################################################################################
# Step 2: Split the code files in chunks
###################################################################################################
def split_code_in_chunks(document: Iterable[Document], language=Language.PYTHON):
    code_splitter = RecursiveCharacterTextSplitter.from_language(language=language,
                                                                 chunk_size=1000,
                                                                 chunk_overlap=100)
    code_chunks = code_splitter.split_documents(document)
    return code_chunks


###################################################################################################
# Step 2: Load the code files (cloned in Step 1 in local dir) from local dir and divide in chunks
###################################################################################################
def load_chunks():
    # Load all the code files downloaded from git
    documents: List[Document] = load_code(GIT_LOCAL_DIR)
    # Split the documents in chunk
    code_chunks = split_code_in_chunks(documents)
    # Add file name to page content for each chunk
    for chunk in code_chunks:
        source = chunk.metadata["source"]
        chunk.page_content = f"# File : {source} \n{chunk.page_content}"

    return code_chunks


if __name__ == "__main__":
    chunked_documents = load_chunks()
    for doc in chunked_documents:
        print("##############################################")
        print(doc)

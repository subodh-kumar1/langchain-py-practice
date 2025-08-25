import os
from typing import List

from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.indexes import SQLRecordManager, index
from langchain_elasticsearch import ElasticsearchStore

from src.const import ES_URL, INDEX_NAME, RECORD_MANAGER_DB, OPENAI_EMBEDDING_MODEL, MAX_RETRIES
from load_chunks import load_chunks


###################################################################################################
# Step 3: Save the code along with embedding in DB
###################################################################################################
def save_embedding_using_index(index_name: str, chunked_documents: List[Document]):
    """
    Convert the text in embedding and save the embedding and Metadata in DB using index.
    """
    # Initialize embedding
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, max_retries=MAX_RETRIES)

    # Initialize the vector store
    vectorstore = ElasticsearchStore(es_url=ES_URL,
                                     index_name=index_name,
                                     embedding=embeddings)

    # Define the record manager
    namespace = f"elasticsearch/{index_name}"
    record_manager = SQLRecordManager(
        namespace, db_url=f"sqlite:///{RECORD_MANAGER_DB}"
    )

    # Create the schema for record manager only when db file is newly created
    if not os.path.exists(RECORD_MANAGER_DB):
        record_manager.create_schema()

    # Update the documents in DB using index
    result = index(
        chunked_documents,
        record_manager,
        vectorstore,
        cleanup="incremental",
        source_id_key="source",
    )

    return result


if __name__ == "__main__":
    chunks = load_chunks()
    result = save_embedding_using_index(INDEX_NAME, chunks)
    print(result)
    print("Saved the data in ES DB")

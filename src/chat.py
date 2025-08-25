from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.const import ES_URL, GIT_LOCAL_DIR, INDEX_NAME, OPENAI_EMBEDDING_MODEL, OPENAI_CHAT_MODEL, MAX_RETRIES

# Initialise model
model = ChatOpenAI(temperature=0, model_name=OPENAI_CHAT_MODEL, max_retries=MAX_RETRIES)

# Initialise memory. Using K=5 to only pass last 5 messages in the chat-history.
memory = ConversationBufferWindowMemory(llm=model, memory_key="chat_history", k=5,
                                        input_key='question', output_key='answer',
                                        return_messages=True)


def initialise_chain(index_name):
    # Initialise embedding
    embedding = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, max_retries=MAX_RETRIES)

    # Initialise vector DB retriever
    es_retriever = ElasticsearchStore(
        index_name=index_name, embedding=embedding, es_url=ES_URL,
        strategy=ElasticsearchStore.ApproxRetrievalStrategy(
            hybrid=True,
        ),
    )

    # Initialise conversational retrieval chain to answer user query
    qa = ConversationalRetrievalChain.from_llm(
        model, memory=memory,
        retriever=es_retriever.as_retriever(),
        return_source_documents=True,
        verbose=True
    )
    return qa


#############################################################################################################
# Step 5: Initialise the retrieval chain with memory > ask user query > Return answers with source documents
#############################################################################################################
def query_model(query, index_name):
    qa = initialise_chain(index_name)
    response = qa.invoke({"question": query})

    source_files = set()
    for doc in response['source_documents']:
        if doc.metadata.get("source") is None:
            continue
        source_file = doc.metadata["source"].rsplit(
            GIT_LOCAL_DIR,
            maxsplit=1
        )[-1]
        source_files.add(source_file)

    return response['answer'], list(source_files)


if __name__ == "__main__":
    while True:
        question = input("Enter your question: ")
        answer, source_docs = query_model(question, INDEX_NAME)
        print(f"Answer: \n{answer}. \n\n\nSource Documents: \n{source_docs}")
        is_continue = input("Do you want to continue? (y/n): ")
        if is_continue != "y":
            break

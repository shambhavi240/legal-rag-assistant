def retrieve_documents(vector_store, query):

    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 8, "fetch_k": 20}
)

    results = retriever.invoke(query)

    return results

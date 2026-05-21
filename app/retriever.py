def retrieve_documents(vector_store, query):

    results = vector_store.similarity_search(
        query,
        k=8
    )

    return results
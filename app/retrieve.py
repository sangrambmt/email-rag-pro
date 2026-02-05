from app.embed import get_collection

def retrieve(query: str, top_k: int = 5, file_filter: str | None = None):
    collection = get_collection()

    where = None
    if file_filter:
        where = {"file": file_filter}

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    return [{"text": d, "meta": m} for d, m in zip(docs, metas)]

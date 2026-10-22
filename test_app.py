
from app import split_into_chunks


def test_chunks_keep_page_numbers():
    pages = [
        {
            "page_number": 1,
            "text": "Python is a programming language.",
        },
        {
            "page_number": 2,
            "text": "Machine learning uses data to learn patterns.",
        },
    ]

    chunks = split_into_chunks(pages)

    assert len(chunks) == 2
    assert chunks[0]["page_number"] == 1
    assert chunks[1]["page_number"] == 2
    assert all("chunk_id" in chunk for chunk in chunks)
    assert all("text" in chunk for chunk in chunks)


from app import retrieve_chunks


def test_retrieval_finds_relevant_passage():
    chunks = [
        {
            "chunk_id": 1,
            "page_number": 1,
            "text": "Python is a popular programming language.",
        },
        {
            "chunk_id": 2,
            "page_number": 2,
            "text": "Photosynthesis allows plants to convert sunlight into energy.",
        },
    ]

    results = retrieve_chunks("What is Python?", chunks)

    assert len(results) > 0
    assert results[0]["chunk_id"] == 1


def test_retrieval_returns_empty_for_no_match():
    chunks = [
        {
            "chunk_id": 1,
            "page_number": 1,
            "text": "Python is a popular programming language.",
        },
        {
            "chunk_id": 2,
            "page_number": 2,
            "text": "Photosynthesis allows plants to convert sunlight into energy.",
        },
    ]

    results = retrieve_chunks(
        "What is the capital of Antarctica?",
        chunks,
    )

    assert results == []

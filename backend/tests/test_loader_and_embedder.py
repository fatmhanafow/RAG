import os
import pytest
from backend.loader import load_txt, clean_text, chunk_text
from backend.embedder import Embedder


def test_load_txt_and_clean_and_chunk():
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'test1_embedding.txt')
    path = os.path.abspath(path)
    txt = load_txt(path)
    assert isinstance(txt, str) and len(txt) > 0

    cleaned = clean_text(txt)
    assert "\n" not in cleaned

    chunks = chunk_text(cleaned, chunk_size=50, overlap=10)
    assert isinstance(chunks, list)
    assert len(chunks) >= 1
    assert all(isinstance(c, str) for c in chunks)


def test_embedder_encode_smoke():
    e = Embedder()
    texts = ["سلام دنیا", "این یک تست است"]
    vecs = e.encode(texts, batch_size=2)
    assert len(vecs) == len(texts)
    # spot check: first vector has numeric elements
    assert hasattr(vecs[0], '__len__')
    assert len(vecs[0]) > 0

import types
import pytest

import backend.weaviate_client as wc

class DummyClientNoQuery:
    # No 'query' and no batch.add_data_object to force REST fallback
    pass

class DummyClientWithBatch:
    class Batch:
        def __init__(self):
            self.batch_size = None
        def add_data_object(self, *args, **kwargs):
            return True
    def __init__(self):
        self.batch = DummyClientWithBatch.Batch()


def test_index_chunks_rest_success(monkeypatch):
    # Ensure we take the REST path by returning a client without batch.add_data_object
    monkeypatch.setattr(wc, '_ensure_client', lambda: DummyClientNoQuery())

    # mock requests.post to succeed
    class Resp:
        def __init__(self, status):
            self.status_code = status
            self.text = ''
    monkeypatch.setattr(wc.requests, 'post', lambda url, json, timeout: Resp(201), raising=True)

    chunks = [{"id": "1", "text": "hi", "vector": [0.1, 0.2], "source": "s"}]
    assert wc.index_chunks(chunks) is True


def test_index_chunks_rest_all_transient_fail(monkeypatch):
    monkeypatch.setattr(wc, '_ensure_client', lambda: DummyClientNoQuery())

    class Resp:
        def __init__(self, status, text=''):
            self.status_code = status
            self.text = text
    def always_503(url, json, timeout):
        return Resp(503, 'service unavailable')
    monkeypatch.setattr(wc.requests, 'post', always_503, raising=True)

    chunks = [{"id": "1", "text": "hi", "vector": [0.1, 0.2], "source": "s"}]
    assert wc.index_chunks(chunks) is False


def test_query_top_k_graphql_success(monkeypatch):
    monkeypatch.setattr(wc, '_ensure_client', lambda: DummyClientNoQuery())

    class Resp:
        def __init__(self, status, json_data=None):
            self.status_code = status
            self._json = json_data or {}
            self.text = ''
        def json(self):
            return self._json

    def ok_graphql(url, json, timeout):
        return Resp(200, {"data": {"Get": {wc.CLASS_NAME: [{"text": "hello", "source": "s"}]}}})

    monkeypatch.setattr(wc.requests, 'post', ok_graphql, raising=True)

    res = wc.query_top_k([0.1, 0.2], k=1)
    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]["text"] == "hello"

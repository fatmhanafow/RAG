import io
from fastapi.testclient import TestClient
import backend.main as main


def test_upload_and_search_endpoints(monkeypatch, tmp_path):
    # stub external weaviate-related functions
    monkeypatch.setattr(main, 'create_schema', lambda: True)
    monkeypatch.setattr(main, 'index_chunks', lambda docs: True)
    monkeypatch.setattr(main, 'query_top_k', lambda v, k=5: [{'text':'dummy','source':'test'}])
    monkeypatch.setattr(main, 'is_connected', lambda: True)

    client = TestClient(main.app)

    # create a small txt file
    p = tmp_path / "small.txt"
    p.write_text("این یک متن تستی برای آپلود است.\nخط دوم.", encoding='utf-8')

    with open(p, 'rb') as f:
        files = {'file': ('small.txt', f, 'text/plain')}
        resp = client.post('/upload', files=files, data={'chunk_size': '20', 'overlap': '5'})
    assert resp.status_code == 200
    j = resp.json()
    assert j['status'] == 'ok'
    assert j['chunks_indexed'] >= 1
    assert j.get('indexed', False) is True

    # test search
    resp2 = client.post('/search', data={'q': 'تست', 'k': '3'})
    assert resp2.status_code == 200
    j2 = resp2.json()
    assert j2['query'] == 'تست'
    assert isinstance(j2['results'], list)


def test_health_endpoint(monkeypatch):
    monkeypatch.setattr(main, 'is_connected', lambda: True)
    client = TestClient(main.app)
    resp = client.get('/health')
    assert resp.status_code == 200
    j = resp.json()
    assert j.get('weaviate_connected') is True

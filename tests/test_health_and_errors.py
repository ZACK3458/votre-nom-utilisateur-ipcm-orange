import json

def test_healthz(client):
    resp = client.get('/healthz')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data.get('status') == 'ok'


def test_404(client):
    resp = client.get('/does-not-exist')
    assert resp.status_code == 404

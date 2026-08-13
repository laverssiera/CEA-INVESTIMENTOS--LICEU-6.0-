from fastapi.testclient import TestClient
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


TEST_ENGINE = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=TEST_ENGINE, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=TEST_ENGINE)


def _sqlite_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _sqlite_db

client = TestClient(app)


def test_orchestration_jobs_list() -> None:
    response = client.get('/api/orchestration/jobs')
    assert response.status_code == 200
    body = response.json()
    assert 'items' in body
    assert 'priorities' in body
    assert 'priority_1' in body['priorities']


def test_decision_engine_endpoints() -> None:
    allocation = client.post('/ml/allocation/auto', json={'amount': 90000, 'profile': 'moderado', 'risk_level': 50})
    assert allocation.status_code == 200
    assert 'strategy' in allocation.json()

    pre_credit = client.post('/ml/credit/pre-approval', json={'score': 710, 'ltv': 0.7, 'risk_flag': False})
    assert pre_credit.status_code == 200
    assert 'approved' in pre_credit.json()

    rebalance = client.post('/ml/rebalance', json={'exposure_by_asset': {'caixa': 20, 'fundo_di': 30, 'debentures': 50}})
    assert rebalance.status_code == 200
    assert 'action' in rebalance.json()

    alerts = client.get('/ml/alerts')
    assert alerts.status_code == 200
    assert isinstance(alerts.json().get('items'), list)


def test_autopilot_pipeline_populates_logs() -> None:
    run_result = client.post('/api/orchestration/run/autopilot_pipeline')
    assert run_result.status_code == 200
    assert run_result.json().get('status') == 'completed'

    logs = client.get('/api/orchestration/logs')
    assert logs.status_code == 200
    assert len(logs.json().get('items', [])) >= 1

    events = client.get('/api/orchestration/events')
    assert events.status_code == 200
    assert isinstance(events.json().get('items'), list)

    notifications = client.get('/api/notifications/logs')
    assert notifications.status_code == 200
    assert isinstance(notifications.json().get('items'), list)


def test_interplanetary_ecosystem_catalog() -> None:
    response = client.get('/interplanetary/ecosystem')
    assert response.status_code == 200
    body = response.json()
    assert body.get('count') == 7
    assert isinstance(body.get('items'), list)
    assert all('status' in item for item in body.get('items', []))
    assert all('active' in item for item in body.get('items', []))
    names = {item.get('name') for item in body.get('items', [])}
    assert {
        'CEA',
        'Interplanetary Bank',
        'Interplanetary Investment',
        'Space Exchange',
        'Patent Exchange',
        'Technology Exchange',
        'Space Insurance',
    }.issubset(names)


def test_interplanetary_domain_activation() -> None:
    forbidden = client.post('/interplanetary/ecosystem/space-exchange/activate', headers={'x-interplanetary-role': 'colaborador'})
    assert forbidden.status_code == 403

    response = client.post('/interplanetary/ecosystem/space-exchange/activate', headers={'x-interplanetary-role': 'admin'})
    assert response.status_code == 200
    body = response.json()
    assert body.get('status') == 'activated'
    assert body.get('domain_id') == 'space-exchange'
    assert body.get('event') == 'cea.interplanetary.domain.activated'

    domain = client.get('/interplanetary/ecosystem/space-exchange')
    assert domain.status_code == 200
    data = domain.json()
    assert data.get('status') == 'active'
    assert data.get('active') is True
    assert data.get('last_activation_at')

    documents = client.get('/api/documents/logs')
    assert documents.status_code == 200
    assert isinstance(documents.json().get('items'), list)

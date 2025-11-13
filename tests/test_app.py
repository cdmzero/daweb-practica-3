import pytest
import json
from app import app as flask_app


def test_home_ok():
    flask_app.testing = True
    client = flask_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


@pytest.fixture
def client():
    flask_app.testing = True
    return flask_app.test_client()


import app as app_module


def test_homepage_renders():
    app = app_module.app
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200
    assert b"Mini To-Do" in r.data


def test_crear_tarea_api():
    app_module.TAREAS.clear()
    app = app_module.app
    client = app.test_client()

    r = client.post("/api/tareas", json={"texto": "Probar test"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["ok"] is True
    assert data["data"]["texto"] == "Probar test"

    r = client.get("/api/tareas")
    listado = r.get_json()["data"]
    assert len(listado) == 1
    assert listado[0]["texto"] == "Probar test"

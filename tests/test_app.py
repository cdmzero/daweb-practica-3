import pytest
import json
from app import app as flask_app


def test_home_ok():
    """Verifica que la ruta principal responde correctamente."""
    flask_app.testing = True
    client = flask_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba."""
    flask_app.testing = True
    return flask_app.test_client()


import app as app_module


def test_homepage_renders():
    """Verifica que la página principal renderiza correctamente."""
    app = app_module.app
    client = app.test_client()
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert b"Mini To-Do" in respuesta.data


def test_crear_tarea_api():
    """Verifica que la API de creación de tareas funciona."""
    app_module.TAREAS.clear()
    app = app_module.app
    client = app.test_client()

    respuesta = client.post("/api/tareas", json={"texto": "Probar test"})
    assert respuesta.status_code == 201
    datos = respuesta.get_json()
    assert datos["ok"] is True
    assert datos["data"]["texto"] == "Probar test"

    respuesta = client.get("/api/tareas")
    listado = respuesta.get_json()["data"]
    assert len(listado) == 1
    assert listado[0]["texto"] == "Probar test"

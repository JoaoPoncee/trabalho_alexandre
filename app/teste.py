import pytest
from flask import Flask
from app.crudOrderDetails import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)

    return mock_cursor

def test_create_order_detail(client, mock_db):
    response = client.post('/order-details', json={
        'order_id': 1,
        'product_id': 1,
        'unit_price': 10.0,
        'quantity': 2,
        'discount': 0.1
    })
    assert response.status_code == 201
    assert response.json == {"message": "Order detail created successfully"}
    mock_db.execute.assert_called_once()  # Verifica se foi chamada a inserção no banco

def test_read_order_detail(client, mock_db):
    mock_db.fetchone.return_value = (1, 1, 10.0, 2, 0.1)
    
    response = client.get('/order-details/1/1')
    assert response.status_code == 200
    assert response.json == {
        "order_id": 1,
        "product_id": 1,
        "unit_price": 10.0,
        "quantity": 2,
        "discount": 0.1
    }
    mock_db.execute.assert_called_once()

def test_update_order_detail(client, mock_db):
    response = client.put('/order-details/1/1', json={
        'unit_price': 12.0,
        'quantity': 3,
        'discount': 0.2
    })
    assert response.status_code == 200
    assert response.json == {"message": "Order detail updated successfully"}
    mock_db.execute.assert_called_once()

def test_delete_order_detail(client, mock_db):
    response = client.delete('/order-details/1/1')
    assert response.status_code == 200
    assert response.json == {"message": "Order detail deleted successfully"}
    mock_db.execute.assert_called_once()

def test_list_order_details(client, mock_db):
    mock_db.fetchall.return_value = [(1, 1, 10.0, 2, 0.1)]

    response = client.get('/order-details/1')
    assert response.status_code == 200
    assert response.json == [{
        "order_id": 1,
        "product_id": 1,
        "unit_price": 10.0,
        "quantity": 2,
        "discount": 0.1
    }]
    mock_db.execute.assert_called_once()

from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection
from flasgger import swag_from
from app.swagger import order_details_docs

app = Blueprint('order_details', __name__)

@app.route('/')
def index():
    return "API para gerenciamento de detalhes de pedidos"

@app.route('/order-details', methods=['POST'])
@swag_from(order_details_docs['create_order_detail'])
def create_order_detail():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['order_id'], data['product_id'], data['unit_price'], 
             data['quantity'], data.get('discount', 0.0))
        )
        conn.commit()
        return jsonify({"message": "Order detail created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/order-details', methods=['GET'])
def get_order_details():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_details")
    order_details = cursor.fetchall()
    return jsonify(order_details), 200

@app.route('/order-details/<int:order_id>/<int:product_id>', methods=['GET'])
@swag_from(order_details_docs['read_order_detail'])
def read_order_detail(order_id, product_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT order_id, product_id, unit_price, quantity, discount 
            FROM order_details 
            WHERE order_id = %s AND product_id = %s
        """, (order_id, product_id))
        order_detail = cursor.fetchone()
        
        if order_detail is None:
            return jsonify({"error": "Order detail not found"}), 404
            
        return jsonify({
            "order_id": order_detail[0],
            "product_id": order_detail[1],
            "unit_price": float(order_detail[2]),
            "quantity": order_detail[3],
            "discount": float(order_detail[4])
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/order-details/<int:order_id>/<int:product_id>', methods=['PUT'])
@swag_from(order_details_docs['update_order_detail'])
def update_order_detail(order_id, product_id):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE order_details
            SET unit_price = %s, quantity = %s, discount = %s
            WHERE order_id = %s AND product_id = %s
            """,
            (data['unit_price'], data['quantity'], 
             data.get('discount', 0.0), order_id, product_id)
        )
        conn.commit()
        return jsonify({"message": "Order detail updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/order-details/<int:order_id>/<int:product_id>', methods=['DELETE'])
@swag_from(order_details_docs['delete_order_detail'])
def delete_order_detail(order_id, product_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM order_details 
            WHERE order_id = %s AND product_id = %s
        """, (order_id, product_id))
        conn.commit()
        return jsonify({"message": "Order detail deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Endpoint adicional para listar todos os detalhes de um pedido específico
@app.route('/order-details/<int:order_id>', methods=['GET'])
@swag_from(order_details_docs['list_order_details'])
def list_order_details(order_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT order_id, product_id, unit_price, quantity, discount 
            FROM order_details 
            WHERE order_id = %s
        """, (order_id,))
        order_details = cursor.fetchall()
        
        if not order_details:
            return jsonify({"error": "No order details found for this order"}), 404
            
        return jsonify([{
            "order_id": detail[0],
            "product_id": detail[1],
            "unit_price": float(detail[2]),
            "quantity": detail[3],
            "discount": float(detail[4])
        } for detail in order_details]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

 
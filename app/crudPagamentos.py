from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection
from flasgger import swag_from
from app.swagger import pagamentos_docs

pagamentos_bp = Blueprint('pagamentos', __name__)

@pagamentos_bp.route('/pagamentos', methods=['POST'])
@swag_from(pagamentos_docs['create_pagamento'])
def create_pagamento():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor_pago'], 
             data.get('forma_pagamento'), data.get('referencia'), data.get('status'))
        )
        conn.commit()
        return jsonify({"message": "Pagamento criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@pagamentos_bp.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
@swag_from(pagamentos_docs['read_pagamento'])
def read_pagamento(id_pagamento):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        pagamento = cursor.fetchone()
        if pagamento is None:
            return jsonify({"error": "Pagamento não encontrado"}), 404
        return jsonify({
            "id_pagamento": pagamento[0],
            "id_aluno": pagamento[1],
            "data_pagamento": pagamento[2],
            "valor_pago": pagamento[3],
            "forma_pagamento": pagamento[4],
            "referencia": pagamento[5],
            "status": pagamento[6]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@pagamentos_bp.route('/pagamentos', methods=['GET'])
@swag_from(pagamentos_docs['read_all_pagamentos'])
def read_all_pagamentos():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pagamento ORDER BY data_pagamento")
        pagamentos = cursor.fetchall()
        
        result = []
        for pagamento in pagamentos:
            result.append({
                "id_pagamento": pagamento[0],
                "id_aluno": pagamento[1],
                "data_pagamento": pagamento[2],
                "valor_pago": pagamento[3],
                "forma_pagamento": pagamento[4],
                "referencia": pagamento[5],
                "status": pagamento[6]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@pagamentos_bp.route('/pagamentos/<int:id_pagamento>', methods=['PUT'])
@swag_from(pagamentos_docs['update_pagamento'])
def update_pagamento(id_pagamento):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE pagamento
            SET id_aluno = %s, data_pagamento = %s, valor_pago = %s, forma_pagamento = %s, referencia = %s, status = %s
            WHERE id_pagamento = %s
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor_pago'], 
             data.get('forma_pagamento'), data.get('referencia'), data.get('status'), id_pagamento)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Pagamento não encontrado"}), 404
        return jsonify({"message": "Pagamento atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@pagamentos_bp.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
@swag_from(pagamentos_docs['delete_pagamento'])
def delete_pagamento(id_pagamento):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pagamento WHERE id_pagamento = %s", (id_pagamento,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Pagamento não encontrado"}), 404
        return jsonify({"message": "Pagamento deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close() 
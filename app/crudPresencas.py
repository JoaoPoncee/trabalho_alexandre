from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection
from flasgger import swag_from
from app.swagger import presencas_docs

presencas_bp = Blueprint('presencas', __name__)

@presencas_bp.route('/presencas', methods=['POST'])
@swag_from(presencas_docs['create_presenca'])
def create_presenca():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO presenca (id_aluno, data_presenca, presente)
            VALUES (%s, %s, %s)
            """,
            (data['id_aluno'], data['data_presenca'], data['presente'])
        )
        conn.commit()
        return jsonify({"message": "Presença criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@presencas_bp.route('/presencas/<int:id_presenca>', methods=['GET'])
@swag_from(presencas_docs['read_presenca'])
def read_presenca(id_presenca):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM presenca WHERE id_presenca = %s", (id_presenca,))
        presenca = cursor.fetchone()
        if presenca is None:
            return jsonify({"error": "Presença não encontrada"}), 404
        return jsonify({
            "id_presenca": presenca[0],
            "id_aluno": presenca[1],
            "data_presenca": presenca[2],
            "presente": presenca[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@presencas_bp.route('/presencas', methods=['GET'])
@swag_from(presencas_docs['read_all_presencas'])
def read_all_presencas():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM presenca ORDER BY data_presenca")
        presencas = cursor.fetchall()
        
        result = []
        for presenca in presencas:
            result.append({
                "id_presenca": presenca[0],
                "id_aluno": presenca[1],
                "data_presenca": presenca[2],
                "presente": presenca[3]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@presencas_bp.route('/presencas/<int:id_presenca>', methods=['PUT'])
@swag_from(presencas_docs['update_presenca'])
def update_presenca(id_presenca):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE presenca
            SET id_aluno = %s, data_presenca = %s, presente = %s
            WHERE id_presenca = %s
            """,
            (data['id_aluno'], data['data_presenca'], data['presente'], id_presenca)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Presença não encontrada"}), 404
        return jsonify({"message": "Presença atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@presencas_bp.route('/presencas/<int:id_presenca>', methods=['DELETE'])
@swag_from(presencas_docs['delete_presenca'])
def delete_presenca(id_presenca):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM presenca WHERE id_presenca = %s", (id_presenca,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Presença não encontrada"}), 404
        return jsonify({"message": "Presença deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close() 
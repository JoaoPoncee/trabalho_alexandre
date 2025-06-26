from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection
from flasgger import swag_from
from app.swagger import atividades_docs

atividades_bp = Blueprint('atividades', __name__)

@atividades_bp.route('/atividades', methods=['POST'])
@swag_from(atividades_docs['create_atividade'])
def create_atividade():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividade (descricao, data_realizacao)
            VALUES (%s, %s)
            """,
            (data['descricao'], data['data_realizacao'])
        )
        conn.commit()
        return jsonify({"message": "Atividade criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@atividades_bp.route('/atividades/<int:id_atividade>', methods=['GET'])
@swag_from(atividades_docs['read_atividade'])
def read_atividade(id_atividade):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade WHERE id_atividade = %s", (id_atividade,))
        atividade = cursor.fetchone()
        if atividade is None:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade[0],
            "descricao": atividade[1],
            "data_realizacao": atividade[2]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@atividades_bp.route('/atividades', methods=['GET'])
@swag_from(atividades_docs['read_all_atividades'])
def read_all_atividades():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade ORDER BY data_realizacao")
        atividades = cursor.fetchall()
        
        result = []
        for atividade in atividades:
            result.append({
                "id_atividade": atividade[0],
                "descricao": atividade[1],
                "data_realizacao": atividade[2]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@atividades_bp.route('/atividades/<int:id_atividade>', methods=['PUT'])
@swag_from(atividades_docs['update_atividade'])
def update_atividade(id_atividade):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE atividade
            SET descricao = %s, data_realizacao = %s
            WHERE id_atividade = %s
            """,
            (data['descricao'], data['data_realizacao'], id_atividade)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({"message": "Atividade atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@atividades_bp.route('/atividades/<int:id_atividade>', methods=['DELETE'])
@swag_from(atividades_docs['delete_atividade'])
def delete_atividade(id_atividade):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM atividade WHERE id_atividade = %s", (id_atividade,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({"message": "Atividade deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close() 
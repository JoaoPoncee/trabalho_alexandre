from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection
from flasgger import swag_from
from app.swagger import turmas_docs

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/turmas', methods=['POST'])
@swag_from(turmas_docs['create_turma'])
def create_turma():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO turma (nome_turma, id_professor, horario)
            VALUES (%s, %s, %s)
            """,
            (data['nome_turma'], data.get('id_professor'), data.get('horario'))
        )
        conn.commit()
        return jsonify({"message": "Turma criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@turmas_bp.route('/turmas/<int:id_turma>', methods=['GET'])
@swag_from(turmas_docs['read_turma'])
def read_turma(id_turma):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM turma WHERE id_turma = %s", (id_turma,))
        turma = cursor.fetchone()
        if turma is None:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({
            "id_turma": turma[0],
            "nome_turma": turma[1],
            "id_professor": turma[2],
            "horario": turma[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@turmas_bp.route('/turmas', methods=['GET'])
@swag_from(turmas_docs['read_all_turmas'])
def read_all_turmas():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM turma ORDER BY nome_turma")
        turmas = cursor.fetchall()
        
        result = []
        for turma in turmas:
            result.append({
                "id_turma": turma[0],
                "nome_turma": turma[1],
                "id_professor": turma[2],
                "horario": turma[3]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@turmas_bp.route('/turmas/<int:id_turma>', methods=['PUT'])
@swag_from(turmas_docs['update_turma'])
def update_turma(id_turma):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE turma
            SET nome_turma = %s, id_professor = %s, horario = %s
            WHERE id_turma = %s
            """,
            (data['nome_turma'], data.get('id_professor'), data.get('horario'), id_turma)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({"message": "Turma atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@turmas_bp.route('/turmas/<int:id_turma>', methods=['DELETE'])
@swag_from(turmas_docs['delete_turma'])
def delete_turma(id_turma):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM turma WHERE id_turma = %s", (id_turma,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({"message": "Turma deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close() 
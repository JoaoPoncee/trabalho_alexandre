from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection
from flasgger import swag_from
from app.swagger import atividades_alunos_docs

atividades_alunos_bp = Blueprint('atividades_alunos', __name__)

# CRUD para atividade_aluno
@atividades_alunos_bp.route('/atividades_alunos', methods=['POST'])
@swag_from(atividades_alunos_docs['create_atividade_aluno'])
def create_atividade_aluno():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividade_aluno (id_atividade, id_aluno)
            VALUES (%s, %s)
            """,
            (data['id_atividade'], data['id_aluno'])
        )
        conn.commit()
        return jsonify({"message": "Atividade-Aluno criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@atividades_alunos_bp.route('/atividades_alunos/<int:id_atividade>/<int:id_aluno>', methods=['GET'])
@swag_from(atividades_alunos_docs['read_atividade_aluno'])
def read_atividade_aluno(id_atividade, id_aluno):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s", (id_atividade, id_aluno))
        atividade_aluno = cursor.fetchone()
        if atividade_aluno is None:
            return jsonify({"error": "Atividade-Aluno não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade_aluno[0],
            "id_aluno": atividade_aluno[1]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@atividades_alunos_bp.route('/atividades_alunos', methods=['GET'])
@swag_from(atividades_alunos_docs['read_all_atividades_alunos'])
def read_all_atividades_alunos():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade_aluno")
        atividades_alunos = cursor.fetchall()
        
        result = []
        for atividade_aluno in atividades_alunos:
            result.append({
                "id_atividade": atividade_aluno[0],
                "id_aluno": atividade_aluno[1]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@atividades_alunos_bp.route('/atividades_alunos/<int:id_atividade>/<int:id_aluno>', methods=['DELETE'])
@swag_from(atividades_alunos_docs['delete_atividade_aluno'])
def delete_atividade_aluno(id_atividade, id_aluno):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s", (id_atividade, id_aluno))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Atividade-Aluno não encontrada"}), 404
        return jsonify({"message": "Atividade-Aluno deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close() 
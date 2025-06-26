from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection
from flasgger import swag_from
from app.swagger import alunos_docs

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/alunos', methods=['POST'])
@swag_from(alunos_docs['create_aluno'])
def create_aluno():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO aluno (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais, endereco, cidade, estado, cep, pais, telefone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data['nome_completo'], data['data_nascimento'], data.get('id_turma'), data.get('nome_responsavel'), 
             data.get('telefone_responsavel'), data.get('email_responsavel'), data.get('informacoes_adicionais'),
             data.get('endereco'), data.get('cidade'), data.get('estado'), data.get('cep'), data.get('pais'), data.get('telefone'))
        )
        conn.commit()
        return jsonify({"message": "Aluno criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['GET'])
@swag_from(alunos_docs['read_aluno'])
def read_aluno(id_aluno):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM aluno WHERE id_aluno = %s", (id_aluno,))
        aluno = cursor.fetchone()
        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify({
            "id_aluno": aluno[0],
            "nome_completo": aluno[1],
            "data_nascimento": aluno[2],
            "id_turma": aluno[3],
            "nome_responsavel": aluno[4],
            "telefone_responsavel": aluno[5],
            "email_responsavel": aluno[6],
            "informacoes_adicionais": aluno[7],
            "endereco": aluno[8],
            "cidade": aluno[9],
            "estado": aluno[10],
            "cep": aluno[11],
            "pais": aluno[12],
            "telefone": aluno[13]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@alunos_bp.route('/alunos', methods=['GET'])
@swag_from(alunos_docs['read_all_alunos'])
def read_all_alunos():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM aluno ORDER BY nome_completo")
        alunos = cursor.fetchall()
        
        result = []
        for aluno in alunos:
            result.append({
                "id_aluno": aluno[0],
                "nome_completo": aluno[1],
                "data_nascimento": aluno[2],
                "id_turma": aluno[3],
                "nome_responsavel": aluno[4],
                "telefone_responsavel": aluno[5],
                "email_responsavel": aluno[6],
                "informacoes_adicionais": aluno[7],
                "endereco": aluno[8],
                "cidade": aluno[9],
                "estado": aluno[10],
                "cep": aluno[11],
                "pais": aluno[12],
                "telefone": aluno[13]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['PUT'])
@swag_from(alunos_docs['update_aluno'])
def update_aluno(id_aluno):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE aluno
            SET nome_completo = %s, data_nascimento = %s, id_turma = %s, nome_responsavel = %s, telefone_responsavel = %s, email_responsavel = %s, informacoes_adicionais = %s, endereco = %s, cidade = %s, estado = %s, cep = %s, pais = %s, telefone = %s
            WHERE id_aluno = %s
            """,
            (data['nome_completo'], data['data_nascimento'], data.get('id_turma'), data.get('nome_responsavel'),
             data.get('telefone_responsavel'), data.get('email_responsavel'), data.get('informacoes_adicionais'),
             data.get('endereco'), data.get('cidade'), data.get('estado'), data.get('cep'), data.get('pais'), data.get('telefone'), id_aluno)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify({"message": "Aluno atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['DELETE'])
@swag_from(alunos_docs['delete_aluno'])
def delete_aluno(id_aluno):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM aluno WHERE id_aluno = %s", (id_aluno,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify({"message": "Aluno deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

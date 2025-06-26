from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection
from flasgger import swag_from
from app.swagger import usuarios_docs

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['POST'])
@swag_from(usuarios_docs['create_usuario'])
def create_usuario():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO usuario (login, senha, nivel_acesso, id_professor)
            VALUES (%s, %s, %s, %s)
            """,
            (data['login'], data['senha'], data.get('nivel_acesso'), data.get('id_professor'))
        )
        conn.commit()
        return jsonify({"message": "Usuário criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
@swag_from(usuarios_docs['read_usuario'])
def read_usuario(id_usuario):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        if usuario is None:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify({
            "id_usuario": usuario[0],
            "login": usuario[1],
            "senha": usuario[2],
            "nivel_acesso": usuario[3],
            "id_professor": usuario[4]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@usuarios_bp.route('/usuarios', methods=['GET'])
@swag_from(usuarios_docs['read_all_usuarios'])
def read_all_usuarios():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        
        result = []
        for usuario in usuarios:
            result.append({
                "id_usuario": usuario[0],
                "login": usuario[1],
                "senha": usuario[2],
                "nivel_acesso": usuario[3],
                "id_professor": usuario[4]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@swag_from(usuarios_docs['update_usuario'])
def update_usuario(id_usuario):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE usuario
            SET login = %s, senha = %s, nivel_acesso = %s, id_professor = %s
            WHERE id_usuario = %s
            """,
            (data['login'], data['senha'], data.get('nivel_acesso'), data.get('id_professor'), id_usuario)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
@swag_from(usuarios_docs['delete_usuario'])
def delete_usuario(id_usuario):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close() 
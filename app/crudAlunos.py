from flask import Blueprint, request, jsonify
from app.Util.bd import create_connection

app = Blueprint('alunos', __name__)

@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO alunos (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data['aluno_id'], data['nome'], data.get('endereco'), data.get('cidade'), 
             data.get('estado'), data.get('cep'), data.get('pais'), data.get('telefone'))
        )
        conn.commit()
        return jsonify({"message": "Aluno criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<string:aluno_id>', methods=['GET'])
def read_aluno(aluno_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM alunos WHERE aluno_id = %s", (aluno_id,))
        aluno = cursor.fetchone()
        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify({
            "aluno_id": aluno[0],
            "nome": aluno[1],
            "endereco": aluno[2],
            "cidade": aluno[3],
            "estado": aluno[4],
            "cep": aluno[5],
            "pais": aluno[6],
            "telefone": aluno[7]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos', methods=['GET'])
def read_all_alunos():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM alunos ORDER BY nome")
        alunos = cursor.fetchall()
        
        result = []
        for aluno in alunos:
            result.append({
                "aluno_id": aluno[0],
                "nome": aluno[1],
                "endereco": aluno[2],
                "cidade": aluno[3],
                "estado": aluno[4],
                "cep": aluno[5],
                "pais": aluno[6],
                "telefone": aluno[7]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<string:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE alunos
            SET nome = %s, endereco = %s, cidade = %s, estado = %s, cep = %s, pais = %s, telefone = %s
            WHERE aluno_id = %s
            """,
            (data['nome'], data.get('endereco'), data.get('cidade'), data.get('estado'),
             data.get('cep'), data.get('pais'), data.get('telefone'), aluno_id)
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

@app.route('/alunos/<string:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM alunos WHERE aluno_id = %s", (aluno_id,))
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

app = Blueprint('turmas', __name__)

@app.route('/turmas', methods=['POST'])
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

@app.route('/turmas/<int:id_turma>', methods=['GET'])
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

@app.route('/turmas', methods=['GET'])
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

@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Turma
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

@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Turma WHERE id_turma = %s", (id_turma,))
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

app = Blueprint('professores', __name__)

@app.route('/professores', methods=['POST'])
def create_professor():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Professor (nome_completo, email, telefone)
            VALUES (%s, %s, %s)
            """,
            (data['nome_completo'], data.get('email'), data.get('telefone'))
        )
        conn.commit()
        return jsonify({"message": "Professor criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['GET'])
def read_professor(id_professor):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Professor WHERE id_professor = %s", (id_professor,))
        professor = cursor.fetchone()
        if professor is None:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({
            "id_professor": professor[0],
            "nome_completo": professor[1],
            "email": professor[2],
            "telefone": professor[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores', methods=['GET'])
def read_all_professores():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Professor ORDER BY nome_completo")
        professores = cursor.fetchall()
        
        result = []
        for professor in professores:
            result.append({
                "id_professor": professor[0],
                "nome_completo": professor[1],
                "email": professor[2],
                "telefone": professor[3]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Professor
            SET nome_completo = %s, email = %s, telefone = %s
            WHERE id_professor = %s
            """,
            (data['nome_completo'], data.get('email'), data.get('telefone'), id_professor)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({"message": "Professor atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Professor WHERE id_professor = %s", (id_professor,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({"message": "Professor deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

app = Blueprint('pagamentos', __name__)

@app.route('/pagamentos', methods=['POST'])
def create_pagamento():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status)
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

@app.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
def read_pagamento(id_pagamento):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
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

@app.route('/pagamentos', methods=['GET'])
def read_all_pagamentos():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Pagamento ORDER BY data_pagamento")
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

@app.route('/pagamentos/<int:id_pagamento>', methods=['PUT'])
def update_pagamento(id_pagamento):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Pagamento
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

@app.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
def delete_pagamento(id_pagamento):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
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

app = Blueprint('presencas', __name__)

@app.route('/presencas', methods=['POST'])
def create_presenca():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Presenca (id_aluno, data_presenca, presente)
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

@app.route('/presencas/<int:id_presenca>', methods=['GET'])
def read_presenca(id_presenca):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Presenca WHERE id_presenca = %s", (id_presenca,))
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

@app.route('/presencas', methods=['GET'])
def read_all_presencas():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Presenca ORDER BY data_presenca")
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

@app.route('/presencas/<int:id_presenca>', methods=['PUT'])
def update_presenca(id_presenca):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Presenca
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

@app.route('/presencas/<int:id_presenca>', methods=['DELETE'])
def delete_presenca(id_presenca):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Presenca WHERE id_presenca = %s", (id_presenca,))
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

app = Blueprint('atividades', __name__)

@app.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Atividade (descricao, data_realizacao)
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

@app.route('/atividades/<int:id_atividade>', methods=['GET'])
def read_atividade(id_atividade):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade WHERE id_atividade = %s", (id_atividade,))
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

@app.route('/atividades', methods=['GET'])
def read_all_atividades():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade ORDER BY data_realizacao")
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

@app.route('/atividades/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Atividade
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

@app.route('/atividades/<int:id_atividade>', methods=['DELETE'])
def delete_atividade(id_atividade):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Atividade WHERE id_atividade = %s", (id_atividade,))
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

app = Blueprint('atividades_alunos', __name__)

# CRUD para Atividade_Aluno
@app.route('/atividades_alunos', methods=['POST'])
def create_atividade_aluno():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Atividade_Aluno (id_atividade, id_aluno)
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

@app.route('/atividades_alunos/<int:id_atividade>/<int:id_aluno>', methods=['GET'])
def read_atividade_aluno(id_atividade, id_aluno):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade_Aluno WHERE id_atividade = %s AND id_aluno = %s", (id_atividade, id_aluno))
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

@app.route('/atividades_alunos', methods=['GET'])
def read_all_atividades_alunos():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade_Aluno")
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

@app.route('/atividades_alunos/<int:id_atividade>/<int:id_aluno>', methods=['DELETE'])
def delete_atividade_aluno(id_atividade, id_aluno):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Atividade_Aluno WHERE id_atividade = %s AND id_aluno = %s", (id_atividade, id_aluno))
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

app = Blueprint('usuarios', __name__)

@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Usuario (login, senha, nivel_acesso, id_professor)
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

@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def read_usuario(id_usuario):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Usuario WHERE id_usuario = %s", (id_usuario,))
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

@app.route('/usuarios', methods=['GET'])
def read_all_usuarios():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Usuario")
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

@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def update_usuario(id_usuario):
    data = request.get_json()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Usuario
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

@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
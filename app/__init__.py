# Arquivo __init__.py para tornar a pasta app um pacote Python.
from flask import Flask, jsonify, redirect

def create_app():
    app = Flask(__name__)
    
    # Registrar todos os blueprints dos CRUDs
    from app.crudAlunos import alunos_bp
    from app.crudTurmas import turmas_bp
    from app.crudProfessores import professores_bp
    from app.crudPagamentos import pagamentos_bp
    from app.crudPresencas import presencas_bp
    from app.crudAtividades import atividades_bp
    from app.crudAtividadesAlunos import atividades_alunos_bp
    from app.crudUsuarios import usuarios_bp
    from app.crudCateg import app as categories_app
    from app.crudOrderDetails import app as order_details_app
    
    app.register_blueprint(alunos_bp)
    app.register_blueprint(turmas_bp)
    app.register_blueprint(professores_bp)
    app.register_blueprint(pagamentos_bp)
    app.register_blueprint(presencas_bp)
    app.register_blueprint(atividades_bp)
    app.register_blueprint(atividades_alunos_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categories_app)
    app.register_blueprint(order_details_app)
    
    # Inicializar Swagger para documentação da API
    from app.swagger import init_swagger
    init_swagger(app)
    
    return app 
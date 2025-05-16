-- Tabela de Professores
-- Cada professor pode estar vinculado a várias turmas (1:N)
CREATE TABLE professor (
    id_professor INTEGER PRIMARY KEY, -- Identificador único do professor
    nome_completo VARCHAR(255) NOT NULL, -- Nome completo do professor
    email VARCHAR(100), -- E-mail do professor
    telefone VARCHAR(20) -- Telefone de contato do professor
);

-- Tabela de Turmas
-- Relacionamento: professor (1) --- (N) turma
CREATE TABLE turma (
    id_turma INTEGER PRIMARY KEY, -- Identificador único da turma
    nome_turma VARCHAR(50) NOT NULL, -- Nome da turma
    id_professor INTEGER, -- FK: cada turma pertence a um professor (1:N)
    horario VARCHAR(100), -- Horário das aulas
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor) -- FK para professor
);

-- Tabela de Alunos
-- Relacionamento: turma (1) --- (N) aluno
CREATE TABLE aluno (
    id_aluno INTEGER PRIMARY KEY, -- Identificador único do aluno
    nome_completo VARCHAR(255) NOT NULL, -- Nome completo do aluno
    data_nascimento DATE NOT NULL, -- Data de nascimento
    id_turma INTEGER, -- FK: cada aluno pertence a uma turma (1:N)
    nome_responsavel VARCHAR(255), -- Nome do responsável
    telefone_responsavel VARCHAR(20), -- Telefone do responsável
    email_responsavel VARCHAR(100), -- E-mail do responsável
    informacoes_adicionais TEXT, -- Observações adicionais
    endereco VARCHAR(255), -- Endereço do aluno
    cidade VARCHAR(100),
    estado VARCHAR(100),
    cep VARCHAR(20),
    pais VARCHAR(100),
    telefone VARCHAR(20), -- Telefone do aluno
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma) -- FK para turma
);

-- Tabela de Pagamentos
-- Relacionamento: aluno (1) --- (N) pagamento
CREATE TABLE pagamento (
    id_pagamento INTEGER PRIMARY KEY, -- Identificador do pagamento
    id_aluno INTEGER, -- FK: cada pagamento está associado a um aluno (1:N)
    data_pagamento DATE NOT NULL, -- Data do pagamento
    valor_pago DECIMAL(10, 2) NOT NULL, -- Valor pago
    forma_pagamento VARCHAR(50), -- Forma de pagamento (dinheiro, cartão, etc)
    referencia VARCHAR(100), -- Referência ou observação
    status VARCHAR(20), -- Status (pago, pendente)
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) -- FK para aluno
);

-- Tabela de Presenças
-- Relacionamento: aluno (1) --- (N) presenca
CREATE TABLE presenca (
    id_presenca INTEGER PRIMARY KEY, -- Identificador da presença
    id_aluno INTEGER, -- FK: cada presença está vinculada a um aluno (1:N)
    data_presenca DATE NOT NULL, -- Data da presença
    presente BOOLEAN, -- Indica se o aluno esteve presente (true/false)
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) -- FK para aluno
);

-- Tabela de Atividades
-- Lista de atividades realizadas na instituição
CREATE TABLE atividade (
    id_atividade INTEGER PRIMARY KEY, -- Identificador da atividade
    descricao TEXT NOT NULL, -- Descrição da atividade
    data_realizacao DATE NOT NULL -- Data em que a atividade foi realizada
);

-- Tabela de Relacionamento Aluno-Atividade (N:N)
-- Relacionamento: atividade (N) --- (N) aluno
CREATE TABLE atividade_aluno (
    id_atividade INTEGER, -- FK: vincula uma atividade a um aluno
    id_aluno INTEGER, -- FK: vincula um aluno a uma atividade
    PRIMARY KEY (id_atividade, id_aluno), -- Chave composta (atividade + aluno)
    FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade), -- FK para atividade
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) -- FK para aluno
);

-- Tabela de Usuários do Sistema
-- Relacionamento: professor (1) --- (N) usuario (opcional, para acesso)
CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY, -- Identificador do usuário
    login VARCHAR(50) UNIQUE NOT NULL, -- Nome de login (único)
    senha VARCHAR(255) NOT NULL, -- Senha do usuário (hash)
    nivel_acesso VARCHAR(20), -- Nível de acesso (admin, professor, etc)
    id_professor INTEGER, -- FK: usuário pode ser vinculado a um professor (1:N)
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor) -- FK
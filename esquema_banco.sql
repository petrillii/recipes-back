-- to do: tb_status_funcionario
CREATE TABLE tb_status_funcionario(
	id_status_funcionario			INTEGER,
	descricao_status_funcionario	VARCHAR(20),
	CONSTRAINT tb_status_func_id_status_func PRIMARY KEY (id_status_funcionario)
);

-- tb_endereco
CREATE TABLE tb_endereco(
	id_endereco				INTEGER,
	cep						VARCHAR(9),
	logradouro				VARCHAR(60),
	cidade					VARCHAR(20),
	estado					VARCHAR(2),
	bairro					VARCHAR(20),
	complemento				VARCHAR(20),
	numero					VARCHAR(10),
	observacao				VARCHAR(60),
	
	CONSTRAINT pk_tb_end_id_endereco PRIMARY KEY (id_endereco)
);

-- tb_departamento
CREATE TABLE tb_departamento(
    sigla_departamento          INTEGER,
    nome                        VARCHAR(20),
    descricao                   VARCHAR(50),

    CONSTRAINT pk_tb_dpto_sigla_dpto PRIMARY KEY (sigla_departamento)
);
-- tb_cargo
CREATE TABLE tb_cargo(
    sigla_cargo             VARCHAR(3),
    status_cago             VARCHAR(50),
    descricao               VARCHAR(50),
    sigla_departamento         INTEGER,

    CONSTRAINT pk_tb_cargo_sigla_cargo PRIMARY KEY (sigla_cargo),
    CONSTRAINT fk_tb_cargo_id_dpto_tb_dpto_sigla_dpto FOREIGN KEY (sigla_departamento)
        REFERENCES tb_departamento(sigla_departamento)
);

-- tb_produto
CREATE TABLE tb_produto(
	id_produto				INTEGER,
	nome					VARCHAR(50),
	descricao				VARCHAR(100),
	preco					NUMERIC(9, 2),
	quantidade				NUMERIC(9, 2),
	
	CONSTRAINT pk_tb_produto_id_produto PRIMARY KEY (id_produto)
);

-- tb_pagamento
CREATE TABLE tb_pagamento(
	id_forma_pagamento		INTEGER,
	descricao_pagamento		VARCHAR(15),
	
	CONSTRAINT pk_tb_pagamento_id_forma_pagamento PRIMARY KEY (id_forma_pagamento)
);

-- tb_status_cliente
CREATE TABLE tb_status_cliente(
	id_status_cliente			INTEGER,
	descricao_status_cliente	VARCHAR(50),
	
	CONSTRAINT pk_tb_status_cliente_id_status_cliente PRIMARY KEY (id_status_cliente)
);

-- tb_cliente
CREATE TABLE tb_cliente(
	id_cliente				INTEGER,
	nome					VARCHAR(30),
	cnpj					VARCHAR(18),
	telefone				VARCHAR(16),
	email					VARCHAR(50),
	id_status_cliente		INTEGER,
	id_endereco				INTEGER,
	
	CONSTRAINT pk_tb_cliente_id_cliente PRIMARY KEY (id_cliente),
	CONSTRAINT fk_tb_cliente_id_status_cliente_tb_stat_cliente_id_cliente FOREIGN KEY (id_status_cliente)
		REFERENCES tb_status_cliente (id_status_cliente)
);

-- tb_status_fornecedor
CREATE TABLE tb_status_fornecedor(
	id_status_fornecedor		INTEGER,
	descricao_status_fornecedor	VARCHAR(50),
	
	CONSTRAINT pk_tb_status_forn_id_status_fornecedor PRIMARY KEY (id_status_fornecedor)
);

-- tb_fornecedor
CREATE TABLE tb_fornecedor(
	id_fornecedor				INTEGER,
	nome					VARCHAR(30),
	cnpj					VARCHAR(18),
	telefone				VARCHAR(16),
	email					VARCHAR(50),
	id_status_fornecedor	INTEGER,
	id_endereco				INTEGER,
	
	CONSTRAINT pk_tb_fornecedor_id_fornecedor PRIMARY KEY (id_fornecedor),
	CONSTRAINT fk_tb_forn_id_status_fornecedor_tb_stat_forn_id_fornecedor FOREIGN KEY (id_status_fornecedor)
		REFERENCES tb_status_fornecedor (id_status_fornecedor)
);

-- tb_status_venda
CREATE TABLE tb_status_venda(
	id_status_venda		INTEGER,
	descricao_status_venda	VARCHAR(50),
	
	CONSTRAINT pk_tb_status_venda_id_status_venda PRIMARY KEY (id_status_venda)
);

-- tb_venda
CREATE TABLE tb_venda(
	id_venda				INTEGER,
	id_produto				INTEGER,
	quantidade				NUMERIC(9,2),
	data_venda				TIMESTAMP,
	id_funcionario			INTEGER,
	id_status_venda			INTEGER,
	id_forma_pagamento		INTEGER,
	id_cliente				INTEGER,
	
	CONSTRAINT pk_tb_venda_id_venda PRIMARY KEY (id_venda),
	CONSTRAINT fk_tb_venda_id_produto_tb_produto_id_produto FOREIGN KEY (id_produto)
		REFERENCES tb_produto(id_produto),
	CONSTRAINT fk_tb_venda_id_func_tb_func_id_funcionario FOREIGN KEY (id_funcionario)
		REFERENCES tb_funcionario(id_funcionario),
	CONSTRAINT fk_tb_venda_id_stat_venda_tb_stat_venda_id_stat_venda FOREIGN KEY (id_status_venda)
		REFERENCES tb_status_venda(id_status_venda),
	CONSTRAINT fk_tb_venda_id_forma_pagamento_tb_pag_id_forma_pagamento FOREIGN KEY (id_forma_pagamento)
		REFERENCES tb_pagamento(id_forma_pagamento),
	CONSTRAINT fk_tb_venda_id_cliente_tb_cliente_id_cliente FOREIGN KEY (id_cliente)
		REFERENCES tb_cliente(id_cliente)
);

-- tb_usuario
CREATE TABLE tb_usuario(
	id				INTEGER,
	usuario			VARCHAR(50),
	email			VARCHAR(50),
	senha			VARCHAR(256),
	
	CONSTRAINT pk_tb_usuario_id PRIMARY KEY (id)
)


SELECT *
FROM tb_user;

-- tb_funcionario
CREATE TABLE tb_funcionario(
	id_funcionario			INTEGER,
	nome					VARCHAR(20),
	sobrenome				VARCHAR(20),
	cpf						VARCHAR(14),
	data_nascimento			DATE,
	email					VARCHAR(50),
	telefone				VARCHAR(16),
	id_status_funcionario	INTEGER,
	sigla_cargo				VARCHAR(3),
	id_usuario				INTEGER,
	id_endereco				INTEGER,
	-- sigla_departamento		VARCHAR(3), Já existe o relacionamento cargo x departamento
	
	CONSTRAINT pk_tb_func_id_func PRIMARY KEY (id_funcionario),
	CONSTRAINT fk_tb_func_id_stat_func_tb_stat_func_id_stat_func FOREIGN KEY (id_status_funcionario)
		REFERENCES tb_status_funcionario(id_status_funcionario),
	CONSTRAINT fk_tb_func_sigla_cago_tb_cargo_sigla_cargo FOREIGN KEY (sigla_cargo)
		REFERENCES tb_cargo(sigla_cargo),
	CONSTRAINT fk_tb_func_id_usuario_tb_usuario_id_usuario FOREIGN KEY (id_usuario)
		REFERENCES tb_usuario(id),
	CONSTRAINT fk_tb_func_id_end_tb_end_id_end FOREIGN KEY (id_endereco)
		REFERENCES tb_endereco(id_endereco)
	--CONSTRAINT fk_tb_func_sigla_dpto_tb_dpto_sigla_dpto FOREIGN KEY (sigla_departamento)
	--	REFERENCES tb_departamento (sigla_departamento)
);



SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'tb_user';
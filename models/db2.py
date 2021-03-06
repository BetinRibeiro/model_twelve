# -*- coding: utf-8 -*-

db.define_table('projeto',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', default='', writable=True, readable=True, notnull=True,requires = IS_UPPER()),
                Field('descricao', 'string', default='', writable=True, readable=True, notnull=True,requires = IS_UPPER()),
                Field('link_acesso', 'string', default='', writable=True, readable=True, notnull=True),
                Field('data_fechamento', 'date', label="Data Fechamento", default=request.now, notnull=True, requires = IS_DATE(format=('%d/%m/%Y'))),
                Field('tipo', 'string', label='Status', default='Assinatura Mensal',requires = IS_UPPER(), notnull=True),
                Field('valor', 'double', writable=True, readable=True, default=0, notnull=True),
                auth.signature,
                format='%(nome)s')

db.projeto.id.writable=False
db.projeto.id.readable=False
db.projeto.tipo.requires = IS_IN_SET(['Assinatura Mensal','Venda Única'])


db.define_table('funcionario',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', default='', writable=True, readable=True, notnull=True,requires = IS_UPPER()),
                Field('descricao', 'string', default='', writable=True, readable=True, notnull=True),
                Field('data_contratacao', 'date', label="Data Contratação", default=request.now, notnull=True, requires = IS_DATE(format=('%d/%m/%Y'))),
                Field('tipo', 'string', label='Tipo', default='Contratado',requires = IS_UPPER(), notnull=True),
                Field('valor_hora', 'double', writable=True, readable=True, default=0, notnull=True),
                auth.signature,
                format='%(nome)s')

db.funcionario.id.writable=False
db.funcionario.id.readable=False
db.funcionario.tipo.requires = IS_IN_SET(['Contratado','Fixo'])

db.define_table('registro_producao',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('projeto','reference projeto', writable=True, readable=True, label='Projeto'),
                Field('funcionario','reference funcionario', writable=True, readable=True, label='funcionario'),
                Field('tipo', 'string', label='Status', default='Desenvolvimento',requires = IS_UPPER(), notnull=True),
                Field('data_registro', 'date', label="Data", default=request.now, notnull=True, requires = IS_DATE(format=('%d/%m/%Y'))),
                Field('modulo', 'string', label='Módulo',requires = IS_UPPER(), notnull=True),
                Field('funcionalidade', 'string', label='Função Prática',requires = IS_UPPER(), notnull=True),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER(), notnull=True),
                Field('tempo', 'integer', label='Tempo (mins)', writable=True, readable=True, default=60, notnull=True),
                Field('valor_servico', 'double', writable=False, readable=False, default=0, notnull=True),
                Field('pago', 'boolean', writable=True, readable=True, default=False),
                auth.signature,
                format='%(funcionalidade)s')

db.registro_producao.id.writable=False
db.registro_producao.id.readable=False
db.registro_producao.tipo.requires = IS_IN_SET(['Desenvolvimento','Ajuste','Correção','Adaptação','Suporte','Treinamento'])



db.define_table('registro_investimento',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER(), notnull=True),
                Field('data_inicial', 'date', label="Data Inicial", default=request.now, notnull=True, requires = IS_DATE(format=('%d/%m/%Y'))),
                Field('data_final', 'date', label="Data Final", default=request.now, notnull=True, requires = IS_DATE(format=('%d/%m/%Y'))),
                Field('valor', 'double', writable=True, readable=True, default=0, notnull=True),
                Field('percentual_rendimento', 'double', writable=True, readable=True, default=0, notnull=True),
                Field('finalizado', 'boolean', writable=True, readable=True, default=False),
                auth.signature,
                format='%(descricao)s')

db.registro_investimento.id.writable=False
db.registro_investimento.id.readable=False

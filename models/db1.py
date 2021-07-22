# -*- coding: utf-8 -*-
db.define_table('empresa',
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                #ultimos 30 dias de entradas e saidas
                Field('quantidade_ultimos_registros', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_ultimos_contactados', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_ultimos_prospectos', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_ultimos_fachamentos', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_clientes', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_assinantes', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_vendas', 'integer', writable=False, readable=False, default=0),
                Field('total_horas_trabalhadas', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_projetos', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_projetos_fixos', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_projetos_mensal', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_investimentos', 'integer', writable=False, readable=False, default=0),
                Field('quantidade_registros_producao', 'integer', writable=False, readable=False, default=0),
                Field('total_capital_rentabilizado', 'double', writable=False, readable=False, default=0, notnull=True),
                Field('total_capital_empregado', 'double', writable=False, readable=False, default=0, notnull=True),
                Field('valor_assinaturas', 'double', writable=False, readable=False, default=0, notnull=True),
                Field('valor_ultimas_entradas', 'double', writable=False, readable=False, default=0, notnull=True),
                Field('valor_ultimas_saidas', 'double', writable=False, readable=False, default=0, notnull=True),
                Field('total_valor_producao', 'double', writable=False, readable=False, default=0, notnull=True),
                auth.signature,
                format='%(nome)s')

db.empresa.id.writable=False
db.empresa.id.readable=False
db.define_table('usuario_empresa',
                Field('usuario','reference auth_user', writable=False, readable=True, label='Usuario'),
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('tipo', 'string', label='tipo',default='Administrador'),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                format='%(nome)s')

db.usuario_empresa.id.writable=False
db.usuario_empresa.id.readable=False

db.usuario_empresa.tipo.requires = IS_IN_SET(['Completo','Fluxo_Caixa'])


db.define_table('registro_fluxo',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('tipo', 'string', default='Entrada', writable=False, readable=False),
                Field('data_pagamento', 'date', label="Data", default=request.now, notnull=True, requires = IS_DATE(format=('%d/%m/%Y'))),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER(), notnull=True),
                Field('valor', 'double', writable=True, readable=True, default=0, notnull=True),
                Field('pago', 'boolean', writable=True, readable=True, default=True),
                auth.signature,
                format='%(descricao)s')

db.registro_fluxo.id.writable=False
db.registro_fluxo.id.readable=False
db.registro_fluxo.tipo.requires = IS_IN_SET(['Entrada','Saida'])

db.define_table('registro_prospeccao',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', default='', writable=True, readable=True, notnull=True,requires = IS_UPPER()),
                Field('telefone', 'string', default='', writable=True, readable=True, notnull=True),
                Field('descricao', 'string', default='', writable=True, readable=True, notnull=True,requires = IS_UPPER()),
                Field('data_contato', 'date', label="Data do Status", default=request.now, notnull=True, requires = IS_DATE(format=('%d/%m/%Y'))),
                Field('status', 'string', label='Status', default='Contactado',requires = IS_UPPER(), notnull=True),
                auth.signature,
                format='%(nome)s')

db.registro_prospeccao.id.writable=False
db.registro_prospeccao.id.readable=False
db.registro_prospeccao.status.requires = IS_IN_SET(['Aguardando','Contactado','Apresentado','Fechado','Despensado'])

db.define_table('cliente',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', default='', writable=True, readable=True, notnull=True,requires = IS_UPPER()),
                Field('telefone', 'string', default='', writable=True, readable=True, notnull=True),
                Field('descricao', 'string', default='', writable=True, readable=True, notnull=True,requires = IS_UPPER()),
                Field('data_fechamento', 'date', label="Data Fechamento", default=request.now, notnull=True, requires = IS_DATE(format=('%d/%m/%Y'))),
                Field('tipo', 'string', label='Status', default='Assinante Mensal',requires = IS_UPPER(), notnull=True),
                Field('valor', 'double', writable=True, readable=True, default=0, notnull=True),
                auth.signature,
                format='%(nome)s')

db.cliente.id.writable=False
db.cliente.id.readable=False
db.cliente.tipo.requires = IS_IN_SET(['Assinante Mensal','Compra de Sistema','Compra de Produto'])

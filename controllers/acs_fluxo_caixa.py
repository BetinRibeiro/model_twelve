# -*- coding: utf-8 -*-
import datetime
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    #caso não exista é por que o usuario acaba de se cadastrar
    #então é redirecionado para o cadastro
    if not usuario:
        redirect(URL('acs_empresa','cadastrar'))
    #caso passe busca a empresa na qual o funcionario pertence
    empresa = db.empresa(usuario.empresa)
    #temos que identificar a o mes da data
    if len(request.args) == 0:
        indice=0
    else:
        try:
            indice = int(request.args[0])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    #pega a data de hoje
    data_hoje= request.now
    data_inicial = datetime.date(data_hoje.year, data_hoje.month+indice, 1)
    data_final = datetime.date(data_hoje.year, data_hoje.month+indice+1, 1)
    rows = db((db.registro_fluxo.empresa==empresa.id)&(db.registro_fluxo.data_pagamento>=data_inicial)&(db.registro_fluxo.data_pagamento<data_final)).select(orderby=db.registro_fluxo.data_pagamento|db.registro_fluxo.tipo)
    return locals()

@auth.requires_login()
def registrar():
    response.view = 'generic.html' # use a generic view
    try:
        if len(request.args) == 0:
            db.registro_fluxo.tipo.default="Saida"
            db.registro_fluxo.descricao.default="Pagamento "
        else:
            db.registro_fluxo.tipo.default="Entrada"
            db.registro_fluxo.descricao.default="Recebimento "
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if not usuario:
            redirect(URL('acs_empresa','cadastrar'))
        #cria tela generica
        request.function='Cadastro de banco'
        db.registro_fluxo.empresa.default=usuario.empresa
        if auth.user.id==1:
            db.registro_fluxo.empresa.label="(Empresa) # Programador"
            db.registro_fluxo.empresa.writable=True
            db.registro_fluxo.empresa.readable=True
            db.registro_fluxo.tipo.label="(Tipo) # Programador"
            db.registro_fluxo.tipo.writable=True
            db.registro_fluxo.tipo.readable=True
        form = SQLFORM(db.registro_fluxo).process()
        if form.accepted:
            response.flash = 'Formulario aceito'
            redirect(URL('atualizar_dados'))
        elif form.errors:
            response.flash = 'Formulario não aceito'
        else:
            response.flash = 'Preencha o formulario'
    except:
        redirect(URL('atualizar_dados'))
    return  dict(form=form)

@auth.requires_login()
def inserir_copia():
    try:
        response.view = 'generic.html' # use a generic view
        registro_fluxo= db.registro_fluxo(request.args(0, cast=int))
        db.registro_fluxo.empresa.default=registro_fluxo.empresa
        db.registro_fluxo.tipo.default=registro_fluxo.tipo
        db.registro_fluxo.data_pagamento.default=registro_fluxo.data_pagamento
        db.registro_fluxo.descricao.default=registro_fluxo.descricao
        db.registro_fluxo.valor.default=registro_fluxo.valor
        db.registro_fluxo.pago.default=registro_fluxo.pago
        form = SQLFORM(db.registro_fluxo).process()
        if form.process().accepted:
            session.flash = 'Dados atualizado'
            redirect(URL('index'))
        elif form.errors:
            response.flash = 'Formulario não aceito'
        else:
            response.flash = 'Preencha o formulario'
    except:
        redirect(URL('atualizar_dados'))
    return dict(form=form)

@auth.requires_login()
def alterar():
    try:
        response.view = 'generic.html' # use a generic view
        request.function='Alterar Cliente'
        registro_fluxo= db.registro_fluxo(request.args(0, cast=int))
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if usuario.empresa!=registro_fluxo.empresa:
            redirect(URL('deafult','index'))
        if auth.user.id==1:
            db.registro_fluxo.empresa.label="(Empresa) # Programador"
            db.registro_fluxo.empresa.writable=True
            db.registro_fluxo.empresa.readable=True
            db.registro_fluxo.tipo.label="(Tipo) # Programador"
            db.registro_fluxo.tipo.writable=True
            db.registro_fluxo.tipo.readable=True
        form = SQLFORM(db.registro_fluxo, request.args(0, cast=int), deletable=True)
        if form.process().accepted:
            session.flash = 'Dados atualizado'
            redirect(URL('index'))
        elif form.errors:
            response.flash = 'Formulario não aceito'
        else:
            response.flash = 'Preencha o formulario'
    except:
        redirect(URL('atualizar_dados'))
    return dict(form=form)

@auth.requires_login()
def atualizar_dados():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    data_hoje= request.now
    data_inicial = datetime.date(data_hoje.year, data_hoje.month-1, data_hoje.day)
    total_entrada = db((db.registro_fluxo.empresa==usuario.empresa)&(db.registro_fluxo.data_pagamento>=data_inicial)&(db.registro_fluxo.data_pagamento<=data_hoje)&(db.registro_fluxo.tipo==("Entrada"))&(  db.registro_fluxo.descricao.contains(["Recebimento"]))).count()
    if total_entrada>0:
        sum = db.registro_fluxo.valor.sum()
        empresa.valor_ultimas_entradas =  db((db.registro_fluxo.empresa==usuario.empresa)&(db.registro_fluxo.data_pagamento>=data_inicial)&(db.registro_fluxo.data_pagamento<=data_hoje)&(db.registro_fluxo.tipo==("Entrada"))&(db.registro_fluxo.descricao.contains(["Recebimento"]))).select(sum).first()[sum]
    else:
        empresa.valor_ultimas_entradas = 0
    total_saidas = db((db.registro_fluxo.empresa==usuario.empresa)&(db.registro_fluxo.data_pagamento>=data_inicial)&(db.registro_fluxo.data_pagamento<=data_hoje)&(db.registro_fluxo.tipo==("Saida"))&(  db.registro_fluxo.descricao.contains(["PAGAMENTO"]))).count()
    if total_saidas>0:
        sum = db.registro_fluxo.valor.sum()
        empresa.valor_ultimas_saidas =  db((db.registro_fluxo.empresa==usuario.empresa)&(db.registro_fluxo.data_pagamento>=data_inicial)&(db.registro_fluxo.data_pagamento<=data_hoje)&(db.registro_fluxo.tipo==("Saida"))&(db.registro_fluxo.descricao.contains(["PAGAMENTO"]))).select(sum).first()[sum]
    else:
        empresa.valor_ultimas_saidas = 0
    empresa.quantidade_ultimos_registros = db((db.registro_fluxo.empresa==usuario.empresa)&(db.registro_fluxo.data_pagamento>=data_inicial)&(db.registro_fluxo.data_pagamento<=data_hoje)).count()
    empresa.update_record()
    return redirect(URL('index', args=[0,total_entrada]))

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
    rows = db((db.registro_prospeccao.empresa==empresa.id)&(db.registro_prospeccao.created_on>=data_inicial)&(db.registro_prospeccao.created_on<data_final)).select(orderby=db.registro_prospeccao.created_on|db.registro_prospeccao.status)
    return locals()


@auth.requires_login()
def registrar():
    response.view = 'generic.html' # use a generic view
    try:
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if not usuario:
            redirect(URL('acs_empresa','cadastrar'))
        #cria tela generica
        request.function='Cadastro de Prospeção'
        db.registro_prospeccao.empresa.default=usuario.empresa
        if auth.user.id==1:
            db.registro_prospeccao.empresa.label="(Empresa) # Programador"
            db.registro_prospeccao.empresa.writable=True
            db.registro_prospeccao.empresa.readable=True
        form = SQLFORM(db.registro_prospeccao).process()
        if form.accepted:
            response.flash = 'Formulario aceito'
            redirect(URL('index'))
        elif form.errors:
            response.flash = 'Formulario não aceito'
        else:
            response.flash = 'Preencha o formulario'
    except:
        redirect(URL('atualizar_dados'))
    return  dict(form=form)


@auth.requires_login()
def alterar():
    try:
        response.view = 'generic.html' # use a generic view
        request.function='Alterar Prospecção'
        registro_prospeccao= db.registro_prospeccao(request.args(0, cast=int))
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if usuario.empresa!=registro_prospeccao.empresa:
            redirect(URL('deafult','index'))
        if auth.user.id==1:
            db.registro_prospeccao.empresa.label="(Empresa) # Programador"
            db.registro_prospeccao.empresa.writable=True
            db.registro_prospeccao.empresa.readable=True
        form = SQLFORM(db.registro_prospeccao, request.args(0, cast=int), deletable=True)
        if form.process().accepted:
            session.flash = 'Dados atualizado'
            redirect(URL('atualizar_dados'))
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

    empresa.quantidade_ultimos_prospectos = db((db.registro_prospeccao.empresa==usuario.empresa)&(db.registro_prospeccao.created_on>=data_inicial)&(db.registro_prospeccao.created_on<=data_hoje)).count()

    empresa.quantidade_ultimos_fachamentos = db((db.registro_prospeccao.empresa==usuario.empresa)&(db.registro_prospeccao.created_on>=data_inicial)&(db.registro_prospeccao.created_on<=data_hoje)&(db.registro_prospeccao.status=="Fechado")).count()

    empresa.quantidade_ultimos_contactados = db((db.registro_prospeccao.empresa==usuario.empresa)&(db.registro_prospeccao.created_on>=data_inicial)&(db.registro_prospeccao.created_on<=data_hoje)&(db.registro_prospeccao.status=="Contactado")).count()
    empresa.update_record()
    return redirect(URL('index',args=[0,empresa.quantidade_ultimos_prospectos]))

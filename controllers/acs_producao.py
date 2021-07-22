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
    rows = db((db.registro_producao.empresa==empresa.id)&(db.registro_producao.data_registro>=data_inicial)&(db.registro_producao.data_registro<data_final)).select(orderby=db.registro_producao.data_registro|db.registro_producao.tipo)
    if len(rows)<1:
        db.registro_producao.insert(empresa=1,projeto=9,funcionario=1,modulo="acs_empresa",funcionalidade="Todas",descricao="Controle de Empresa",tempo=360,valor_servico=200)
        db.registro_producao.insert(empresa=1,projeto=9,funcionario=1,modulo="acs_equipe",funcionalidade="Todas",descricao="Controle de Equipe",tempo=360,valor_servico=200)
        db.registro_producao.insert(empresa=1,projeto=9,funcionario=1,modulo="acs_mercadoria",funcionalidade="Todas",descricao="Controle de Mercadoria",tempo=360,valor_servico=200)
        db.registro_producao.insert(empresa=1,projeto=9,funcionario=1,modulo="acs_registros",funcionalidade="Todas",descricao="Controle de registros",tempo=360,valor_servico=200)
        db.registro_producao.insert(empresa=1,projeto=9,funcionario=1,modulo="acs_despesa",funcionalidade="Todas",descricao="Controle de Despesa",tempo=360,valor_servico=200)
        db.registro_producao.insert(empresa=1,projeto=9,funcionario=1,modulo="acs_relatorio",funcionalidade="Todas",descricao="Controle de Relatorios",tempo=360,valor_servico=200)
        db.registro_producao.insert(empresa=1,projeto=9,funcionario=1,modulo="acs_logins",funcionalidade="Todas",descricao="Controle de Logins",tempo=360,valor_servico=200)
        db.registro_producao.insert(empresa=1,projeto=9,funcionario=1,modulo="acs_recebimentos",funcionalidade="Todas",descricao="Controle de Recebimentos",tempo=360,valor_servico=200)
        redirect(URL('atualizar_dados'))
    return locals()

@auth.requires_login()
def registrar():
    response.view = 'generic.html' # use a generic view
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
#     try:
    if not usuario:
        redirect(URL('acs_empresa','cadastrar'))
    #cria tela generica
    request.function='Cadastro de Registro'
    db.registro_producao.empresa.default=usuario.empresa
    if auth.user.id==1:
        db.registro_producao.empresa.label="(Empresa) # Programador"
        db.registro_producao.empresa.writable=True
        db.registro_producao.empresa.readable=True
    db.registro_producao.funcionario.requires = IS_IN_DB(db(db.funcionario.empresa == usuario.empresa), 'funcionario.id', '%(nome)s')
    db.registro_producao.projeto.requires = IS_IN_DB(db(db.projeto.empresa == usuario.empresa), 'projeto.id', '%(nome)s')
    form = SQLFORM(db.registro_producao).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('atualizar_dados'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
#     except:
#         redirect(URL('atualizar_dados'))
    return  dict(form=form)

@auth.requires_login()
def alterar():
    try:
        response.view = 'generic.html' # use a generic view
        request.function='Alterar Registro'
        registro_producao= db.registro_producao(request.args(0, cast=int))
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if usuario.empresa!=registro_producao.empresa:
            redirect(URL('deafult','index'))
        if auth.user.id==1:
            db.registro_producao.empresa.label="(Empresa) # Programador"
            db.registro_producao.empresa.writable=True
            db.registro_producao.empresa.readable=True
            db.registro_producao.tipo.label="(Tipo) # Programador"
            db.registro_producao.tipo.writable=True
            db.registro_producao.tipo.readable=True
        form = SQLFORM(db.registro_producao, request.args(0, cast=int), deletable=True)
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

    total_horas = db((db.registro_producao.empresa==usuario.empresa)&(db.registro_producao.data_registro>=data_inicial)&(db.registro_producao.data_registro<=data_hoje)).count()
    empresa.quantidade_registros_producao = total_horas
    if total_horas>0:
        sum = db.registro_producao.tempo.sum()
        empresa.total_horas_trabalhadas =  db((db.registro_producao.empresa==usuario.empresa)&(db.registro_producao.data_registro>=data_inicial)&(db.registro_producao.data_registro<=data_hoje)).select(sum).first()[sum]
    else:
        empresa.total_horas_trabalhadas = 0
    if total_horas>0:
        sum = db.registro_producao.valor_servico.sum()
        empresa.total_valor_producao =  db((db.registro_producao.empresa==usuario.empresa)&(db.registro_producao.data_registro>=data_inicial)&(db.registro_producao.data_registro<=data_hoje)).select(sum).first()[sum]
        
    empresa.update_record()
    return redirect(URL('index'))

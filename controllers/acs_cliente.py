# -*- coding: utf-8 -*-

import datetime
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    paginacao = 10
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        pagina = 1
    total = db((db.cliente.empresa==usuario.empresa)).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.cliente.empresa==usuario.empresa)).select(
      limitby=limites,orderby=~db.cliente.tipo|db.cliente.id
      )
    consul=(request.args(1))
    if (consul):
        registros = db((db.cliente.empresa==usuario.empresa)&(db.cliente.nome.contains(consul))).select(limitby=(0,paginacao))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, consul=consul)


@auth.requires_login()
def cadastrar():
    try:
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if not usuario:
            redirect(URL('acs_empresa','cadastrar'))
        #cria tela generica
        response.view = 'generic.html' # use a generic view
        request.function='Cadastro de Cliente'
        db.cliente.empresa.default=usuario.empresa
        form = SQLFORM(db.cliente).process()
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
        request.function='Alterar Cliente'
        cliente= db.cliente(request.args(0, cast=int))
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if usuario.empresa!=cliente.empresa:
            redirect(URL('acs_empresa','cadastrar'))
        if auth.user.id==1:
            db.cliente.empresa.label="(Empresa) # Programador"
            db.cliente.empresa.writable=True
            db.cliente.empresa.readable=True
        form = SQLFORM(db.cliente, request.args(0, cast=int), deletable=True)
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

    empresa.quantidade_clientes = db((db.cliente.empresa==usuario.empresa)).count()

    empresa.quantidade_assinantes = db((db.cliente.empresa==usuario.empresa)&(db.cliente.tipo=="Assinante Mensal")).count()

    total_clientes = db((db.cliente.empresa==usuario.empresa)&(db.cliente.tipo==("Assinante Mensal"))).count()
    if total_clientes>0:
        sum = db.cliente.valor.sum()
        empresa.valor_assinaturas =  db((db.cliente.empresa==usuario.empresa)&(db.cliente.tipo==("Assinante Mensal"))).select(sum).first()[sum]
    else:
        empresa.valor_assinaturas = 0
    empresa.update_record()
    return redirect(URL('index'))

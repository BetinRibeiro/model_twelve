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
    total = db((db.funcionario.empresa==usuario.empresa)).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.funcionario.empresa==usuario.empresa)).select(
      limitby=limites,orderby=~db.funcionario.tipo|db.funcionario.id
      )
    consul=(request.args(1))
    if (consul):
        registros = db((db.funcionario.empresa==usuario.empresa)&(db.funcionario.nome.contains(consul))).select(limitby=(0,paginacao))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, consul=consul)


@auth.requires_login()
def cadastrar():
    try:
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if not usuario:
            redirect(URL('acs_empresa','cadastrar'))
        #cria tela generica
        response.view = 'generic.html' # use a generic view
        request.function='Cadastro de funcionario'
        db.funcionario.empresa.default=usuario.empresa
        form = SQLFORM(db.funcionario).process()
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
        request.function='Alterar funcionario'
        funcionario= db.funcionario(request.args(0, cast=int))
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if usuario.empresa!=funcionario.empresa:
            redirect(URL('acs_empresa','cadastrar'))
        if auth.user.id==1:
            db.funcionario.empresa.label="(Empresa) # Programador"
            db.funcionario.empresa.writable=True
            db.funcionario.empresa.readable=True
        form = SQLFORM(db.funcionario, request.args(0, cast=int), deletable=True)
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

    
    empresa.update_record()
    return redirect(URL('index'))

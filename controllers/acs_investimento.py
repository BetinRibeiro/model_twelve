# -*- coding: utf-8 -*-

import datetime
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(db.empresa.id==usuario.empresa)
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
    total = db((db.registro_investimento.empresa==usuario.empresa)).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.registro_investimento.empresa==usuario.empresa)).select(
      limitby=limites,orderby=~db.registro_investimento.data_inicial|db.registro_investimento.id
      )
    consul=(request.args(1))
    if (consul):
        registros = db((db.registro_investimento.empresa==usuario.empresa)&(db.registro_investimento.descricao.contains(consul))).select(limitby=(0,100))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, consul=consul, empresa=empresa)


@auth.requires_login()
def cadastrar():
    try:
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if not usuario:
            redirect(URL('acs_empresa','cadastrar'))
        #cria tela generica
        response.view = 'generic.html' # use a generic view
        request.function='Cadastro de registro_investimento'
        db.registro_investimento.empresa.default=usuario.empresa
        form = SQLFORM(db.registro_investimento).process()
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
        request.function='Alterar registro_investimento'
        registro_investimento= db.registro_investimento(request.args(0, cast=int))
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if usuario.empresa!=registro_investimento.empresa:
            redirect(URL('acs_empresa','cadastrar'))
        if auth.user.id==1:
            db.registro_investimento.empresa.label="(Empresa) # Programador"
            db.registro_investimento.empresa.writable=True
            db.registro_investimento.empresa.readable=True
        form = SQLFORM(db.registro_investimento, request.args(0, cast=int), deletable=True)
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
    try:
        sum = db.registro_investimento.valor.sum()
        empresa.total_capital_rentabilizado =  db((db.registro_investimento.empresa==usuario.empresa)).select(sum).first()[sum]
    except:
        empresa.total_capital_rentabilizado =0
    empresa.quantidade_investimentos=  db((db.registro_investimento.empresa==usuario.empresa)).count()
#     empresa.total_capital_empregado=0
    empresa.update_record()
    return redirect(URL('index'))

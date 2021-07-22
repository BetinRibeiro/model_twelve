# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    #caso não exista é por que o usuario acaba de se cadastrar
    #então é redirecionado para o cadastro
    if not usuario:
        redirect(URL('acs_empresa','cadastrar'))
    #caso passe busca a empresa na qual o funcionario pertence
    empresa = db.empresa(usuario.empresa)
    return locals()

@auth.requires_login()
#função que simlpesmente faz o cadastro da empresa
#automaticamente, utilizado basicamente uma unica vez
#pelo usuario
def cadastrar():
    #insere uma empresa com os valores padão
    empresa=db.empresa.insert(
        nome=auth.user.first_name+" "+auth.user.last_name+" LTDA",)
    #vincula o login a empresa, criando um "usuario da empresa"
    db.usuario_empresa.insert(empresa=empresa,usuario=auth.user.id, nome=empresa.nome)
    #o retorno da função é um redirecionamento para o
    #index dessa propria classe empresa
    return redirect(URL('index'))

@auth.requires_login()
#função para alterar o nome da empresa
# é utilizada por todos assim, mas caso o usuario seja 
#o usuario 01 que no caso é o programador
#mostra todas as opções
def alterar():
    response.view = 'generic.html' # view generica 
    request.function='Alterar nome da Empresa' #redefine nome da função
    #busca a empresa vinculada ao usuario logado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    #caso seja 01 libera outras opções
    if auth.user.id==1:
        db.empresa.id.label="Programador # (id)"
        db.empresa.id.writable=True
        db.empresa.id.readable=True
        db.empresa.ativo.label="(Ativo) # Programador"
        db.empresa.ativo.writable=True
        db.empresa.ativo.readable=True
    #renderiza formulario automatico
    form = SQLFORM(db.empresa, usuario.empresa, deletable=False)
    if form.process().accepted:
#         session.flash = 'Projeto atualizado'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)

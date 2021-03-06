# -*- coding: utf-8 -*-
from datetime import date
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    lista=[]
    data_fim=date.today()
    primeira_data=date.fromordinal(data_fim.toordinal()-30)
    a=1
    while a<6:
        total_entrada = db((db.registro_fluxo.empresa==usuario.empresa)&(db.registro_fluxo.data_pagamento>=primeira_data)&(db.registro_fluxo.data_pagamento<=data_fim)&(db.registro_fluxo.tipo==("Entrada"))&(db.registro_fluxo.descricao.contains(["Recebimento"]))).count()
        if total_entrada>0:
            sum = db.registro_fluxo.valor.sum()
            lista.append(db((db.registro_fluxo.empresa==usuario.empresa)&(db.registro_fluxo.data_pagamento>=primeira_data)&(db.registro_fluxo.data_pagamento<=data_fim)&(db.registro_fluxo.tipo==("Entrada"))&(db.registro_fluxo.descricao.contains(["Recebimento"]))).select(sum).first()[sum])
        else:
            lista.append(0)
        a+=1
        
        data_fim=primeira_data
        primeira_data=date.fromordinal(data_fim.toordinal()-30)
    return locals()

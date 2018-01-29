import requests,os,json
from datetime import datetime

'''
 git remote add origin git@bitbucket.org:PedroHenrique/nmpedidobot.git
 git push -u origin master
'''


CHAVE_API = os.environ.get('API_LOJAINTEGRADA_TOKEN')
CHAVE_APLICACAO = os.environ.get('LOJAINTEGRADA_APLICACAO_TOKEN')

API_LOJAINTEGRADA_BASE_URL = 'https://api.awsli.com.br/v1'
URL_AUTH = '&chave_api='+CHAVE_API+'&chave_aplicacao='+CHAVE_APLICACAO+''

def list_order_today():
    now = datetime.today().date()
    url = '/pedido/search/?since_criado='+str(now)+'&format=json'+URL_AUTH+''
    try:
        req = requests.get(API_LOJAINTEGRADA_BASE_URL+url)
        if(req.status_code==200):
            api_response = json.loads(req.text)
            api_response = api_response['objects']
            orders_numbers = []
            for i in range(0,len(api_response),1):
                if((api_response[i]['situacao']['codigo']=='pedido_efetuado') or (api_response[i]['situacao']['codigo']=='aguardando_pagamento')):
                    orders_numbers.append({
                        'ID':api_response[i]['numero']
                    })
        return orders_numbers
    except:
        print('Problemas na Conexao')

def order_details(order_id):

    url = '/pedido/'+str(order_id)+'/?&format=json'+URL_AUTH+''
    req = requests.get(API_LOJAINTEGRADA_BASE_URL+url)
    response = json.loads(req.text)
    print(response)
    # order_basic_info = []
    #
    # for res in response['objects']:
    #     order_basic_info.append({
    #
    #         'numero':res['numero'],
    #         'cliente':res['cliente'],
    #         'detalhe_url':res['resource_uri'],
    #         'situacao':res['situacao']['nome'],
    #         'valor_total':res['valor_total']
    #
    #     })
    # return order_basic_info


orders_numbers = list_order_today()

print(orders_numbers)











import requests,os,json
from datetime import datetime


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
    try:
        req = requests.get(API_LOJAINTEGRADA_BASE_URL+url)
        if(req.status_code==200):
            api_response = json.loads(req.text)
            order_basic_info = []
            order_basic_info.append({
                'cliente':api_response['cliente']['nome'],
                'envio':api_response['envios'][0]['forma_envio']['nome'],
                'forma_pagamento':api_response['pagamentos'][0]['forma_pagamento']['nome'],
                'forma_pagamento_icon':api_response['pagamentos'][0]['forma_pagamento']['imagem'],
                'valor_total':api_response['valor_total']
            })
        return order_basic_info
    except:
        print('Problemas na Conexao')


orders_numbers = list_order_today()
print(order_details(orders_numbers[0]['ID']))












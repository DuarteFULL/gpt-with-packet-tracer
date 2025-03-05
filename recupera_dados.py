import requests
from openai import OpenAI
import json
import base64
import tempfile
from playsound import playsound

# Essa função obtén os dados de autenticação
def get_ticket(username, password):
    url = 'http://localhost:58000/api/v1/ticket'
    body = {'username': username, 'password': password}
    resp = requests.post(url, json=body)
    resp_data = resp.json()
    ticket = resp_data['response']['serviceTicket']
    return ticket

# Essa função gera uma lista dos dispositivos de rede
def get_devices(ticket):
    url = 'http://localhost:58000/api/v1/network-device'
    headers = {'X-Auth-Token': ticket}
    resp = requests.get(url, headers=headers)
    return resp.json()['response']

def play_mp3_data(mp3_data):
    # Cria um arquivo temporário para gerar o MP3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(mp3_data)
        temp_file_path = temp_file.name
    # Reproduz o MP3
    playsound(temp_file_path)

# Essa função gera uma lista dos hosts
def get_hosts(ticket):
    url = 'http://localhost:58000/api/v1/host'
    headers = {'X-Auth-Token': ticket}
    resp = requests.get(url, headers=headers)
    return resp.json()['response']

def chama_gpt(userPrompt):
    gpt = OpenAI()
    
    prompt = f'''
    
    Analise os dados providos sobre a configuração de rede e gere uma resposta baseado em:

    {userPrompt}

    Tente ser específico sobre números e tipos de dispositivos e não invente nenhuma informação sobre a rede.
    Não responda nenhum assunto que não seja referente a essa topologia de rede.
    
    Dispositivos de rede:
    {get_devices(admin_ticket)}
    
    hosts:
    {get_hosts(admin_ticket)}
    
    '''   
    
    completion = gpt.chat.completions.create(
        # para audio, remova esse comentario model='gpt-4o-audio-preview',
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'developer', 'content': 'You are an experience network engineer. Reply in Portuguese-BR'},
            {'role': 'user', 'content': prompt}
        ]
        # descomente as linas abaixo para escutar o áudio:
        #, modalities=['text', 'audio'],
        #audio={"voice": "coral", "format": "mp3"}
    )
    print('---')
    print(completion.choices[0].message.content)
    print('---')
    
    # descomente as linhas abaixo para escutar o áudio:
    # analysis = completion.choices[0].message.audio.transcript
    # print(analysis)
    # mp3_data = base64.b64decode(completion.choices[0].message.audio.data)
    # play_mp3_data(mp3_data)




# Código principal que roda a aplicação
if __name__ == '__main__':
    admin_ticket = get_ticket('cisco', 'cisco123!')
    print(admin_ticket)

    my_devices = get_devices(admin_ticket)
    my_hosts = get_hosts(admin_ticket)

    def opcao1():
        print("======")
        print("Você escolheu a opção 1, aqui esta a lista de dispositivos de rede:")
        print("======")
        for device in my_devices:
            print(device['id'], device['hostname'], device['type'], device['managementIpAddress'])
        print("======")
        print("FIM")
        input("Pressione <Enter> para continuar...")
        print("======")

    def opcao2():
        print("======")
        print("Você escolheu a opção 2, aqui esta a lista de hosts:")
        print("======")
        for host in my_hosts:
            print(host['id'], host['hostName'], host['hostType'], host['hostIp'])
        print("======")
        print("FIM")
        input("Pressione <Enter> para continuar...")
        print("======")

    def opcao3():
        print("======")
        print("Você escolheu a opção 3, agora faça uma pergunta ao ChatGPT:")
        print("======")
        userPrompt = input("Pergunta: ")
        chama_gpt(userPrompt)
        print("======")
        print("FIM")
        input("Pressione <Enter> para continuar...")
        print("======")
        
    
    def menu():
        while True:
            print("\n===== MENU INTERATIVO =====")
            print("1 - Listar Dispositivos de Rede")
            print("2 - Listar Hosts")
            print("3 - Faça uma pergunta ao ChatGPT")
            print("0 - Encerrar")
            
            escolha = input("Escolha uma opção: ")
            
            match escolha:
                case "1":
                    opcao1()
                case "2":
                    opcao2()
                case "3":
                    opcao3()
                case "0":
                    print("Aplicação Encerrada!")
                    break
                case _:
                    print("Opção inválida! Tente novamente.")

    menu()






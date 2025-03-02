from openai import OpenAI

gpt = OpenAI(api_key='usar uma variável de ambiente')

completion = gpt.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'developer', 'contente': 'You are an experience network engineer. Reply in Portuguese-BR'},
        {'role': 'user', 'content': 'exiba uma lista resumida dos tipos de LSA OSPF.'}
    ]
)

print(completion.choices[0].message.content)

pass
from openai import OpenAI

gpt = OpenAI()

completion = gpt.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'developer', 'content': 'You are an experience network engineer. Reply in Portuguese-BR'},
        {'role': 'user', 'content': 'exiba uma lista resumida dos tipos de LSA OSPF.'}
    ]
)

print(completion.choices[0].message.content)
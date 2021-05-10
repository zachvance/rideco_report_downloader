import requests
response = requests.get("https://dash.sctc.rideco.com/#/exports",
                    params = {'agendas':'7c336a5f-4224-48a2-91a7-bddb36e2954f',
                              'export_type': 'ride',
                              'first_date':'2021-01-06',
                              'programs':'a0b63f37-a251-4e15-a769-36432ad8c00d',
                              'second_date':'2021-01-06', # YYYY-MM-DD format
                              'timezone':'America/Toronto'})
print(response.url)
print(response.text)
print(response.headers)

'''
response = requests.post('https://localhost:4000/bananas/12345.png', data = '[ 1, 2, 3, 4 ]')
data = response.content

with open(path, 'wb') as s:
    s.write(data)
'''
import requests

headers = {
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1NDE2NTc1fQ.gOUCOvASBE6sw3m2i2x-jES9ag8-H2VoAafrs4zWmdM" 
}
requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers= headers)
print(requisicao)
print(requisicao.json())
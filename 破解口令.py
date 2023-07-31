import requests

kouling = 1000
url = f"http://www.html22.com/cg.php?dtype=checkKouling&kouling={kouling}&did=5QpWT7Dt3btaxH3KXzs3EfE4Ai2fD3m6"

payload = {}
headers = {
    'hfs-session-id': 'eyJhbGciOiJIUzI1NiJ9.NjIzODAxNWYwMDAwMDI4NzRlNzEwZGVkLTE2NDc4Mzc1MzUzMDI.utn8lcW_CuV-PJ4w0wQ__djFdpxEMVeUOeWkNPIyof4',
    'Cookie': 'SDWG=c15c8bd7427bf359f8273c70bc996111'
}
for i in range(8999):
    kouling += 1
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)

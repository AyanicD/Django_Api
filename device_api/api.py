import requests
import json
url = "https://api.apilayer.com/exchangerates_data"
symbol_url = url+"/symbols"

payload = {}
headers= {
  "apikey": "0XZYHtg7jXVlC6G2b7GS7tFShOzHOjoX"
}

response = requests.request("GET", symbol_url, headers=headers, data = payload)

status_code = response.status_code
print(dir(response))
symbols = response.text
json_symbols = json.loads(symbols)

print("These are all the available currency: ")
for key, val in json_symbols["symbols"].items():
    print(key+': '+val)


base_curr = input("Enter Base Currency : ")
conv_curr = input("Enter Converted Currency : ")
amount = input("Enter amount to be converted : ")
conv_url = f'{url}/convert?to={conv_curr}&from={base_curr}&amount={amount}'

response = requests.request("GET", conv_url, headers=headers, data = payload)

status_code = response.status_code
result = response.text
print(response.data)
json_result = json.loads(result)
print(f'{amount} {base_curr} = {json_result["result"]} {conv_curr}')
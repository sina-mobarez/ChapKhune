import requests




def send_sms(receptor, token):
    key = "bCk-lgVEMa522x0b4ErHBT9m12Wyl1v2AAQb7WVs71Y="
    pat = 'czajmyrekf'
    url = f'http://ippanel.com:8080/?apikey={key}&pid={pat}&fnum=3000505&tnum=0{receptor}&p1=code&v1={token}'

    response = requests.get(url)
    print(response)
# pypi.org
# python -m pip install requests

from requests import get

websites = (
    'google.com',
    'naver.com',
    'https://twitter.com',
    'facebook.com',
    'https://tiktok.com'
)

results = {}

for website in websites:
    if not website.startswith("https://"):
        website = f"https://{website}"
    response = get(website)
    # print(response.status_code) # 200=OK, 400=Bad

    if response.status_code == 200: 
        results[website] = "OK"
    else: 
        results[website] = "FAILED"

print(results)

'''
HTTP Status Code

1XX : Information responses
2XX : Successful responses
3XX : Redirection messages
4XX : Client error responses
5XX : Server error reponses
'''
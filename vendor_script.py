from requests import request


## Open token file the screen
try:

    fin = open('token.txt','r')

except FileNotFoundError:
    print('Add your screen token')
    exit()

token = fin.read()
token = token.strip()


## Collect list of ads to be displayed
response = request('GET','http://127.0.0.1:8000/api?id='+token)
response=response.json()
if response['status']!='ok':
    print('Something Went wrong')
    exit()

c=0
## Download required images from the server
for url in response['media_path']:
    x='http://127.0.0.1:8000/media/'+url
    
    img=request('GET',x)
    fout = open(str(c)+'.jpg','wb')
    fout.write(img.content)
    fout.close()
    c+=1

from requests import request

"""
This Script demonstrates a raspberry-pi accessing adware-API.
copy paste your screen-token from "my screens" section into a token.txt file in the same folder.
Script will download all the images and save in current script directory.
"""

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

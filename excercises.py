import requests as re
from bs4 import BeautifulSoup
import os

URL='https://www.kaggle.com/'
response=re.get(URL)

print('response-->',response,'\ntype-->',type(response))
print('text-->',response.text,'\ncontent',response.content,'\nstatus_code-->',response.status_code)

##500-> internal server error
##503-> service in the server is unavailable

if response.status_code!=200:
    print("Http connection is not successful")
else:
    print("Http connection is successful")

soup=BeautifulSoup(response.content,"html.parser")

print('title with tags',soup.title,'title without tags',soup.title.text)

for link in soup.find_all("link"):
    print(link.get("href"))

print(soup.get_text())

## Creating a folder Mini Dataset
folder='mini_dataset'

if not os.path.exists(folder):
    os.mkdir(folder)

## Define a function that scrapes and return the url
def scrape_content(url):
    response=re.get(url)
    if response.status_code==200:
        print("Https connection was successful",url)
        return response
    else:
        print("Https connection was not successful",url)
        return None
## Define the function that saves the scraped html files
path=os.getcwd()+"/"+folder

def save_file(to_where,text,name):
    file=name+".html"
    with open(os.path.join(to_where,file),"w",encoding="utf-8") as f:
        f.write(text)

test_text=response.text
save_file(path,test_text,"example")

## Create a URL_list
url_list=['https://interviewing.io/',
          'https://stackoverflow.com/',
          'https://www.programiz.com/java-programming/online-compiler/',
          'https://www.hello.com/',
          'https://www.tutorialspoint.com/',
          'https://www.onlinegdb.com/online_java_compiler',
          'https://httpbin.org/html',
          'https://realpython.com/',
          'https://www.w3schools.com/',
          'https://www.freecodecamp.org/']

def create_min_data(to_where,url_list):
    for i in range(0,len(url_list)):
        content=scrape_content(url_list[i])

        if content is not None:
            save_file(to_where,content.text,str(i))
        else:
            pass

    print("MINI DATASET CREATED")

create_min_data(path,url_list)

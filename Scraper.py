#Per la rimozione delle stopwords, e' possibile utilizzare la collezione di stopwords contenuta nel pacchetto NLTK, famoso pacchetto dedicato al Natural Language Processing. Fare riferimento al capitolo 2, paragrafo 4.1, secondo esempio dell'NLTK book. https://www.nltk.org/book/ch02.html
#E' necessario il download del driver corrispondente per il browser a https://chromedriver.chromium.org/ (nel caso di utilizzo del browser Chrome
from selenium import webdriver
import json
number_of_pages = 300
driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://ricerca.repubblica.it/ricerca/repubblica?query=+mascherine&fromdate=2020-03-15&todate=2020-04-15&sortby=ddate&author=&mode=all")
#driver.get("https://ricerca.repubblica.it/ricerca/repubblica?query=+mascherine&fromdate=2020-03-15&todate=2020-04-15&sortby=ddate&author=&mode=all")
articles_list=[]
for page in range(number_of_pages):
    try:
        articles = driver.find_elements_by_tag_name("article")
        for i in articles:
            article={}
            title = i.find_element_by_tag_name("h1")
            #print(title.text)
            article['title'] = title.text
            abstract = i.find_element_by_tag_name("p")
            #print(abstract.text)
            article['abstract'] = abstract.text
            articles_list.append(article)
    #get the address from the "next" button
        navbar = driver.find_elements_by_class_name("pagination")
        pages_links = navbar[0].find_elements_by_tag_name("li")
        address = pages_links[-1].find_element_by_tag_name("a").get_attribute("href")
        print(address)
        with open("nomefile.json","w") as json_file:
            json.dump(articles_list, json_file)
        driver.get(address)
    except:
        driver.close()
driver.close()

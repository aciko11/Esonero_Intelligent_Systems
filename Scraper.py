#Per la rimozione delle stopwords, e' possibile utilizzare la collezione di stopwords contenuta nel pacchetto NLTK, famoso pacchetto dedicato al Natural Language Processing. Fare riferimento al capitolo 2, paragrafo 4.1, secondo esempio dell'NLTK book. https://www.nltk.org/book/ch02.html
#E' necessario il download del driver corrispondente per il browser a https://chromedriver.chromium.org/ (nel caso di utilizzo del browser Chrome
from selenium import webdriver
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os.path
import csv


number_of_pages = 192
#number_of_pages = 10
driver = webdriver.Chrome()
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




# Open the json file with all the data from the search
with open("nomefile.json") as json_file:
    json_data = json.load(json_file)


# Tokenize the words (with apostrophe)
json_data_tokenized = []
for t in json_data:
    json_data_tokenized.append(word_tokenize(t["title"]))

# Tokenize the words with no apostrophe
json_data_tokenized_no_apostrophe = []
for word in json_data_tokenized:
    tmp = [x.split("'") for x in word]
    json_data_tokenized_no_apostrophe.append([y for x in tmp for y in x])

############# Merging the NomeMaiuscolo #############
temp_data = []
for t in json_data_tokenized_no_apostrophe:
    word_tokens = t
    i = 0
    while i < len(word_tokens):
        j = i
        while i < len(word_tokens) and word_tokens[i].istitle():
            i = i + 1
        if i != j:
            i = i - 1
        if i != j:
            temp = word_tokens[j:i]
            word_tokens[j:i] = ["".join(word_tokens[j:i])]
        i = i + 1
    temp_data.append(word_tokens)




############# Cleaning the file from stopwords #############
#region cleaning_the_file_from_stopwords


# List that will contain the stop words
stop_words = []

#region check_for_my_corrected_stop_words_file 
if not os.path.exists("./stopwords.txt"):
    nltk.download("stopwords")
    nltk.download('punkt')

    temp_stop_words = stopwords.words("italian")
    print(stop_words)
    for word in temp_stop_words:
        stop_words.append(word)
        stop_words.append(word.title())
    with open("stopwords.txt", "w") as file_out:
        for item in stop_words:
            file_out.write("%s\n" % item)
else:
    with open("stopwords.txt", "r") as stop_words_file:
        for line in stop_words_file:
            stop_words.append(line[:-1])

#endregion check_for_my_corrected_stop_words_file

temp_words = []
final_data = []
for t in temp_data:
    print("Titolo non filtrato: ")
    print(t)
    final_data.append([word for word in t if not word in stop_words])
    print("Titolo filtrato: ")
    print(final_data[-1])

with open("final_data.json","w") as json_file:
            json.dump(final_data, json_file)

#endregion cleaning_the_file_from_stopwords



###################### Create the GEPHI file ####################

with open('gephi_final_data.csv', 'w', newline='') as file:
    writer = csv.writer(file, quoting = csv.QUOTE_NONE, escapechar=' ')
    for row in final_data:
        for i in range(len(row)):
            j = i + 1
            while j < len(row):
                test = row[i] + "," + row[j]
                writer.writerow([test])
                j = j + 1

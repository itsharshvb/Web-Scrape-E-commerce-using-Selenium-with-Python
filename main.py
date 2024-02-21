import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from matplotlib import pyplot as plt


class Amazon():

    def get_url(search_term,page):
        template = 'https://www.amazon.in/s?k={}&page={}'
        search_term = search_term.replace(' ','+')
        return template.format(search_term,page)



    def extract_record(item):
        #link tag
        atag= item.h2.a
        #item name
        description = atag.text.split('(')[0].strip()
        if not len(description):
            description = '(' + atag.text.split('(')[1].strip()
        elif len(description)<15:
            description = atag.text.strip()
        #item link
        url2 = 'https://www.amazon.in' +atag.get('href')
        #item price
        try:
            parent_price = item.find('span','a-price')
            price = parent_price.find('span','a-offscreen').text.replace(',','')
        except AttributeError:
            price = 'not avaliable'
        #reviews
        try:
            review_count = item.find('span', {'class':'a-size-base s-underline-text'}).text.replace(',','').replace('-','').replace('(','').replace(')','')
        except AttributeError:
            review_count = '0'

        try:
            rating = item.i.text.split(' ')[0].replace(',','')
            if not len(rating):
                rating = 'N/A'
        except AttributeError:
            rating='not avaliable'

        return(description[:50],price[1:],review_count,rating,url2)



    def main(search_term):
        driver = webdriver.Edge()
        with open('amaresults.csv', 'w', newline='', encoding='utf-8') as csvfile:
            articlewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            articlewriter.writerow(('Description','Price','Review','Rating','Url'))
        for page in range(1,5):

            url= Amazon.get_url(search_term,page)
            driver.get(url)

            soup  = BeautifulSoup(driver.page_source,'html.parser')
            results = soup.find_all('div',{'data-component-type':'s-search-result'})

            with open('amaresults.csv', 'a', newline='', encoding='utf-8') as csvfile:
                articlewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for items in results:
                    #print(extract_record(items))
                    articlewriter.writerow(Amazon.extract_record(items))
        driver.quit()


class Flipkart():
            
    def get_url(search_term,page):
        template = 'https://www.flipkart.com/search?q={}&page={}'
        search_term = search_term.replace(' ','+')
        return template.format(search_term,page)



    def extract_record(item):

        #item name
        description = item .find('div',{'class':'_4rR01T'}).text.split('-')[0]

        #item link
        url2 = 'https://www.flipkart.com/'+(item .find('a',{'class':'_1fQZEK'})).get('href')



        #item price
        try:
            price = item .find('div',{'class':'_30jeq3 _1_WHN1'}).text.strip().replace(',','')
        except AttributeError:
            price = 'XXX'
        #reviews
        try:
            review_count = (item.find('span',{'class':'_2_R_DZ'})).text.split()[3].strip().replace(',','')
        except AttributeError:
            review_count=''
        #rating
        try:
            rating = rating = item .find('div',{'class':'_3LWZlK'}).text.strip().replace(',','')
        except AttributeError:
            rating=''

        return(description,price[1:],review_count,rating,url2)



    def main(search_term):
        driver = webdriver.Edge()
        with open('flipresults.csv', 'w', newline='', encoding='utf-8') as csvfile:
            articlewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            articlewriter.writerow(('Description','Price','Review','Rating','Url'))
        for page in range(1,5):

            url= Flipkart.get_url(search_term,page)
            driver.get(url)

            soup  = BeautifulSoup(driver.page_source,'html.parser')
            results = soup.find_all('div',{'class':'_2kHMtA'})

            with open('flipresults.csv', 'a', newline='', encoding='utf-8') as csvfile:
                articlewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for items in results:
                    #print(extract_record(items))
                    articlewriter.writerow(Flipkart.extract_record(items))
        driver.quit()


class sortGraph():
    
    def main(filetobe):

        df = pd.read_csv(filetobe+'.csv').head(15)
        df1 = df.sort_values(by=['Review','Rating'],ascending= [False,False]).head(10)

        name = df['Description'].head(12)
        price = df['Price'].head(12)

        fig, ax = plt.subplots(figsize =(16, 9))

        ax.barh(name, price)
        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)

        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

        ax.invert_yaxis()

        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5,
                     str(round((i.get_width()), 2)),
                     fontsize = 10, fontweight ='bold',
                     color ='grey')

        # Add Plot Title
        ax.set_title('Product Searched for',
                     loc ='left', fontsize=20 , fontweight = 'bold' )

        # Add Text watermark
        fig.text(0.9, 0.15, 'Harshvardhan 26', fontsize = 12,
                 color ='grey', ha ='right', va ='bottom',
                 alpha = 0.7)

        plt.savefig(filetobe+'chartResult.jpg')

        df1.to_csv(filetobe +"2.csv")


class torun():
    def main(search_term):
        Amazon.main(search_term)
        Flipkart.main(search_term)
        sortGraph.main('amaresults')
        sortGraph.main('Flipresults')

    

search_term = input('\n \tEnter item to be searched for - ')

torun.main(search_term)

print("\n \tResult Generated Successfully\n")
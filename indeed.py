import requests
from bs4 import BeautifulSoup
from time import sleep
from threading import *

class indeed(Thread):
    def __init__(self, search_key, loc,number_websites):
        self.search_key=search_key
        self.loc=loc
        self.number_websites=number_websites
        super().__init__()
    def run(self):
        self.scrape_indeed(self.search_key, self.loc, self.number_websites)
    
    def join(self):
        super().join()
        return self.data_indeed

    
    def generate_indeed_url(self,search_key,loc):
        search_key=search_key.lower()
        key = search_key.split(' ')
        key = '-'.join(key)
        loc=loc.lower()
        location = loc.split(' ')
        location = '-'.join(location)
        url= "https://www.indeed.co.in/jobs?q="+key+"&l="+location+"&start="
        return url
    def scrape_indeed(self,search_key, loc,number_websites):
        counter=0
        self.data_indeed={}
        flag = True
        url=self.generate_indeed_url(search_key, loc)
        i=-10

        while(flag):
            i=i+10
            #if i>20:
                #return data_indeed
            curl=url+str(i)
            #print("i  ---> "+str(i))
            #print("curl ----> "+curl)

            page = requests.get(curl)
            #print(page)
            soup = BeautifulSoup(page.text,'html.parser')
            search_card=soup.find_all('div',{'class':'jobsearch-SerpJobCard'})
            #print('Length of search_cards --->> '+str(len(search_card)))
            '''
            if(i>50):
                break
            '''
            for card in search_card:
                #print("indeed")
                try:
                    title=card.find('a',{'class':'turnstileLink'}).get_text()
                except:
                    title="Error"
                    #print("Error in title")

                try:
                    company =card.find('span',{'class':'company'}).get_text()
                except:
                    company="Error"
                    #print("Error in Company")


                try:
                    sponsored = card.find_all('span',{'class':'sponsoredGray'})

                    if(len(sponsored)>0):
                        location = card.find('div',{'class':'location'}).get_text()
                    else:
                        location = card.find('span',{'class':'location'}).get_text()

                except:
                    location="Error"
                    #print('Error in Location')

                job_link_present=True
                try:
                    link = card.find('a',{'class':'turnstileLink'})["href"]
                    link = "https://www.indeed.co.in"+link
                except:
                    link="error"
                    #print('Error in link')
                    job_link_present=False

                exp="  "
                kskills="  "

    ##            if(job_link_present):
    ##                job_page= requests.get(link)
    ##                job = BeautifulSoup(job_page.text,'html.parser')

    ##                try:
    ##                    exp = "Not given"

    ##                except:
    ##                    exp="Error"
    ##                    print("Error in experience")

    ##                try:
    ##                    jd = job.find('div',{'class':'jobsearch-JobComponent-description'}).get_text()

    ##                except:
    ##                    jd="Error"
    ##                    print("Error in Job Description")

    ##               try:

    ##                    kskills = "Not specified"

    ##                except:
    ##                    kskills="error"
    ##                    print("error in skills")

    ##            else:
    ##                exp="Error in link"
    ##                jd="Error in link"
    ##                kskills="Error in link"


                self.data_indeed[counter]={}
                self.data_indeed[counter]["job_title"]=title
                self.data_indeed[counter]["company"]=company
                self.data_indeed[counter]["location"]=location
                self.data_indeed[counter]["experience"]=exp
                self.data_indeed[counter]["skills"]=kskills
                self.data_indeed[counter]["link"]='<a target="_blank" href="'+link+'">Click here Indeed jobs</a>'
                counter+=1
                if counter==number_websites:
                    return self.data_indeed
            #return data_indeed
            pagination = soup.select('div.pagination a')

            next_present = False
            for link in pagination:
                if 'Next' in link.get_text():
                    next_present = True
                    #print(link.get_text())
                    break
            if(next_present==False):
                flag=False
                #print("Next Present is False")
            #print("Flag value ---> "+str(flag))
            if(i%3==0):
                #print("Sleep ---> 75")
                sleep(75)
            elif(i%4==0):
                #print("Sleep ---> 90")
                sleep(90)
            elif(i%6==0):
                #print("Sleep ---> 80")
                sleep(80)
            else:
                #print("Sleep ---> 60")
                sleep(60)
        #print("Out of while loop")
        return self.data_indeed

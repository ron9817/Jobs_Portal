import requests
from bs4 import BeautifulSoup
from time import sleep
from threading import *

class aasaan(Thread):
    def __init__(self,search_key, exp, loc,number_websites):
        self.search_key=search_key
        self.exp=exp
        self.loc=loc
        self.number_websites=number_websites
        super().__init__()
        
    def run(self):
        self.scrape_aasaan(self.search_key, self.exp, self.loc, self.number_websites)
    
    def generate_aasaan_url(self,search_key,exp,loc):
        search_key=search_key.lower()
        key = search_key.split(' ')
        key = '-'.join(key)
        loc=loc.lower()
        location = loc.split(' ')
        location = '-'.join(location)
        if(type(exp)==int):
            url= "https://www.aasaanjobs.com/s/"+key+"-jobs-in-"+location+"/?experience="+str(exp)+"&page="
        else:
            url= "https://www.aasaanjobs.com/s/"+key+"-jobs-in-"+location+"/?experience="+exp+"&page="
        return url
    def join(self):
        super().join()
        return self.data_aasaan


    def scrape_aasaan(self,search_key, exp, loc,number_websites):
        counter=0
        self.data_aasaan={}
        flag = True
        url=self.generate_aasaan_url(search_key,exp,loc)
        i=0
        while(flag):
            i=i+1
            #if i>3:
                #return data_aasaan
            curl=url+str(i)
            #print("i  ---> "+str(i))
            #print("url ----> "+curl)
            page = requests.get(curl)
            soup = BeautifulSoup(page.text,'html.parser')
            search_card = soup.select('div.search-card')
            for card in search_card:
                #print("aasaan")
                try:
                    title=card.select('div a span[itemprop="title"]')[0].get_text()
                except:
                    title="Error"
                    #print("Error in title")

                try:
                    company =card.select('div p a')[0].get_text()
                except:
                    company="Error"
                    #print("Error in Company")

                try:
                    loc_sign = card.find('img',{"alt":"Location"})
                    location = loc_sign.next_element.get_text()
                except:
                    location="Error"
                    #print('Error in Location')


                exp="  "
                kskills="  "

                job_link_present=True
                try:
                    link = card.select('div a[href]')[0].get("href")
                    link = "https://www.aasaanjobs.com"+link
                except:
                    link="error"
                    #print('Error in link')
                    job_link_present=False

    ##          if(job_link_present):
    ##                job_page= requests.get(link)
    ##                job = BeautifulSoup(job_page.text,'html.parser')

    ##                try:
    ##                    exp = job.find('img',{'alt':'Experience'}).find_parent('div').find_next_sibling('div').get_text()

    ##                except:
    ##                    exp="Error"
    ##                    print("Error in experience")

    ##                try:
    ##                    jd =  job.find('div',{'itemprop':"description"}).get_text()

    ##                except:
    ##                    jd="Error"
    ##                    print("Error in Job Description")

    ##                try:
    ##                    skills = job.find_all('a',{'data-track-source':"Checklist Skills"})
    ##                    kskills = ""
    ##                    for skill in skills:
    ##                        kskills += skill.get_text() + ' , '
    ##                except:
    ##                   kskills="error"
    ##                    print("error in skills")
    ##            else:
    ##                exp="Error in link"
    ##                jd="Error in link"
    ##                kskills="Error in link"




                self.data_aasaan[counter]={}
                self.data_aasaan[counter]["job_title"]=title
                self.data_aasaan[counter]["company"]=company
                self.data_aasaan[counter]["location"]=location
                self.data_aasaan[counter]["experience"]=exp
                self.data_aasaan[counter]["skills"]=kskills
                self.data_aasaan[counter]["link"]='<a target="_blank" href="'+link+'">Click here  Aasaan jobs</a>'
                counter+=1
                if counter==number_websites:
                    return self.data_aasaan



            #return data_aasaan
            pagination = soup.select('div ul.pagination-links li')

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
                sleep(7)
            elif(i%4==0):
                #print("Sleep ---> 90")
                sleep(9)
            else:
                #print("Sleep ---> 60")
                sleep(6)
        #print("Out of while loop")
        #data =pd.DataFrame(list(zip(job_title,job_company,job_location,experience,job_link,key_skill,job_description,job_site)),columns=['Title','Company','Location','Experience','Link','Key Skills','Description','Site'])
        return self.data_aasaan

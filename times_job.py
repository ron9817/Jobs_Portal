import requests
from bs4 import BeautifulSoup
from time import sleep
from threading import *

class times_job(Thread):
    def __init__(self,search_key, exp, loc,number_websites):
        self.search_key=search_key
        self.loc=loc
        self.exp=exp
        self.number_websites=number_websites
        self.data_times={}
        super().__init__()

    def run(self):
        self.scrape_times(self.search_key, self.exp, self.loc, self.number_websites)
    
    def join(self):
        super().join()
        return self.data_times
    
    def generate_times_url(self,search_key,loc,exp):
        url=""
        search_key=search_key.lower()
        key = search_key.split(' ')
        key = '+'.join(key)
        loc=loc.lower()
        location = loc.split(' ')
        location = '+'.join(location)

        url= "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords="+key+"&txtLocation="+location+"&cboWorkExp1="+exp
        return url
    
    def scrape_times(self,search_key, exp, loc,number_websites):
        counter=0
        self.data_times={}
        flag = True

        url=self.generate_times_url(search_key,loc,exp)
        i=0
        while(flag):
            i=i+1
            curl=url+"&sequence="+str(i)+"&startPage=1"
            #print("i  ---> "+str(i))
            #print("url ----> "+curl)
            page = requests.get(curl)
            soup = BeautifulSoup(page.text,'html.parser')
            search_card = soup.find_all("li",{'class':'job-bx'})
            for card in search_card:
                #print("times")
                #print("In card")
                try:
                    title=card.find('a').text
                    #print(title)
                except:
                    title="Error"
                    #print("Error in title")

                try:
                    company =card.find('h3',{'class':"joblist-comp-name"}).text
                except:
                    company="Error"
                    #print("Error in Company")

                try:
                    exp = card.find_all('i',{"class":"material-icons"})[0].find_parent('li').text[11:]

                except:
                    exp="Error"
                    #print("Error in experience")


                try:
                    location = card.find_all('i',{"class":"material-icons"})[1].find_parent('li').text[11:]
                except:
                    location="Error"
                    #print('Error in Location')

                job_link_present=True
                try:
                    link = card.find('a')['href']

                except:
                    link="error"
                    #print('Error in link')
                    job_link_present=False

                if(job_link_present):
                    job_page= requests.get(link)
                    job = BeautifulSoup(job_page.text,'html.parser')


                    #try:
                     #   jd =  job.find('div',{'class':'job-description-main'}).get_text()

                    #except:
                     #   jd="Error"
                      #  print("Error in Job Description")

                    try:
                        skills = job.find_all('span',{'class':'jd-skill-tag'})
                        kskills = ""
                        for skill in skills:
                            kskills += skill.get_text() + ' , '
                    except:
                        kskills="error"
                        #print("error in skills")

                    #try:
                    #    salary = job.find('i',{'class':'rupee'}).find_parent('li').text

                    #except:
                     #   salary="Error"
                      #  print("Error in salary")
                else:
                    exp="Error in link"
                    jd="Error in link"
                    kskills="Error in link"


                self.data_times[counter]={}
                self.data_times[counter]["job_title"]=title
                self.data_times[counter]["company"]=company
                self.data_times[counter]["location"]=location
                self.data_times[counter]["experience"]=exp
                self.data_times[counter]["skills"]=kskills
                self.data_times[counter]["link"]='<a target="_blank" href="'+link+'">Click here Time Jobs</a>'
                counter+=1
                if counter==number_websites:
                    return self.data_times
            try:
                pagination =  soup.find('div',{'class':'srp-pagination'}).find_all('em')

                #Comment from line 123 to 131 if don't want to scrap all jobs
                #And remove ''' from line 132 and line 144

                flag=False
                if(len(pagination[len(pagination)-1].find_all('a'))!=0):
                    flag = True
                    #print("It's not end page")

                else:
                    pass
                    #print("It's  end page")
            except:
                pass

            '''
            #Example If only three pages need to scraped
            if(i==2):
                flag= False
            else:
                flag=False
                if(len(pagination[len(pagination)-1].find_all('a'))!=0):
                    flag = True
                    #print("It's not end page")

                else:
                    #print("It's  end page")
            '''

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
        #print("TIMES")
        return self.data_times
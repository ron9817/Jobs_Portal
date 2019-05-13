import requests
from bs4 import BeautifulSoup
from threading import *

class data_monster_module(Thread):
    def __init__(self,ftss,exps,lmys,number_websites):
        self.ftss=ftss
        self.exps=exps
        self.lmys=lmys
        self.number_websites=number_websites
        super().__init__()
    def run(self):
        self.monster_scrape(self.ftss,self.exps,self.lmys,self.number_websites)
    
    def join(self):
        super().join()
        return self.scraped_results
    
    def monster_scrape(self,ftss,exps,lmys,number_websites):
        self.scraped_results={}
        ftss=ftss.lower()
        exps=exps.lower()
        lmys=lmys.lower()
        counter=0
        url="https://www.monsterindia.com/"+ftss+"-jobs-in-"+lmys+".html"

        try:
            r = requests.post(url, data=dict(fts=ftss, exp=exps,lmy=lmys))
            soup = BeautifulSoup(r.text, "html.parser")
            tags = soup.find_all("div", "joblnk")
            for first in tags:
                #print("monster")
                job_title=""
                company=""
                location=""
                experience=""
                skills=""
                try:
                    job_titlee=first.find_all("span","title_in")
                    if len(job_titlee)==1:
                        job_title=job_titlee[0].text
                except:
                    job_title=ftss

                try:
                    companye=first.find_all("a","orange")
                    if len(companye)==1:
                        companye=companye[0].find_all("span")
                        if len(companye)==1:
                            company=companye[0].text
                except:
                    company="N.A."
                try:
                    locatione=first.find_all("div","ico1")
                    if len(locatione)==1:
                        locatione=locatione[0].find_all("span")
                        if len(locatione)==1:
                            location=locatione[0].text
                except:
                    location="near "+lmys
                try:
                    experiencee=first.find_all("div","ico2")
                    if len(experiencee)==1:
                        experiencee=experiencee[0].find_all("span")
                        if len(experiencee)==1:
                            experience=experiencee[0].text
                except:
                    experience="min "+exps
                try:
                    skillse=first.find_all("span","hightlighted_keyword")
                    if len(skillse)==1:
                        skills=skillse[0].parent.text
                    elif len(skillse)> 1:
                        skills=skillse[-1].parent.text
                except:
                    skills=ftss+'etc..'
                self.scraped_results[counter]={}
                self.scraped_results[counter]["job_title"]=job_title
                self.scraped_results[counter]["company"]=company
                self.scraped_results[counter]["location"]=location
                self.scraped_results[counter]["experience"]=experience
                self.scraped_results[counter]["skills"]=skills
                self.scraped_results[counter]["link"]='<a target="_blank" href="'+url+'">Click here Monster Jobs</a>'
                counter+=1
                if counter==number_websites:
                    return (1,self.scraped_results)
            return (1,self.scraped_results)
        except RuntimeError as e:
            return (-1,self.scraped_results)

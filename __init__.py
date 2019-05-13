import data_monster_module
import aasaan
import indeed
import times_job
from flask import Flask,render_template,request,redirect,url_for

app=Flask(__name__)

def dict_to_list(data):
    l=[]
    for i in data:
        k=[]
        for j in data[i]:
            k.append(data[i][j])
        l.append(k)
    return l


@app.route('/',methods=['get','post'])
def index():
    if request.method == "POST":
        ftss=request.form['skill']
        exps=request.form['experience']
        lmys=request.form['location']
        search_website=request.form.getlist('search_website')
        number_websites=int(request.form['number_websites'])
        if len(search_website) != 0:
            if  "monster" in search_website:
                try:
                    data_monster_O=data_monster_module.data_monster_module(ftss,exps,lmys,number_websites)
                    data_monster_O.start()
                    #data_monster=dict_to_list(data_monster)
                except Exception as e:
                    #print("M_O_N_S_T_E_R_E_R_R_O_R", e)
                    return redirect(url_for('index'))
            else:
                data_monster=[]
            if "aasaan" in search_website:
                try:
                    data_aasaan_O=aasaan.aasaan(ftss, exps, lmys,number_websites)
                    data_aasaan_O.start()
                    #data_aasaan=dict_to_list(data_aasaan)
                except Exception as e:
                    #print("A_S_S_A_A_N_E_R_R_O_R", e)
                    return redirect(url_for('index'))
            else:
                data_aasaan=[]
            if "indeed" in search_website:
                try:
                    data_indeed_O=indeed.indeed(ftss,lmys,number_websites)
                    data_indeed_O.start()
                    #data_indeed=dict_to_list(data_indeed)
                except Exception as e:
                    #print("I_N_D_E_E_D_E_R_R_O_R", e)
                    return redirect(url_for('index'))
            else:
                data_indeed=[]
            if "times" in search_website:
                try:
                    data_times_O=times_job.times_job(ftss,exps,lmys,number_websites)
                    data_times_O.start()
                    #data_times=data_times_O.join()
                    #data_times=dict_to_list(data_times)
                except Exception as e:
                    #print("T_I_M_E_S_E_R_R_O_R", e)
                    return redirect(url_for('index'))
            else:
                data_times=[]
                
            
            #print(data_monster, data_indeed, data_aasaan, data_times)
            
            if "monster" in search_website:
                try:
                    data_monster=data_monster_O.join()
                    data_monster=dict_to_list(data_monster)
                except Exception as e:
                    #print("M_O_N_S_T_E_R_E_R_R_O_R", e)
                    return redirect(url_for('index'))
            else:
                data_monster=[]
            if "aasaan" in search_website:
                try:
                    data_aasaan=data_aasaan_O.join()
                    data_aasaan=dict_to_list(data_aasaan)
                except Exception as e:
                    #print("A_A_S_A_A_n_E_R_R_O_R", e)
                    return redirect(url_for('index'))
            else:
                data_aasaan=[]
            if "indeed" in search_website:
                try:
                    data_indeed=data_indeed_O.join()
                    data_indeed=dict_to_list(data_indeed)
                except Exception as e:
                    #print("I_N_D_E_E_D_E_R_R_O_R", e)
                    return redirect(url_for('index'))
            else:
                data_indeed=[]
            if "times" in search_website:
                try:
                    data_times=data_times_O.join()
                    data_times=dict_to_list(data_times)
                except Exception as e:
                    #print("T_I_M_E_S_E_R_R_O_R", e)
                    return redirect(url_for('index'))
            else:
                data_times=[]
                
            
            return render_template('home.html',data_monster=data_monster, data_indeed=data_indeed, data_aasaan=data_aasaan, data_times=data_times, skill=ftss,experience=exps,location=lmys)
        else:
            return redirect(url_for('index'))
    return render_template('home.html')


if __name__=="__main__":
    app.run(debug=True)
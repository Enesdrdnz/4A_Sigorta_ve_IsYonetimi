from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime
import shutil
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import re
class Sigorta():
    def __init__(self) -> None:
        pass     
    def Sign_in(self,account_name,account_name2,account_psw_1,account_psw_2):
        self.browser=webdriver.Chrome()
        self.account_name=account_name
        self.account_name2=account_name2
        self.account_psw_1=account_psw_1
        self.account_psw_2=account_psw_2
        self.browser.get("https://uyg.sgk.gov.tr/SigortaliTescil/amp/loginldap")
        username=self.browser.find_element(By.NAME,"j_username")
        username.send_keys(self.account_name)
        username_cont=self.browser.find_element(By.NAME,"isyeri_kod")
        username_cont.send_keys(self.account_name2)
        password1=self.browser.find_element(By.NAME,"j_password")
        password2=self.browser.find_element(By.NAME,"isyeri_sifre")
        password1.send_keys(self.account_psw_1)
        password2.send_keys(self.account_psw_2)
        # BU NOKTADAN SONRA KULLANICININ GÜVENLİK KODUNU GİRMESİ 8 SANİYE BEKLENECEKTİR
        guvenlik_code=self.browser.find_element(By.NAME,"isyeri_guvenlik")
        guvenlik_code.click()
        button=self.browser.find_element(By.NAME,"buttonOK")
        time.sleep(8)
        button.click()
    def ENTER_LEAVE_CONTROL(self,Fday,Fmonth,Fyear,Lday,Lmonth,Lyear):
        self.Sign_in()
        action=webdriver.ActionChains(self.browser)
        button_page=self.browser.find_elements(By.TAG_NAME,"a")[-2]
        button_page.click()
        days_in_month_turkish = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
        while True:
            inputs=self.browser.find_elements(By.TAG_NAME,"input")
            inputs[3].send_keys(Fday)
            time.sleep(1)
            action.key_down(Keys.TAB).perform()
            inputs[4].send_keys(Fmonth)
            time.sleep(1)
            action.key_down(Keys.TAB).perform()
            inputs[5].send_keys(Fyear)
            time.sleep(1)
            if (Fday+14 <=days_in_month_turkish[int(Fmonth)]):
                Fday+=14
            else:          
                Fday=14-(days_in_month_turkish[int(Fmonth)]-Fday)
                if (Fmonth==12):
                    Fmonth=1
                    Fyear+=1
                else:
                    Fmonth+=1
            try:
                current_date = datetime.datetime(Fyear,Fmonth,Fday).date()
                target_date = datetime.datetime(Lyear,Lmonth,Lday).date()
            except:
                pass
            if (Fmonth==Lmonth and Fyear==Lyear and Fday>Lday):
                Fday=Lday       
            17/3/2014
            action.key_down(Keys.TAB).perform()
            inputs[6].send_keys(Fday)
            time.sleep(1)
            action.key_down(Keys.TAB).perform()
            inputs[7].send_keys(Fmonth)
            time.sleep(1)
            action.key_down(Keys.TAB).perform()
            year_input=self.browser.find_element(By.XPATH,"/html/body/table[3]/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[1]/input[6]")
            inputs[8].send_keys(Fyear)
            time.sleep(3)
            search_button=self.browser.find_element(By.NAME,"sorgulabtn")
            search_button.click()
            time.sleep(4)
            try:
                exeldownload=self.browser.find_elements(By.TAG_NAME,"span")[-1]
                exeldownload.click()
            except:
                pass
            
            if Fday==days_in_month_turkish[Fmonth]:
                Fday=1
            else:
                Fday+=1
            if target_date<current_date :
                Fday=datetime.datetime.now().day
                Fmonth=datetime.datetime.now().month+1
                Fyear=datetime.datetime.now().year
                break
    def get_Excels(self):
        #exel dosyaları indirilenlere düştüğü ve orada daha önce hareket.xls dosyası bulunmadığı varsayılmıştır!
        #gönderilecek sayı en son exel 
        in_count=0
        while True:
            if in_count==0:
                shutil.copyfile('C:\\Users\\Enes\\Downloads\\hareket.xls','exel\\hareket.txt')
                in_count+=1
            elif in_count>0:
                try:
                    shutil.copyfile(f'C:\\Users\\Enes\Downloads\\hareket ({in_count}).xls',f'exel\\hareket ({in_count}).txt')
                    in_count+=1
                except:
                    break          
    def Process_employees_info(self):
        veri=[]
        sayac_pr=0
        while True:
            if sayac_pr==0:
                with open("exel\\hareket.txt") as file:
                    for satir in file:
                        veri.append(satir)
                sayac_pr+=1
            else:
                try:
                    with open(f'exel\\hareket ({sayac_pr}).txt') as file:
                        for satir in file:
                            veri.append(satir)
                    sayac_pr+=1
                except:
                    break
            
        
        veri_2=[]
        for inf in veri:
            series=[]
            for j in [1,3,5,7,13,15,17]:
                if j ==3:
                    series.append(re.sub(r'\s+', ' ',inf.split("\"")[3]))
                else:
                    series.append(inf.split("\"")[j])
            veri_2.append(series)
        dataframe=pd.DataFrame(veri_2,columns=["T.C","NAME","TYPE","BASLANGIC_TARIH","ISLEM","ISLEM_TARIH","ISLEM_SAAT"])
        remove=dataframe.loc[dataframe["T.C"].apply(lambda x: len(str(x))) != 11].index
        dataframe.drop(remove,inplace=True)
        
        dataframe["ISLEM_TARIH"]=pd.to_datetime(dataframe["ISLEM_TARIH"],format='%d.%m.%Y')
        dataframe["BASLANGIC_TARIH"]=pd.to_datetime(dataframe["BASLANGIC_TARIH"],format='%d.%m.%Y')

        return dataframe 
    def Get_active_employees(self,dataframe):
        #bu fonksiyonu kullanmadan Process_employees_info() fonksiyonundan return edilen değeri kaydet değişkene
        #ve diğer fonksiyondan dönen dataframe i buna parametre olarak gir
        isemployees=[]
        grouped=dataframe.groupby("T.C")

        for group_name, group_indices in grouped.groups.items():
            group_data = dataframe.loc[group_indices]
            
            if len(group_data[["T.C","NAME","TYPE","ISLEM"]].to_numpy().tolist())>1:
                keep=[]
                for i in range(len(group_data[["T.C","NAME","TYPE","ISLEM"]].to_numpy().tolist())):
                    keep.append(group_data[["T.C","NAME","TYPE","ISLEM"]].to_numpy().tolist()[i])
                isemployees.append(keep)
            else:
                isemployees.append(group_data[["T.C","NAME","TYPE","ISLEM"]].to_numpy().tolist())

        for i in range(len(isemployees)):
            recordsayac=0
            for j in range(len(isemployees[i])):
                if((isemployees[i][j][1]=="Giriş") and (isemployees[i][j][2]=="Kayıt")):
                    recordsayac+=1
                elif((isemployees[i][j][1]=="Giriş") and (isemployees[i][j][2]=="Silme")):
                    recordsayac-=1
                elif(isemployees[i][j][1]=="Çıkış" and (isemployees[i][j][2]=="Kayıt")):
                    recordsayac-=1
                elif(isemployees[i][j][1]=="Çıkış" and (isemployees[i][j][2]=="Silme")):
                    recordsayac+=1
            
            
            if recordsayac<=0:
                isemployees[i][0].append("pasive")
            elif recordsayac>0:
                isemployees[i][0].append("active") 

        last_list=[]
        for employee in isemployees:
            last_list.append(employee[0])
        return last_list
    def give_exel(self,Fday,Fmonth,Fyear,Lday,Lmonth,Lyear,data):
        columns = ["id", "tc", "name", "aktif_tarih", "islem_tarih", "kayıt-silme", "islem"]
        dataframe_exel=pd.DataFrame(data,columns=columns)
        dataframe_exel['aktif_tarih'] = pd.to_datetime(dataframe_exel['aktif_tarih'])
        dataframe_exel['islem_tarih'] = pd.to_datetime(dataframe_exel['islem_tarih'])
        
        specific_date_starting = pd.to_datetime(f'{Fyear}-{Fmonth}-{Fday}', format='%Y-%m-%d')
        specific_date_ending=pd.to_datetime(f'{Lyear}-{Lmonth}-{Lday}', format='%Y-%m-%d')
        filtered_df = dataframe_exel[dataframe_exel['islem_tarih'] >= specific_date_starting]
        filtered_df = filtered_df[filtered_df['islem_tarih'] <= specific_date_ending]

        filtered_df['islem_tarih']=filtered_df["islem_tarih"].dt.strftime('%d.%m.%y')
        filtered_df['aktif_tarih']=filtered_df["aktif_tarih"].dt.strftime('%d.%m.%y')

        with pd.ExcelWriter(path=r"Sigorta_kayit.xlsx") as writer:
            filtered_df.to_excel(writer,sheet_name="sigorta")        















































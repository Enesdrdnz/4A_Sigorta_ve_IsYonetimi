import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import tkinter as tk  
import main
from tkinter import messagebox
import hashlib
import mysql.connector
from unidecode import unidecode
import time

class my_App(tk.Tk):
    def __init__(self):
        super().__init__()
        # set_window_config
        self.uygulama_name=""
        self.uygulama_password=""

        self.sha_name=""
        self.sha_password=""
        self.giris=False
        self.geometry("1024x900")
        self.title("INSURANCE APP")

        self.resizable(width=False,height=False)
        self.main_frame=self
        self.load_main_widgets()
        #style add
        self.style = Style(theme='journal')
    def set_theme(self, theme):
        self.style.theme_use(theme)
    def get_Employees(self):
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password=self.uygulama_password,
            database="sigorta_db",
            auth_plugin="mysql_native_password"
        )

        mycursor=mydb.cursor()
        mycursor.execute("SELECT * FROM employees")
        result=mycursor.fetchall()
        return result
    def UPDATE_CONTROL(self):
        last_day=int(self.active_detail_Entry_1.get())
        last_month=int(self.active_detail_Entry_2.get())
        last_year=int(self.active_detail_Entry_3.get())
        firstfull=self.active_detail_2.cget("text").split(".")
        if "." not in firstfull:
            firstfull=self.active_detail_2["text"].split(".")
        first_day=int(firstfull[0])
        first_month=int(firstfull[1])
        first_year=int(firstfull[2])
        selenium.ENTER_LEAVE_CONTROL(first_day,first_month,first_year,last_day,last_month,last_year)
        time.sleep(3)
        # selenium.get_Excels()
        dataframe_employees=selenium.Process_employees_info()
        list_employees=dataframe_employees.values.tolist()
        print(len(list_employees))
        for person in list_employees:
            mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password=self.uygulama_password,
                database="sigorta_db",
                auth_plugin="mysql_native_password"
            )
            sql="INSERT INTO employees(TC,NAMESURNAME,AKTIFTARIH,ISLEMTARIH,KAYIT_SILME,ISLEM) VALUES (%s,%s,%s,%s,%s,%s)"
            values=(int(person[0]),person[1],person[3].strftime("%Y-%m-%d"),person[5].strftime("%Y-%m-%d"),person[4],person[2])    
            mycursor=mydb.cursor()
            mycursor.execute(sql,values)
            try:
                mydb.commit()
            except mysql.connector.errors as err:
                print("hata:",err)
            finally:
                mydb.close()
                print("bitti")

            
            self.tvw.insert("",END,values=(person[0],person[1],person[3].strftime("%Y-%m-%d"),person[4],person[5]))
        tarih=f"{last_day}.{last_month}.{last_year}"
        with open("date.txt","w") as file:
            file.write(tarih)
        self.active_detail_2["text"]=tarih
    def exel_yaz(self):
        fd=int(self.exel_detail_Entry_1.get())
        fm=int(self.exel_detail_Entry_2.get())
        fy=int(self.exel_detail_Entry_3.get())

        ld=int(self.exel_detail_Entry_4.get())
        lm=int(self.exel_detail_Entry_5.get())
        ly=int(self.exel_detail_Entry_6.get())
        selenium.give_exel(fd,fm,fy,ld,lm,ly,self.get_Employees())

        messagebox.showinfo(message="Masaüstüne kayıt edilmiştir!")

        self.exel_detail_Entry_1.delete(0,END)
        self.exel_detail_Entry_2.delete(0,END)
        self.exel_detail_Entry_3.delete(0,END)
        self.exel_detail_Entry_4.delete(0,END)
        self.exel_detail_Entry_5.delete(0,END)
        self.exel_detail_Entry_6.delete(0,END)
    def load_main_widgets(self):
        self.first_frame=tb.Frame(self.main_frame)
        self.first_frame.pack()
        self.second_frame=tb.Frame(self.main_frame)
        self.second_frame.pack()
        self.create_pager()
        self.Uygulama_giris()
        # self.search_employee()
    def indicate(self,page):
        self.delete_pages()
        page()
    def delete_pages(self):
        for frame in  self.second_frame.winfo_children():
            frame.destroy()   
    def create_pager(self):
        self.pager=tb.Frame(
            self.first_frame,
            height=150
        )
        self.pager.columnconfigure(0,weight=1)
        self.pager.columnconfigure(1,weight=1)
        self.pager.grid(column=0,row=0)
        self.encounter_image_1=tb.PhotoImage(file="")
        self.encounterLabel_2=tb.Label(self.pager,image=self.encounter_image_1)
        self.encounterLabel_2.grid(column=0,row=0,padx=(0,50))

        button_1=tb.Button(self.pager,text="SİGORTA HAREKETLERİ",padding=20,bootstyle="dark",width=20,command=lambda:self.indicate(self.create_SIGORTA_page_container))
        button_1.grid(column=1,row=0)
        
        button_2=tb.Button(self.pager,text="YAKINDA",padding=20,bootstyle="dark",width=15)
        button_2.grid(column=4,row=0,padx=20)

        button_2=tb.Button(self.pager,text="BÖLGE-GÖRÜNTÜLE",padding=20,bootstyle="dark",width=22,command=lambda:self.indicate(self.Bolge_Goruntule))
        button_2.grid(column=3,row=0,padx=20)

        button_2=tb.Button(self.pager,text="ELEMAN ARA",padding=20,bootstyle="dark",width=15,command=lambda:self.indicate(self.search_employee_func))
        button_2.grid(column=2,row=0,padx=20)
        
        #self.first_frame e bağlı
        self.label=tb.Label(self.first_frame,background="black",width=170)
        self.label.grid(column=0,row=1)
    def create_SIGORTA_page_container(self):
        if self.giris:
            sigorta_hareket=["Tüm Hareketler","Giriş Hareketleri","Çıkış Hareketleri"]
            self.hareket_comboBox=tb.Combobox(self.second_frame,values=sigorta_hareket,bootstyle="dark",width=43,font="Arial 24")
            self.hareket_comboBox.current(0)
            self.hareket_comboBox.pack(pady=15)

            self.Active_employee_frame=tb.Frame(self.second_frame)
            self.Active_employee_frame.pack(padx=10,pady=10)
            self.child_active_frame_1=tb.Frame(self.Active_employee_frame,bootstyle="dark")
            self.child_active_frame_1.pack(fill=X)
            
            self.my_Scroll=tb.Scrollbar(self.child_active_frame_1,orient="vertical")
            self.my_Scroll.pack(side="right",fill=Y) 
            self.tvw=tb.Treeview(self.child_active_frame_1,show="headings",height=20,bootstyle="dark",yscrollcommand=self.my_Scroll.set)
            self.tvw.pack()
        
            self.my_Scroll.config(command=self.tvw.yview)
            # column
            self.tvw["column"]=("TC","NAME-SURNAME","AKTIF-TARIH","KAYIT-SİLME","ISLEM")
            self.tvw.column("#0",width=150,minwidth=100) 
            self.tvw.column("#1",width=150,minwidth=100)
            self.tvw.column("#2",width=250,minwidth=100)
            self.tvw.column("#3",width=150,minwidth=100)
            self.tvw.column("#4",width=150,minwidth=100)

            self.tvw.heading("TC",text="TC",anchor="w")
            self.tvw.heading("NAME-SURNAME",text="NAME-SURNAME",anchor="w")
            self.tvw.heading("AKTIF-TARIH",text="AKTIF-TARIH",anchor="w")
            self.tvw.heading("KAYIT-SİLME",text="KAYIT-SİLME",anchor="w")
            self.tvw.heading("ISLEM",text="ISLEM",anchor="w")
            
            data_hareket=self.get_Employees()
            
            self.child_active_frame_2=tb.Labelframe(self.Active_employee_frame,bootstyle="dark",text="TÜM KAYITLAR")
            self.child_active_frame_2.pack(fill=X,pady=20)
            
            self.active_detail_1=tb.Label(self.child_active_frame_2,text="EN SON GÜNCELLENME TARİHİ",bootstyle="secondary inverse",padding=10)
            self.active_detail_1.grid(column=0,row=0,padx=10,pady=10)
            
            with open ("date.txt","r") as file:
                date=file.read()
            self.active_detail_2=tb.Label(self.child_active_frame_2,text=date,bootstyle="secondary inverse",padding=10,width=17,anchor="center")
            self.active_detail_2.grid(column=1,row=0,padx=10,pady=10)
            
            self.active_detail_1=tb.Label(self.child_active_frame_2,text="GÜNCELLENECEK TARİH",bootstyle="secondary inverse",padding=10,width=28,anchor="center")
            self.active_detail_1.grid(column=0,row=1,padx=10,pady=10,sticky="w")
            self.active_detail_Entry_frame=tb.Frame(self.child_active_frame_2)
            self.active_detail_Entry_frame.grid(column=1,row=1)

            self.active_detail_Entry_1=tb.Entry(self.active_detail_Entry_frame,width=3,bootstyle="dark")
            self.active_detail_Entry_1.grid(column=0,row=0,padx=3)

            self.active_detail_Entry_2=tb.Entry(self.active_detail_Entry_frame,width=3,bootstyle="dark")
            self.active_detail_Entry_2.grid(column=1,row=0,padx=3)

            self.active_detail_Entry_3=tb.Entry(self.active_detail_Entry_frame,width=3,bootstyle="dark")
            self.active_detail_Entry_3.grid(column=2,row=0,padx=3)

            self.update_button=tb.Button(self.child_active_frame_2,text="GÜNCELLE",bootstyle="dark inserve",command=self.UPDATE_CONTROL)
            self.update_button.grid(column=3,row=1,padx=10)


            # exel döndürecek kısım
            self.exel_return=tb.Labelframe(self.Active_employee_frame,bootstyle="dark",text="EXEL AL")
            self.exel_return.pack(fill=X,pady=20)
            self.exel_table=tb.Label(self.exel_return,text="Tarih Aralığı",bootstyle="secondary inverse",padding=10,width=28,anchor="center")
            self.exel_table.grid(column=0,row=1,padx=10,pady=10)
            
            
            #başlık 
            self.exel_entry_label_1=tb.Label(self.exel_return,text="Baslangıç Tarihi",bootstyle="secondary inverse",anchor="center",padding=5)
            self.exel_entry_label_1.grid(column=1,row=0,padx=5)
            
            self.exel_entry_label_2=tb.Label(self.exel_return,text="Bitiş Tarihi",bootstyle="secondary inverse",anchor="center",padding=5)
            self.exel_entry_label_2.grid(column=2,row=0,padx=5)

            #1.entry kısmı
            self.exel_entry_frame=tb.Frame(self.exel_return)
            self.exel_entry_frame.grid(column=1,row=1,padx=10)

            self.exel_detail_Entry_1=tb.Entry(self.exel_entry_frame,width=3,bootstyle="dark")
            self.exel_detail_Entry_1.grid(column=0,row=1,padx=3)

            self.exel_detail_Entry_2=tb.Entry(self.exel_entry_frame,width=3,bootstyle="dark")
            self.exel_detail_Entry_2.grid(column=1,row=1,padx=3)

            self.exel_detail_Entry_3=tb.Entry(self.exel_entry_frame,width=3,bootstyle="dark")
            self.exel_detail_Entry_3.grid(column=2,row=1,padx=3)

            #2.entry kısmı
            
            self.exel_entry_frame_2=tb.Frame(self.exel_return)
            self.exel_entry_frame_2.grid(column=2,row=1,padx=10)

            self.exel_detail_Entry_4=tb.Entry(self.exel_entry_frame_2,width=3,bootstyle="dark")
            self.exel_detail_Entry_4.grid(column=0,row=1,padx=3)

            self.exel_detail_Entry_5=tb.Entry(self.exel_entry_frame_2,width=3,bootstyle="dark")
            self.exel_detail_Entry_5.grid(column=1,row=1,padx=3)

            self.exel_detail_Entry_6=tb.Entry(self.exel_entry_frame_2,width=3,bootstyle="dark")
            self.exel_detail_Entry_6.grid(column=2,row=1,padx=3)

            self.exel_button=tb.Button(self.exel_return,text="EXEL GETİR",bootstyle="dark inserve",command=self.exel_yaz)
            self.exel_button.grid(column=3,row=1,padx=20)
            self.hareket_treeview_guncelle()
            self.tvw.tag_configure("bigfont",font="Arial 12")
            for item in self.tvw.get_children():
                self.tvw.item(item, tags=("bigfont",))
            self.hareket_comboBox.bind("<<ComboboxSelected>>",self.hareket_treeview_guncelle)
        else:
            self.Uygulama_giris()
    def hareket_treeview_guncelle(self,event=None):
        data_hareket=self.get_Employees()
        for item in self.tvw.get_children():
            self.tvw.delete(item)
        type_hareket=self.hareket_comboBox.get()
        for employee in data_hareket:
            if employee[6]=='Giriş' and type_hareket=="Giriş Hareketleri": 
                self.tvw.insert("",END,values=(employee[1],employee[2],f"{employee[3].split('-')[2]}.{employee[3].split('-')[1]}.{employee[3].split('-')[0]}",employee[5],employee[6]))
            elif employee[6]=='Çıkış' and type_hareket=="Çıkış Hareketleri":
                self.tvw.insert("",END,values=(employee[1],employee[2],f"{employee[3].split('-')[2]}.{employee[3].split('-')[1]}.{employee[3].split('-')[0]}",employee[5],employee[6]))
            elif type_hareket=="Tüm Hareketler":
                self.tvw.insert("",END,values=(employee[1],employee[2],f"{employee[3].split('-')[2]}.{employee[3].split('-')[1]}.{employee[3].split('-')[0]}",employee[5],employee[6]))
        for item in self.tvw.get_children():
            self.tvw.item(item, tags=("bigfont",))
    def Bolge_Goruntule(self):
        if self.giris:
            self.bolge_employee_frame=tb.Frame(self.second_frame)
            self.bolge_employee_frame.pack(padx=10,pady=10)
            self.child_bolge_active_frame_1=tb.Frame(self.bolge_employee_frame,bootstyle="dark")
            self.child_bolge_active_frame_1.pack(fill=X)
            
            self.my_Scroll_1=tb.Scrollbar(self.child_bolge_active_frame_1,orient="vertical")
            self.my_Scroll_1.pack(side="right",fill=Y) 
            self.tvw_bolge=tb.Treeview(self.child_bolge_active_frame_1,show="headings",height=20,bootstyle="dark",yscrollcommand=self.my_Scroll_1.set)
            self.tvw_bolge.pack()
            
            self.my_Scroll_1.config(command=self.tvw_bolge.yview)
            # column
            self.tvw_bolge["column"]=("TC","NAME-SURNAME","GİRİŞ-TARİH")
            self.tvw_bolge.column("#0",width=250,minwidth=100) 
            self.tvw_bolge.column("#1",width=250,minwidth=100)
            self.tvw_bolge.column("#2",width=250,minwidth=100)

            self.tvw_bolge.heading("TC",text="TC",anchor="w")
            self.tvw_bolge.heading("NAME-SURNAME",text="NAME-SURNAME",anchor="w")
            self.tvw_bolge.heading("GİRİŞ-TARİH",text="BÖLGE",anchor="w")
        

            self.tvw_bolge.tag_configure("bigfont",font="Arial 12")
            for item in self.tvw_bolge.get_children():
                self.tvw_bolge.item(item, tags=("bigfont",))
            
            
            
            bolgeler=["EXAMPLE1","EXAMPLE2","EXAMPLE3"]
            self.bolge_comboBox=tb.Combobox(self.bolge_employee_frame,values=bolgeler,bootstyle="dark",width=38,font="Arial 24")
            self.bolge_comboBox.current(0)
            self.bolge_comboBox.pack(pady=15)
            
            self.detail_bolge_frame=tb.Labelframe(self.bolge_employee_frame,bootstyle="dark",text="BÖLGE BİLGİLERİ")
            self.detail_bolge_frame.pack(padx=10,pady=10,fill=X)

            self.detail_bolge_label_1=tb.Label(self.detail_bolge_frame,bootstyle="dark inverse",text="BOLGEYE EKLE",padding=10,width=18,anchor="center")
            self.detail_bolge_label_1.grid(column=0,row=2,padx=10,pady=10)

            self.detail_bolge_label_2=tb.Label(self.detail_bolge_frame,bootstyle="dark inverse",width=16,anchor="center",text="TC",padding=10)
            self.detail_bolge_label_2.grid(column=1,row=1,padx=10,pady=10)

            self.detail_bolge_label_3=tb.Label(self.detail_bolge_frame,bootstyle="dark inverse",width=16,anchor="center",text="Adı Soyadı",padding=10)
            self.detail_bolge_label_3.grid(column=2,row=1,padx=10,pady=10)

            self.detail_bolge_label_4=tb.Label(self.detail_bolge_frame,bootstyle="dark inverse",width=18,anchor="center",text="Bölge",padding=10)
            self.detail_bolge_label_4.grid(column=3,row=1,padx=10,pady=10)

            self.detail_bolge_label_5=tb.Label(self.detail_bolge_frame,bootstyle="dark inverse",width=18,anchor="center",text="BOLGEDEN ÇIKART",padding=10)
            self.detail_bolge_label_5.grid(column=0,row=3,padx=10,pady=10)

            self.detail_bolge_entry_1=tb.Entry(self.detail_bolge_frame,bootstyle="dark",width=10,font="Arial 15")
            self.detail_bolge_entry_1.grid(column=1,row=2)

            self.detail_bolge_entry_2=tb.Entry(self.detail_bolge_frame,bootstyle="dark",width=10,font="Arial 15")
            self.detail_bolge_entry_2.grid(column=2,row=2)

            self.detail_bolge_entry_3=tb.Entry(self.detail_bolge_frame,bootstyle="dark",width=10,font="Arial 15")
            self.detail_bolge_entry_3.grid(column=1,row=3)

            self.bolge_add_combobox=tb.Combobox(self.detail_bolge_frame,values=bolgeler,bootstyle="dark",width=10,font="Arial 14")
            self.bolge_add_combobox.grid(row=2,column=3,padx=5)

            self.bolge_add_employee=tb.Button(self.detail_bolge_frame,bootstyle="dark",width=10,padding=10,text="Ekle",command=self.bolge_eleman_ekle)
            self.bolge_add_employee.grid(column=4,row=2)

            self.bolge_add_employee_2=tb.Button(self.detail_bolge_frame,bootstyle="dark",width=10,padding=10,text="Çıkart",command=self.bolge_eleman_cıkart)
            self.bolge_add_employee_2.grid(column=2,row=3)
            self.bolge_comboBox.bind("<<ComboboxSelected>>",self.bolge_treeview_güncelle)
            
            self.bolge_treeview_güncelle()
            self.tvw_bolge.tag_configure("bigfont",font="Arial 12")
            for item in self.tvw_bolge.get_children():
                self.tvw_bolge.item(item, tags=("bigfont",))  
        else:
            self.Uygulama_giris()
    def bolge_eleman_ekle(self):
        
        tc=self.detail_bolge_entry_1.get()
        name=self.detail_bolge_entry_2.get()
        secim=self.bolge_add_combobox.get()
        if len(tc)!=11 or secim=="":
            messagebox.showerror(message="Hatalı işlem tekrar deneyiniz")
        else:
            mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password=self.uygulama_password,
                database="sigorta_db",
                auth_plugin="mysql_native_password"
            )   
            sql="INSERT INTO region_employees(tc,name_surname,region) VALUES (%s,%s,%s)"
            values=(tc,name,secim)    
            mycursor=mydb.cursor()
            mycursor.execute(sql,values)
            try:
                mydb.commit()
            except mysql.connector.errors as err:
                print("hata:",err)
            finally:
                mydb.close()
                self.bolge_treeview_güncelle()

                self.detail_bolge_entry_1.delete(0,END)
                self.detail_bolge_entry_2.delete(0,END)
    def bolge_eleman_cıkart(self):
        
        
        try:
            tc_remove=self.detail_bolge_entry_3.get()
            mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password=self.uygulama_password,
                database="sigorta_db",
                auth_plugin="mysql_native_password"
            )
            cursor=mydb.cursor()
            sql = "DELETE FROM region_employees WHERE tc=%s"
            values = (tc_remove,)
            cursor.execute(sql, values)
            mydb.commit()

           
        except  Exception as e:
            messagebox.showerror("Database hatası", str(e))
        finally:
            mydb.close()
            

        try:
            mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password=self.uygulama_password,
                database="sigorta_db",
                auth_plugin="mysql_native_password"
            )
            mycursor=mydb.cursor()
            mycursor.execute("SELECT * FROM region_employees")
            result=mycursor.fetchall()
        except:
            pass
        finally:
            mydb.close()
        tcs=[]
        for eleman in result:
            tcs.append(str(eleman[1]))
            print(tcs)
        print(self.detail_bolge_entry_3.get())
        if self.detail_bolge_entry_3.get() not in tcs:
            messagebox.showinfo("Success", "Record deleted successfully!")
            self.detail_bolge_entry_3.delete(0,END)
            self.bolge_treeview_güncelle()
        else:
            messagebox.showerror(message="BU KİMLİK HERHANGİ BİR BÖLGEYE TANIMLI DEĞİL")
            self.bolge_treeview_güncelle()         
    def bolge_treeview_güncelle(self,event=None):
        items=self.tvw_bolge.get_children()
        for item in items:
            self.tvw_bolge.delete(item)
        bolge=self.bolge_comboBox.get()
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password=self.uygulama_password,
            database="sigorta_db",
            auth_plugin="mysql_native_password"
        )
        mycursor=mydb.cursor()
        mycursor.execute("SELECT * FROM region_employees")
        result=mycursor.fetchall()
        for employee in result:
            if employee[3]==bolge:
                self.tvw_bolge.insert("",END,values=(employee[1],employee[2],employee[3]))
        self.tvw_bolge.tag_configure("bigfont",font="Arial 12")
        for item in self.tvw_bolge.get_children():
            self.tvw_bolge.item(item, tags=("bigfont",))
    
    def Uygulama_giris(self):
        self.uygulama_giris_frame=tb.LabelFrame(self.second_frame,text="UYGULAMAYA GİRİŞ",bootstyle="dark",padding=50)
        self.uygulama_giris_frame.pack(padx=20,pady=60)

        uygulama_label_1=tb.Label(self.uygulama_giris_frame,text="Kullanıcı adı",bootstyle="dark  inverse",font="Arial 18",padding=5)
        uygulama_label_1.grid(column=0,row=0,pady=5)
        uygulama_label_2=tb.Label(self.uygulama_giris_frame,text="Şifre",anchor="center",bootstyle="dark inverse",font="Arial 18",width=11)
        uygulama_label_2.grid(column=0,row=1,pady=5)
        self.uygulama_entry_1=tb.Entry(self.uygulama_giris_frame,bootstyle="dark",font="Arial 13")
        self.uygulama_entry_1.grid(column=1,row=0,padx=15)
        self.uygulama_entry_2=tb.Entry(self.uygulama_giris_frame,bootstyle="dark",font="Arial 13",show="*")
        self.uygulama_entry_2.grid(column=1,row=1,padx=15)
        self.button_uygulama_gir=tb.Button(self.uygulama_giris_frame,text="GİRİŞ",padding=5,width=30,bootstyle="dark",command=self.Verify)
        self.button_uygulama_gir.grid(column=1,row=2,pady=5)
    def Verify(self):
        try:
           
            self.uygulama_name=self.uygulama_entry_1.get()
            self.uygulama_password=self.uygulama_entry_2.get()
            sha256_name = hashlib.sha256()
            sha256_name.update(self.uygulama_name.encode('utf-8'))
            self.hashed_name = sha256_name.hexdigest() 

            sha256_password=hashlib.sha256()
            sha256_password.update(self.uygulama_password.encode('utf-8'))
            self.hashed_password = sha256_password.hexdigest() 

            if self.sha_name==self.hashed_name and self.sha_password==self.hashed_password:
                self.giris=True
                for frame in  self.second_frame.winfo_children():
                    frame.destroy()   
                self.create_SIGORTA_page_container()
        except:
            pass
    def search_employee_func(self):
        if self.giris:
            self.search_label=tb.Label(self.second_frame,bootstyle="dark",font="Arial 20",text="ELEMAN ARAMA",anchor="center")
            self.search_label.pack(pady=10)
            self.search_employee_frame=tb.Frame(self.second_frame)
            self.search_employee_frame.pack(padx=10,pady=10)
            self.child_search_active_frame_1=tb.Frame(self.search_employee_frame,bootstyle="dark")
            self.child_search_active_frame_1.pack(fill=X)
            
            self.my_Scroll_2=tb.Scrollbar(self.child_search_active_frame_1,orient="vertical")
            self.my_Scroll_2.pack(side="right",fill=Y) 
            self.tvw_search=tb.Treeview(self.child_search_active_frame_1,show="headings",height=20,bootstyle="dark",yscrollcommand=self.my_Scroll_2.set)
            self.tvw_search.pack()
            
            self.my_Scroll_2.config(command=self.tvw_search.yview)
            # column
            self.tvw_search["column"]=("TC","NAME-SURNAME","GİRİŞ-TARİH","ISLEM-TARİH","KAYIT-SİLME","ISLEM")
            self.tvw_search.column("#0",width=150,minwidth=100) 
            self.tvw_search.column("#1",width=150,minwidth=100)
            self.tvw_search.column("#2",width=250,minwidth=100)
            self.tvw_search.column("#3",width=150,minwidth=100)
            self.tvw_search.column("#4",width=150,minwidth=100)
            self.tvw_search.column("#5",width=150,minwidth=100)



            self.tvw_search.heading("TC",text="TC",anchor="w")
            self.tvw_search.heading("NAME-SURNAME",text="NAME-SURNAME",anchor="w")
            self.tvw_search.heading("GİRİŞ-TARİH",text="GİRİŞ-TARİH",anchor="w")
            self.tvw_search.heading("ISLEM-TARİH",text="ISLEM-TARİH",anchor="w")
            self.tvw_search.heading("KAYIT-SİLME",text="KAYIT-SİLME",anchor="w")
            self.tvw_search.heading("ISLEM",text="ISLEM",anchor="w")


            self.tvw_search.tag_configure("bigfont",font="Arial 12")
            for item in self.tvw_search.get_children():
                self.tvw_search.item(item, tags=("bigfont",))
            
            

            self.search_box=tb.Frame(self.second_frame,)
            self.search_box.pack()
            self.search_label_1=tb.Label(self.search_box,bootstyle="secondary inverse    ",text="TC",padding=5,width=15,anchor="center")
            self.search_label_1.grid(column=1,row=0,padx=5,pady=5)

            self.search_label_2=tb.Label(self.search_box,bootstyle="secondary inverse",text="ARAMA SEÇENEKLERİ",padding=5,width=18,anchor="center")
            self.search_label_2.grid(column=0,row=1,padx=5,pady=5)

            self.search_label_2=tb.Label(self.search_box,bootstyle="secondary inverse",text="İSİM",padding=5,width=15,anchor="center")
            self.search_label_2.grid(column=2,row=0,padx=5,pady=5)

            self.search_entry_1=tb.Entry(self.search_box,bootstyle="secondary",width=15,font="Arial 18")
            self.search_entry_1.grid(column=1,row=1,padx=5,pady=5)
            
            self.search_entry_2=tb.Entry(self.search_box,bootstyle="secondary",width=15,font="Arial 18")
            self.search_entry_2.grid(column=2,row=1,padx=5,pady=5)

            self.search_button=tb.Button(self.search_box,bootstyle="dark",padding=10,width=18,text="LİSTELE",command=self.search_employee)
            self.search_button.grid(column=3,row=1,padx=5,pady=5)
        else:
            self.Uygulama_giris()
    def search_employee(self):
        tc=self.search_entry_1.get()
        name=self.search_entry_2.get()
        for item in self.tvw_search.get_children():
            self.tvw_search.delete(item)
        for employee in self.get_Employees():
            if tc !="" and name!="" and (tc ==str(employee[1])[0:len(tc)]) and (name == employee[2][0:len(name)].lower()):
                self.tvw_search.insert("",END,values=(str(employee[1]),employee[2],f"{employee[3].split('-')[2]}.{employee[3].split('-')[1]}.{employee[3].split('-')[0]}",f"{employee[4].split('-')[2]}.{employee[4].split('-')[1]}.{employee[4].split('-')[0]}",employee[5],employee[6]))
            elif tc!="" and name=="" and (tc == str(employee[1])[0:len(tc)]):
                self.tvw_search.insert("",END,values=(str(employee[1]),employee[2],f"{employee[3].split('-')[2]}.{employee[3].split('-')[1]}.{employee[3].split('-')[0]}",f"{employee[4].split('-')[2]}.{employee[4].split('-')[1]}.{employee[4].split('-')[0]}",employee[5],employee[6]))
            elif tc=="" and name!="" and (unidecode(name)==unidecode(employee[2][0:len(name)].lower())):
                self.tvw_search.insert("",END,values=(str(employee[1]),employee[2],f"{employee[3].split('-')[2]}.{employee[3].split('-')[1]}.{employee[3].split('-')[0]}",f"{employee[4].split('-')[2]}.{employee[4].split('-')[1]}.{employee[4].split('-')[0]}",employee[5],employee[6]))
        self.tvw_search.tag_configure("bigfont",font="Arial 12")
        for item in self.tvw_search.get_children():
            self.tvw_search.item(item, tags=("bigfont",))

window=my_App()
selenium=main.Sigorta()



window.mainloop()




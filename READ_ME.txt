#Describing
It is an application about Turkey's employment insurance history and manager

#feature
1-you can take Insurance history with selenium but just complete authentication and algorithm will download files
2-you can filter record with "TC"(tc is like social number) or employee name
3-you can set employees work region,add remove employee and define regions

important points

# selenium connection of insurance website
if you dont want to write username,you can add parametre like this
("11111111111","1","11111","1111111111") in ENTER_LEAVE_CONTROL function from main.py

#give selenium Insurance history date in "date.txt" file
you should give beginning date for "create SIGORTA page_container()" function


# file direction
1-you should download selenium.chrome browser into "seleniumFile"
2-you should change Downloads path in "get_Excels()" function for 2 times.

# Database
1-Project use Mysql database and i prefer to select localhost  and its password
for authentication. When you open project, you should write default name which
i selected "muhasebe" and this is not important for connection but password is providing
connection of mysql.Moreover i had to check password for every page open button,so i used sha256 encryption,you
should change encripted sql password in "verify()" function from application.py
2-you should change mysql connect parameters in application 

#change img file
you should change img path and name in "create_pager()" function from application.py
self.encounter_image_1=tb.PhotoImage(file="1.png")

#Employee_region define 
you should define regions variable "bolgeler" in "bolge_goruntule()" function from application.py 
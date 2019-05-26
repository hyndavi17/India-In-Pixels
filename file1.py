import requests
from bs4 import BeautifulSoup
download_dir = "file1.csv" #where you want the file to be downloaded to 

csv = open(download_dir, "w") 
#"w" indicates that you're writing strings to the file

columnTitleRow = "name, score\n"
csv.write(columnTitleRow)
for i in range(65,91):
	t=chr(i)
	page = requests.get("http://www.howstat.com/cricket/Statistics/Players/PlayerList.asp?Country=ALL&Group="+t)
	#THIS URL GOES FROM A-Z TO GET THE PLAYERS NAMES AND THEIR ODI SCORES
	soup = BeautifulSoup(page.text, 'html.parser')
	j=soup.find_all('td',attrs={'width':'200'})
	list1=[]
	for i in j:
		k=i.find('a',attrs={'class':'LinkNormal'})
		links='http://www.howstat.com/cricket/Statistics/Players/'+k.get('href')
		#THIS URL GIVES THE PLAYERS ENTIRE SCORE LISTS WHICH INCLUDE ALL LEVELS
		list1.append(links)
		#print(links)
	#print(list1)
	for i in list1:
		page1= requests.get(i)
		soup1=BeautifulSoup(page1.text,'html.parser')
		s=soup1.find_all('td',attrs={'class':'ODIHeading'})
		#HERE WE GET TO KNOW IF ACTUALLY THE PLAYER PLAYED ODI's OR NOT 
		for i in s:
			s1=i.find('a',attrs={'class':'LinkOff'})
			links1='http://www.howstat.com/cricket/Statistics/Players/'+s1.get('href')
			#IF THE PLAYER HAVE ODI MATCHES IN HIS RECORDS THEN WE ARE FINDING THE CUMMULATIVE SCORES
			#print(links1)
			page2=requests.get(links1)
			soup2=BeautifulSoup(page2.text,'html.parser')
			h=soup2.find('td',attrs={'class':'TextGreenBold12'})
			#print(h)
			#HERE COMES OUR PLAYERS NAMES WHICH BECOME THE KEY's TO THE dict WE ARE ABOUT TO FORM 
			h1=h.contents[0]
			h2=h1.strip()

			#print(h.contents[0])
			y=soup2.find('table',attrs={'border':'0','width':'270','cellpadding':'1'})
			u=y.find_all('tr',limit=4)[3]
			r=u.find('td',attrs={'class':'FieldValue'})
			r1=r.contents[0]
			r2=r1.strip()
			#HERE WE GET THE ODI CUMMULATIVE SCORES
			dict1 = {h2:r2};
			print(dict1)
			#FINALLY WE GET  PLAYERS NAMES:SCORES AS KEY :VALUE PAIRS 
			for key in dict1.keys():
				name = key
				score = dict1[key]
				row = name + "," + score + "\n"
				csv.write(row)
import praw, urllib, time, re, pickle
from urllib import urlopen

# Authenticate praw, the Reddit API
user_agent = ('itsmybot')
r = praw.Reddit(user_agent=user_agent, log_requests=1)
r.login()

#So I don't repost links
posted_links = []

while True:
	f = urllib.urlopen('http://seattletimes.com/html/localnews/')
	words = f.read().decode('utf-8')
	all_links = re.findall("/html/localnews/(.+)\.html", words) #Scrapes to find articles labeled local news
	for j in all_links:
		a = j
		full_link = 'http://seattletimes.com/html/localnews/%s.html'%(a) 
		g = urllib.urlopen(full_link)
		wordit = g.read().decode('utf-8')
		findtitle = re.findall("<title>(.+)\| Local News", wordit) #searches html of article to find title
		if full_link not in posted_links:
			if len(findtitle) == 1:
				cached_link = 'http://webcache.googleusercontent.com/search?q=cache:%s'%(full_link) #gets google cache version
				r.submit('FreeSeattleTimes', findtitle[0], url=cached_link) #posts link w/title
				posted_links.append(full_link)

#saves info in a file in case I want to stop running idle, but want to know what links have been posted
	outFile = open('times_articles.txt', 'wb')
	pickle.dump(posted_links, outFile)
	outFile.close()				
	time.sleep(600)		

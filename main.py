import requests, re, json
from pocket import Pocket, PocketException
from bs4 import BeautifulSoup
from newspaper import Article

with open('configs.json') as configsFile: #read the configuration file
	configs = json.load(configsFile)
p = Pocket(consumer_key=configs["consumer_key"], access_token=configs["access_token"]) #get the pocket interface object

def getArticleTime(text):
	req = requests.post("http://niram.org/read/", {"words":text})
	parsed_html = BeautifulSoup(req.text, "html.parser")
	time = parsed_html.body.find('div', attrs={'class':'alert alert-info'})
	p = re.compile("(\d+) minute")
	search = p.findall(time.text) if time else None
	return int(search[0]) if search else -1

def roundTime(minutes): #rounds 0 to 0, 1 to 5, 5 to 5, 6 to 10, 10 to 10, etc
	return minutes + 5 - (minutes % 5) if minutes % 10 != 0 else minutes

def getArticle(a):
	article = Article(a["given_url"])
	try:
		article.download()
		article.parse()
	except:
		print("Unable to download article: %s\nPrevious changes will be committed" % a["resolved_title"])
		p.commit()
	return article

try:
	articles = p.retrieve(offset=configs["offset_articles_start"], count=configs["count_articles_to_tag"])
	# [print("%s(%s)" % (a["given_url"], a["resolved_title"])) for id, a in articles["list"].items()]
	print("Found %d articles, starting: \n" % len(articles["list"].items()))
	articlePos = 0 #display count
	for id, data in articles["list"].items():
		articlePos+=1 #increment article count
		article = getArticle(data)
		minutes = getArticleTime(article.text)
		title = data["resolved_title"] if "resolved_title" in data else "No Title Available"
		print("\nArticle %d: %s\n%s minutes\n%s rounded minutes" % (articlePos, title, minutes, roundTime(minutes)))
		if configs["delete_other_tags"]: #delete other tags is set to true
			p.tags_clear(id)
		if configs["add_tags"]: #add tags is set to true
			p.tags_add(id, "%s min" % (roundTime(minutes)), 0)
		if not configs["commit_tags_only_at_the_end"]:
			p.commit() #commit on every instance
	if configs["commit_tags_only_at_the_end"]:
		p.commit() #commit at the end
except PocketException as e:
	print(e.message + "\nCheck your consumer_key('%s') access_token('%s')" % (configs["consumer_key"],configs["access_token"]))
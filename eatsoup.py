import BeautifulSoup, urllib, urllib2, base64, re, datetime

def getsoups():
	url = 'http://www.eat.co.uk/pages/soup.shtml'
	req = urllib2.Request( url, None, headers = {'User-agent':'Mozilla/5.0'} )
	page = urllib2.urlopen( req ).read()
	soup = BeautifulSoup.BeautifulSoup( page )

	popuplink = soup.findAll('a', href=re.compile("^javascript:"))[0].__str__()

	newurl = re.findall(r"smenu\(\'([^\']+)", popuplink)[0]
	newurl = newurl.replace('&amp;', '&')

	if len(newurl) > 0:
		req = urllib2.Request( newurl, None, headers = {'User-agent':'Mozilla/5.0'} )
		page = urllib2.urlopen( req ).read()
		soup = BeautifulSoup.BeautifulSoup( page )
	
		table = soup.findAll('table')[1]
	
		soups = table.findAll('font', color="#6B4A43")
		
		formatsoups = []
		
		for soup in soups:
			formatsoups.append(soup.findAll('strong')[0].renderContents())
			
		return formatsoups
			
def today():
	today = datetime.datetime.today()
	return today.weekday()

def sendtotwitter(simple, bold):
	status = "Simple: " + simple + ", Bold: " + bold
	values = { "status" : status }
	data = urllib.urlencode(values)
	req = urllib2.Request('http://twitter.com/statuses/update.xml', data)
	base64string = base64.encodestring('%s:%s' % ('eatsoups', 'm0v1ngserver!'))[:-1]
	req.add_header("Authorization", "Basic %s" % base64string)
	response = urllib2.urlopen(req)
	the_page = response.read()
	return

we = today()
if we <= 4:
	soups = getsoups()
	
	soupsimple = soups[we*2]
	soupbold = soups[we*2+1]
	
	sendtotwitter(soupsimple, soupbold)
	
	print 'Done'
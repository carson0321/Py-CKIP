#-*-coding:utf-8-*-
import urllib, urllib2, cookielib, re

def parseTree(string):
	if not isinstance(string, unicode):
		try:
			string = string.decode('utf-8')
		except:
			raise UnicodeError('Input encoding should be UTF8 of UNICODE')
	string = string.encode('cp950')

	URL = 'http://parser.iis.sinica.edu.tw/'

	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	opener.addheaders = [
	('User-Agent', 'Mozilla/5.0 Gecko/20100101 Firefox/29.0'),
	('referer', 'http://parser.iis.sinica.edu.tw/'),
	('Host', 'parser.iis.sinica.edu.tw')
	]

	raw = urllib.urlopen(URL).read()
	fid = re.search('name="id" value="(\d+)"', raw).group(1)

	postdata = dict()
	postdata['myTag'] = string
	postdata['id'] = fid

	postdata = urllib.urlencode(postdata)

	resURL = 'http://parser.iis.sinica.edu.tw/svr/webparser.asp'

	res = opener.open(resURL, postdata).read()
	res = res.decode('cp950')
	res = re.findall('<nobr>#\d+:(.*?)</nobr>', res)

	return res
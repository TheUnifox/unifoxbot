import requests
from bs4 import BeautifulSoup

#Base: https://www.google.com/search?q=
#then search term, with spaces as +
#then for images: &source=lnms&tbm=isch

class GoogleSearch:
	url = 'https://www.google.com/search?q='
	
	def key_words_search_words(self, user_message):
		words = user_message.split()
		keywords = '+'.join(words)
		search_words = ' '.join(words)
		return keywords, search_words

	def search(self, url=url, keywords=None):
		response = requests.get(url+keywords)
		content = response.content
		contentfile = open('content.txt', 'w')
		contentfile.write(str(content))
		soup = BeautifulSoup(content, 'html.parser')
		result_links = soup.findAll('a')
		return result_links

	def imagesearch(self, url=url, additional=False, keywords=None):
		endadd = '&source=lnms&tbm=isch'
		
		if not additional:
			print('getting html')
			response = requests.get(url+keywords)
			print('got html')
		elif additional:
			print('getting html')
			response = requests.get(url+keywords+endadd)
			print('got html')
		content = response.content
		contentfile = open('content.html', 'wb')
		contentfile.write(content)
		soup = BeautifulSoup(content, 'html.parser')
		links = soup.findAll('img')
		images = list()
		for link in links:
			image = link['src']
			images.append(image)
		checkindex = 0
		for check in images:
			if check.startswith('/'):
				images.pop(checkindex)
				checkindex -= 1
			checkindex += 1
		return images
      
	def send_link(self, result_links, search_words): 
		send_link = set()
		for link in result_links:
			text = link.text.lower()
			if 'google.com' in text:
				continue
			elif search_words in text:  
				send_link.add(link.get('href'))
		return send_link
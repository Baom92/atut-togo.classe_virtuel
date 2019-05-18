from googlesearch import search
from googlesearch import search_images
from googlesearch import search_videos


class Gsearch_python:
    def __init__(self, name_search, result_number):
        self.name = name_search
        self.result_number = result_number

    def classicSearch(self):
        list_urls = []
        for i in search(query=self.name, tld='fr', lang='fr', num=10, stop=self.result_number, pause=2):
            list_urls.append(i)
        return list_urls

    def imageSearch(self):
        list_urls = []
        for i in search_images(query=self.name, tld='fr', lang='fr', num=10, stop=self.result_number, pause=2):
            list_urls.append(i)
        return list_urls

    def videoSearch(self):
        list_urls = []
        for i in search_videos(query=self.name, tld='fr', lang='fr', num=10, stop=self.result_number, pause=2):
            list_urls.append(i)
        return list_urls
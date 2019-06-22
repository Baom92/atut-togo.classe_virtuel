from bs4 import BeautifulSoup
import requests
import json


class ScrappingTwitter:
    def __init__(self, web_url):
        """
        The scrapping class constructor. We initialize the parameters to be used in the subsequent methods.
        :param web_url: The starup twitter link
        """
        self.url = web_url
        self.document_soup = BeautifulSoup(requests.get(web_url).text, 'html.parser')
        self.nom_balise = 'a'
        self.nom_tag = 'ProfileHeaderCard-nameLink u-textInheritColor js-nav'

    def getStartUpName(self):
        """
        We scrappe the starup name on its twiter page
        :return: the starup name
        """
        startup_name_document = self.document_soup.find(self.nom_balise, class_=self.nom_tag)
        return startup_name_document.string

    def parsePostSoup(self, post_document):
        try:
            author = post_document.find('strong', class_='fullname').string.strip()
        except:
            author = ''

        try:
            post_creation_date = post_document.find('a', class_='tweet-timestamp js-permalink js-nav js-tooltip').get(
                'title').strip()
        except:
            post_creation_date = ''

        try:
            nbr_like = post_document.find('div',
                                          class_='ProfileTweet-action ProfileTweet-action--favorite js-toggleState').find(
                'span', class_="ProfileTweet-actionCountForPresentation").text.strip()
            if not nbr_like:
                nbr_like = '0'
        except:
            nbr_like = '0'

        try:
            nbr_share = post_document.find('div',
                                           class_='ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt').find(
                'span', class_="ProfileTweet-actionCountForPresentation").text.strip()
            if not nbr_share:
                nbr_share = '0'
        except:
            nbr_share = '0'

        try:
            nbr_comment = post_document.find('div', class_='ProfileTweet-action ProfileTweet-action--reply').find(
                'span', class_="ProfileTweet-actionCountForPresentation").text.strip()
            if not nbr_comment:
                nbr_comment = '0'
        except:
            nbr_comment = '0'

        try:
            tags = [tag.text.strip() for tag in
                    post_document.find_all('a', class_='twitter-hashtag pretty-link js-nav')]
        except:
            tags = []

        return {
            "author": author,
            "post_creation_date": post_creation_date,
            "nbr_like": int(nbr_like),
            "nbr_dislike": 0,
            "nbr_share": int(nbr_share),
            "nbr_comment": int(nbr_comment),
            "tags": tags
        }

    def get_start_post_list(self):
        startup_post = self.document_soup.find('ol', id='stream-items-id')
        li_list = startup_post.find_all('li', class_='js-stream-item')
        startup_name = self.getStartUpName()
        social_network = "TWITTER"
        url_on_social_network = self.url

        post_list = []
        for li in li_list:
            result = self.parsePostSoup(li)
            result['startup_name'] = startup_name
            result['social_network'] = social_network
            result['url_on_social_network'] = url_on_social_network
            post_list.append(result)

        return post_list


if __name__ == '__main__':
    url = 'https://twitter.com/ageofempires?lang=fr'

    scrapping = ScrappingTwitter(url)
    results = scrapping.get_start_post_list()
    print(results)
import requests

from bs4 import BeautifulSoup


class NaverComicsCrawler:
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.title_id = ""
        self.latest_epi_no = 1

        self.getComicInfo()

    def getComicInfo(self):
        comic_parsed = requests.get(self.url)
        comic_soup = BeautifulSoup(comic_parsed.text, "html.parser")

        self.title = comic_soup.title.string[:-10]

        latest_epi_url = comic_soup.find(class_="viewList")
        latest_epi_url = latest_epi_url.find_all("tr")[2].find('a')['href']
        url, query = latest_epi_url.split('?')
        for pair in query.split('&'):
            if "titleId" in pair:
                self.title_id = pair.split("=")[1]
            elif "no" in pair:
                self.latest_epi_no = pair.split("=")[1]

        print(f"ComicTitle = {self.title}, titleId = {self.title_id}, latestEpisode = {self.latest_epi_no}")

    def getImage(self, first_epi, last_epi):
        for i in range(first_epi, last_epi + 1):
            wt_viewer_parsed = requests.get(f"https://comic.naver.com/webtoon/detail.nhn?titleId={self.title_id}&no={i}")
            wt_viewer_soup = BeautifulSoup(wt_viewer_parsed.text, "html.parser")
            wt_viewer = wt_viewer_soup.find(class_="wt_viewer")
            wt_imgs = wt_viewer.find_all("img")

            idx = 1
            for wt_img in wt_imgs:
                img_url = wt_img['src']
                img = requests.get(img_url, headers={'referer': self.url})
                with open(f'{idx}.jpg', 'wb') as f:
                    f.write(img.content)
                    f.close()
                idx += 1
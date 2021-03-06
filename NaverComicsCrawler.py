import os
import re
import shutil
import zipfile

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
        latest_epi_url = latest_epi_url.find(class_="title").find('a')['href']
        url, query = latest_epi_url.split('?')
        for pair in query.split('&'):
            if "titleId" in pair:
                self.title_id = pair.split("=")[1]
            elif "no" in pair:
                self.latest_epi_no = int(pair.split("=")[1])

        print(f"\n웹툰 제목 = {self.title}, 웹툰 ID = {self.title_id}, 최근화 = {self.latest_epi_no}화\n")

    def getImage(self):
        for i in range(1, self.latest_epi_no + 1):
            print(f"{i}화 / {self.latest_epi_no}화 다운로드 중...")

            folder_name = re.sub('[\/:*?"<>|]', '', self.title) + f"/{i}화"
            os.makedirs(folder_name, exist_ok=True)

            wt_viewer_parsed = requests.get(f"https://comic.naver.com/webtoon/detail.nhn?titleId={self.title_id}&no={i}")
            wt_viewer_soup = BeautifulSoup(wt_viewer_parsed.text, "html.parser")
            wt_viewer = wt_viewer_soup.find(class_="wt_viewer")
            wt_imgs = wt_viewer.find_all("img")

            idx = 1
            for wt_img in wt_imgs:
                img_url = wt_img['src']
                img = requests.get(img_url, headers={'referer': self.url})
                with open(f'{folder_name}/{idx}.jpg', 'wb') as f:
                    f.write(img.content)
                    f.close()
                idx += 1

            self.zipImage(folder_name)

    def zipImage(self, folder_name):
        comic_zip = zipfile.ZipFile((folder_name + ".zip"), 'w')

        for folder, _, files in os.walk(folder_name):
            for file in files:
                if file.endswith('.jpg'):
                    comic_zip.write(os.path.join(folder, file), file, compress_type=zipfile.ZIP_DEFLATED)
        comic_zip.close()

        shutil.rmtree(folder_name)

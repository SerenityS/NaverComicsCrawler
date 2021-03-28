from NaverComicsCrawler import NaverComicsCrawler

if __name__ == '__main__':
    print("NaverComicsCrawler\n")
    url = input("웹툰 URL을 입력하세요 : ")
    crawler = NaverComicsCrawler(url)
    crawler.getImage()

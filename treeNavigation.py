from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

# 첫 번째 타이틀 행을 포함하여 테이블에 들어있는 모든 제품 목록을 출력
for child in bs.find('table', {'id': 'giftList'}).children:
    print(child)
    
# 첫 번째 타이틀 행을 제외한 모든 제품 행을 출력
for sibling in bs.find('table', {'id': 'giftList'}).tr.next_siblings:
    print(sibling)
    
# 부모 검색 함수
print(bs.find('img', {'src': '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())
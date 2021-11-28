import requests
from bs4 import BeautifulSoup
isbn="979-11-5839-179-9"


#이건 크롤링 소스였고,
#일요일날 할일 . 소스를 몽땅 다 갈아 엎어서... .바코드용으로 재탄생 시키긱.
def isbnOutput(isbn):
    url = 'https://www.nl.go.kr/NL/contents/search.do?' \
          'srchTarget=total&pageNum=1&pageSize=10&kwd={}'.format(isbn)
    print("url is \n",url)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
               '537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    response = requests.get(url,headers=headers)


    if response.status_code == 200:
        #html = response.text
        html=response.content
        soup = BeautifulSoup(html, 'html.parser')
        #soup_one는 맨 위의 이미지 1개만.
        title = soup.select_one('#sub_content > div.content_wrap > div > '
                                'div.integSearch_wrap > div.search_cont_wrap >'
                                ' div > div > div.search_right_section > div.sect'
                                'ion_cont_wrap > div:nth-child(1) > div.cont_list.lis'
                                't_type > div.row > span.txt_left.row_txt_tit > a')
        textTitle = title.get_text()

        author = soup.select_one('#sub_content > div.content_wrap > div > '
                                 'div.integSearch_wrap > div.search_cont_wrap > div > '
                                 'div > div.search_right_section > div.section_cont_wrap > '
                                 'div:nth-child(1) > div.cont_list.list_type > div.row > span:nth-child(6)')
        textAuthor = author.get_text()

        publisher = soup.select_one('#sub_content > div.content_wrap > div > '
                                    'div.integSearch_wrap > div.search_cont_wrap > div > '
                                    'div > div.search_right_section > div.section_cont_wrap '
                                    '> div:nth-child(1) > div.cont_list.list_type > div.row'
                                    '> span:nth-child(7)')
        textPublisher = publisher.get_text()



        image = soup.select_one('#popDetailView > div.layer_popup.detail_layer_popup > div.popup_contents > div.detail_top_wrap.grid_wrap > div.grid.grid_l.img_wrap > img')
        print("image",image)#성공시 이미지 출력.
        #일단 이미지는 나중에 생각해보자.


        print("book name is \n",textTitle)
    else :
        print(response.status_code)


    return textTitle,textPublisher,textAuthor,image
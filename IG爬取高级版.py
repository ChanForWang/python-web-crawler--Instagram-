import requests
import os

#request 网址，并返回json data
def getHTML(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
        'cookie': 'mid=YKc58AALAAFoSfrpLcjRB1RpuqGU; ig_did=893A37A8-D006-425A-9D37-5520552FB248; ig_nrcb=1; shbid=1381; shbts=1621572088.066615; rur=VLL; csrftoken=inPklO7gdfr1rMjwatEJcCqkQnIlGI6c; ds_user_id=338966265; sessionid=338966265%3ApR7o6KkeENg3lh%3A28'
    }

    html = requests.get(url,headers=headers)
    data = html.json()
    return data


#获取所有网址list，一个网址就包含12个url图片src
def getURLlist(url,id):
    #headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
           #    'cookie': 'mid=YKc58AALAAFoSfrpLcjRB1RpuqGU; ig_did=893A37A8-D006-425A-9D37-5520552FB248; ig_nrcb=1; shbid=1381; shbts=1621572088.066615; rur=VLL; csrftoken=inPklO7gdfr1rMjwatEJcCqkQnIlGI6c; ds_user_id=338966265; sessionid=338966265%3ApR7o6KkeENg3lh%3A28'}

    url_list = [url]
    while url != None or has_next_page_data_info['has_next_page'] == True:
        data = getHTML(url)

        #判断有没有下一个page
        has_next_page_data_info = data['data']['user']['edge_owner_to_timeline_media']['page_info']
        if has_next_page_data_info['has_next_page'] == True:
            #获取下一页所需要的新的after参数
            after_new = has_next_page_data_info['end_cursor'].rstrip('=')
            url = "https://www.instagram.com/graphql/query/?query_hash=02e14f6a7812a876f7d133c9555b1151&variables=%7B%22id%22%3A%22"+id+"%22%2C%22first%22%3A12%2C%22after%22%3A%22" + after_new + "%3D%3D%22%7D"
            url_list.append(url)
        else:
            break

    return url_list


#获取图片list
def getImageURL(data):
    img_data_info = data['data']['user']['edge_owner_to_timeline_media']['edges']
    #print(img_data_info)

    img_url_list = []
    for i in img_data_info:
        img_url = i['node']['display_url']
        img_url_list.append(img_url)
    #print(img_url_list)
    print("共"+str(len(img_url_list))+"张")
    return img_url_list


#访问图片url list内的url，然后下载图片
def scapyImage(img_url_list,id):
    for img_url in img_url_list:
        img_data = requests.get(img_url).content
        img_name = img_url.split('?')[0].split('/')[-1].split('_')[0] + ".jpg"
        file_name = "id=" + id
        if not os.path.exists(file_name):
            os.mkdir(file_name)
        with open(file_name+"\\" + img_name,"wb") as f:
            print('正在下载：' + img_name)
            f.write(img_data)






if __name__ == "__main__":
    id = input('请输入该个人IG的id参数是（在network的字符参数查看）：')
    after = input('请输入after参数：')

    print("正在准备中，请稍后。。。")
    #目标网址，第一个url
    first_url = 'https://www.instagram.com/graphql/query/?query_hash=02e14f6a7812a876f7d133c9555b1151&variables=%7B%22id%22%3A%22'+id+ '%22%2C%22first%22%3A12%2C%22after%22%3A%22'+after+'%3D%3D%22%7D'
    url_list = getURLlist(first_url,id)

    for url_li in url_list:
        print('==============正在下载第{}页数据：'.format(str(url_list.index(url_li)+1)))
        data = getHTML(url_li)
        img_url_list = getImageURL(data)
        scapyImage(img_url_list,id)

import requests
import json
import urllib.request
import simplejson
from pywinauto import Application
import os
from dotenv import load_dotenv
# import time

load_dotenv()
api_call = os.environ.get("API_URL")
API_KEY= os.environ.get("API_KEY")

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def splitURL(url):
    video_id=url.split('=')
    id_to_api=video_id[1]
    return id_to_api

def apiCall(id_to_api):
    final_url = api_call+id_to_api
    url_api = final_url
    return url_api

def dislikeCount(url_api):
    response_API=requests.get(url_api)
    data = response_API.text
    parse_json = json.loads(data)
    number_dislikes = parse_json['dislikes']
    return number_dislikes

def fetchURl():
    try:
        app = Application(backend='uia')
        app.connect(title_re=".*Chrome.*")
        element_name="Address and search bar"
        dlg = app.top_window()
        url = dlg.child_window(title=element_name, control_type="Edit").get_value()
        return url
    except:
        pass

def getTitle(VIDEO_ID):
    url_for_api = "https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id=%s&key=%s"%(VIDEO_ID,API_KEY)
    headers = {
	"Accept" : 'application/json'
	}
    request = requests.get(url_for_api,headers=headers)
    j = json.loads(request.text)
    title = j['items'][0]['snippet']['title']
    channel_title = j['items'][0]['snippet']['channelTitle']
    return title,channel_title

if __name__=='__main__':
    while(True):
        list_id =[]
        check_list = []
        youtube_video_url_chrome = str(fetchURl())
        if(youtube_video_url_chrome != ""):
            if 'youtube.com/' in youtube_video_url_chrome:
                id_to_api = splitURL(youtube_video_url_chrome)
                check_list.append(id_to_api)
                # print(check_list)
                if(set(check_list)==set(list_id)):
                    pass
                else:
                    list_id.append(id_to_api)
                    # print(list_id)
                    url_api = apiCall(id_to_api)
                    number_of_dislike = dislikeCount(url_api)
                    title,channel_title = getTitle(id_to_api)
                    if(number_of_dislike==None):
                        pass
                    else:
                        print(title,'\n\tby : ',channel_title,'\n\thas : ', number_of_dislike,'dislikes')
            else:
                pass
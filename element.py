from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import time
import pytube
from tqdm import tqdm

cluster = MongoClient( 'mongodb+srv://RonYaacov:ron22522@cluster0.uhbd5.mongodb.net/<dbname>?retryWrites=true&w=majority' )
db = cluster["youtube_app"]
collection = db["user info"]


class YouTube:
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    URL = 'https://youtube.com'


class FindSkipAd( YouTube ):

    def __init__(self):

        self.driver = webdriver.Chrome( YouTube.PATH )
        self.driver.get( YouTube.URL )

        while True:
            try:

                duration = self.driver.find_element_by_class_name( "ytp-time-duration" ).text
                if duration == '00:20':
                    self.driver.refresh()
                    continue
            except:
                pass

            try:
                skip = self.driver.find_element_by_class_name( 'ytp-ad-skip-button-container' )
                skip.click()
                continue

            except:
                time.sleep( 1 )


class inspect( YouTube ):

    def find_details(self):

        self.user_input = input( 'what video would you like to get details on ? ' )
        print( 'loading...' )
        self.hide_driver = webdriver.ChromeOptions()
        self.hide_driver.add_argument( '--headless' )
        self.hide_driver.add_argument( '--mute-audio' )
        driver = webdriver.Chrome( YouTube.PATH, options=self.hide_driver )
        driver.get( YouTube.URL )
        driver.implicitly_wait( 10 )
        print( "looking in YouTube" )

        try:

            driver.implicitly_wait( 10 )
            time.sleep( 1 )
            search_bar = driver.find_element_by_name( 'search_query' )
            search_bar.clear()
            search_bar.send_keys( self.user_input )
            search_bar.send_keys( Keys.RETURN )
            self.user_input.split()
            driver.implicitly_wait( 10 )
            time.sleep( 3 )

            results = driver.find_elements_by_id( "video-title" )
            results_list = list( result.text for result in results )
            ad_selection = list(
                result for word in self.user_input for result in results_list for i in result if
                word.lower() == i.lower() )
            first_video = ad_selection[0]
            ad_selection = set( ad_selection )
            ad_selection = list( ad_selection )
            ad_selection_remove = list( item for item in ad_selection if item == first_video )
            if len( ad_selection_remove ) > 0:
                ad_selection.remove( ad_selection_remove[0] )
            ad_selection.insert( 0, first_video )
            titles = list( enumerate( ad_selection[0:5], start=1 ) )
            print( "those are your options" )
            time.sleep( 1.5 )
            for number, title in titles:
                print( number, ".", title )
            choice = int( input( "witch of those videos would you like to inspect ---> " ) )
            for title in titles:
                if choice == title[0]:
                    video = title[1]
            for result in results:
                if result.text == video:
                    item = result
                    item.click()
                    time.sleep( 2 )
                    break
        except:
            print( "ERROR: choose one of the options! " )

        try:
            driver.implicitly_wait( 30 )
            views = driver.find_element_by_id( 'info-text' ).text
            views = views.split()[0]
            likes = driver.find_elements_by_xpath(
                '//yt-formatted-string[@class="style-scope ytd-toggle-button-renderer style-text"]' )
            youtuber = driver.find_elements_by_xpath(
                '//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]' )
            youtuber = list(
                channel.text for channel in youtuber if isinstance( channel.text, str ) and len( channel.text ) > 0 )
            sub = driver.find_elements_by_id( "owner-sub-count" )
            sub = ((sub[0].text).split()[0])
            print( f'the channel name is -----------> {youtuber[0]}' )
            print( f'the number of subscribers is -> {sub}' )
            print( f'the number of views is --------> {views}' )
            print( f'the number of likes is --------> {likes[1].text}' )
            print( f'the number of dislikes is -----> {likes[2].text}' )


        except:
            print( "ERROR: you probably chose an add please try again " )


class QuickDownload( YouTube ):

    def __init__(self):
        user_input = input( 'what video would you like to download ? ' )
        print( 'loading...' )
        hide_driver = webdriver.ChromeOptions()
        hide_driver.add_argument( '--headless' )
        hide_driver.add_argument( '--mute-audio' )
        driver = webdriver.Chrome( YouTube.PATH, options=hide_driver )
        driver.get( YouTube.URL )
        driver.implicitly_wait( 10 )
        print( "looking in YouTube" )

        try:
            driver.implicitly_wait( 10 )
            time.sleep( 1 )
            search_bar = driver.find_element_by_name( 'search_query' )
            search_bar.clear()
            search_bar.send_keys( user_input )
            search_bar.send_keys( Keys.RETURN )
            user_input.split()
            print( "found your video" )
            driver.implicitly_wait( 10 )
            time.sleep( 1 )

            while True:
                try:
                    results = driver.find_elements_by_id( "video-title" )
                    results_list = list( result.text for result in results )
                    ad_selection = list( result for word in user_input for result in results_list for i in result if
                                         word.lower() == i.lower() )
                    first_video = ad_selection[0]
                    for title in results_list:
                        if title == first_video:
                            for result in results:
                                if title == result.text:
                                    result.click()

                    driver.implicitly_wait( 10 )
                    time.sleep( 3 )
                    print( driver.title )
                    video_url = driver.current_url

                    time.sleep( 1 )
                    driver.quit()
                    print( "downloading..." )
                    break
                except:
                    continue


        except:
            pass

        try:
            yt = pytube.YouTube( video_url )
            yt.streams.filter( only_audio=True ).first().download( './youtube bot vids/songs' )
            print( "download done!" )


        except:
            print( "Error: download not possible" )


class download( YouTube ):
    def __init__(self):
        user_input = input( 'what video would you like to download ? ' )
        print( "witch format would you like to download the video ? " )
        print( "1. mp3" )
        print( "2. mp4" )
        try:
            user_format = int( input( "your answer ---> " ) )
            if user_format > 2:
                raise SystemExit


        except:
            print( "enter only digit !" )
            raise SystemExit

        print( 'loading...' )
        hide_driver = webdriver.ChromeOptions()
        hide_driver.add_argument( '--headless' )
        hide_driver.add_argument( '--mute-audio' )
        driver = webdriver.Chrome( YouTube.PATH, options=hide_driver )
        driver.get( YouTube.URL )
        driver.implicitly_wait( 10 )
        print( "looking in YouTube" )

        try:
            driver.implicitly_wait( 10 )
            time.sleep( 1 )
            search_bar = driver.find_element_by_name( 'search_query' )
            search_bar.clear()
            search_bar.send_keys( user_input )
            search_bar.send_keys( Keys.RETURN )
            user_input.split()
            driver.implicitly_wait( 10 )
            time.sleep( 1 )

            results = driver.find_elements_by_id( "video-title" )
            results_list = list( result.text for result in results )
            ad_selection = list(
                result for word in user_input for result in results_list for i in result if word.lower() == i.lower() )
            first_video = ad_selection[0]
            ad_selection = set( ad_selection )
            ad_selection = list( ad_selection )
            ad_selection_remove = list( item for item in ad_selection if item == first_video )
            if len( ad_selection_remove ) > 0:
                ad_selection.remove( ad_selection_remove[0] )
            ad_selection.insert( 0, first_video )
            titles = list( enumerate( ad_selection[0:5], start=1 ) )
            print( "those are your options" )
            time.sleep( 1.5 )
            for number, title in titles:
                print( number, ".", title )
            choice = int( input( "witch of those videos would you like to download ---> " ) )
            for title in titles:
                if choice == title[0]:
                    video = title[1]

            for result in results:
                if result.text == video:
                    item = result
                    item.click()
                    time.sleep( 2 )
                    video_url = driver.current_url
                    break

        except:
            print( "ERROR: choose one of the options! " )

        time.sleep( 1 )
        driver.quit()
        print( "downloading..." )
        index = 0

        while True:

            if user_format == 1:
                try:
                    yt = pytube.YouTube(video_url)
                    yt.streams.filter( only_audio=True ).first().download( './youtube bot vids/songs' )
                    print( "download done!" )
                    break


                except:
                    if index > 10:
                        print( "Error: download not possible " )
                        break
                    index += 1


            elif user_format == 2:
                try:
                    yt = pytube.YouTube( video_url )
                    try:
                        yt.streams.filter( progressive=True, res='720p' ).first().download( './youtube bot vids' )
                    except:
                        yt.streams.filter( progressive=True ).first().download( './youtube bot vids' )

                    print( "download done!" )
                    break



                except:
                    if index > 10:
                        print( "Error: download not possible" )
                        break
                    index += 1


class download_playlist( YouTube ):
    def __init__(self):
        user_input = input( 'what playlist would you like to download ? --> ' )
        try:
            user_choice = int( input( "how many videos do you wish to download from the playlist ? --> " ) )
        except:
            print( "invalid answer" )
            raise SystemExit
        print( 'loading...' )
        hide_driver = webdriver.ChromeOptions()
        hide_driver.add_argument( '--headless' )
        hide_driver.add_argument( '--mute-audio' )
        driver = webdriver.Chrome( YouTube.PATH, options=hide_driver )
        driver.get( YouTube.URL )
        driver.implicitly_wait( 10 )
        print( "looking in YouTube" )

        try:
            driver.implicitly_wait( 10 )
            time.sleep( 1 )
            search_bar = driver.find_element_by_name( 'search_query' )
            search_bar.clear()
            search_bar.send_keys( user_input )
            search_bar.send_keys( Keys.RETURN )
            print( "found your playlist" )
            driver.implicitly_wait( 10 )
            time.sleep( 1 )

            try:
                playlist = driver.find_elements_by_class_name( "style-scope ytd-radio-renderer" )
                playlist[0].click()

                try:
                    driver.implicitly_wait( 10 )
                    time.sleep( 1 )
                    playlist = driver.find_elements_by_xpath(
                        '//a[@class="yt-simple-endpoint style-scope ytd-child-video-renderer"]' )
                    playlist[0].click()


                except:
                    pass

            except:
                print( "no playlist found" )
                raise SystemExit

            try:
                try:
                    while True:
                        driver.implicitly_wait( 10 )
                        time.sleep( 2 )
                        all_playlist_videos = driver.find_elements_by_xpath( '//ytd-playlist-panel-video-renderer' )
                        if len( all_playlist_videos ) < user_choice:
                            user_choice = len( all_playlist_videos ) + 1
                        wish_playlist = all_playlist_videos[0:user_choice]
                        break
                except:
                    print( "im very helpful" )
                    pass

                while True:
                    url_list = []
                    try:
                        for video in wish_playlist:
                            video.click()
                            driver.implicitly_wait( 10 )
                            time.sleep( 1 )
                            url = driver.current_url
                            url_list.append( url )
                        break
                    except:
                        continue

                for url in tqdm( url_list ):
                    while True:
                        try:
                            yt = pytube.YouTube( url )
                            yt.streams.filter( only_audio=True ).first().download(
                                f'./youtube bot vids/playlist/{user_input}' )
                            break
                        except:
                            continue
                print( "all downloads are done " )
                print( "enjoy!" )




            except:
                print( "failed... try again" )
                raise SystemExit

        except:
            raise SystemExit


class Users:
    def create_new_user(self):
        self.user_name = input( "enter user name" )
        self.password = input( "enter password" )
        self.user_name_exist = collection.find( {} )
        for i in self.user_name_exist:
            if i["user name"] == self.user_name:
                print( "this user already exist!" )
                raise SystemExit

        id = collection.find( {} )
        ids = []
        for i in id:
            ids.append( i["_id"] )
        new_id = max( ids ) + 1
        new_user = {"_id": new_id, "user name": self.user_name, "password": self.password, "accesses": "user"}
        collection.insert_one( new_user )

    def connect(self, user_name, password):
        self.user_name = user_name
        self.password = password
        self.connect = collection.find( {"user name": self.user_name} )
        for i in self.connect:
            if i["password"] == self.password:
                print( f"welcome {self.user_name} " )
                return True
            else:
                print( "wrong password " )
                return False

        if len( list( self.connect ) ) == 0:
            print( "no user found" )
            return False

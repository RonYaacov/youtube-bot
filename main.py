import time
import element


if __name__ == '__main__':

    print( f'''hello welcome to your YouTube bot 
what would you like to do ???
1. view
2. download
3. inspect
4. quick download
5. playlist download
9. create new account''')
    try:
        answer = int(input("your answer --> "))

    except:
        print( "ERROR --- invalid answer don't be a smart ass" )
        time.sleep( 3 )
        raise SystemExit

    if answer == 1:
        watch = element.FindSkipAd()

    elif answer == 2:
        download = element.download()

    elif answer == 3:
        inspect = element.inspect.find_details(element.inspect)

    elif answer == 4:
        quick_download = element.QuickDownload()

    elif answer == 5 :
        playlist_download = element.download_playlist()

    elif answer == 8 :
        connect = element.Users.connect(element.Users)


    elif answer == 9 :
        element.Users.create_new_user(element.Users)
    else:
        print("invalid answer !")
        raise SystemExit
else:
    print("do you want to sing up? ")
    print("""
1. yse
2. no""")
    while True:
        try:
            answer1 = int(input("your answer ---> "))
            if answer1 == 1:
                element.Users.create_new_user(element.Users)
                break
            else:
                break
        except:
            print("invalid answer try again")
            continue


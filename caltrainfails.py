import urllib2
import tweepy
import serial
import time, datetime
import json
import csv


#this should be updated with your creds

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY= ''
ACCESS_TOKEN_SECRET= ''



def get_users_tweets(username, count, sid):
    """
    get X number of tweets from an arbitary twitter user,
    since the specified ID of the tweet - this lets you make updates per the below
    """

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)


    r = api.user_timeline(screen_name = username, count = count,include_rts = 0, since_id = sid)
    with open("caltrainoutput.csv", 'wb') as fp:
        writer = csv.writer(fp)

        lastsid = 0
        
        for tweet in r:
            handle = tweet.user.screen_name
            time = tweet.created_at.strftime('%Y%m%d%H%M%S')
            text = tweet.text.encode('utf-8')
            sid = tweet.id
            if lastsid < sid:
                lastsid = sid
                
            writer.writerow([handle, time, text, sid])
            #print(handle, time, text, sid)
        writer.writerow(["lastsid", lastsid])
#tests
#get_users_tweets('caltrain', 100, '388677443831070720L')
#get_users_tweets('caltrain', 100,'')

def update_csv(username, count):
    """
    from the file we generated above of tweets, picks out the most recent tweet id
    and add all the tweets since then to catch it  up
    """

    
    with open("caltrainoutput.csv", 'r') as fp:
        data = csv.reader(fp,delimiter=',')
        rewritelist = []
        for row in data:
            print(row)
            if row[0] != 'lastsid':
                rewritelist.append(row)
            else:
                lastsid = row[1]
                print(lastsid, "i found lastsid!")

        
    get_users_tweets(username, count, lastsid)
    with open("caltrainoutput.csv", 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(rewritelist)
    print("I'm done updating")


#tests
#update_csv('caltrain', 100)


def parse_db(filename):

    """
    open the output file and compute some basic stats about how
    also, outputs its own file that grabs the train direction, time of report,
    and a (usually accurate) delay amount
    """

    import re

    with open("caltrainoutput.csv", 'r') as fp:
        with open("caltrainoutput_2.csv", 'wb') as f:
            data = csv.reader(fp,delimiter=',')
            writer = csv.writer(f)
            total = 0
            oldesttime = datetime.datetime.now()
            newesttime = datetime.datetime.strptime('20000101120000', '%Y%m%d%H%M%S')
            
            regexlate = re.compile("(\d{1,2}) min")
            regexnb = re.compile("nb", re.IGNORECASE)
            regexsb = re.compile("sb", re.IGNORECASE)
            
            for row in data:
                try:            
                    if datetime.datetime.strptime(row[1], '%Y%m%d%H%M%S') > newesttime: 
                        newesttime = datetime.datetime.strptime(row[1], '%Y%m%d%H%M%S')

                    if datetime.datetime.strptime(row[1], '%Y%m%d%H%M%S') < oldesttime:
                        
                        oldesttime = datetime.datetime.strptime(row[1], '%Y%m%d%H%M%S')

       
                    r1 = regexlate.findall(str(row))
                    sb = regexsb.findall(str(row))
                    nb = regexnb.findall(str(row))
                    
                    dayofweek = datetime.datetime.strptime(row[1], '%Y%m%d%H%M%S').weekday()
                    timeofday = datetime.datetime.strptime(row[1], '%Y%m%d%H%M%S').strftime('%H:%M:%S')

                    print(r1,sb,nb,dayofweek, timeofday)
                    writer.writerow([str(r1),sb,nb,dayofweek, timeofday])
                    
                    for thing in r1:
                        total += int(thing)
                except:
                    print("couldn't do conversion - skipping")

    # use sloppy conversion of removing 2/7 days per week to account for weekends
    weekdaysbetwixt = int((newesttime - oldesttime).days) * 5/7 
    print(weekdaysbetwixt)
        
    print("the trains were %s min late in time period %s" % (total, newesttime - oldesttime))
    print("that's, like, %s min per day of lost time" % (total/weekdaysbetwixt))

#tests
parse_db("caltrainoutput.csv")




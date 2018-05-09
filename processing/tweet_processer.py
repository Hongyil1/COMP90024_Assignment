
"""
===================================================
 Xiaolu Zhang 886161
 Jianbo Ma 807590
 Hongyi Lin 838776
 Xiaoyu Wang 799778
 Shalitha Weerakoon Karunatilleke 822379

 COMP90024 Cluster and Cloud Computing
 Social Media Analytics on Melbourne & Sydney
====================================================
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import string

import connection
import nltk
import tweepy
from dateutil import parser
from nltk.corpus import stopwords
from shapely.geometry.point import Point
from textblob import TextBlob
from tweepy import OAuthHandler

# Get stop words and tokenization from nltk data set
nltk.download('stopwords')
nltk.download('punkt')

# The suburb file
suburbs_melb = "melbourne.json"
suburbs_syd = "sydney.json"

# get punctuation
punctuation = string.punctuation


class Proccesser():

    def get_formated_tweet(self, tweet, text, hashtags, sub_dic):

        # Analysis those tweets that retweet more than 20 times
        if int(tweet["retweet_count"]) > 20:
            # Analysis the original tweet
            # The quoted tweet
            if tweet["is_quote_status"] == True:
                if "quoted_status" in tweet:
                    original_text = tweet["quoted_status"]["full_text"]
                    # sentiment analysis
                    original_sentiment = self.get_tweet_sentiment(original_text)
                else:
                    # If cannot get orginal tweet's text, fetch that tweet according to its id
                    consumer_key, consumer_secret, access_token, access_secret = connection.access_twitter_id_configuration()
                    auth = OAuthHandler(consumer_key, consumer_secret)
                    auth.set_access_token(access_token, access_secret)
                    api = tweepy.API(auth)

                    original_id = tweet['quoted_status_id_str']
                    original_tweet = api.get_status(original_id)
                    original_text = str(original_tweet.text)
                    # sentiment analysis
                    original_sentiment = self.get_tweet_sentiment(original_text)
            else:
                # The retweet
                if "retweeted_status" in tweet:
                    original_text = tweet["retweeted_status"]["full_text"]
                    # sentiment analysis
                    original_sentiment = self.get_tweet_sentiment(original_text)
                else:
                    original_sentiment = None
        else:
            # dont need to analysis the orginal tweet if retweet less than 20 times
            original_sentiment = None

        if tweet['coordinates'] != None:
            # Data pre-process
            coordinates = tweet['coordinates']['coordinates']
            latitude = coordinates[1]
            longitude = coordinates[0]
            
            # get suburb
            suburb = self.get_tweet_suburb(latitude, longitude, sub_dic)
            if suburb != None:
                # Process the text
                tweet_word_set = self.text_preprocess(text)
                # Get sentiment
                sentiment = self.get_tweet_sentiment(text)
                # Get publish time
                created_at = tweet["created_at"]
                when = self.get_tweet_when(created_at)

                # Get lifestyle
                lifestyle = self.get_tweet_lifestyle(tweet_word_set)
                
                # get crime
                crime = self.get_tweet_crime(tweet_word_set)
                
                # get liquor
                liquor = self.get_tweet_liquor(tweet_word_set)
                
            else:
                sentiment = ""
                when = ""
                suburb = None
                lifestyle = ""
                crime = ""
                liquor = ""

        elif tweet["place"] != None:
            if tweet["place"]["name"] != None:
                place = tweet["place"]["name"]
                suburb = self.get_tweet_suburb_from_location(place.lower(), sub_dic)
                if suburb != None:
                    tweet_word_set = self.text_preprocess(text)
                    sentiment = self.get_tweet_sentiment(text)
                    created_at = tweet["created_at"]
                    when = self.get_tweet_when(created_at)
                    lifestyle = self.get_tweet_lifestyle(tweet_word_set)
                    crime = self.get_tweet_crime(tweet_word_set)
                    liquor = self.get_tweet_liquor(tweet_word_set)
                else:
                    sentiment = ""
                    when = ""
                    suburb = None
                    lifestyle = ""
                    crime = ""
                    liquor = ""
        else:
            sentiment = ""
            when = ""
            suburb = None
            lifestyle = ""
            crime = ""
            liquor = ""

        return self.formate(tweet, text, hashtags, sentiment, when, suburb, lifestyle, crime, liquor,
                            original_sentiment)

    def get_tweet_sentiment(self, text):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # translate
        text = str(self.get_tweet_translation(text))

        # Change emoticons to text
        text = self.process_emoticons(text)

        # get rid of @, symbols and url
        text = self.clean_tweet(text)

        t = TextBlob(str(text))

        if t.sentiment.polarity > 0:
            return 'positive'
        elif t.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    # sort the created_at into "morning", "afternoon", or "night"
    def get_tweet_when(self, created_at):
        created_at = parser.parse(created_at)
        hour = int(created_at.strftime('%H'))
        if 4 <= hour < 12:
            return "morning"
        elif 12 <= hour < 20:
            return "afternoon"
        else:
            return "night"

    def get_tweet_suburb(self, lat, long, sub_dic):

        # sub_dic = suburbs_shapely_processor.read_json(suburbs_melb, suburbs_syd)
        # lati=-37, long=144
        point_cor = Point([long, lat])
        # Detect in Mel
        for name, pol_area in sub_dic['Big_Mel'].items():
            if pol_area.contains(point_cor):
                return name
        # Detect in Syd
        for name, pol_area in sub_dic['Big_Syd'].items():
            if pol_area.contains(point_cor):
                return name
        return None

    def get_tweet_suburb_from_location(self, place, sub_dic):

        if place is "melbourne" is place is "sydney":
            return place
        else:
            # Detect in Mel
            for name, area in sub_dic['Big_Mel'].items():
                if place.find(name):
                    return name
            # Detect in Syd
            for name, pol_area in sub_dic['Big_Syd'].items():
                if place.find(name):
                    return name
        return None

    def get_tweet_suburb_from_user_location(self, place, sub_dic):
        if place.find("melbourne"):
            return "melbourne"
        if place.find("sydney"):
            return "sydney"
        else:
            # Detect in Mel
            for name, area in sub_dic['Big_Mel'].items():
                if place.find(name):
                    return name
            # Detect in Syd
            for name, pol_area in sub_dic['Big_Syd'].items():
                if place.find(name):
                    return name

        return None

    def get_tweet_lifestyle(self, tweet_word_set):
        dic = {
            "Education": ["High school", "University", "Primary school", "Kindergarten",
                          "Class", "College", "Teacher", "Student", "Professor", "report",
                          "Learn", "School", "Train", "Degree", "Library", "Museum",
                          "Education", "Exam", "Examination", "Scholarship", "Homework",
                          "Curriculum", "Course", "Seminar", "Lecture", "Workshop", "Reflection", "Tutor",
                          "Due", "Deadline", "Assignment", "Subject", "Presentation", "Recording", "Record",
                          "LMS", "Discussion", "Board", "Study", "Lesson", "Experiment", "Enrol", "Timetable",
                          "Enrollment", "Hard", "Training", "PHD", "Essay"],
            "Shopping": ["Mall", "Myer", "David Jones", "Luxury goods", "Cloth", "Bag",
                         "Shop", "Beauty", "Shoe", "Coles", "Woolworth", "Market", "Grocery",
                         "Supermarket", "Purchase", "Coupon", "Discount", "Sale", "Promotion", "Shoes", "Mac",
                         "Makeup", "Price", "Online", "Cart", "Order", "Payment", "Pay",
                         "Chadstone", "DFO", "Apple", "Electronic", "Laptop", "Phone", "TV", "Appliance",
                         "Pet", "Gift", "Cash", "Gift card", "Refund", "Return", "Customer", "Membership",
                         "Store", "Book", "Music", "CD", "Instrument", "Buy", "Sell", "Receipt", "Shopping"],
            "Food": ["Delivery", "Take away", "Restaurant", "Delicious", "Yummy", "Brunch", "Breakfast",
                     "Dinner", "Lunch", "Recipe", "Food", "Cook", "Sushi", "Coffee", "Dessert", "Rice",
                     "Restaurant", "Eat", "Drink", "Wine", "Chinese", "Japanese", "Pizza", "Pasta", "Bread",
                     "Milk", "Fruit", "Banana", "Pancake", "Source", "Eat", "Heat", "Meat", "Frozen", "Fresh",
                     "Fish", "Beef", "Chicken", "Soup", "BQQ", "Vegetable", "Vegetarian", "Gluten",
                     "Latte", "Sugar", "Flat White", "Reservation", "Book", "Allergic", "Buffet", "Seafood",
                     "Bun", "Butter", "Cheese", "Apple", "Orange", "Mandarin", "Broccoli",
                     "Chilly", "Salt", "Vinegar", "Forks", "Fried", "Foodie", "Kitchen"],
            "Entertainment": ["Movie", "KTV", "Pub", "Performance", "Show", "Concert",
                              "Club", "Hang out", "Karaoke", "Restaurant", "Play", "Song", "Cinema", "Film",
                              "Trailer", "Youtube", "Instagram", "Twitter", "Tweet", "Facebook", "Media",
                              "Social", "Playground", "Aquarium", "Acrobatics", "Band", "Casino", "Circus",
                              "Fashion show", "Show", "Fair", "Theater", "Vacation", "Zoo", "Garden", "Parade",
                              "Box", "Ticket", "Entertainment"],
            "Living": ["Property", "Green land", "Apartment", "House", "Decoration", "Furniture", "Realestate",
                       "Utility", "Bill", "Rent", "Property", "Townhouse", "Agency", "Sell", "Sold", "Contract",
                       "Agreement", "Lease", "Rent", "Invoice", "Open", "Metre", "Meter", "Square", "Room",
                       "Balcony", "Floor", "Elevator", "Lift", "Sofa", "Move", "Loan", "Bank", "Living"],
            "Travel": ["Holiday", "Vocation", "Visit", "Vacation", "Trip", "Hotel", "Gold Coast", "Great Ocean Road",
                       "Tour", "Great", "View", "Self-drive", "Rent", "Road", "Music", "Motel", "Hotel",
                       "Sightseeing", "Scenery", "Baggage", "Accommodation", "Flight",
                       "Cruise", "Destination", "Backpack", "Ticket", "Beach", "Parking",
                       "Airbnb", "Type", "Book", "Animal", "Charge", "Insurance", "Atlas", "Travel",
                       "Tourist", "Tourism", "Melbourne", "Sydney", "Opera"],
            "Medical": ["Hospital", "Sick", "Fever", "Nurse", "Doctor", "Medicine", "Health",
                        "Disease", "A first", "Obesity", "Overweight", "Suicide", "Diet", "Band Aid", "Infection",
                        "Virus", "Dentist", "Dental", "Surgery", "Cancer", "Examine", "Insurance", "Medicare", "Check",
                        "Vaccine", "Patient", "Pharmacy", "Pharmacist", "GP", "Physician", "Hurt",
                        "Radio", "Medical"],
            "Sports": ["Sport", "Cricket", "Football", "Soccer", "Tennis", "Rugby league", "Olympics", "Swim", "Diving",
                       "Skydiving", "Ski", "Surf", "Snorkeling", "Scuba diving", "Running", "Gym", "Work out",
                       "Exercise", "Melbourne Cup", "Baseball", "Basketball", "Bowling", "Sports",
                       "Ticket", "Skating", "F1", "Footy", "AFL", "Brisbane Lions", "Greater Western Sydney Giants",
                       "Sydney Swans", "West Coast Eagles", "Western Bulldogs"],
            "Traffic": ["Tram", "Metro", "Car", "Bike", "Bicycle", "Train", "Boat", "Speedboat",
                        "Plane", "Aviation", "Fleet", "Airline", "Flight", "Ship", "Traffic jam", "Traffic", "Bus",
                        "Starbus", "Traffic", "Transport", "Skybus", "Jet", "Star", "Ticket",
                        "Dock", "Airbag", "Auto", "Avenue", "Road", "brakes", "bike", "carpool", "crash", "detour",
                        "drive", "driver", "driver's license", "driveway", "expressway", "emission", "fast", "slow",
                        "fuel", "tire", "gasoline", "GPS", "gutter", "highway", "kilometer", "motor", "parking",
                        "pedestrian", "pedal", "pass", "park", "speed", "stop", "vehicle", "underpass",
                        "zebra crossing", "signal", "light"],
        }

        lifestyle = []
        for key, value in dic.items():
            # Normalizing Case
            value = map(lambda word: word.lower(), value)
            if len(set(value) & tweet_word_set) > 0:
                lifestyle.append(key.lower())
              
        return lifestyle

    def get_tweet_crime(self, tweet_word_set):
        dic = ["Assault", "Attack", "Armed", "Bombing", "Drugs", "Gun", "Kidnapping", "Malice", "Missing person",
               "Offender", "theft", "Prison", "Robbery", "Sentence", "Serial killer", "Sex crimes", "Shooting",
               "Survivor", "Terrorism", "Victim", "Weapon", "Witness",
               "Jail", "Criminal", "Crime", "Cell", "Justice", "terrorist", "Killer", "Murderer", "robber",
               "smuggler", "court", "sentence", "law", "illegal", "offence"]

        # Normalizing Case
        dic = map(lambda word: word.lower(), dic)
        if len(set(dic) & tweet_word_set) > 0:
            return True
        else:
            return False

    def get_tweet_liquor(self, tweet_word_set):

        dic = ["booze", "liquor", "strong drink", "alcohol", "beer", "wine", "whiskey", "rum", "brandy",
               "bourbon", "drunk", "tequila", "alcoholic", "liqueur", "bar", "whisky", "alcoholism", "pulp",
               "cellar", "batter", "vodka", "liquor license", "gin", "alcohol", "headache", "Drunk",
               "Disorder", "Messy", "Disorder", "Smashed", "Sober", "AA", "handover", "stomach", "pain",
               "cider", "pale", "urine", "glass", "shot", "swig", "toast", "sip"]

        dic = map(lambda word: word.lower(), dic)
        if len(set(dic) & tweet_word_set) > 0:
            return True
        else:
            return False

    def text_preprocess(self, text):

        # Translate the text
        text = str(self.get_tweet_translation(text))

        # Change emoticons to text
        text = self.process_emoticons(text)

        # get rid of @, symbols and url
        text = self.clean_tweet(text)

        # Normalizing Case and get rid of stop word
        tweet_word_set = self.nlp_tweeet(text)

        return tweet_word_set

    def process_emoticons(self, text):
        # transfer the emoticons in String type
        # Smile: :) :D :-) =) (: (-: (=
        text = re.sub(r'(:\))|(:D)|(:-\))|(=\))|(\(:)|(\(-:)|(\(=)', 'happy', text)
        # Sad :( :-( :-< =( ): )-: >-: )=
        text = re.sub(r'(:\()|(:-\()|(:-<)|(=\()|(\):)|(\)-:)|(>-:)|(\)=)', 'sad', text)
        # Surprised :-O O-:
        text = re.sub(r'(:-O)|(O-:)', 'surprised', text)
        # Scream :@ :-@ @: @-:
        text = re.sub(r'(:@)|(:-@)|(@:)|(@-:)', 'scream', text)
        # Confused O.o o.O
        text = re.sub(r'(O.o)|(o.O)', 'confused', text)

        # transfer the emoticons in UTF-16 type
        # positive: 😀😁😂🤣😄😅😆😉😊😋😎😍😘😗😚🤗🤩
        text = re.sub(r'(\\ud83d\\ude03)|(\\ud83d\\ude01)|(\\ud83d\\ude02)|(\\ud83e\\udd23)|(\\ud83d\\ude04)|'
                      r'(\\ud83d\\ude05)|(\\ud83d\\ude06)|(\\ud83d\\ude09)|(\\ud83d\\ude0a)|(\\ud83d\\ude0b)|'
                      r'(\\ud83d\\ude0e)|(\\ud83d\\ude0d)|(\\ud83d\\ude18)|(\\ud83d\\ude17)|(\\ud83d\\ude19)|'
                      r'(\\ud83d\\ude1a)|(\\u263a)|(\\ud83e\\udd29)', 'happy', text)

        # negative: 🙁😖😞😟😤😢😭😦😧😨😩🤯😬😰😱😳😵
        text = re.sub(r'(\\u2639)|(\\ud83d\\ude41)|(\\ud83d\\ude16)|(\\ud83d\\ude1e)|(ud83d\\ude1f)|'
                      r'(\\ud83d\\ude24)|(\\ud83d\\ude22)|(\\ud83d\\ude2d)|(\\ud83d\\ude26)|(\\ud83d\\ude27)|'
                      r'(\\ud83d\\ude28)|(\\ud83e\\udd2f)|(\\ud83d\\ude2c)|(\\ud83d\\ude30)|(\\ud83d\\ude31)|'
                      r'(\\ud83d\\ude33)|(\\ud83d\\ude35)', 'sad', text)

        # angery: 😡😠🤬
        text = re.sub(r'(\\ud83d\\ude21)|(\\ud83d\\ude20)|(\\ud83e\\udd2c)', 'angry', text)

        # sick: 😷🤒🤕🤢🤮🤧
        text = re.sub(r'(\\ud83d\\ude37)|(\\ud83e\\udd12)|(\\ud83e\\udd15)|(\\ud83e\\udd22)|'
                      r'(\\ud83e\\udd2e)|(\\ud83e\\udd27)', 'sick', text)

        return text

    def clean_tweet(self, text):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''

        # get rid of @
        # get rid of all symbols
        # get rid of url
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

    def get_tweet_translation(self, text):
        '''
        use TextBlob to translate non-English twitter and correct the spelling
        '''
        try:
            temp = TextBlob(text)  # skip the too short tweet less than 3 character
            # get language of the twitter
            lang = temp.detect_language()
            if lang != 'en':
                translated = temp.translate(from_lang=lang, to='en')
                translated = translated.correct()
                return translated
                # except TranslatorError:
                #     return False
                # except NotTranslated:
                #     return False
            else:
                temp = TextBlob(text)
                text = str(temp.correct())
                return text
        except:
            return text

    def nlp_tweeet(self, text):
        sentence = text
        # Tokenize the sentence
        tokens = nltk.word_tokenize(sentence)

        # Normalizing Case
        tokens = map(lambda word: word.lower(), tokens)

        # Remove the stop word
        stops = set(stopwords.words("english"))

        filtered_word = set(tokens) - stops
        # print(filtered_word)

        tweet_word_set = filtered_word

        return tweet_word_set

    def formate(self, data, text, hashtags, sentiment, when, suburb, lifestyle, crime, liquor, original_sentiment):
        dic = {
            "_id": data['id_str'],
            "id": data['id_str'],
            "time": {
                "created_at": data["created_at"],
                "when": when
            },
            "content": {
                "text": text,
                "hashtags": hashtags,
                "source": data["source"],
                # "is_quote_status": data["is_quote_status"],
                "lang": data["lang"]
            },
            "location": {
                "suburb": suburb,
                "geo": data["geo"],
                "coordinates": data["coordinates"],
                "place": data["place"]
            },
            "sentiment": sentiment,
            "user": {
                "id": data['user']['id_str'],
                "location": data['user']['location'],
                "description": data['user']["description"],
                # "utc_offset": data['user']["utc_offset"],
                # "time_zone": data['user']["time_zone"]
            },
            # record the re-tweet number
            "followers_count": data['user']['followers_count'],
            "retweet": {
                "retweet_count": data["retweet_count"],
                # "retweet_id": data["retweeted_status"]["id"] if "retweeted_status" in data else None
                "original_sentiment": original_sentiment,
            },
            "lifestyle": lifestyle,
            "crime": crime,
            "liquor": liquor
        }
        return dic

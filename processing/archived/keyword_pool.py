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

from collections import Counter
from itertools import takewhile


# Return first nth element with the same value
def get_items_upto_count(dct, n):
    data = dct.most_common()
    val = data[n - 1][1]
    return list(takewhile(lambda x: x[1] >= val and x[1] != 0, data))


def word_dic():
    dic = {
        "Education": ["High school", "University", "Primary school", "Kindergarten",
                      "Class", "College", "Teacher", "Student", "Professor",
                      "Learn", "School", "Train", "Degree", "Library", "Museum",
                      "Education", "Exam", "Examination", "Scholarship", "Homework",
                      "Curriculum", "Course", "Seminar"],
        "Shopping": ["Mall", "Myer", "David Jones", "Luxury goods", "Cloth", "Bag",
                     "Shop", "Beauty", "Shoe", "Coles", "Woolworth", "Market", "Grocery",
                     "Supermarket", "Purchase", "Coupon", "Discount", "Sale"],
        "Food": ["Delivery", "Take away", "Restaurant", "Delicious", "Yummy", "Brunch", "Breakfast",
                 "Dinner", "Lunch", "Recipe", "Food", "Cook", "Sushi", "Coffee", "Dessert",
                 "Restaurant", "Eat", "Drink", "wine"],
        "Entertainment": ["Movie", "KTV", "Pub", "Performance", "Show", "Concert",
                          "club", "Hang out", "Karaoke", "Restaurant"],
        "Living": ["Property", "Green land", "Apartment", "House", "Decoration", "Furniture", "Realestate",
                   "Utility", "Bill", "Rent", "Property", "Townhouse"],
        "Travel": ["Holiday", "Visit", "Vacation", "Trip", "Hotel", "Gold Coast", "Great Ocean Road", "Tour",
                   "Sightseeing", "Scenery", "Baggage", "Accommodation", "Flight",
                   "Cruise", "Destination", "Backpack", "Ticket", "Beach", "parking"],
        "Medical": ["Hospital", "Sick", "Fever", "Nurse", "Doctor", "Medicine", "Health",
                    "Disease", "A first", "Obesity", "Overweight", "Suicide", "Diet", "Band Aid", "Infection", "Virus",
                    "Vaccine", "Patient", "Pharmacy", "pharmacist", "GP", "Physician"],
        "Sports": ["Sport", "Cricket", "Football", "Soccer", "Tennis", "Rugby league", "Olympics", "Swim", "Diving",
                   "Skydiving", "Ski", "Surf", "Snorkeling", "Scuba diving", "Running", "Gym", "Work out", "Exercise",
                   "Melbourne Cup"],
        "Traffic": ["Tram", "Metro", "Car", "Bike", "Bicycle", "Train", "Boat", "Speedboat",
                    "Plane", "Aviation", "Fleet", "Airline", "Flight", "ship", "traffic jam", "Traffic", "Bus"],
    }

    return dic


def lifestyle_count(text):
    dic = word_dic()

    text_count = Counter()

    for key in dic:
        text_count[key] = 0
        for word in dic[key]:
            if word.lower() in text.lower():
                text_count[key] += 1

    return get_items_upto_count(text_count, 1)


if __name__ == "__main__":
    print(lifestyle_count("sport and ktv"))
    for ele in lifestyle_count("sport and ktv"):
        key = ele[0]
        print("key: ", key)

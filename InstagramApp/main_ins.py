import sys
import instaloader
import json
import heapq
import time
import pyinputplus as pyip
from datetime import datetime
from itertools import takewhile



class InstagramApp:
    def __init__(self, user_name, password):
        """
        Class to manage instagram connections and functionalities
        :param user_name: instagram user
        :param password: instagram password
        """
        self.user_name = user_name
        self._password = password
        self._instaloader = instaloader.Instaloader()
        self._context = self._instaloader.context
        self._profile = instaloader.Profile.from_username(self._context, user_name)

    def login(self):
        print(f"Start application for user {self.user_name}")
        i = 0
        while True:
            try:
                self._instaloader.login(self.user_name, self._password)
                print("Login successful\n")
                break
            except instaloader.BadCredentialsException:
                print("Login error, check your credentials\n")
                time.sleep(5)
                raise sys.exit()
            except instaloader.InstaloaderException:
                if i == 2:
                    print("Login error\n")
                    raise
                print("Exception found\n")
                print("Trying again...")
                i += 1

    def close(self):
        self._instaloader.close()

    # Return followers
    def followers(self):
        return set(f.username for f in self._profile.get_followers())

    # Return followees
    def followees(self):
        return set(f.username for f in self._profile.get_followees())

    # Return top n likes and posts url
    def top_n_likes(self, n):
        print(f"Getting the {n} most liked photos for {self.user_name}...")
        # Get post likes and shortcodes
        dict_likes = {f.shortcode: f.likes for f in self._profile.get_posts()}
        # Get max number of likes
        lst = heapq.nlargest(n, [value for key, value in dict_likes.items()])
        # Get results
        sorted_dict = sorted(dict_likes.items(), key=lambda item: item[1], reverse=True)
        for element in [(key, value) for key, value in sorted_dict if value in lst]:
            print(f"Post url: https://www.instagram.com/p/{element[0]}/    Likes: {element[1]}")

    # Get people that doesn't follow you back
    def unfollow(self):
        print(f"Checking followees that aren't followers...")
        skip_list = [i.rstrip("\n") for i in open("data/skip_list.txt", "r")]
        followers = set(self._profile.get_followers())
        followees = set(self._profile.get_followees())
        unfollow = [f.username for f in followees.difference(followers) if f.username not in skip_list]
        print("\n".join(unfollow))

    # Download stories from user in a range of time
    # TODO Improve data output
    def download_posts(self, since, user_name):
        new_profile = instaloader.Profile.from_username(self._context, user_name)
        print(f"Downloading posts for user {user_name}")
        for post in takewhile(lambda p: p.date > since, new_profile.get_posts()):
            print(f"Date {post.date}")
            self._instaloader.download_post(post, user_name)

    # Download stories from user in a range of time
    # TODO Improve data output
    def download_videos(self, since, user_name):
        new_profile = instaloader.Profile.from_username(self._context, user_name)
        print(f"Downloading videos for user {user_name}")
        for post in takewhile(lambda p: p.date > since, new_profile.get_posts()):
            if post.is_video:
                print(f"Date {post.date}")
                self._instaloader.download_post(post, user_name)





# Start application
if __name__ == '__main__':
    user_cred = json.load(open("data/user.json", "r"))
    user_options = ["Check people not following you back", "Get top 10 likes", "Download posts from user",
                    "Download videos from user", "Exit"]
    user1 = InstagramApp(user_cred["user"], user_cred["password"])
    user1.login()

    # Menu
    while True:
        # Return integer based on choice
        choice = user_options.index(pyip.inputMenu(user_options, numbered=True, allowRegexes=['(1-5)'], limit=10))+1
        print()

        # Execute action for each choice
        if choice == 1:
            user1.unfollow()
        elif choice == 2:
            user1.top_n_likes(10)
        elif choice == 3:
            user_n = input("Type instagram username: ")
            date_since = input("Type beginning date to download in format YYYY, MM, DD: ")
            user1.download_posts(datetime.strptime(date_since, "%Y, %m, %d"), user_n)
        elif choice == 4:
            user_n = input("Type instagram username: ")
            date_since = input("Type beginning date to download in format YYYY, MM, DD: ")
            user1.download_posts(datetime.strptime(date_since, "%Y, %m, %d"), user_n)
        elif choice == 5:
            user1.close()
            sys.exit()
        print("\n")
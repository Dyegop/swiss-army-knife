from datetime import datetime
import sys
import instaloader
import json
import heapq
from itertools import takewhile, dropwhile



class InstagramApp:
    def __init__(self, user_name, password):
        """
        Class to manage instagram connections and functionalities
        :param user: instagram user
        :param password: instagram password
        """
        self.user_name = user_name
        self._password = password
        self._instaloader = instaloader.Instaloader()
        self._context = self._instaloader.context
        self._profile = instaloader.Profile.from_username(self._context, user_name)

    def login(self):
        print(f"Start application for user {self.user_name}")
        try:
            self._instaloader.login(self.user_name, self._password)
            print("Login successful\n")
        except instaloader.BadCredentialsException:
            print("Login error, check your credentials\n")
            raise sys.exit()
        except instaloader.InstaloaderException:
            print("Exception found\n")
            raise

    def close(self):
        self._instaloader.close()

    # Return followers
    def followers(self):
        return [f.username for f in self._profile.get_followers()]

    # Return followees
    def followees(self):
        return [f.username for f in self._profile.get_followees()]

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
        skip_list = [i.rstrip("\n") for i in open("skip_list.txt", "r")]
        followers = self.followers()
        followees = self.followees()
        for f in followees:
            if f not in followers and f not in skip_list:
                print(f)
        print()

    # Download stories from user in a range of time
    # TODO Improve data output
    def download_posts(self, since, user_name):
        new_profile = instaloader.Profile.from_username(self._context, user_name)
        print(f"Downloading posts for user {user_name}")
        for post in takewhile(lambda p: p.date > since, new_profile.get_posts()):
            print(f"Date {post.date}")
            self._instaloader.download_post(post, user_name)





# Main
if __name__ == '__main__':
    user_cred = json.load(open("user.json", "r"))
    user1 = InstagramApp(user_cred["user"], user_cred["password"])
    user1.login()
    user1.unfollow()
    # user1.top_n_likes(10)
    # user1.download_posts(datetime(2019, 1, 12), "type_user_name")
    user1.close()

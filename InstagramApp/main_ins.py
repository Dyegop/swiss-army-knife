import instaloader
import json



class InstagramApp:
    def __init__(self, user, password):
        """
        Class to manage instagram connections and functionalities

        Attributes:
            -instaloader:
            -profile:

        :param user: instagram user
        :param password: instagram password
        """
        self.user = user
        self.password = password
        self._instaloader = instaloader.Instaloader()
        self._context = self._instaloader.context
        self._profile = instaloader.Profile.from_username(self._context, user)

    def login(self):
        try:
            self._instaloader.login(self.user, self.password)
            print("Login successful")
        except instaloader.InstaloaderException:
            print(f"Exception found")
            raise

    def close(self):
        self._instaloader.close()

    def followers(self):
        return [f.username for f in self._profile.get_followers()]

    def followees(self):
        return [f.username for f in self._profile.get_followees()]

    def unfollow(self):
        print(f"Checking people that don't follow {self.user} back...")
        skip_list = ["pycoders", "wildlifeplanet", "earth", "heroefitness", "gastroobscura", "natgeoadventure",
                     "spacex", "danielkordan", "natgeo", "kpunkka", "davidlloyd", "itsabandoned", "8fact", "science",
                     "papateachme", "scoobysworkshop", "bbcnews", "ancient_origins", "atlasobscura",
                     "jimmy.nelson.official", "atodaleche", "teslamotors", "cuestafrank", "natgeotravel", "paulnicklen",
                     "madrid_secreto", "iflscience", "nasa", "eminem", "discoverwildlife", "jmvillatoro_psicologo"]
        followers = user1.followers()
        followees = user1.followees()
        for f in followees:
            if f not in followers and f not in skip_list:
                print(f)



# Main
if __name__ == '__main__':
    user_cred = json.load(open("user.json", "r"))
    user1 = InstagramApp(user_cred["user"], user_cred["password"])
    user1.login()
    user1.unfollow()
    user1.close()

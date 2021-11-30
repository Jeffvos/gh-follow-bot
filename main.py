import os
import requests
import time
from tqdm import tqdm

class githubFollow():
    def __init__(self):
        os.system("clear")
        self.ghUser = os.environ.get("ghuser")
        self.ghToken = os.environ.get("ghtoken")
        self.checkIfCreds()
        self.baseUrl = "https://api.github.com"
        self.count = 0
        self.followCount = 0

    def checkIfCreds(self):
            if not self.ghToken and self.ghUser:
                print("please export login credentials")
                quit()

    def createRequest(self, url, method):
        r = requests.request(method, self.baseUrl+url, params={"per_page":100}, auth=(self.ghUser,self.ghToken))
        try:
            jsonLoad = r.json()
        except:
            jsonLoad = r.status_code
        return jsonLoad
    
    def parseLoad(self, jsonData):
        for user in jsonData:
            self.getFollowingFollows(user['login'])

    def getFollowing(self):
        #get current users following
        url = "/user/following"
        following = self.createRequest(url, "GET")
        self.parseLoad(following)
        return following

    def getFollowingFollows(self, user):
        url = f"/users/{user}/following"
        followingFollows = self.createRequest(url, "GET")
        print(f"{user} || checking {len(followingFollows)} accounts || followed {self.followCount} users || total accounts checked {self.count}")
        try:
            for user in tqdm(followingFollows):
                self.followFollowingFollows(user['login'])
        except KeyboardInterrupt:
            os.system("clear")
            print("Stopped")
            print(f"checked {self.count} accounts and started following {self.followCount} accounts")
            quit()
        os.system("clear")

    def validateFollowed(self, username):
        url = f"/user/following/{username}"
        validateFollower = self.createRequest(url, "GET")
        if validateFollower == 204:
            return True
        else:
            return False

    def followFollowingFollows(self, username):
        self.count = self.count + 1
        alreadyFollowing = self.validateFollowed(username)
        if not alreadyFollowing:
            url = f"/user/following/{username}"
            followUser = self.createRequest(url, "PUT")
            if followUser != 204:
                print(followUser)
                time.sleep(360)
                followUser = self.createRequest(url, "PUT")
            self.followCount = self.followCount + 1
        return username
        

follow = githubFollow()
follow.getFollowing()
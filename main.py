import os
import requests
import time
from tqdm import tqdm
import versioncontrol

class githubFollow():
    def __init__(self):
        os.system("clear")
        self.validateVersion()
        self.ghUser = os.environ.get("ghuser")
        self.ghToken = os.environ.get("ghtoken")
        #self.checkIfCreds()
        self.baseUrl = "https://api.github.com"
        self.count = 0
        self.followCount = 0

    def checkIfCreds(self):
        if len(self.ghToken) <= 0 or len(self.ghUser) <= 0:
            print('please export ghtoken and ghuser')
            quit()

    def validateVersion(self):
        versionCheck = versioncontrol.checkVersion()
        if versionCheck.running_latest() == False:
            quit()

    def create_single_r(self, url, method):
        r = requests.request(method, self.baseUrl+url, auth=(self.ghUser,self.ghToken))
        return r

    def createRequest(self, url, method):
        page=True
        current_page=1
        list_pages=[]
        while page:
            r = requests.request(method, self.baseUrl+url, params={"per_page":100, "page":current_page}, auth=(self.ghUser,self.ghToken))
            current_page=current_page+1
            try:
                jsonLoad = r.json()
                list_pages.append(jsonLoad)

            except:
                jsonLoad = r.status_code
            if len(jsonLoad) == 0:
                page=False
        return list_pages

    def parseLoad(self, jsonData):
        for user in jsonData:
            self.getFollowingFollows(user['login'])

    def getFollowing(self):
        url = "/user/following"
        following = self.createRequest(url, "GET")
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
            print("Stopped..")
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
            else:
                self.followCount = self.followCount + 1
        return username
        
    def check_if_following(self):
        count_follow=0
        count_no_follow=0
        url ='/user/followers'
        followers = {}
        followings = {}
        get_followers = self.createRequest(url, "GET")
        following = self.getFollowing()

        for follower in get_followers[0]:
            followers[follower['login']] = follower['login']
        

        for listing in following:
            for follow in tqdm(listing):
                if follow['login']in followers:
                    count_follow = count_follow+1
                else:
                    count_no_follow = count_no_follow+1
                    self.unfollow_user(follow['login'])
                followings[follow['login']] = follow['login'] 

        print(f"not following back {count_no_follow} following {count_follow}")
    
    def unfollow_user(self, user):
        url = f'/user/following/{user}'
        request = self.create_single_r(url, 'DELETE')
if __name__ == "__main__":  
    follow = githubFollow()
    follow.check_if_following()
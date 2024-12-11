from asyncio.windows_events import NULL
import os
from contextlib import suppress
import requests
import json

AUTH_TOKEN = ''


class PassException:
    def __enter__(self):
        pass

    def __exit__(self, *args):
        return True


class TinderProfile:
    def __init__(self, json_child: dict, x_auth_token=None, save_pics=False):
        self.json_child = json_child
        self.id = ''
        self.verified = False
        self.bio = ''
        self.birth_date = ''
        self.name = ''
        self.photos = []
        self.gender = 0
        self.city = ''
        self.show_gender_on_profile = False
        self.recently_active = False
        self.online_now = False
        self.distance_mi = 0
        self.distance_km = 0
        self.teaser = ''
        self.s_number = 0
        self.constructor()
        self.match = False
        self.x_auth_token = x_auth_token
        if save_pics:
            self.save_photos()

        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def constructor(self):
        root_user = self.json_child['user']
        with suppress(Exception): self.id = root_user['_id']
        with suppress(Exception): self.verified = True if len(root_user['badges']) > 0 else False
        with suppress(Exception): self.bio = root_user['bio'].replace("'", "")
        with suppress(Exception): self.birth_date = root_user['birth_date']
        with suppress(Exception): self.name = root_user['name']
        with suppress(Exception): self.photos = [i['url'] for i in root_user['photos']]
        with suppress(Exception): self.gender = root_user['gender']
        with suppress(Exception): self.city = root_user['city']['name'].replace("'", '')
        with suppress(Exception): self.show_gender_on_profile = root_user['show_gender_on_profile']
        with suppress(Exception): self.recently_active = root_user['recently_active']
        with suppress(Exception): self.online_now = root_user['online_now']
        with suppress(Exception): self.distance_mi = self.json_child['distance_mi']
        with suppress(Exception): self.distance_km = int(self.distance_mi / 1.60934)
        with suppress(Exception): self.teaser = self.json_child['teaser']['string'].replace("'", '')
        with suppress(Exception): self.s_number = self.json_child['s_number']

    def save_photos(self):
        for photo in self.photos:
            response = requests.get(photo)

            if not os.path.exists(f'Photos/{self.id}'):
                os.mkdir(f'Photos/{self.id}')
            try:
                with open(f'Photos/{self.id}/{photo.split("/")[5].split("?")[0]}', 'wb') as f:
                    f.write(response.content)
                f.close()
            except:
                pass

    def getAll(self):
        return [i for _, i in self.__dict__.items()][1:]
    
    def find_matches(self, verbose=False):
        url = "https://api.gotinder.com/v2/matches/"

        querystring = {"locale": "zh-tw", "count": "60", "message": "1", "is_tinder_u": "false"}

        headers = {
            'Connection': 'close',
            'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            'Support-Short-Video': '1',
            'App-Session-Time-Elapsed' : '2726',
            'X-Auth-Token': self.x_auth_token,
            'User-Session-Time-Elapsed': '2549',
            'Sec-Ch-Ua-Platform': "Windows",
            'X-Supported-Image-Formats': "webp,jpeg",
            'Persistent-Device-Id' : '79fc234e-920e-4ce9-89c3-80b6f12d070e',
            'Tinder-Version': '5.27.0',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36',
            'User-Session-Id': 'd6b09029-aaa3-4a86-8ca0-ae55fa7fd313',
            'Accept': 'application/json',
            'Platform': 'web',
            'App-Session-Id': 'e94d2ac5-310f-455f-9b2c-3f526171a93b',
            'App-Version': '1052700',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br',
            'Priority': 'u=1, i'
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print("The response of upload = ",response.json())
        return 0

    def upload_location(self, verbose=False):
        url = "https://api.gotinder.com/user/ping"

        querystring = {"data": "{\"lat\": 22.6661460, \"lon\": 121.4710558}"}

        headers = {
            'Connection': 'close',
            'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            'app-session-time-elapsed': "12785",
            'x-auth-token': self.x_auth_token,
            'user-session-time-elapsed': "12419",
            'sec-ch-ua-platform': "\"Windows\"",
            'x-supported-image-formats': "jpeg",
            'persistent-device-id': "262f940f-3185-4408-kl49-6a4190a9051e",
            'tinder-version': "3.20.0",
            'sec-ch-ua-mobile': "?0",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            'user-session-id': "9118e59f-2cb9-44cb-b3d5-5u938bf6146e",
            'accept': "application/json",
            'platform': "web",
            'app-session-id': "01483a4d-5326-4a24-8cae-8ebfec150be3",
            'app-version': "1032000",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print("The response of upload = ",response)
        return 0
    
    def action(self, option=None):
        if option and self.x_auth_token:
            try:
                url = f"https://api.gotinder.com/{option}/{self.id}"

                querystring = {"locale": "en"}

                payload = {"s_number": self.s_number}
                headers = {
                    'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
                    'app-session-time-elapsed': "1937",
                    'x-auth-token': self.x_auth_token,
                    'user-session-time-elapsed': "1937",
                    'sec-ch-ua-platform': "\"Windows\"",
                    'x-supported-image-formats': "jpeg",
                    'persistent-device-id': "262f940f-3185-4408-b249-6a4190a9051e",
                    'tinder-version': "3.22.0",
                    'sec-ch-ua-mobile': "?0",
                    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
                    'content-type': "application/json",
                    'user-session-id': "a31a8ed7-00fd-4ff0-951b-8c3d832e4d8a",
                    'accept': "application/json",
                    'platform': "web",
                    'app-session-id': "5f80ac4d-ddd4-4701-9cb5-52cc4b785750",
                    'app-version': "1032200",
                    'cache-control': "no-cache"
                }

                response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

                if response.status_code == 200:
                    if response.json()['match']:
                        self.match = True

                    return 1
                else:
                    print('error: change X-AUTH_TOKEN')
            except Exception as e:
                print(f'error {e}')

        else:
            print('Please add x_auth_token=xxxxxx')

    def like(self, colorful=None):
        print('Liking...')
        # message = f'{self.name} {self.distance_km} KM {self.birth_date}'
        if self.action('like') == 1:
            print(f'{self.name} {self.distance_km} KM {self.birth_date}')

    def dislike(self):
        self.action('pass')


class Tinder:
    def __init__(self, x_auth_token):
        self.x_auth_token = x_auth_token
        if not os.path.exists(f'Photos'):
            os.mkdir(f'Photos')
    
    def send_message(self, verbose=False, sendID = "", message=""):
        url = "https://api.gotinder.com/user/matches/" + sendID 
        s = sendID
        from_id = s[: len(s) // 2]
        to_id = s[len(s) // 2 :]
        
        body = {
            'matchId': sendID,
            'message': message,
            'userId': from_id,
            'otherId': to_id,
            'sessonId': None
        }
        data = requests.post("https://api.gotinder.com" + f'/user/matches/{sendID}', json=body, headers={"X-Auth-Token": self.x_auth_token}).json()
        return data
    
    def find_matches(self, verbose=False):
        url = "https://api.gotinder.com"
        header = {
            
            'X-Auth-Token': self.x_auth_token,
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{url}/v2/matches?count=60",
            headers=header
        )
        response.raise_for_status()
        

        
        data = response.json()["data"]["matches"]
        #print(type(data))
        allMessages = {}
        for i in range(len(data)):
            try:
                toID   = str(data[i].get('messages')[0].get('to'))
            except Exception as e:
                print(e)
                pass
            try:
                fromID = str(data[i].get('messages')[0].get('from'))
            except Exception as e:
                print(e)
                pass
            try:
                message = str(data[i].get('messages')[0].get('message'))
            except Exception as e:
                print(e)
                pass
            try:
                matchID = str(data[i].get('messages')[0].get('match_id'))
            except Exception as e:
                print(e)
                pass
            #allMessages[matchID] = message
            if(matchID.find(fromID) > 3):
                #print(matchID)
                allMessages[matchID] = message
        return allMessages
    
    def get_recommend(self, verbose=False):
        url = "https://api.gotinder.com/v2/matches"

        querystring = {"count": "3"}

        headers = {
            'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            'app-session-time-elapsed': "12785",
            'x-auth-token': self.x_auth_token,
            'user-session-time-elapsed': "12419",
            'sec-ch-ua-platform': "\"Windows\"",
            'x-supported-image-formats': "jpeg",
            'persistent-device-id': "262f940f-3185-4408-kl49-6a4190a9051e",
            'tinder-version': "3.20.0",
            'sec-ch-ua-mobile': "?0",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            'user-session-id': "9118e59f-2cb9-44cb-b3d5-5u938bf6146e",
            'accept': "application/json",
            'platform': "web",
            'app-session-id': "01483a4d-5326-4a24-8cae-8ebfec150be3",
            'app-version': "1032000",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, data = querystring)
        print(response.text)
        return -1

    def get_potential_matches(self, verbose=False):
        url = "https://api.gotinder.com/v2/recs/core"

        querystring = {"locale": "en"}

        headers = {
            'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            'app-session-time-elapsed': "12785",
            'x-auth-token': self.x_auth_token,
            'user-session-time-elapsed': "12419",
            'sec-ch-ua-platform': "\"Windows\"",
            'x-supported-image-formats': "jpeg",
            'persistent-device-id': "262f940f-3185-4408-kl49-6a4190a9051e",
            'tinder-version': "3.20.0",
            'sec-ch-ua-mobile': "?0",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            'user-session-id': "9118e59f-2cb9-44cb-b3d5-5u938bf6146e",
            'accept': "application/json",
            'platform': "web",
            'app-session-id': "01483a4d-5326-4a24-8cae-8ebfec150be3",
            'app-version': "1032000",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if verbose:
            print(response.text)
        if response.status_code == 200 and response.json()['meta']['status'] == 200:
            try:
                return response.json()['data']['results']
            except Exception as e:
                if verbose:
                    print(f'error: {e}')

            if "1800000}}" in response.text:
                return 2
        print(f'response: {response.text}')
        return -1
    
    def upload_location(self, verbose=False):
        url = "https://api.gotinder.com/user/ping"

        querystring = {"data": "{\"lat\": 22.6661460, \"lon\": 121.4710558}"}

        headers = {
            'Connection': 'close',
            'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            'app-session-time-elapsed': "12785",
            'x-auth-token': self.x_auth_token,
            'user-session-time-elapsed': "12419",
            'sec-ch-ua-platform': "\"Windows\"",
            'x-supported-image-formats': "jpeg",
            'persistent-device-id': "262f940f-3185-4408-kl49-6a4190a9051e",
            'tinder-version': "3.20.0",
            'sec-ch-ua-mobile': "?0",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            'user-session-id': "9118e59f-2cb9-44cb-b3d5-5u938bf6146e",
            'accept': "application/json",
            'platform': "web",
            'app-session-id': "01483a4d-5326-4a24-8cae-8ebfec150be3",
            'app-version': "1032000",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print("The response of upload = ",response.text)
        return 0
        if verbose:
            print(response.text)
        if response.status_code == 200 and response.json()['meta']['status'] == 200:
            try:
                return response.json()['data']['results']
            except Exception as e:
                if verbose:
                    print(f'error: {e}')

            if "1800000}}" in response.text:
                return 2
        print(f'response: {response.text}')
        return -1

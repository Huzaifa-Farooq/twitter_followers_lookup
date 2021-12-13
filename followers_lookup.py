import pandas as pd
import requests
import os
import time

access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''
BEARER_TOKEN = ''



def get_data(response):
    """ gets an HTTP response and return user's data as per demand """
    data_to_return = []
    try:
        data = response['data']
    except Exception as e:
        print(str(e))
        print(f"Encountered an error\n{response}")
    else:
        for user_data in data:
            try:
                t = user_data['location']
            except KeyError:
                user_data['location'] = ''

            temp = [user_data['id'], user_data['name'], user_data['username'], user_data['location'],
                    user_data['created_at'], user_data['public_metrics']['followers_count'],
                    user_data['public_metrics']['following_count'], user_data['public_metrics']['tweet_count'],
                    user_data['verified'], user_data['protected']]
            data_to_return.append(temp)

        return data_to_return


def get_info(path):
    """ function to get required info """

    try:
        with open(f"{path}\\info.txt", 'r') as f:
            info = f.read()
            info = info.split(',')
            return info[0], int(info[1]), int(info[2])
    except FileNotFoundError:
        return None, None, None


def save_info(path, pagination_token, followers_retrieved, file_no):
    """ function to save data """
    try:
        with open(f"{path}\\info.txt", 'w') as f:
            f.write(f'{pagination_token},{str(followers_retrieved)},{str(file_no)}')

    except Exception as e:
        print(str(e))


def get_user_info(username):
    """ gets id  of a user and return its username, total_followers"""
    import tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    user_info = api.get_user(username)

    return user_info._json['id'], user_info._json['followers_count']


def check_directories(username):
    """ checks if required directories exists if not then creates them """
    path = f"D:\\Huzaifa\\ai\\AI\\COVID\\twitter\\{username}"

    # if path does not exists
    if not os.path.exists(path):
        os.mkdir(path)
        os.mkdir(f"{path}\\followers")
        print("Created Required directories")


def wait(secs):
    # wait for 3 mins
    print(f"waiting for {secs} secs")
    print("")
    for i in reversed(range(1, secs)):
        print(f"{i} seconds left", end="\r")
        time.sleep(1)


def create_params(fields, pagination_token):
    """ creates and returns params(parameters for a request """

    # if there is no pagination token then it is the first request
    if pagination_token is None:
        params = {"max_results": 1000, "user.fields": ','.join(fields)}
    else:
        params = {"max_results": 1000, "user.fields": ','.join(fields),
                  "pagination_token": pagination_token}
    return params


def lookup_using_bearer(username, info_path):
    """ uses Twitter API to get followers of a user using its id """

    # pagination token is required to start from where we left
    pagination_token, total_followers_retrieved, file_no = get_info(info_path)

    # getting user_id using api call
    user_id, total_followers = get_user_info(username)

    # checking directories
    check_directories(username)

    if total_followers_retrieved is None:
        total_followers_retrieved = 0
        file_no = 0

    url = f"https://api.twitter.com/2/users/{user_id}/followers"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    # required fields
    fields = ['created_at', 'description', 'entities', 'location', 'name', 'pinned_tweet_id',
              'profile_image_url', 'protected', 'public_metrics', 'url', 'username', 'verified', 'withheld']

    # continues till all followers are retrieved
    while total_followers_retrieved < total_followers:

        # getting parameters for request
        params = create_params(fields, pagination_token)

        response = requests.get(url, headers=headers, params=params)
        try:
            # converting reponse to json object
            response = response.json()
            print(response)
        except Exception as e:
            print(str(e))
            print(response.content)
            # waiting fro 200 secs
            wait(200)

        else:
            # getting data
            data = get_data(response)

            # next_token will be changing every time
            pagination_token = response['meta']['next_token']
            print(pagination_token)

            total_followers_retrieved += response['meta']['result_count']

            print("____________________________________________________________________________")
            print(f"No of Followers Retrieved: {total_followers_retrieved}")
            print(f"{int((total_followers_retrieved / total_followers)) * 100}% Completed...")
            print("____________________________________________________________________________")


            path = f"D:\\Huzaifa\\ai\\AI\\COVID\\twitter\\{username}\\followers\\followers{file_no}.csv"
            try:
                # maximum of 40000 rows in a single csv file
                if 39000 < pd.read_csv(path).shape[0] < 40000:
                    file_no += 1
            except FileNotFoundError:
                pass

            # writing info for future use
            save_info(info_path, pagination_token, total_followers_retrieved, file_no)

            # save data after every iteration into a csv file
            save_data(data, path)


def save_data(data, path):
    """ function to save data to a file """
    df = pd.DataFrame(data, columns=['id', 'name', 'username', 'location', 'created_at', 'followers_count',
                                     'following_count', 'tweet_count', 'is_verified', 'protected'])

    # error checking
    try:
        # append if csv already exists
        df.to_csv(path_or_buf=path, mode='a', header=not os.path.exists(path))
    except Exception as e:
        print(str(e))
    else:
        print(f"Saved Dataframe to {path}")


def main():
    username = ""
    info_path = f""

    lookup_using_bearer(username, info_path)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 1:
        sys.exit("Usage: python followers_lookup.py")
    main()

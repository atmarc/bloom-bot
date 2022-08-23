import requests
import schedule
import time
import os
import json

LAST_TWEET = 0

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

# print(bearer_token)
def create_url(user_id, last_tweet):
    # Replace with user ID below
    
    return f"https://api.twitter.com/2/users/{user_id}/mentions/?since_id={last_tweet}"


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserMentionsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def routine():
    global LAST_TWEET
    print(LAST_TWEET)
    user_id = 901746159361957888
    url = create_url(user_id, LAST_TWEET)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    if json_response['meta']['result_count'] > 0:
        LAST_TWEET = json_response['meta']['newest_id']
        for tweet in json_response['data']:
            # call model
            print(tweet['text'])


def main():
    # every 10 secs
    schedule.every(3).seconds.do(routine)
    while True:
        schedule.run_pending()
        time.sleep(1)
    


if __name__ == "__main__":

    main()
    

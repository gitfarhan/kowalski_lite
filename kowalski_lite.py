from text_mining import TextCleaner
import tweepy
import click
from dotenv import load_dotenv
from tweepy.error import TweepError
import os
import pandas as pd
from datetime import datetime
load_dotenv()


consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


def collection(top_words_df):
    if os.path.exists('collection.csv'):
        col = pd.read_csv('collection.csv')
        col = pd.concat([col, top_words_df], axis=0)
        col.to_csv('collection.csv', index=False)
    else:
        top_words_df.to_csv('collection.csv', index=False)


def get_top_words(user_name, min_freq=1):
    print(f"tweet summary for @{user_name}:")
    # collecting tweets
    try:
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        user_tweets = api.user_timeline(screen_name=user_name, count=100)
    except TweepError as e:
        error_code = eval(str(e))[0]['code']
        if str(error_code) == '34':
            print('page does not exist')
            return None
        else:
            raise TweepError(e)

    all_tweets = []
    for i in user_tweets:
        status = api.get_status(i.id, tweet_mode="extended")
        text = status.full_text
        text = " ".join(list(set(text.split())))
        all_tweets.append(text)

    all_tweets = " ".join(all_tweets)
    all_tweets = " ".join([i for i in all_tweets.split() if '@' not in i])
    all_tweets = " ".join([i for i in all_tweets.split() if '_' not in i])

    # text cleaning
    cleaner = TextCleaner()
    clean_df = cleaner.get_clean_text(text=all_tweets)
    clean_df = clean_df[clean_df['count'] > min_freq]
    clean_df = clean_df.head(10)
    clean_df['username'] = user_name

    # add time
    today = datetime.now()
    date = f"{today.year}{today.strftime('%m')}{today.strftime('%d')}"
    time = f"{today.hour:02d}:{today.minute:02d}"
    clean_df['report_date'] = date
    clean_df['time'] = time

    return clean_df

@click.command()
@click.option('--username', '-u')
def main(username):
    top_words = get_top_words(user_name=username)
    collection(top_words_df=top_words)
    click.echo(top_words)

if __name__ == '__main__':
    main()
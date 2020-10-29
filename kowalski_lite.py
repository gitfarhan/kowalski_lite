from text_mining import TextCleaner
import tweepy
import click
from dotenv import load_dotenv
import os
load_dotenv()


consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


def get_top_words(user_name, min_freq=1):
    print(f"tweet summary for {user_name}:")
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user_tweets = api.user_timeline(screen_name=user_name, count=100)
    all_tweets = []
    for i in user_tweets:
        status = api.get_status(i.id, tweet_mode="extended")
        text = status.full_text
        text = " ".join(list(set(text.split())))
        all_tweets.append(text)

    all_tweets = " ".join(all_tweets)
    all_tweets = " ".join([i for i in all_tweets.split() if '@' not in i])
    all_tweets = " ".join([i for i in all_tweets.split() if '_' not in i])

    cleaner = TextCleaner()
    clean_df = cleaner.get_clean_text(text=all_tweets)
    clean_df = clean_df[clean_df['count'] > min_freq]

    return clean_df.head(10)

@click.command()
@click.option('--username', '-u')
def main(username):
    click.echo(get_top_words(user_name=username))

if __name__ == '__main__':
    main()
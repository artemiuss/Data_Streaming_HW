#!/usr/bin/env python3
import praw, random
from langdetect import detect
from iso639 import languages
from multi_rake import Rake
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def main():
    """
    The Main
    """
    reddit = praw.Reddit(
        client_id = "akSgjjdnVqB57EIDMMvSTw",
        client_secret = "pBMc9cndlNkmJqyDWyTyXGaJXwcsTQ",
        #password = "1",
        user_agent = "test /u/Brilliant_Cup_3679",
        username = "Brilliant_Cup_3679",
    )

    rake = Rake()

    nltk.download('vader_lexicon')
    # Initialize the sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    while True:
        try:
            comments = reddit.random_subreddit().comments(limit=25)
            comments_list = list(comments)
            random_comment = random.choice(comments_list)
            #print(random_comment)
            print(random_comment.body)
            #print(random_comment.controversiality)
            #print(random_comment.score)
            #print(random_comment.polarity)
            detect_result = detect(random_comment.body)
            detect_result = languages.get(part1=detect_result)
            #print(detect_result.name)
            if detect_result.name != "English":
                print(detect_result.name)
            
            keywords = rake.apply(random_comment.body)
            print(f"keywords= {keywords[:10]}")

            # Analyze sentiment
            sentiment_scores = sid.polarity_scores(random_comment.body)
            print(f"sentiment_scores= {sentiment_scores}")
            
            # Determine if the sentiment is positive or negative based on the compound score
            if sentiment_scores['compound'] >= 0.05:
                print("Positive sentiment")
            elif sentiment_scores['compound'] <= -0.05:
                print("Negative sentiment")
            else:
                print("Neutral sentiment")

        except Exception as e:
            pass

if __name__ == '__main__':
    main()

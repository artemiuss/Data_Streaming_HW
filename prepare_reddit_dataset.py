#!/usr/bin/env python3
import praw, random
from langdetect import detect
from iso639 import languages

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

    while True:
        try:
            comments = reddit.random_subreddit().comments(limit=25)
            comments_list = list(comments)
            random_comment = random.choice(comments_list)
            print(random_comment)
            detect_result = detect(random_comment.body)
            detect_result = languages.get(part1=detect_result)
            print(detect_result.name)
        except Exception as e:
            pass

# TODO
# Sentiment Analysis
# Keyword Analysis

if __name__ == '__main__':
    main()

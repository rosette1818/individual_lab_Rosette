#!/usr/bin/python3
"""
data-detective.py

Lab 2: The Social Media Data Detective.

Reads a messy Twitter-style CSV dataset and offers a menu so you can
run each quest on its own:
1. Clean the data (handle missing Text/Likes/Retweets).
2. Find the tweet with the most Likes (no max()).
3. Sort all tweets by Likes, descending (no .sort()/sorted()).
4. Search tweets for a keyword and extract matches.

No .sort(), sorted(), or max() are used anywhere in this file.
"""
import csv
import sys
import os
import time
import threading


def load_raw_data(filename):
    """
    Loads the CSV file into a list of dictionaries exactly as it is (messy).
    """
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    raw_tweets = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            raw_tweets.append(row)

    return raw_tweets


def clean_data(tweets):
    """
    QUEST 1: Handle missing fields.
    Check for missing text, and replace empty likes/retweets with 0.
    Return a clean list of tweets.
    """
    clean_tweets = []
    fixed_count = 0
    removed_count = 0

    for tweet in tweets:
        text = tweet.get('Text')

        # Drop rows that have no tweet text at all.
        if text is None or text.strip() == '':
            removed_count += 1
            continue

        row_was_fixed = False

        # Replace missing/blank Likes with 0.
        likes = tweet.get('Likes', '')
        if likes is None or str(likes).strip() == '':
            tweet['Likes'] = 0
            row_was_fixed = True
        else:
            tweet['Likes'] = int(likes)

        # Replace missing/blank Retweets with 0.
        retweets = tweet.get('Retweets', '')
        if retweets is None or str(retweets).strip() == '':
            tweet['Retweets'] = 0
            row_was_fixed = True
        else:
            tweet['Retweets'] = int(retweets)

        if row_was_fixed:
            fixed_count += 1

        clean_tweets.append(tweet)

    print(f"Data Audit Complete: {removed_count} row(s) removed "
          f"(missing text), {fixed_count} row(s) fixed "
          f"(missing likes/retweets).")

    return clean_tweets


def find_viral_tweet(tweets):
    """
    QUEST 2: Loop through the list to find the tweet with the highest
    'Likes'. Do not use the max() function.
    """
    if not tweets:
        print("No tweets available to search.")
        return None

    top_tweet = tweets[0]

    for tweet in tweets:
        if tweet['Likes'] > top_tweet['Likes']:
            top_tweet = tweet

    print("\n--- Most Viral Tweet ---")
    print(f"Username: {top_tweet['Username']}")
    print(f"Likes: {top_tweet['Likes']}")
    print(f"Text: {top_tweet['Text']}")

    return top_tweet


def custom_sort_by_likes(tweets):
    """
    QUEST 3: Selection Sort by 'Likes', descending. NO .sort()/sorted()
    allowed! The sort runs on a background thread so the main thread
    can print a friendly status message every ~3 seconds while it works.
    """
    sorted_tweets = tweets.copy()
    n = len(sorted_tweets)

    # Shared progress counter the sort thread updates and the main
    # thread reads every few seconds. A single-item list is enough
    # here since only one thread ever writes to it.
    progress = [0]

    def do_sort():
        for i in range(n):
            max_index = i
            for j in range(i + 1, n):
                if sorted_tweets[j]['Likes'] > sorted_tweets[max_index]['Likes']:
                    max_index = j
            sorted_tweets[i], sorted_tweets[max_index] = (
                sorted_tweets[max_index], sorted_tweets[i]
            )
            progress[0] = i + 1

    messages = ["Still sorting through the tweets, thanks for hanging in there.🙏🙏",

                "Komereza utegereze wihanganye😉😉.",

                "Selection Sort is doing its rounds, nearly there😊😊.",

                "Haracyabura gato cyane🤭🤭.",

                "Working through the pile of tweets, hang tight👌👌.",

                "Hasigaye umwanya muto gusa🫴🫴.",
    ]

    print(f"\n[Quest 3] Sorting {n:,} tweets by Likes (Selection Sort)...")
    start = time.time()

    sort_thread = threading.Thread(target=do_sort)
    sort_thread.start()

    msg_index = 0
    while sort_thread.is_alive():
        sort_thread.join(timeout=10)
        if sort_thread.is_alive():
            elapsed = int(time.time() - start)
            pct = (progress[0] / n) * 100 if n else 100
            print(f"  {messages[msg_index % len(messages)]} "
                  f"({pct:.1f}% complete, {elapsed}s elapsed)")
            msg_index += 1

    total_time = time.time() - start
    print(f"Sorting finished in {total_time:.2f} seconds!\n")

    return sorted_tweets


BLUE = "\033[94m"
RESET = "\033[0m"


def highlight_keyword(text, keyword):
    """
    Wraps every case-insensitive occurrence of `keyword` inside `text`
    with ANSI codes so it prints in blue, while keeping the tweet's
    original capitalization.
    """
    import re
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(lambda m: f"{BLUE}{m.group(0)}{RESET}", text)


def search_tweets(tweets, keyword):
    """
    QUEST 4: Search for a keyword and extract matching tweets into a
    new list.
    """
    matches = []
    keyword_lower = keyword.lower()

    for tweet in tweets:
        if keyword_lower in tweet['Text'].lower():
            matches.append(tweet)

    # Show the count first, with the search word itself in blue.
    print(f"\nFound {len(matches)} tweet(s) matching "
          f"'{BLUE}{keyword}{RESET}':\n")

    for tweet in matches:
        highlighted_text = highlight_keyword(tweet['Text'], keyword)
        print(f"- {tweet['Username']} ({tweet['Likes']} likes): "
              f"{highlighted_text}")

    return matches


def print_menu():
    print("\n===== The Social Media Data Detective =====")
    print("1. Quest 1 - Data Audit (clean the data)")
    print("2. Quest 2 - Find the most viral tweet")
    print("3. Quest 3 - Sort tweets by Likes (Top 10)")
    print("4. Quest 4 - Search tweets by keyword")
    print("5. Exit")


if __name__ == "__main__":
    print("Loading twitter_dataset.csv ...")
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets.")

    # Data must be cleaned before Quests 2-4 can trust the Likes/Retweets
    # values, so we clean it once up front, then let the menu control
    # which quest to *display*.
    clean_dataset = clean_data(dataset)

    while True:
        print_menu()
        choice = input("Choose a quest (1-5): ").strip()

        if choice == "1":
            print("\n--- Quest 1: Data Audit ---")
            print(f"{len(clean_dataset)} tweets remain after cleaning.")

        elif choice == "2":
            print("\n--- Quest 2: The Viral Post ---")
            find_viral_tweet(clean_dataset)

        elif choice == "3":
            print("\n--- Quest 3: The Algorithm Builder ---")
            top_tweets = custom_sort_by_likes(clean_dataset)
            print("--- Top 10 Most Liked Tweets ---")
            for i, tweet in enumerate(top_tweets[:10], start=1):
                print(f"{i}. {tweet['Username']} - {tweet['Likes']} likes")

        elif choice == "4":
            print("\n--- Quest 4: The Content Filter ---")
            search_word = input("Enter a keyword to search tweets for: ").strip()
            if search_word:
                search_tweets(clean_dataset, search_word)
            else:
                print("No keyword entered, skipping search.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Please enter a number from 1 to 5.")

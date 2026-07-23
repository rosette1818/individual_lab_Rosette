# Lab 2: The Social Media Data Detective

## Files
- `data-detective.py` — interactive menu that cleans, analyzes, sorts, and searches the tweet dataset.
- `feed-analyzer.sh` — Bash pipeline that prints the Top 5 Most Active Users.
- `twitter_dataset.csv` — the dataset used for testing.

## Requirements
- Python 3
- Bash (Linux/macOS/WSL)
- A terminal that supports ANSI colors (most do) — needed to see the blue keyword highlighting in Quest 4.

## Running the Python script
```bash
python3 data-detective.py
```
It will:
1. Load `twitter_dataset.csv` (must be in the same folder).
2. Clean the data automatically — report rows removed (missing Text) and rows fixed (missing Likes/Retweets).
3. Show a menu so you can run each quest on its own:
   ```
   ===== The Social Media Data Detective =====
   1. Quest 1 - Data Audit (clean the data)
   2. Quest 2 - Find the most viral tweet
   3. Quest 3 - Sort tweets by Likes (Top 10)
   4. Quest 4 - Search tweets by keyword
   5. Exit
   ```

### Quest 1 — Data Audit
Shows how many tweets remain after cleaning (rows with missing Text removed, missing Likes/Retweets zero-filled).

### Quest 2 — The Viral Post
Prints the single tweet with the highest Likes (found with a manual loop, no `max()`).

### Quest 3 — The Algorithm Builder
Sorts all tweets by Likes, descending, using a hand-written **Selection Sort** (no `.sort()`/`sorted()`). Since this is O(n²) over 10,000 tweets, it runs on a background thread while the main thread prints a friendly status message roughly every 3 seconds, including live progress:
```
[Quest 3] Sorting 10,000 tweets by Likes (Selection Sort)...
  Still sorting through the tweets, thanks for hanging in there. (47.2% complete, 3s elapsed)
Sorting finished in 4.40 seconds!
```
Once done, it prints the Top 10 most-liked tweets.

### Quest 4 — The Content Filter
Prompts for a keyword, then:
1. Prints the match count first, with the keyword itself shown in blue.
2. Lists every matching tweet, with each occurrence of the keyword highlighted in blue inside the tweet text.

Example:
```
Found 342 tweet(s) matching 'party':

- julie81 (25 likes): Party least receive say or single. ...
```
(In a real terminal, "party"/"Party" appears in blue both in the count line and inside the tweet text.)

## Running the Bash script
```bash
chmod +x feed-analyzer.sh
./feed-analyzer.sh twitter_dataset.csv
```
Prints the Top 5 Most Active Users (by tweet count)..

# Lab 2: The Social Media Data Detective

## Files
- `data-detective.py` — cleans, analyzes, sorts, and searches the tweet dataset.
- `feed-analyzer.sh` — Bash pipeline that prints the Top 5 Most Active Users.
- `twitter_dataset.csv` — the dataset used for testing.

## Requirements
- Python 3
- Bash (Linux/macOS/WSL)

## Running the Python script
```bash
python3 data-detective.py
```
It will:
1. Load `twitter_dataset.csv` (must be in the same folder).
2. Clean the data — report rows removed (missing Text) and rows fixed (missing Likes/Retweets).
3. Print the single most-viral tweet.
4. Print the Top 10 most-liked tweets (sorted with a hand-written Selection Sort — no `.sort()`/`sorted()`/`max()` used).
5. Prompt you for a keyword and print every tweet whose Text contains it.

## Running the Bash script
```bash
chmod +x feed-analyzer.sh
./feed-analyzer.sh twitter_dataset.csv
```
Prints the Top 5 Most Active Users (by tweet count).

**Note on the pipeline:** some Tweet Text fields contain line breaks inside
quotes, so a plain `cut -d','` on raw file lines would grab the wrong
column. The script first pulls out just the `Username` field with Python's
`csv` module (which correctly understands quoted, multi-line fields), then
feeds that clean one-username-per-line list into the classic
`sort | uniq -c | sort -nr | head` pipeline.

## Custom sort explanation
`custom_sort_by_likes` uses **Selection Sort**: for each position `i` in the
list, it scans the remaining unsorted items to find the one with the
highest `Likes`, then swaps it into position `i`. Repeating this for every
position produces a fully descending-by-Likes list without ever calling
`.sort()` or `sorted()`.

#!/bin/bash
# organizer.sh
# Umufasha w'inyandiko / The grade file organizer.
# Archives the current grades.csv with a timestamp, resets a fresh
# grades.csv for the next batch, and logs every run to organizer.log.

ARCHIVE_DIR="archive"
SOURCE_FILE="grades.csv"
LOG_FILE="organizer.log"

# 1. Make sure the archive directory exists / Kurema dosiye "archive" niba idahari
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archive directory / Twaremye dosiye 'archive'."
fi

# 2. Check the source file actually exists before doing anything
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found. Nothing to archive. / Ntabwo dosiye ibonetse."
    exit 1
fi

# 3. Generate a timestamp string (e.g. 20260721-143005)
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# 4. Build the new archived filename and move the file there.
#    Guard against two runs in the same second overwriting each other
#    by appending a counter suffix if that name is already taken.
NEW_NAME="grades_${TIMESTAMP}.csv"
COUNTER=1
while [ -f "$ARCHIVE_DIR/$NEW_NAME" ]; do
    NEW_NAME="grades_${TIMESTAMP}_${COUNTER}.csv"
    COUNTER=$((COUNTER + 1))
done

mv "$SOURCE_FILE" "$ARCHIVE_DIR/$NEW_NAME"
echo "Archived '$SOURCE_FILE' as '$ARCHIVE_DIR/$NEW_NAME'."

# 5. Reset the workspace: create a fresh, empty grades.csv
touch "$SOURCE_FILE"
echo "Created a fresh, empty '$SOURCE_FILE' for the next batch. / Twiteguye itsinda rikurikira."

# 6. Log the operation (append, so history accumulates across runs)
echo "${TIMESTAMP} | original: ${SOURCE_FILE} | archived_as: ${ARCHIVE_DIR}/${NEW_NAME}" >> "$LOG_FILE"
echo "Logged this run to '$LOG_FILE'. / Byanditswe muri organizer.log."

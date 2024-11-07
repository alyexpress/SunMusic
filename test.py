from database import db

with open("/Users/igor_alymov/Downloads/Michael_Jackson_-_Earth_Song_35137997.mp3", 'rb') as file:
    data = file.read()

query = """
UPDATE music
SET file = ?
WHERE title = 'Earth Song'
"""
db.cur.execute(query, (data,))
db.db.commit()
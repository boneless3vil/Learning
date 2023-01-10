# make_album_mine.py
# Python crash course, 2nd edition
# here, I tried to do exercise chapter 8-7, but added inputs, so I can build
# the dictionary from scratch... It doesn't seem to work just yet

def make_album(artist, title, year):
    """ assigns artist, album to dictionary"""
    album = {
        'artist': artist.title(),
        'title': title.title()}
    if year:
        album['year'] = year
    return album

# organize inputs or whatever
print("\nAdd an Album to the Dictionary")
print("(enter 'q' at any time to quit)")

# while loop
while True:
    artist = input("\nArtist: ")
    if artist == 'q':
        break
    title = input("Album: ")
    if title == 'q':
        break
    year = input("Year: ")
    if year == 'q':
        break

# album_d = make_album()
    total = make_album(artist, title, year)
    print(total)

print("\nEnjoy your albums!")
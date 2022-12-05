# make_album_mine.py
# Python crash course, 2nd edition
# here, I tried to do exercise chapter 8-7, but added inputs, so I can build
# the dictionary from scratch... It doesn't seem to work just yet

def make_album(artist='', title='', year=''):
    """ assigns artist, album to dictionary"""
    album = {
        'artist': artist,
        'title': title}
    if year:
        album['year'] = year
    return album

while True:
    print("\nAdd an Album to the Dictionary")
    print("(enter 'q' at any time to quit)")
    artist_n = input("Artist: ")
    if artist_n == 'q':
        break
    title_n = input("Album: ")
    if title_n == 'q':
        break
    year_n = input("Year: ")
    if year_n == 'q':
        break

# album_d = make_album()
print(make_album)
"""
total = make_album('sting', 'englishman in new york', '1988')
print(total)
total = make_album('inxs', 'listen like thieves', ' 1986')
print(total)
total = make_album('depeche mode', 'music for the masses', '1987')
print(total)
"""
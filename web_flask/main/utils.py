from web_flask.models import Artwork

def search_artworks_by_title(query):
    artworks = Artwork.query.all()
    return [artwork for artwork in artworks if query.lower() in artwork.title.lower()]
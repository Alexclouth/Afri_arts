from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from web_flask import db
from flask_login import current_user
from web_flask.models import Artwork, Comment
from web_flask.main.utils import search_artworks_by_title

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    artwork = Artwork.query.order_by(Artwork.date_posted.desc()).all()

    comment_counts = {}
    like_counts = {}
    user_liked = {}

    for art in artwork:
        # Count the number of comments for the current artwork
        comment_count = Comment.query.filter_by(artwork_id=art.id).count()
        comment_counts[art.id] = comment_count

        # Count the number of likes for the current artwork
        like_count = art.liked_by.count()
        like_counts[art.id] = like_count

        # Check if the current user has liked this artwork
        if current_user.is_authenticated:
            user_liked[art.id] = current_user in art.liked_by
        else:
            user_liked[art.id] = False

    return render_template('home.html', artwork=artwork, comment_counts=comment_counts, like_counts=like_counts, user_liked=user_liked)

@main.route("/like_toggle", methods=["POST"])
def like_toggle():
    artwork_id = request.json.get("artwork_id")
    artwork = Artwork.query.get_or_404(artwork_id)

    if not current_user.is_authenticated:
        # User not logged in, send redirect response
        return jsonify({"redirect": url_for('users.signin')}), 401

    if current_user in artwork.liked_by:
        artwork.liked_by.remove(current_user)
        liked = False
    else:
        artwork.liked_by.append(current_user)
        liked = True

    db.session.commit()

    return jsonify({
        "liked": liked,
        "like_count": artwork.liked_by.count()
    })

@main.route("/about")
def about():
    return render_template('about.html')


def search_artworks_by_title(query):
    artworks = Artwork.query.all()
    return [artwork for artwork in artworks if query.lower() in artwork.title.lower()]


@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    if query:
        artworks = search_artworks_by_title(query)
        
        if artworks:  # If results are found
            if len(artworks) == 1:
                # If only one result, redirect to that artwork
                return redirect(url_for('posts.single_post', art_id=artworks[0].id))
            else:
                artwork = artworks

                comment_counts = {}
                like_counts = {}
                user_liked = {}

                for art in artwork:
                    # Count the number of comments for the current artwork
                    comment_count = Comment.query.filter_by(artwork_id=art.id).count()
                    comment_counts[art.id] = comment_count

                    # Count the number of likes for the current artwork
                    like_count = art.liked_by.count()
                    like_counts[art.id] = like_count

                    # Check if the current user has liked this artwork
                    if current_user.is_authenticated:
                        user_liked[art.id] = current_user in art.liked_by
                    else:
                        user_liked[art.id] = False

                return render_template('search_results.html', artwork=artwork, comment_counts=comment_counts, like_counts=like_counts, user_liked=user_liked)

        else:
            # No results found
            flash('No result found!', 'failure')
            return redirect(url_for('main.home'))


<<<<<<< HEAD
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from web_flask import db
=======
from flask import render_template, url_for, flash, redirect, request, abort
from web_flask import app, db
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9
from web_flask.posts.forms import  PostForm, CommentForm
from flask_login import  current_user, login_required
from web_flask.models import Artwork, Comment
from web_flask.posts.utils import save_artwork

<<<<<<< HEAD
posts = Blueprint('posts', __name__)

@posts.route("/post", methods=['GET', 'POST'])
=======


@app.route("/post", methods=['GET', 'POST'])
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            arwork_file = save_artwork(form.image.data)
        post = Artwork(title=form.title.data,
                        description=form.description.data,
                        price=form.price.data,
                        art_type=form.art_type.data,
                        style=form.style.data,
                        image=arwork_file,
                        uploader=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Artwork has been uploaded!', 'success')
<<<<<<< HEAD
        return redirect(url_for('main.home'))
    return render_template('post.html', form=form)

@posts.route("/post/<int:art_id>", methods=['GET', 'POST'])
=======
        return redirect(url_for('home'))
    return render_template('post.html', form=form)

@app.route("/post/<int:art_id>", methods=['GET', 'POST'])
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9
@login_required
def single_post(art_id):
    post = Artwork.query.get_or_404(art_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, artwork_id=post.id)
        db.session.add(comment)
        db.session.commit()
<<<<<<< HEAD
        return redirect(url_for('posts.single_post', art_id=post.id))
=======
        return redirect(url_for('single_post', art_id=post.id))
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9
    
    # Fetch comments related to the artwork using the new backref name
    comments = Comment.query.filter_by(artwork_id=post.id).order_by(Comment.date_posted.desc()).all()
    num_comments = len(comments)

    return render_template('single_post.html', post=post, form=form, comments=comments, num_comments=num_comments)



<<<<<<< HEAD
@posts.route("/post/<int:art_id>/update", methods=['GET', 'POST'])
=======
@app.route("/post/<int:art_id>/update", methods=['GET', 'POST'])
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9
@login_required
def update_post(art_id):
    post = Artwork.query.get_or_404(art_id)
    if post.uploader != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.price = form.price.data
        post.art_type=form.art_type.data,
        post.style=form.style.data,
        db.session.commit()
        flash('Your post has been updated!', 'success')
<<<<<<< HEAD
        return redirect(url_for('main.home', art_id=post.id))
=======
        return redirect(url_for('home', art_id=post.id))
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.price.data = post.price
        form.art_type.data = post.art_type
        form.style.data = post.style
        form.image.data= post.image
        image = url_for('static', filename='artworks/' + post.image)

    return render_template('update_post.html', form=form, image=image)


<<<<<<< HEAD
@posts.route("/post/<int:art_id>/delete", methods=['POST'])
=======
@app.route("/post/<int:art_id>/delete", methods=['POST'])
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9
@login_required
def delete_post(art_id):
    post = Artwork.query.get_or_404(art_id)
    if post.uploader != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
<<<<<<< HEAD
    return redirect(url_for('main.home'))
=======
    return redirect(url_for('home'))
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9

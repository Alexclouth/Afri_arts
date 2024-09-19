from flask import render_template, url_for, flash, redirect, request, abort
from web_flask import app, db
from web_flask.posts.forms import  PostForm, CommentForm
from flask_login import  current_user, login_required
from web_flask.models import Artwork, Comment
from web_flask.posts.utils import save_artwork



@app.route("/post", methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    return render_template('post.html', form=form)

@app.route("/post/<int:art_id>", methods=['GET', 'POST'])
@login_required
def single_post(art_id):
    post = Artwork.query.get_or_404(art_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, artwork_id=post.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('single_post', art_id=post.id))
    
    # Fetch comments related to the artwork using the new backref name
    comments = Comment.query.filter_by(artwork_id=post.id).order_by(Comment.date_posted.desc()).all()
    num_comments = len(comments)

    return render_template('single_post.html', post=post, form=form, comments=comments, num_comments=num_comments)



@app.route("/post/<int:art_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('home', art_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.price.data = post.price
        form.art_type.data = post.art_type
        form.style.data = post.style
        form.image.data= post.image
        image = url_for('static', filename='artworks/' + post.image)

    return render_template('update_post.html', form=form, image=image)


@app.route("/post/<int:art_id>/delete", methods=['POST'])
@login_required
def delete_post(art_id):
    post = Artwork.query.get_or_404(art_id)
    if post.uploader != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
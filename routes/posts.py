from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Post, Comment, User
from datetime import datetime

posts_bp = Blueprint("posts", __name__)

# Список всех публикаций
@posts_bp.route("/posts")
def posts():
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("posts.html", posts=all_posts)

# Создание новой публикации (только Analyst/Admin)
@posts_bp.route("/posts/new", methods=["GET", "POST"])
def create_post():
    if "role" not in session or session["role"] not in ["analyst", "admin"]:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tag = request.form["tag"]
        author = session.get("role", "анонім")

        post = Post(
            title=title,
            content=content,
            tag=tag,
            author=author,
            created_at=datetime.utcnow()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("posts.posts"))

    return render_template("new_post.html")

# Просмотр статьи и добавление комментария
@posts_bp.route("/posts/<int:id>", methods=["GET", "POST"])
def view_post(id):
    post = Post.query.get_or_404(id)
    comments = Comment.query.filter_by(post_id=id).order_by(Comment.created_at.desc()).all()

    if request.method == "POST":
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        content = request.form["content"]
        comment = Comment(
            post_id=id,
            user_id=session["user_id"],
            content=content,
            created_at=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("posts.view_post", id=id))

    return render_template("view_post.html", post=post, comments=comments)

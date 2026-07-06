from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)

from app.extensions import oauth
from flask import url_for
from flask_login import login_user
from app.models.user import User
from app.extensions import db

from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm

from app.services.auth_service import (
    create_user,
    authenticate_user,
)

auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = authenticate_user(
            form.email.data.lower(),
            form.password.data,
        )

        if user is None:

            flash("Invalid email or password.")

            return redirect(
                url_for("auth.login")
            )

        login_user(user)

        return redirect(
            url_for("auth.dashboard")
        )

    return render_template(
        "login.html",
        form=form,
    )


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        user, error = create_user(
            form.username.data,
            form.email.data.lower(),
            form.password.data,
        )

        if error:

            flash(error)

            return redirect(
                url_for("auth.register")
            )

        flash("Account created successfully!")

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html",
        form=form,
    )


@auth_bp.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("chat.home")
    )
    
@auth_bp.route("/google")
def google_login():

    redirect_uri = url_for(
        "auth.google_callback",
        _external=True,
    )

    return oauth.google.authorize_redirect(
        redirect_uri
    )
    
@auth_bp.route("/google/callback")
def google_callback():

    token = oauth.google.authorize_access_token()

    user_info = token["userinfo"]

    user = User.query.filter_by(
    email=user_info["email"]
    ).first()

    if user is None:

        user = User(
            username=user_info["name"],
            email=user_info["email"],
            google_id=user_info["sub"],
            password_hash=None,
            profile_picture=user_info.get("picture"),
        )

        db.session.add(user)

    else:

        if not user.google_id:
            user.google_id = user_info["sub"]

        if user_info.get("picture"):
            user.profile_picture = user_info["picture"]

    db.session.commit()

    login_user(user)

    return redirect(url_for("auth.dashboard"))
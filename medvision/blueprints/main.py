from flask import Blueprint, current_app, redirect, render_template, request, session, url_for

from ..services.content import get_disease_catalog, get_system_overview


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    lang = session.get("lang", current_app.config["DEFAULT_LANGUAGE"])
    diseases = [d for d in get_disease_catalog(lang) if d["slug"] != "no-finding"][:4]
    overview = get_system_overview(lang)
    return render_template("main/index.html", featured_diseases=diseases, overview=overview)


@main_bp.route("/language/<lang>")
def set_language(lang):
    if lang in current_app.config["LANGUAGES"]:
        session["lang"] = lang
    next_url = request.args.get("next")
    return redirect(next_url or request.referrer or url_for("main.index"))

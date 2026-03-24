from flask import Blueprint, abort, current_app, render_template, request, session

from ..services.content import get_disease_by_slug, get_disease_catalog, get_system_overview


diseases_bp = Blueprint("diseases", __name__)


@diseases_bp.route("/diseases")
def index():
    lang = session.get("lang", current_app.config["DEFAULT_LANGUAGE"])
    query = request.args.get("q", "").strip().lower()
    diseases = get_disease_catalog(lang)
    if query:
        diseases = [d for d in diseases if query in d["title"].lower() or query in d["model_label"].lower()]
    overview = get_system_overview(lang)
    return render_template("diseases/index.html", diseases=diseases, overview=overview, query=query)


@diseases_bp.route("/diseases/<slug>")
def detail(slug):
    lang = session.get("lang", current_app.config["DEFAULT_LANGUAGE"])
    disease = get_disease_by_slug(slug, lang)
    if disease is None:
        abort(404)
    return render_template("diseases/detail.html", disease=disease)

"""Public and user-facing pages."""
from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import current_user, login_required

from services import openmeteo
from services.regions import get_region

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def index():
    """Landing page (logged-in users go straight to their dashboard)."""
    if current_user.is_authenticated:
        return redirect(url_for("views.dashboard"))
    return render_template("index.html")


@views_bp.route("/dashboard")
@login_required
def dashboard():
    overview = openmeteo.get_overview()
    return render_template(
        "dashboard.html", overview=overview, summary=_summarise(overview)
    )


def _summarise(overview):
    """National headline numbers derived from the region cards."""
    regions = [r for r in overview["regions"] if r.get("pm25") is not None]
    if not regions:
        return None
    return {
        "avg_pm25": round(sum(r["pm25"] for r in regions) / len(regions), 1),
        "cleanest": min(regions, key=lambda r: r["pm25"]),
        "worst": max(regions, key=lambda r: r["pm25"]),
    }


@views_bp.route("/regions/<slug>")
@login_required
def region(slug):
    reg = get_region(slug)
    if reg is None:
        abort(404)
    data = openmeteo.get_region_detail(slug)
    return render_template("region.html", region=reg, data=data)

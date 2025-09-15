import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template, redirect, make_response
from supabase import create_client, Client
from typing import Optional

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_API_KEY") 

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Flask app pointing to parent template and static folders
app = Flask(__name__, template_folder="templates", static_folder="static")

@app.get("/")
def login_page():
    user_id = request.cookies.get("user_id")
    if user_id:
        return redirect("/content")
    return render_template("login.html")

@app.get("/onboarding")
def onboarding_page():
    user_id = request.cookies.get("user_id")
    if not user_id:
        return redirect("/")
    return render_template("onboarding.html", user_id=user_id)

@app.get("/content")
def content_page():
    user_id = request.cookies.get("user_id")
    if not user_id:
        return redirect("/")
    return render_template("content.html", user_id=user_id)

@app.post("/api/login")
def api_login():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"error": "user_id required"}), 400
    user_id = data["user_id"].strip()
    if not user_id:
        return jsonify({"error": "invalid user_id"}), 400

    # Upsert user
    supabase.table("app_user").upsert({"user_id": user_id}).execute()
    # Insert first login if missing
    existing = supabase.table("session_login").select("id").eq("user_id", user_id).execute()
    if not existing.data:
        supabase.table("session_login").insert({"user_id": user_id}).execute()

    resp = make_response(jsonify({"ok": True}))
    resp.set_cookie("user_id", user_id, httponly=True, samesite="Lax", secure=False) #to see on localhost
    return resp

@app.post("/api/visit-start")
def visit_start():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"error": "user_id required"}), 400
    user_id = data["user_id"].strip()
    if not user_id:
        return jsonify({"error": "invalid user_id"}), 400

    res = supabase.table("visit").insert({"user_id": user_id}).execute()
    visit_id = res.data[0]["id"] if res.data else None
    return jsonify({"visit_id": visit_id})

@app.post("/api/visit-end")
def visit_end():
    data = request.get_json(silent=True)
    if not data:
        data = request.form.to_dict()

    user_id = (data.get("user_id") or "").strip()
    if not user_id:
        return jsonify({"error": "invalid user_id"}), 400

    visit_id = data.get("visit_id")
    started_at = data.get("started_at")

    now = datetime.now(timezone.utc)
    duration = None
    started_dt = None
    if started_at:
        try:
            started_dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
            duration = int((now - started_dt).total_seconds())
        except ValueError:
            started_dt = None

    if visit_id:
        supabase.table("visit").update({
            "ended_at": now.isoformat(),
            "duration_seconds": duration
        }).eq("id", visit_id).execute()
    else:
        supabase.table("visit").insert({
            "user_id": user_id,
            "started_at": started_dt.isoformat() if started_dt else now.isoformat(),
            "ended_at": now.isoformat(),
            "duration_seconds": duration
        }).execute()

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)

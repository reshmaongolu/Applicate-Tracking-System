from flask import Flask, render_template, request, redirect, url_for, flash

from .services import ATSService

app = Flask(__name__)
app.secret_key = "change-me-to-a-secure-random-key"


def get_service() -> ATSService:
    return ATSService()


@app.route("/")
def index():
    service = get_service()
    return render_template(
        "index.html",
        candidates=service.list_candidates(),
        jobs=service.list_jobs(),
        applications=service.list_applications(),
    )


@app.route("/candidates")
def candidates():
    service = get_service()
    return render_template("candidates.html", candidates=service.list_candidates())


@app.route("/jobs")
def jobs():
    service = get_service()
    return render_template("jobs.html", jobs=service.list_jobs())


@app.route("/applications")
def applications():
    service = get_service()
    return render_template("applications.html", applications=service.list_applications())


@app.route("/add-candidate", methods=("GET", "POST"))
def add_candidate():
    service = get_service()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        skills = [skill.strip() for skill in request.form.get("skills", "").split(",") if skill.strip()]

        if not name or not email:
            flash("Name and email are required.", "error")
        else:
            service.add_candidate(name, email, skills)
            flash("Candidate created successfully!", "success")
            return redirect(url_for("candidates"))

    return render_template("add_candidate.html")


@app.route("/add-job", methods=("GET", "POST"))
def add_job():
    service = get_service()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        department = request.form.get("department", "").strip()
        location = request.form.get("location", "Remote").strip() or "Remote"

        if not title or not department:
            flash("Title and department are required.", "error")
        else:
            service.add_job(title, department, location)
            flash("Job created successfully!", "success")
            return redirect(url_for("jobs"))

    return render_template("add_job.html")


@app.route("/submit-application", methods=("GET", "POST"))
def submit_application():
    service = get_service()
    candidates = service.list_candidates()
    jobs = service.list_jobs()

    if request.method == "POST":
        candidate_id = request.form.get("candidate_id")
        job_id = request.form.get("job_id")

        if not candidate_id or not job_id:
            flash("Both candidate and job selection are required.", "error")
        else:
            service.submit_application(int(candidate_id), int(job_id))
            flash("Application submitted successfully!", "success")
            return redirect(url_for("applications"))

    return render_template("submit_application.html", candidates=candidates, jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)

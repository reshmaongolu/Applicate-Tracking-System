import click

from .services import ATSService

@click.group()
@click.option("--db-path", default=None, help="Path to SQLite database file.")
@click.pass_context
def cli(ctx: click.Context, db_path: str) -> None:
    """Applicant Tracking System CLI."""
    ctx.obj = ATSService() if db_path is None else ATSService()

@cli.command("add-candidate")
@click.option("--name", prompt=True, help="Candidate full name.")
@click.option("--email", prompt=True, help="Candidate email address.")
@click.option("--skills", multiple=True, help="Candidate skills; repeat the option to add more.")
def add_candidate(name: str, email: str, skills: tuple[str, ...]) -> None:
    service = ATSService()
    candidate = service.add_candidate(name, email, list(skills))
    click.echo(f"Candidate added: {candidate.id} - {candidate.name}")

@cli.command("add-job")
@click.option("--title", prompt=True, help="Job title.")
@click.option("--department", prompt=True, help="Job department.")
@click.option("--location", default="Remote", help="Job location.")
def add_job(title: str, department: str, location: str) -> None:
    service = ATSService()
    job = service.add_job(title, department, location)
    click.echo(f"Job added: {job.id} - {job.title} ({job.department})")

@cli.command("submit-application")
@click.option("--candidate-id", type=int, prompt=True, help="Candidate ID.")
@click.option("--job-id", type=int, prompt=True, help="Job ID.")
def submit_application(candidate_id: int, job_id: int) -> None:
    service = ATSService()
    application = service.submit_application(candidate_id, job_id)
    click.echo(f"Application submitted: {application.id} for candidate {candidate_id} to job {job_id}")

@cli.command("list-candidates")
def list_candidates() -> None:
    service = ATSService()
    candidates = service.list_candidates()
    for candidate in candidates:
        click.echo(f"{candidate.id}: {candidate.name} <{candidate.email}> | Skills: {', '.join(candidate.skills)}")

@cli.command("list-jobs")
def list_jobs() -> None:
    service = ATSService()
    jobs = service.list_jobs()
    for job in jobs:
        click.echo(f"{job.id}: {job.title} - {job.department} ({job.location})")

@cli.command("list-applications")
def list_applications() -> None:
    service = ATSService()
    applications = service.list_applications()
    for application in applications:
        click.echo(f"{application.id}: Candidate {application.candidate_id} -> Job {application.job_id} | Status: {application.status}")

@cli.command("search-candidates")
@click.argument("query")
def search_candidates(query: str) -> None:
    service = ATSService()
    candidates = service.search_candidates(query)
    for candidate in candidates:
        click.echo(f"{candidate.id}: {candidate.name} <{candidate.email}> | Skills: {', '.join(candidate.skills)}")

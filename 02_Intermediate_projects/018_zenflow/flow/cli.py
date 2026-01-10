import click
from .organizer import run_organizer
from .scheduler import start_scheduler
from .organizer import run_organizer, run_undo 

@click.group()
def entry_point():
    """ZenFlow: Your CLI Productivity Assistant"""
    pass

@entry_point.command()
@click.option('--dry-run', is_flag=True, help="See what would happen.")
def organize(dry_run):
    """Clean up your configured folders."""
    run_organizer(dry_run=dry_run)

@entry_point.command()
def schedule():
    """Start the reminder scheduler."""
    click.echo("Starting scheduler (Press Ctrl+C to stop)...")
    start_scheduler()

@entry_point.command()
def undo():
    """Undo the last organization action."""
    run_undo()

if __name__ == "__main__":
    entry_point()
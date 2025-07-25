from datetime import datetime, timezone
import click

from data import (
    load_data,
    save_data,
    add_brand as data_add_brand,
    add_account as data_add_account,
    schedule_post as data_schedule_post,
    list_posts as data_list_posts,
    mark_posted,
)

@click.group()
def cli():
    """Simple social media management tool"""
    pass

@cli.group()
def brand():
    """Manage brands"""
    pass

@brand.command('add')
@click.argument('name')
def add_brand(name):
    """Add a brand"""
    if data_add_brand(name):
        click.echo(f"Added brand {name}")
    else:
        click.echo("Brand already exists")

@cli.group()
def account():
    """Manage accounts"""
    pass

@account.command('add')
@click.argument('brand')
@click.argument('platform')
@click.argument('username')
def add_account(brand, platform, username):
    """Add an account to a brand"""
    if data_add_account(brand, platform, username):
        click.echo(f"Added {username} on {platform} to {brand}")
    else:
        click.echo("Account already exists or brand not found")

@account.command('remove')
@click.argument('brand')
@click.argument('platform')
@click.argument('username')
def remove_account(brand, platform, username):
    """Remove an account from a brand"""
    data = load_data()
    for b in data.get('brands', []):
        if b['name'] == brand and username in b.get('accounts', {}).get(platform, []):
            b['accounts'][platform].remove(username)
            save_data(data)
            click.echo(f"Removed {username} from {brand} on {platform}")
            return
    click.echo("Account not found")

@cli.group()
def post():
    """Manage posts"""
    pass

@post.command('schedule')
@click.argument('brand')
@click.argument('platform')
@click.argument('message')
@click.option('--time', 'time_str', default=None, help='Time in YYYY-mm-dd HH:MM format')
def schedule_post(brand, platform, message, time_str):
    """Schedule a post"""
    post_time = None
    if time_str:
        post_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M').isoformat()
    data_schedule_post(brand, platform, message, post_time)
    click.echo(f"Scheduled post for {brand} to {platform}")

@post.command('list')
def list_posts():
    """List scheduled posts"""
    for idx, p in enumerate(data_list_posts(), 1):
        status = 'POSTED' if p.get('posted') else 'PENDING'
        brand = p.get('brand')
        click.echo(f"{idx}. [{status}] {brand} -> {p['platform']}: {p['message']} @ {p.get('time')}")

@post.command('run')
def run_posts():
    """Run due posts"""
    data = load_data()
    now = datetime.now(timezone.utc).isoformat()
    for idx, p in enumerate(data.get('posts', [])):
        if not p.get('posted') and (p['time'] is None or p['time'] <= now):
            click.echo(f"Posting for {p['brand']} to {p['platform']}: {p['message']}")
            mark_posted(idx)

if __name__ == '__main__':
    cli()

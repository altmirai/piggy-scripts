import app.scripts.cloudhsm_mgmt_utility as CMU
import click

@click.group()
def script():
    pass

@script.command()
@click.option('-type', 'type', required=False)
def users(type):
    users = CMU.listUsers()

    click.echo(users)

@script.command()
@click.option('-cotype', 'co_type', required=True)
@click.option('-coname', 'co_username', required=True)
@click.option('-copassword', 'co_password', required=True)
@click.option('-type', 'user_type', required=True)
@click.option('-name', 'username', required=True)
@click.option('-password', 'new_password', required=True)
def change_password(co_type, co_username, co_password, user_type, username, new_password):
    resp = CMU.changePswd(
        co_type=co_type,
        co_username=co_username,
        co_password=co_password,
        user_type=user_type,
        username=username,
        new_password=new_password
    )

    click.echo(resp)

@script.command()
@click.option('-cotype', 'co_type', required=True)
@click.option('-coname', 'co_username', required=True)
@click.option('-copassword', 'co_password', required=True)
@click.option('-type', 'user_type', required=True)
@click.option('-name', 'username', required=True)
@click.option('-password', 'password', required=True)
def create_user(co_type, co_username, co_password, user_type, username, password):
    resp = CMU.createUser(
        co_type=co_type,
        co_username=co_username,
        co_password=co_password,
        user_type=user_type,
        username=username,
        password=password
    )

    click.echo(resp)



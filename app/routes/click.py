from app.controllers.activate_controller import Activate
import click


@click.group()
def script():
    pass


@script.command()
@click.option('-eniip', 'eni_ip', required=True)
@click.option('-copassword', 'crypto_officer_password', required=True)
@click.option('-cuusername', 'crypto_user_username', required=True)
@click.option('-cupassword', 'crypto_user_password', required=True)
def activate(eni_ip, crypto_officer_password, crypto_user_username, crypto_user_password):
    activate = Activate(
        eni_ip=eni_ip,
        crypto_officer_password=crypto_officer_password,
        crypto_user_username=crypto_user_username,
        crypto_user_password=crypto_user_password
    )

    activate.run()
    return

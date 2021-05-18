from app.controllers.activate_controller import Activate
import app.controllers.key_mgmt_utility_controller as kmu
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


@script.command()
@click.option('-eniip', 'eni_ip', prompt="HSM EniIp: ", required=True)
@click.option('-username', 'username', prompt="Username: ", required=True)
@click.option('-password', 'password', prompt="password: ", required=True)
@click.option('-label', 'key_label', prompt="Key label: ", required=True)
def gen_ecc_key_pair(eni_ip, username, password, key_label):

    resp = kmu.genECCKeyPair(
        username=username,
        password=password,
        key_label=key_label,
        eni_ip=eni_ip
    )
    return

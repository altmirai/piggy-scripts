from app.controllers.activate_controller import Activate
import app.controllers.key_mgmt_utility_controller as kmu
import app.scripts.cloudhsm_mgmt_utility_scripts as cmu
import click
import app.scripts.terminal_scripts as term


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


@script.command()
@click.option('-eniip', 'eni_ip', required=True)
@click.option('-username', 'username', required=True)
@click.option('-password', 'password', required=True)
@click.option('-label', 'key_label', required=True)
def gen_ecc_key_pair(eni_ip, username, password, key_label):

    resp = kmu.genECCKeyPair(
        username=username,
        password=password,
        key_label=key_label,
        eni_ip=eni_ip
    )

    click.echo(resp)


@script.command()
@click.option('-eniip', 'eni_ip', required=True)
@click.option('-username', 'username', required=True)
@click.option('-password', 'password', required=True)
@click.option('-tx', 'tx_file', required=True)
@click.option('-vkhandle', 'pub_key_handle', required=True)
@click.option('-skhandle', 'private_key_handle', required=True)
@click.option('-count', 'count', required=True)
def sign(eni_ip, username, password, tx_file, pub_key_handle, private_key_handle, count):
    resp = kmu.sign(
        eni_ip=eni_ip,
        username=username,
        password=password,
        tx_file=tx_file,
        pub_key_handle=pub_key_handle,
        private_key_handle=private_key_handle,
        count=count
    )

    click.echo(resp)


@script.command()
@click.option('-eniip', 'eni_ip', required=True)
def test(eni_ip):
    moved = term.move_customer_ca_cert()

    breakpoint()

    click.echo(moved)

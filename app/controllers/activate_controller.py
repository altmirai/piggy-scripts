import app.scripts.terminal_scripts as term
import app.scripts.cloudhsm_mgmt_utility_scripts as cmu
import os
import time


class Activate:

    def __init__(self, eni_ip, crypto_officer_password, crypto_user_username, crypto_user_password):
        self.eni_ip = eni_ip
        self.crypto_officer_password = crypto_officer_password
        self.crypto_user_username = crypto_user_username
        self.crypto_user_password = crypto_user_password

    def run(self):
        try:
            moved = term.move_customer_ca_crt()
            assert moved, 'Unable move customerCA.crt'

            configured = term.configure_cloudhsm_mgmt_utility(
                eni_ip=self.eni_ip)
            assert configured, 'Unable to configure the CloudHSM Mgmt Utility'

            test_connected = _can_connect_to_cloudhsm_mgmt_utility()
            assert test_connected, 'Unable to Connect to CloudHSM Mgmt Utility'

            connected, child = cmu.connect()
            assert connected, 'Unable to Connect to CloudHSM Mgmt Utility'

            logged_in, child = cmu.login(
                child=child,
                crypto_officer_type='PRECO',
                crypto_officer_username='admin',
                crypto_officer_password='password'
            )
            assert logged_in, 'Unable to Login to the CloudHSM Mgmt Utility'

            changed = cmu.change_user_password(
                child=child,
                user_type='PRECO',
                user_username='admin',
                user_password=self.crypto_officer_password
            )
            assert changed, 'Unable to change user password'

            created = cmu.create_user(
                crypto_officer_type="CO",
                crypto_officer_username="admin",
                crypto_officer_password=self.crypto_officer_password,
                user_type="CU",
                user_username=self.crypto_user_username,
                user_password=self.crypto_user_password
            )

            return True
        except Exception as Error:
            breakpoint()

    def _change_preco_password(self):
        cmu.change_user_password(
            crypto_officer_type='PRECO',
            crypto_officer_username='admin',
            crypto_officer_password='password',
            user_type='PRECO',
            user_username='admin',
            user_password=self.crypto_officer_password
        )
        return

    def _create_crypto_user(self):
        cmu.create_user(
            crypto_officer_type="CO",
            crypto_officer_username="admin",
            crypto_officer_password=self.crypto_officer_password,
            user_type="CU",
            user_username=self.crypto_user_username,
            user_password=self.crypto_user_password
        )

        return


def _can_connect_to_cloudhsm_mgmt_utility(count=0):
    count += 1
    connected = cmu.test_connection()
    if connected is True:
        return True
    else:
        if count > 5:
            return False
        else:
            time.sleep(1)
            return _can_connect_to_cloudhsm_mgmt_utility(count=count)


class ConnectionError(Exception):
    pass


class FileNotFoundError(Exception):
    pass


class CloudHSMMgmtUtilityConfigureError(Exception):
    pass

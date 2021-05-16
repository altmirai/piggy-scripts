import app.scripts.terminal_scripts as term
import app.scripts.cloudhsm_mgmt_utility_scripts as cmu
import os


class Activate:

    def __init__(self, eni_ip, crypto_officer_password, crypto_user_username, crypto_user_password):
        self.eni_ip = eni_ip
        self.crypto_officer_password = crypto_officer_password
        self.crypto_user_username = crypto_user_username
        self.crypto_user_password = crypto_user_password

    def run(self):
        self._move_customer_ca_crt()
        self._edit_cloudhsm_client()
        output = self._change_preco_password()
        output = self._create_crypto_user()
        return

    def _move_customer_ca_crt(self):
        if os.path.exists('/opt/cloudhsm/etc/customerCA.crt') is True:
            return
        elif os.path.exists(os.path.join(os.getcwd(), 'customerCA.crt')) is True:
            term.move_customer_ca_cert()
            while os.path.exists('/opt/cloudhsm/etc/customerCA.crt') is False:
                pass
            return
        else:
            raise Exception('customerCA.crt file not found')

    def _edit_cloudhsm_client(self):
        term.edit_cloudhsm_client(eni_ip=self.eni_ip)
        return

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

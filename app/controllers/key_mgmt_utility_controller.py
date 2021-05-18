import app.scripts.terminal_scripts as term
import app.scripts.key_mgmt_utility_scripts as kmu


def genECCKeyPair(eni_ip, username, password, key_label):

    term.configure_cloudhsm_client(eni_ip=eni_ip)
    key_handles = kmu.generate_key_pair(
        username=username, password=password, key_label=key_label)
    pub_key_handle = key_handles['public_key']
    pub_key_pem_file_name = kmu.export_public_key(
        username=username, password=password, pub_key_handle=pub_key_handle)

    breakpoint()
    return

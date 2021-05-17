import app.scripts.terminal_scripts as term
import app.scripts.key_mgmt_utility_scripts as kmu


def genECCKeyPair(eni_ip, username, password, key_label, out_file):

    term.configure_cloudhsm_client(eni_ip=eni_ip)
    breakpoint()

    resp = kmu.generate_key_pair(
        username=username, password=password, key_label=key_label, out_file=out_file)

    return resp

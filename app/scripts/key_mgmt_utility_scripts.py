import pexpect
import sys
import io
from datetime import datetime
import os


def login(username, password):
    (output, exitstatus) = pexpect.run(
        'sudo service cloudhsm-client start', withexitstatus=1)
    assert exitstatus == 0, 'sudo service cloudhsm-client start failed.'

    child = pexpect.spawn('/opt/cloudhsm/bin/key_mgmt_util')
    child.expect_exact('Command:')
    child.sendline(f'loginHSM -u CU -p {password} -s {username}')
    index = child.expect(
        ['HSM Error: RET_USER_LOGIN_FAILURE', 'HSM Return: SUCCESS'])
    if index == 0:
        child.sendline('exit')
        child.expect(pexpect.EOF)
        raise LoginHSMError(f'Username {username} login failed')
    else:
        return child


def generate_key_pair(username, password, key_label):
    log_file = _get_log_file_path(function_name='genEECKeyPair')

    child = login(username=username, password=password)
    child.logfile = open(log_file, 'wb')
    child.sendline(f'genECCKeyPair -i 16 -l {key_label}')
    child.expect('HSM Return: SUCCESS')
    child.sendline('logoutHSM')
    child.expect('Command:')
    child.sendline('exit')
    child.expect(pexpect.EOF)
    child.logfile.close()

    key_handles = _get_key_handles(log_file)
    return key_handles


def export_public_key(username, password, pub_key_handle):
    log_file = _get_log_file_path(function_name='exportPubKey')

    child = login(username=username, password=password)
    child.logfile = open(log_file, 'wb')
    child.sendline(
        f'exportPubKey -k {pub_key_handle} -out pubKey{pub_key_handle}.pem')
    child.expect('HSM Return: SUCCESS')
    child.sendline('logoutHSM')
    child.expect('Command:')
    child.sendline('exit')
    child.expect(pexpect.EOF)
    child.logfile.close()

    return f'pubKey{pub_key_handle}.pem'


def _get_key_handles(log_file):
    with open(log_file, 'rb') as file:
        output = file.read()
    output = output.decode().split()
    private_key_handle_index_start = output.index('private')
    public_key_handle_index_start = output.index('public')

    private_key_handle = output[private_key_handle_index_start + 3]
    public_key_handle = output[public_key_handle_index_start + 3]

    try:
        int(private_key_handle)
    except:
        raise KeyHandleError(
            f'Unable to locate Private Key Handle from {log_file}.')

    try:
        int(public_key_handle)
    except:
        raise KeyHandleError(
            f'Unable to locate Public Key Handle from {log_file}.')

    return {
        'public_key': public_key_handle,
        'private_key': private_key_handle
    }


def _get_log_file_path(function_name):
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S.log")
    path = os.path.join(os.getcwd(), f'{function_name}Logs')
    if os.path.isdir(path) is False:
        os.mkdir(path)
    return os.path.join(path, date_time)


class LoginHSMError(Exception):
    pass


class ECCKeyGenError(Exception):
    pass


class KeyHandleError(Exception):
    pass

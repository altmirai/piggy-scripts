import pexpect


def generate_key_pair(password, username, key_label, out_file):
    child = pexpect.spawn('/opt/cloudhsm/bin/key_mgmt_util')
    child.expect_exact('Command:')
    child.sendline(f'loginHSM -u CU -p {password} -s {username}')
    i = child.expect(
        ['HSM Error: RET_USER_LOGIN_FAILURE', 'HSM Return: SUCCESS'])
    if i == 0:
        child.sendline('exit')
        child.expect(pexpect.EOF)
        raise LoginHSMError(f'Username {username} login failed')
    elif i == 1:
        child.sendline(f'genECCKeyPair -i 16 -l {key_label}')
        i1 = child.expect(['HSM Return: SUCCESS'])
        if i1 != 0:
            child.sendline('exit')
            child.expect(pexpect.EOF)
        else:
            output = child.before
            breakpoint()


class LoginHSMError(Exception):
    pass

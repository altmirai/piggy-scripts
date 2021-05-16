import pexpect


def listUsers():
    child = pexpect.spawn('/opt/cloudhsm/bin/cloudhsm_mgmt_util /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg')
    child.expect('aws-cloudhsm>')
    child.sendline('listUsers')
    child.expect('aws-cloudhsm>')
    resp = child.before
    child.sendline('quit')

    return _user_dict(resp.decode().split())

def changePswd(co_type, co_username, co_password, user_type, username, password):
    child = pexpect.spawn('/opt/cloudhsm/bin/cloudhsm_mgmt_util /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg')
    child.expect('aws-cloudhsm>')
    child.sendline(f'loginHSM {co_type} {co_username} {co_password}')
    i = child.expect(['HSM Error', 'aws-cloudhsm>'])
    if i == 0:
        child.sendline('quit')
        child.expect(pexpect.EOF)
        raise LoginHSMError(f'Username: {co_username} login failed')
    elif i == 1:
        child.sendline(f'changePswd {user_type} {username} {new_password}')
        child.expect('Do you want to continue(y/n)?')
        child.sendline('y')
        i1 = child.expect(['Retry/Ignore/Abort?(R/I/A)', 'aws-cloudhsm>'])
        if i1 == 0:
            child.sendline('A')
            child.expect('aws-cloudhsm>')
            child.sendline('quit')
            child.expect(pexpect.EOF)
            raise ChangePasswordError(f'Change password for username: {username} failed')
        elif i1 == 1:
            resp = child.before
            child.sendline('quit')
            child.expect(pexpect.EOF)

    if 'success' in resp.decode().split():
        return ' '.join(resp.decode().split()[1:])
    else:
        raise Exception('Unspecified change password failure.')

def createUser(co_type, co_username, co_password, user_type, username, password):
    child = pexpect.spawn('/opt/cloudhsm/bin/cloudhsm_mgmt_util /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg')
    child.expect('aws-cloudhsm>')
    child.sendline(f'loginHSM {co_type} {co_username} {co_password}')
    i = child.expect(['HSM Error', 'aws-cloudhsm>'])
    if i == 0:
        child.sendline('quit')
        child.expect(pexpect.EOF)
        raise LoginHSMError(f'Username: {co_username} login failed')
    elif i == 1:
        child.sendline(f'createUser {user_type} {username} {password}')
        child.expect('Do you want to continue(y/n)?')
        child.sendline('y')
        i1 = child.expect(['Retry/Ignore/Abort?(R/I/A)', 'aws-cloudhsm>'])
        if i1 == 0:
            child.sendline('A')
            child.expect('aws-cloudhsm>')
            child.sendline('quit')
            child.expect(pexpect.EOF)
            raise ChangePasswordError(f'Create user: {username} failed')
        elif i1 == 1:
            resp = child.before
            child.sendline('quit')
            child.expect(pexpect.EOF)

    breakpoint()

    if 'success' in resp.decode().split():
        return ' '.join(resp.decode().split()[1:])
    else:
        raise Exception('Unspecified create user failure.')

def _user_dict(user_list):
    user_list = user_list[user_list.index('2FA') + 1:]
    n, users = 0, []
    for elem in user_list:
        n += 1
        mod = n % 6
        if mod == 1:
            dict = {}
            dict['id'] = elem
        elif mod == 2:
            dict['user_type'] = elem
        elif mod == 3:
            dict['username'] = elem
        elif mod == 4:
            dict['MofnPubKey'] = elem
        elif mod == 5:
            dict['LoginFailureCnt'] = elem
        elif mod == 0:
            dict['2FA'] = elem
            users.append(dict)
    return users


class LoginHSMError(Exception):
    pass

class ChangePasswordError(Exception):
    pass

import pexpect


def move_customer_ca_cert():
    (output, exitstatus) = pexpect.run(
        'sudo mv customerCA.crt /opt/cloudhsm/etc/customerCA.crt', withexitstatus=1)
    assert exitstatus == 0, 'sudo mv customerCA.crt /opt/cloudhsm/etc/customerCA.crt failed.'
    return


def edit_cloudhsm_client(eni_ip):
    (output, exitstatus) = pexpect.run(
        f'sudo /opt/cloudhsm/bin/configure -a {eni_ip}', withexitstatus=1)
    assert exitstatus == 0, f'sudo /opt/cloudhsm/bin/configure -a {eni_ip} failed.'
    return


def configure_cloudhsm_client(EniIp):
    (output, exitstatus) = pexpect.run(
        'sudo service cloudhsm-client stop', withexitstatus=1)
    assert exitstatus == 0, 'sudo service cloudhsm-client stop failed.'
    (output, exitstatus) = pexpect.run(
        f'sudo /opt/cloudhsm/bin/configure -a {EniIp}', withexitstatus=1)
    assert exitstatus == 0, f'sudo /opt/cloudhsm/bin/configure -a {EniIp} failed.'

    (output, exitstatus) = pexpect.run(
        'sudo service cloudhsm-client start', withexitstatus=1)
    assert exitstatus == 0, 'sudo service cloudhsm-client start failed.'

    (output, exitstatus) = pexpect.run(
        'sudo /opt/cloudhsm/bin/configure -m', withexitstatus=1)
    assert exitstatus == 0, 'sudo /opt/cloudhsm/bin/configure -m failed.'

    return

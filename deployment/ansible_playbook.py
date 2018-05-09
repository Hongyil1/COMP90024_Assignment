"""
===================================================
 Xiaolu Zhang 886161
 Jianbo Ma 807590
 Hongyi Lin 838776
 Xiaoyu Wang 799778
 Shalitha Weerakoon Karunatilleke 822379

 COMP90024 Cluster and Cloud Computing
 Social Media Analytics on Melbourne & Sydney
====================================================
"""

import json
import os
from tempfile import NamedTemporaryFile

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback.default import CallbackModule
from ansible.vars.manager import VariableManager

private_key_file = os.path.expanduser('~/.ssh/team56')


class Options(object):
    def __init__(self, **kwargs):

        props = (
            'ask_pass', 'ask_sudo_pass', 'ask_su_pass', 'ask_vault_pass',
            'become_ask_pass', 'become_method', 'become', 'become_user',
            'check', 'connection', 'diff', 'extra_vars', 'flush_cache',
            'force_handlers', 'forks', 'inventory', 'listhosts', 'listtags',
            'listtasks', 'module_path', 'module_paths',
            'new_vault_password_file', 'one_line', 'output_file',
            'poll_interval', 'private_key_file', 'python_interpreter',
            'remote_user', 'scp_extra_args', 'seconds', 'sftp_extra_args',
            'skip_tags', 'ssh_common_args', 'ssh_extra_args', 'subset', 'sudo',
            'sudo_user', 'syntax', 'tags', 'timeout', 'tree',
            'vault_password_files', 'verbosity')

        # set options
        for p in props:
            if p in kwargs:
                setattr(self, p, kwargs[p])
            else:
                if p == 'tags' or p == 'skip_tags':
                    setattr(self, p, [])
                else:
                    setattr(self, p, None)


class ResultCallback(CallbackModule):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        super(ResultCallback, self).v2_runner_on_ok(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))
        super(ResultCallback, self).v2_runner_on_failed(result, ignore_errors)


def run_playbook(hosts, playbook, tags=[], private_key_file=private_key_file):
    # initialize needed objects
    loader = DataLoader()
    options = Options(connection='ssh', private_key_file=private_key_file, module_path='', forks=100, become=True,
                      become_method='sudo', become_user='root', check=False, tags=tags)

    passwords = dict(vault_pass='')
    results_callback = ResultCallback()

    host_file = NamedTemporaryFile(delete=False)
    host_file.write(b'[servers]\n')
    for i, h in enumerate(hosts):
        print(i, " : ", h)
        host_file.write(bytes('{0} num={1}\n'.format(h, i), encoding='utf8'))
    host_file.close()

    # set inventory
    inventory = InventoryManager(loader=loader, sources=host_file.name)
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # setup playbook executor, before the run
    pbex = PlaybookExecutor(
        playbooks=[playbook],
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords=passwords
    )

    pbex._tqm._stdout_callback = results_callback
    # run playbook and get stats
    result = pbex.run()
    stats = pbex._tqm._stats

    outputs = {0: 'deployment successful',
               1: 'error occurred during deployment',
               2: 'one or more hosts failed',
               4: 'one or more hosts unreachable',
               255: 'unknown error occurred during deployment'
               }

    run_success = True
    hosts = sorted(stats.processed.keys())
    for h in hosts:
        t = stats.summarize(h)
        if t['unreachable'] > 0 or t['failures'] > 0:
            run_success = False

    os.remove(host_file.name)

    try:
        out = outputs[result]
    except KeyError:
        out = 'unrecognised error code'
    return result, out

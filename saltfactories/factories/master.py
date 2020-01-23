# -*- coding: utf-8 -*-
'''
saltfactories.factories.master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Master Factory
'''

# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals

# Import Salt libs
import salt.config
import salt.utils.dictupdate as dictupdate

# Import Salt Factories libs
from saltfactories.utils import compat, ports


class MasterFactory(object):
    def __init__(self, tempdir, config):
        self.tempdir = tempdir
        self.config = config

    @staticmethod
    def default_config(root_dir, master_id, default_options=None, config_overrides=None):
        if default_options is None:
            default_options = salt.config.DEFAULT_MASTER_OPTS.copy()

        root_dir = root_dir.join('masters', master_id).ensure(dir=True)
        conf_dir = root_dir.join('conf').ensure(dir=True)
        conf_file = conf_dir.join('master').strpath
        state_tree_root = root_dir.join('state-tree').ensure(dir=True)
        state_tree_root_base = state_tree_root.join('base').ensure(dir=True).strpath
        state_tree_root_prod = state_tree_root.join('prod').ensure(dir=True).strpath
        pillar_tree_root = root_dir.join('pillar-tree').ensure(dir=True)
        pillar_tree_root_base = pillar_tree_root.join('base').ensure(dir=True).strpath
        pillar_tree_root_prod = pillar_tree_root.join('prod').ensure(dir=True).strpath

        stop_sending_events_file = conf_dir.join('stop-sending-events-{}'.format(master_id)).strpath
        with compat.fopen(stop_sending_events_file, 'w') as wfh:
            wfh.write('')

        _default_options = {
            'id': master_id,
            'conf_file': conf_file,
            'root_dir': root_dir.strpath,
            'interface': '127.0.0.1',
            'publish_port': ports.get_unused_localhost_port(),
            'ret_port': ports.get_unused_localhost_port(),
            'tcp_master_pub_port': ports.get_unused_localhost_port(),
            'tcp_master_pull_port': ports.get_unused_localhost_port(),
            'tcp_master_publish_pull': ports.get_unused_localhost_port(),
            'tcp_master_workers': ports.get_unused_localhost_port(),
            'worker_threads': 3,
            'pidfile': 'run/master.pid',
            'pki_dir': 'pki',
            'cachedir': 'cache',
            'timeout': 3,
            'sock_dir': '.salt-unix',
            'open_mode': True,
            'syndic_master': 'localhost',
            'fileserver_list_cache_time': 0,
            'fileserver_backend': ['roots'],
            'pillar_opts': False,
            'peer': {'.*': ['test.*']},
            'log_file': 'logs/master.log',
            'log_level_logfile': 'debug',
            'key_logfile': 'logs/key.log',
            'token_dir': 'tokens',
            'token_file': root_dir.join('ksfjhdgiuebfgnkefvsikhfjdgvkjahcsidk').strpath,
            'file_buffer_size': 8192,
            'log_fmt_console': '[%(levelname)-8s][%(name)-5s:%(lineno)-4d] %(message)s',
            'log_fmt_logfile': '[%(asctime)s,%(msecs)03.0f][%(name)-5s:%(lineno)-4d][%(levelname)-8s] %(message)s',
            'file_roots': {'base': state_tree_root_base, 'prod': state_tree_root_prod},
            'pillar_roots': {'base': pillar_tree_root_base, 'prod': pillar_tree_root_prod},
            'hash_type': 'sha256',
            'transport': 'zeromq',
            'pytest': {
                'log': {'prefix': 'salt-master({})'.format(master_id)},
                'engine': {
                    'port': ports.get_unused_localhost_port(),
                    'stop_sending_events_file': stop_sending_events_file,
                    #'events': ['pytest/master/{}/start'.format(master_id)],
                },
            },
        }
        for varname in ('sock_dir',):
            # These are settings which are tested against and provided by Salt's test suite, so,
            # let's not override them if provided
            if varname in default_options:
                _default_options.pop(varname)
        # Merge in the initial default options with the internal _default_options
        dictupdate.update(default_options, _default_options, merge_lists=True)

        if config_overrides:
            # Merge in the default options with the master_config_overrides
            dictupdate.update(default_options, config_overrides, merge_lists=True)

        return default_options
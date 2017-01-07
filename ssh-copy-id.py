# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 16:12:44 2017

@author: Zhengyi
"""

import os
import sys
import argparse
from getpass import getuser

try:
    from fabric.api import settings, hide, run, execute
except ImportError:
    print ("ERROR: fabric libraries not present.")
    print ("run 'pip install fabric' to fix")
    sys.exit(1)


class DeployKey():

    def __init__(self, hostname, username=None, password=None, port=22,
                 local_key_path=None, remote_key_path=None):
        self.hostname = hostname

        if username is None:
            self.username = getuser()
        else:
            self.username = username

        self.password = password
        self.port = port
		
        if local_key_path is None:
            self.local_key_path = self._get_defalut_local_key_path()
        else:
            self.local_key_path = os.path.abspath(local_key_path)
        if remote_key_path is None:
            self.remote_key_path = self._get_defalut_remote_key_path()
        else:
            self.remote_key_path = remote_key_path

    def _get_defalut_local_key_path(self):
        return os.path.expanduser('~') + os.sep + '.ssh' + os.sep + 'id_rsa.pub'

    def _get_defalut_remote_key_path(self):
        return '~/.ssh/authorized_keys'

    def _get_local_key(self):
        try:
            key = open(self.local_key_path).read().strip()
        except:
            print ("ERROR: key file '%s' could not be opened." %
                   self.local_key_path)
            sys.exit(1)
        return key

    def deploy_key(self):
        key = self._get_local_key()
        copied = 0
        with(settings(hide('everything'),
            user=self.username, host_string=self.hostname,
                password=self.password, port=self.port,)):
            if '1' in (run('[ -f %s ] && echo 1 || echo 0' %
                           self.remote_key_path)):
                authorized_keys = run('cat %s' % self.remote_key_path)
                if key not in authorized_keys:
                    run('echo >> %s' % self.remote_key_path)
                    run('echo %s >> %s' % (key, self.remote_key_path))
                    copied += 1
                else:
                    print ("WARNING: ssh public key already exists in '%s'" %
                           self.remote_key_path)
            else:
                dirpath, filename = os.path.split(self.remote_key_path)
                run('mkdir -p %s' % dirpath)
                run('echo %s > %s' % (key, self.remote_key_path))
                run('chmod 600 %s' % self.remote_key_path)
                copied += 1
            print
            print 'Number of key copyed: ', copied
            print ("Now try logging into the machine with: 'ssh %s@%s'" %
                   (self.username, self.hostname))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ssh-copy-id by Zhengyi')
    parser.add_argument('hostname', help='[user@]machine')
    parser.add_argument('-i', nargs='?', dest='identity_file', default=None,
                        help='defaults to ~/.ssh/id_rsa.pub')
    parser.add_argument('-p', nargs='?', dest='port', type=int, default=22,
                        help='defaults to 22')
    args = parser.parse_args()

    hostname = args.hostname
    username = None
    if '@' in args.hostname:
        if args.hostname.count('@') > 1:
            print ('ERROR: unrecognized [user@]machine %s ' % args.hostname)
            sys.exit(1)
        username, hostname = hostname.split('@')

    ssh_copy_id = DeployKey(hostname, username, port=args.port,
                            local_key_path=args.identity_file).deploy_key
    try:
        execute(ssh_copy_id)
    except KeyboardInterrupt:
        print '\nKeyboardInterrupt'
    except SystemExit:
        print '\nSystemExit'
    except Exception as e:
        print '\nERROR: ', e

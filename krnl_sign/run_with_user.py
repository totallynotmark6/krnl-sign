import os
import pwd
import subprocess


def run_with_user(cmd, user, **kwargs):
    pw_record = pwd.getpwnam(user)
    homedir = pw_record.pw_dir
    # user_uid = pw_record.pw_uid
    # user_gid = pw_record.pw_gid
    env = os.environ.copy()
    env.update({'HOME': homedir, 'LOGNAME': user, 'PWD': os.getcwd(), 'USER': user})
    proc = subprocess.run(cmd, env=env, user=user, **kwargs)
    return proc

def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result
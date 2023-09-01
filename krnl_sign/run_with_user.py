import os
import pwd
import subprocess


def run_with_user(cmd, user):
    res = os.fork()
    if res == 0:
        # we are the child
        pw_record = pwd.getpwnam(user)
        homedir = pw_record.pw_dir
        # user_uid = pw_record.pw_uid
        # user_gid = pw_record.pw_gid
        env = os.environ.copy()
        env.update({'HOME': homedir, 'LOGNAME': user, 'PWD': os.getcwd(), 'USER': user})
        proc = subprocess.run(cmd, env=env, preexec_fn=demote(pw_record.pw_uid, pw_record.pw_gid))
        exit(proc.returncode)
    else:
        # we are the parent
        result = os.waitpid(res, 0)
        return subprocess.CompletedProcess(cmd, result[1])
    

def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result
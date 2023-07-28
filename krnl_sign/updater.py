import pwd
import os
import subprocess


def as_krnl_user():
    user_name = "krnl"
    pw_record = pwd.getpwnam(user_name)
    user_name      = pw_record.pw_name
    user_home_dir  = pw_record.pw_dir
    user_uid       = pw_record.pw_uid
    user_gid       = pw_record.pw_gid
    env = os.environ.copy()
    env[ 'HOME'     ]  = user_home_dir
    env[ 'LOGNAME'  ]  = user_name
    env[ 'USER'     ]  = user_name
    return env, demote(user_uid, user_gid)

def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result

def update_exists():
    # determines if an update exists
    # returns True if an update exists, False otherwise
    env, pre_exec_fn = as_krnl_user()

    # use git to check for updates (commits on remote)
    process = subprocess.run(["git", "fetch", "origin", "main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=pre_exec_fn, env=env)
    if process.returncode != 0:
        return False
    process = subprocess.run(["git", "rev-list", "--count", "HEAD..origin/main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=pre_exec_fn, env=env)
    if process.returncode != 0:
        return False
    if int(process.stdout) > 0:
        return True
    return False

def update():
    # performs the update
    # returns True if successful, False otherwise
    env, pre_exec_fn = as_krnl_user()

    # use git to update
    process = subprocess.run(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=pre_exec_fn, env=env)
    if process.returncode != 0:
        return False
    return True
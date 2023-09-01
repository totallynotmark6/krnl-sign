import os
import pwd
import subprocess

def run_with_user(cmd, user, **kwargs):
    pw_record = pwd.getpwnam(user)
    homedir = pw_record.pw_dir
    user_uid = pw_record.pw_uid
    user_gid = pw_record.pw_gid
    env = os.environ.copy()
    env.update({'HOME': homedir, 'LOGNAME': user, 'PWD': os.getcwd(), 'USER': user})
    proc = subprocess.run(cmd, env=env, cwd=homedir, preexec_fn=demote(user_uid, user_gid), **kwargs)
    return proc

def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result

def check_for_updates():
    # check if the git repo has any updates
    proc = run_with_user(["git", "fetch", "origin", "main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print("Error fetching updates from git repo")
        return False
    proc = run_with_user(["git", "diff", "--name-only", "HEAD", "origin/main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print("Error checking for updates")
        return False
    if proc.stdout.decode("utf-8") == "":
        return False
    return True
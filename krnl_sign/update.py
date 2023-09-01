import subprocess

def check_for_updates():
    # check if the git repo has any updates
    proc = subprocess.run(["sudo", "-u", "krnl", "git", "fetch", "origin", "main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print("Error fetching updates from git repo")
        return False
    proc = subprocess.run(["sudo", "-u", "krnl", "git", "diff", "--name-only", "HEAD", "origin/main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print("Error checking for updates")
        return False
    if proc.stdout.decode("utf-8") == "":
        return False
    return True
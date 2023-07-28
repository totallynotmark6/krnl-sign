import subprocess

def update_exists():
    # determines if an update exists
    # returns True if an update exists, False otherwise

    # use git to check for updates (commits on remote)
    process = subprocess.Popen(["git", "fetch"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return False
    process = subprocess.Popen(["git", "log", "HEAD..origin/main", "--oneline"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return False
    if output:
        return True
    return False

def update():
    # performs the update
    # returns True if successful, False otherwise

    # use git to update
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return False
    return True
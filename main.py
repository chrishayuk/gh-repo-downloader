import subprocess
import os
import urllib.parse
import configparser

def read_config(config_file):
    # Read configuration from an INI file.
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        "output_directory": config.get("DEFAULT", "output_directory", fallback="./cloned_repos"),
        "repo_list_file": config.get("DEFAULT", "repo_list_file", fallback="repos.txt")
    }

def read_repos_from_file(file_path):
    # Read a list of GitHub repository URLs from a file.
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_org_from_repo_url(repo_url):
    # Extract the organization or username from the url
    path = urllib.parse.urlparse(repo_url).path
    parts = path.strip('/').split('/')
    if len(parts) > 1:
        return parts[0]
    return None

def clone_repos(repo_list, destination_folder='.'):
    # Clone a list of GitHub repositories to a local machine

    # Check if the repo exists already
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # loop through the repos
    for repo_url in repo_list:
        # get the org name from the repo url
        org_name = get_org_from_repo_url(repo_url)
        if not org_name:
            print(f"Failed to extract organization/user name from {repo_url}. Skipping...")
            continue
        org_folder = os.path.join(destination_folder, org_name)

        # create the org folder
        if not os.path.exists(org_folder):
            os.makedirs(org_folder)
        
        try:
            # perform a git clone
            subprocess.check_call(['git', 'clone', repo_url], cwd=org_folder)
            print(f"Successfully cloned {repo_url} into {org_folder}")
        except subprocess.CalledProcessError:
            print(f"Failed to clone {repo_url}")

if __name__ == "__main__":
    # Read configurations from the config file
    config = read_config('config.ini')
    destination = config["output_directory"]
    repo_file_path = config["repo_list_file"]

    repos_to_clone = read_repos_from_file(repo_file_path)
    clone_repos(repos_to_clone, destination)

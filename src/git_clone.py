from utils import is_directory_empty, delete_directory_contents
from const import GIT_LOCAL_DIR, GIT_REPO_URL
from git import Repo


###################################################################################################
# Step 1: Cloned the code in local dir
###################################################################################################
def clone_code(repo_url: str):
    # Clone repo using Git and save in local dir location git_code
    local_folder_location = GIT_LOCAL_DIR
    try:
        # Delete the data from local dir if already exists
        if not is_directory_empty(local_folder_location):
            delete_directory_contents(local_folder_location)

        # Clone the code in local dir
        repo = Repo.clone_from(repo_url, local_folder_location)
        repo.close()

        return "success"
    except Exception as ex:
        print(ex)

    return "failure"


if __name__ == "__main__":
    result = clone_code(GIT_REPO_URL)
    print(result)

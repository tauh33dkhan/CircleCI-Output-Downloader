# CircleCI Output Downloader

CircleCI Output Downloader is a Python script that allows you to fetch and save CircleCI build output messages from multiple projects within a GitHub organization.

## How It Works

The script follows these steps to fetch and save CircleCI build output messages:

1. **Fetching Project Names**: The script sends a request to the GitHub API to fetch all project names belonging to a specified GitHub organization.

2. **Fetching Build Numbers**: For each project, the script sends a request to the CircleCI API to fetch the build numbers associated with that project.

3. **Fetching Output URLs and Bash Commands**: For each build of each project, the script sends a request to the CircleCI API to fetch output URLs and corresponding bash commands. It extracts this information from the JSON response.

4. **Saving Output Messages**: The script then saves the output messages associated with each output URL to text files. It organizes the files by project and build number, and also includes the corresponding bash command if available.


## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/tauh33dkhan/CircleCI-Output-Downloader
    ```

2. Navigate to the project directory:

    ```bash
    cd CircleCI-Output-Downloader
    ```

3. Run the script with your GitHub organization name as an argument:

    ```bash
    python CircleCI-Output-Downloader.py <organization_name>
    ```

    Replace `<organization_name>` with the name of your GitHub organization.

4. The script will fetch project names, build numbers, output URLs, and bash commands, and save the output messages to files in a directory named `circle_output`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

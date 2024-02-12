import os
import sys
import requests
import json
import re
from colorama import Fore, Style

# Function to fetch all project names from a GitHub organization
def fetch_project_names(org_name):
    print(f"{Fore.LIGHTBLUE_EX}Fetching project names from GitHub organization: {org_name}...{Style.RESET_ALL}")
    url = f"https://api.github.com/users/{org_name}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return [repo["name"] for repo in response.json()]
    else:
        print(f"{Fore.RED}Failed to fetch project names{Style.RESET_ALL}")
        return []

# Function to sanitize filename by removing special characters
def sanitize_filename(filename):
    # Define a regex pattern to match special characters
    pattern = r"[^\w\-.]"
    # Replace special characters with underscores
    return re.sub(pattern, "_", filename)

# Function to fetch build ID's for a project
def fetch_build_numbers(org_name, project_name):
    print(f"{Fore.LIGHTBLUE_EX}Fetching build ID's for project: {project_name}...{Style.RESET_ALL}")
    url = f"https://circleci.com/api/v1.1/project/github/{org_name}/{project_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return [build["build_num"] for build in response.json()]
    else:
        print(f"{Fore.RED}Failed to fetch build ID's for project: {project_name}{Style.RESET_ALL}")
        return []

# Function to fetch output URLs and corresponding bash commands for each build of a project
def fetch_output_info(org_name, project_name, build_numbers):
    output_info = {}
    print(f"{Fore.LIGHTBLUE_EX}Fetching output URLs and bash commands for project: {project_name}...{Style.RESET_ALL}")
    base_url = f"https://circleci.com/api/v1.1/project/github/{org_name}/{project_name}/"
    for build_num in build_numbers:
        print(f"\n{Fore.LIGHTBLUE_EX}Fetching output info for build number: {build_num}...{Style.RESET_ALL}")
        url = base_url + str(build_num)
        response = requests.get(url)
        if response.status_code == 200:
            build_info = response.json()
            for step in build_info.get("steps", []):
                for action in step.get("actions", []):
                    bash_command = action.get("bash_command")
                    output_url = action.get("output_url")
                    if output_url:
                        # If bash_command is None or empty, replace it with a placeholder string
                        bash_command = bash_command if bash_command else "No bash command provided"
                        output_info[f"{build_num}_{action['name']}"] = {'bash_command': bash_command, 'output_url': output_url}
        else:
            print(f"{Fore.RED}Failed to fetch output info for build number {build_num} of project: {project_name}{Style.RESET_ALL}")
    return output_info

# Function to save message from output URLs to files
def save_messages(org_name, project_name, output_info):
    print(f"{Fore.LIGHTBLUE_EX}Saving messages for project: {project_name}...{Style.RESET_ALL}")
    if not os.path.exists("circle_output"):
        os.makedirs("circle_output")
    for name, info in output_info.items():
        response = requests.get(info['output_url'])
        if response.status_code == 200:
            data = response.json()
            message = data[0].get("message", "")
            # Sanitize filename
            safe_name = sanitize_filename(name)
            # Add project name and bash command to the filename
            filename = f"circle_output/{org_name}_{project_name}_{safe_name}.txt"
            with open(filename, "w") as f:
                f.write(f"Bash command: {info['bash_command']}\n\n")
                f.write(message)
        else:
            print(f"{Fore.RED}Failed to fetch output for URL: {info['output_url']}{Style.RESET_ALL}")

# Main function
def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python script.py <organization_name>{Style.RESET_ALL}")
        sys.exit(1)

    org_name = sys.argv[1]
    print(f"{Fore.LIGHTGREEN_EX}Starting the process for organization: {org_name}...{Style.RESET_ALL}\n")
    project_names = fetch_project_names(org_name)
    project_names_str = ', '.join(project_names)
    print(f"\n{Fore.LIGHTBLUE_EX}Project Names:{Style.RESET_ALL} {project_names_str}")
    for project_name in project_names:
        print(f"\n{Fore.LIGHTGREEN_EX}Processing project: {project_name}{Style.RESET_ALL}")
        build_numbers = fetch_build_numbers(org_name, project_name)
        output_info = fetch_output_info(org_name, project_name, build_numbers)
        save_messages(org_name, project_name, output_info)
        print(f"\n{Fore.LIGHTGREEN_EX}Finished processing project: {project_name}{Style.RESET_ALL}")

    print(f"\n{Fore.LIGHTGREEN_EX}Process completed for organization: {org_name}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

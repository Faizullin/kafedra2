import subprocess
import sys

def run_command(command):
    """Helper function to run a shell command."""
    try:
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

def validate_environment(env):
    """Validate the given environment argument."""
    if env not in ["dev", "prod"]:
        print("Error: Environment must be 'dev' or 'prod'.")
        sys.exit(1)

def get_compose_file(env):
    """Returns the appropriate docker-compose file based on the environment."""
    return f"../docker-compose.{env}.yml"

def join_additional_args(args):
    """Helper to join additional arguments for commands."""
    return " ".join(args) if args else ""

def main():
    if len(sys.argv) < 3:
        print("Usage: helper.py [dev|prod] [action] [additional_args...]")
        sys.exit(1)

    # Get arguments
    env = sys.argv[1]
    action = sys.argv[2]
    additional_args = sys.argv[3:]  # Remaining arguments

    # Validate environment
    validate_environment(env)

    # Set compose file and other configurations
    compose_file = get_compose_file(env)
    container_name = "kafedra-backend-1"
    settings_extension = "local" if env == "dev" else "prod"

    # Define available actions
    actions = {
        "build": f"docker-compose -f {compose_file} build {join_additional_args(additional_args)}",

        "collectstatic": f"docker exec -it {container_name} python3 manage.py collectstatic --noinput --settings=backend.settings.{settings_extension}",

        "migrate": [
            f"docker exec -it {container_name} python3 manage.py makemigrations --settings=backend.settings.{settings_extension}",
            f"docker exec -it {container_name} python3 manage.py migrate --settings=backend.settings.{settings_extension}"
        ],

        "seed": f"docker exec -it {container_name} python3 manage.py shell -c \"from seeding.seed import *; seed(False)\" --settings=backend.settings.{settings_extension}",

        "remove_migrations_and_db": f"docker exec -it {container_name} python3 manage.py shell -c \"from seeding.remove_migrations_and_db import *; remove_migrations_and_db();\" --settings=backend.settings.{settings_extension}",

        "shell": f"docker exec -it {container_name} sh",

        "django-shell": f"docker exec -it {container_name} sh -c \"python3 manage.py shell --settings=backend.settings.{settings_extension}\"",

        "deploy": [
            f"docker-compose -f {compose_file} down {join_additional_args(additional_args)}",
            f"docker-compose -f {compose_file} pull {join_additional_args(additional_args)}",
            f"docker-compose -f {compose_file} up -d --build {join_additional_args(additional_args)}"
        ],

        "run": [
            f"docker-compose -f {compose_file} up {join_additional_args(additional_args)}"
        ],

        "logs": f"docker-compose -f {compose_file} logs {join_additional_args(additional_args)}",

        "down": f"docker-compose -f {compose_file} down {join_additional_args(additional_args)}"
    }

    # Validate action
    if action not in actions:
        print(f"Error: Invalid action '{action}'. Available actions: {', '.join(actions.keys())}")
        sys.exit(1)

    # Execute the action(s)
    print(f"Executing '{action}' for {env} environment...")

    commands = actions[action]
    if isinstance(commands, list):  # Handle multiple commands
        for cmd in commands:
            run_command(cmd)
    else:
        run_command(commands)

    print(f"'{action}' execution completed successfully!")

if __name__ == "__main__":
    main()

"""
Pip Upgrader - A simple tool to update Python packages

What this tool does:
1. Updates Python packages safely with backups
2. Lets you skip packages you don't want to update
3. Shows what changed after updates

Main features:
- Makes backups automatically
- Can skip packages you choose
- Shows changes before making them
- Shows clear reports

Basic use:
    python pip-upgrader.py [--requirements file] [--quiet] [--dry-run] [--skip-pip]

Simple example:
    python pip-upgrader.py --dry-run

Author: Hamad AlQassar
License: MIT
"""

import subprocess
import sys
import platform
import argparse
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

# Check Python version
if sys.version_info < (3, 6):
    print("Python 3.6 or higher is required")
    sys.exit(1)

class PipUpgrader:
    """
    Main tool to update Python packages.
    
    What it does:
    - Updates packages and keeps backups
    - Skips packages you don't want to update
    - Shows changes before making them
    
    Settings:
        requirements_file: Where to find package list
        quiet: Show less output
        dry_run: Just show what would change
    """
    
    def __init__(
        self, requirements_file: str = "requirements.txt", quiet: bool = False,
        dry_run: bool = False
    ):
        """
        Initialize PipUpgrader with configuration options.

        Args:
            requirements_file (str): Path to the requirements file
            quiet (bool): Whether to suppress detailed output
            dry_run (bool): Show proposed changes without executing them
        """
        self.requirements_file = Path(requirements_file).resolve()
        self.quiet = quiet
        self.dry_run = dry_run
        self.is_windows = platform.system().lower() == "windows"
        self.python_cmd = "python" if self.is_windows else "python3"
        self.setup_logging()

        if not self.requirements_file.exists():
            raise FileNotFoundError(f"Requirements file not found: {requirements_file}")

    def setup_logging(self) -> None:
        """Configure logging based on quiet mode."""
        level = logging.WARNING if self.quiet else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def get_skipped_packages(self) -> List[str]:
        """
        Read the skip_packages.txt file and return list of packages to skip.

        Returns:
            List[str]: List of package names to skip
        """
        skip_file = Path("skip_packages.txt")
        try:
            if skip_file.exists():
                return [
                    line.strip()
                    for line in skip_file.read_text().splitlines()
                    if line.strip()
                ]
            return []
        except Exception as e:
            logging.error(f"Error reading skip_packages.txt: {e}")
            return []

    def run_pip_command(self, command: str) -> subprocess.CompletedProcess:
        """
        Safely run a pip command and handle errors.

        Args:
            command (str): Pip command to run

        Returns:
            subprocess.CompletedProcess: Result of the command
        """
        try:
            # Make command platform-independent
            if self.is_windows:
                # Windows-specific command handling
                command = command.replace("python -m pip", f"{self.python_cmd} -m pip")
                shell = True
            else:
                # Unix-like systems
                command = command.replace("python -m pip", f"{self.python_cmd} -m pip")
                shell = False

            return subprocess.run(
                command if shell else command.split(),
                shell=shell,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running pip command: {e}")
            logging.debug(f"Command output: {e.output}")
            return e
        except Exception as e:
            logging.error(f"Unexpected error running pip command: {e}")
            raise

    def get_installed_packages(self) -> Dict[str, str]:
        """
        Get dictionary of installed packages and their versions.

        Returns:
            Dict[str, str]: Dictionary of package names and versions
        """
        result = self.run_pip_command("pip freeze")
        packages = {}
        for line in result.stdout.splitlines():
            if "==" in line:
                package, version = line.split("==")
                packages[package.lower()] = version
        return packages

    def upgrade_pip_if_available(self) -> None:
        """Upgrade pip if a newer version is available."""
        logging.info("Checking if pip needs an upgrade...")
        self.run_pip_command("python -m pip install --upgrade pip -q")
        logging.info("Pip upgrade check complete.")

    def create_backup(self) -> Optional[str]:
        """
        Create a backup of the requirements file.
        
        Returns:
            Optional[str]: Name of backup file if successful, None otherwise
        """
        if self.requirements_file.exists():
            backup_name = (
                f"requirements_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            try:
                import shutil
                shutil.copy2(self.requirements_file, backup_name)
                logging.info(f"Created backup: {backup_name}")
                return backup_name
            except Exception as e:
                logging.error(f"Failed to create backup: {e}")
                if not self.dry_run:
                    raise  # Only raise if not in dry-run mode
                return None
        return None

    def upgrade_packages(self) -> None:
        """
        Updates packages safely.
        
        Steps:
        1. Reads list of packages to skip
        2. Saves current versions
        3. Makes backup
        4. Updates packages
        5. Shows what changed

        Handles problems with:
        - Backup fails
        - Update fails
        - File problems
        """
        try:
            # Get skipped packages
            skipped_packages = self.get_skipped_packages()
            if skipped_packages:
                logging.info(f"Skipping packages: {', '.join(skipped_packages)}")

            # Get current versions
            old_packages = self.get_installed_packages()

            if self.dry_run:
                logging.info("DRY RUN - No changes will be made")
                self._simulate_upgrades(old_packages, skipped_packages)
                return

            # Create backup before any modifications
            backup_file = self.create_backup()
            if not backup_file:
                logging.error("Failed to create backup, aborting")
                return

            # Process requirements file
            try:
                self._process_requirements(skipped_packages)
            except Exception as e:
                self._restore_backup(backup_file)
                raise

            # Upgrade packages
            logging.info("Upgrading packages...")
            result = self.run_pip_command("pip install -r requirements.txt --upgrade")
            if isinstance(result, subprocess.CalledProcessError):
                self._restore_backup(backup_file)
                logging.error("Package upgrade failed, restored backup")
                return

            # Compare versions
            new_packages = self.get_installed_packages()
            self._report_changes(old_packages, new_packages, skipped_packages)

        except Exception as e:
            logging.error(f"Error during upgrade process: {e}")
            raise

    def _simulate_upgrades(self, current_packages: Dict[str, str], 
                          skipped_packages: List[str]) -> None:
        """
        Shows what would change without making changes.
        
        Inputs:
            current_packages: List of packages and their versions now
            skipped_packages: Packages to not update
        
        Shows:
            - Which packages would update
            - Current and new versions
        """
        logging.info("Checking for available upgrades...")
        for package, version in current_packages.items():
            if package not in skipped_packages:
                result = self.run_pip_command(f"pip index versions {package}")
                if not isinstance(result, subprocess.CalledProcessError):
                    logging.info(f"Would upgrade {package} from {version}")

    def _restore_backup(self, backup_file: str) -> None:
        """Restore from backup file if upgrade fails."""
        try:
            import shutil
            shutil.copy2(backup_file, self.requirements_file)
            logging.info("Restored requirements.txt from backup")
        except Exception as e:
            logging.error(f"Failed to restore backup: {e}")

    def _process_requirements(self, skipped_packages: List[str]) -> None:
        """Process and update requirements file."""
        with open(self.requirements_file, "r") as file:
            requirements = file.readlines()

        with open(self.requirements_file, "w") as file:
            for line in requirements:
                line = line.strip()
                if not line or line.startswith('#'):
                    file.write(line + '\n')
                    continue
                    
                if '==' in line:
                    package_name = line.split('==')[0].lower()
                    if package_name in skipped_packages:
                        file.write(line + '\n')
                    else:
                        file.write(line.replace("==", ">=") + '\n')
                else:
                    file.write(line + '\n')

    def _report_changes(
        self,
        old_packages: Dict[str, str],
        new_packages: Dict[str, str],
        skipped_packages: List[str],
    ) -> None:
        """
        Report package version changes.

        Args:
            old_packages (Dict[str, str]): Original package versions
            new_packages (Dict[str, str]): New package versions
            skipped_packages (List[str]): Packages that were skipped
        """
        updates = []
        for package, old_version in old_packages.items():
            if package in new_packages and package not in skipped_packages:
                new_version = new_packages[package]
                if old_version != new_version:
                    updates.append(f"{package}: {old_version} -> {new_version}")

        if updates:
            logging.info("Updated packages:")
            for update in updates:
                logging.info(update)
        else:
            logging.info("No packages were updated.")


def main():
    """Main entry point for the script."""
    # Check if pip is installed
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        print("pip is not installed. Please install pip first.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Upgrade pip packages while maintaining control over versions."
    )
    parser.add_argument(
        "--requirements",
        default="requirements.txt",
        help="Path to requirements file (default: requirements.txt)",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed output")
    parser.add_argument("--skip-pip", action="store_true", help="Skip pip self-upgrade")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show proposed changes without executing them")

    args = parser.parse_args()

    try:
        upgrader = PipUpgrader(
            requirements_file=args.requirements,
            quiet=args.quiet,
            dry_run=args.dry_run
        )

        if not args.skip_pip and not args.dry_run:
            upgrader.upgrade_pip_if_available()

        upgrader.upgrade_packages()
        logging.info("Script execution finished successfully.")

    except Exception as e:
        logging.error(f"Script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Pip Upgrader - A utility to safely upgrade pip packages.

This script helps you upgrade your pip packages while maintaining control over specific
package versions. It supports skipping certain packages and provides detailed output
of version changes.

Author: Your Name
License: MIT
"""

import subprocess
import re
import sys
import argparse
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


class PipUpgrader:
    def __init__(self, requirements_file: str = "requirements.txt", quiet: bool = False):
        """
        Initialize PipUpgrader with configuration options.

        Args:
            requirements_file (str): Path to the requirements file
            quiet (bool): Whether to suppress detailed output
        """
        self.requirements_file = Path(requirements_file)
        self.quiet = quiet
        self.setup_logging()

    def setup_logging(self) -> None:
        """Configure logging based on quiet mode."""
        level = logging.WARNING if self.quiet else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
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
                return [line.strip() for line in skip_file.read_text().splitlines() if line.strip()]
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
            return subprocess.run(
                command,
                shell=True,
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

    def create_backup(self) -> None:
        """Create a backup of the requirements file."""
        if self.requirements_file.exists():
            backup_name = f"requirements_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
                self.requirements_file.rename(Path(backup_name))
                logging.info(f"Created backup: {backup_name}")
            except Exception as e:
                logging.error(f"Failed to create backup: {e}")

    def upgrade_packages(self) -> None:
        """Main method to handle the package upgrade process."""
        try:
            # Get skipped packages
            skipped_packages = self.get_skipped_packages()
            if skipped_packages:
                logging.info(f"Skipping packages: {', '.join(skipped_packages)}")

            # Get current versions
            old_packages = self.get_installed_packages()

            # Generate and modify requirements.txt
            self.run_pip_command("pip freeze > requirements.txt")
            
            # Read and modify requirements
            with open(self.requirements_file, 'r') as file:
                requirements = file.readlines()

            # Create backup before modifying
            self.create_backup()

            # Write modified requirements
            with open(self.requirements_file, 'w') as file:
                for line in requirements:
                    package_name = line.split("==")[0].lower()
                    if package_name in skipped_packages:
                        file.write(line)
                    else:
                        file.write(line.replace("==", ">="))

            # Upgrade packages
            logging.info("Upgrading packages...")
            self.run_pip_command("pip install -r requirements.txt --upgrade -q")

            # Compare versions
            new_packages = self.get_installed_packages()
            self._report_changes(old_packages, new_packages, skipped_packages)

        except Exception as e:
            logging.error(f"Error during upgrade process: {e}")
            raise

    def _report_changes(self, old_packages: Dict[str, str], 
                       new_packages: Dict[str, str], 
                       skipped_packages: List[str]) -> None:
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
    parser = argparse.ArgumentParser(description="Upgrade pip packages while maintaining control over versions.")
    parser.add_argument("--requirements", default="requirements.txt",
                      help="Path to requirements file (default: requirements.txt)")
    parser.add_argument("--quiet", action="store_true",
                      help="Suppress detailed output")
    parser.add_argument("--skip-pip", action="store_true",
                      help="Skip pip self-upgrade")
    
    args = parser.parse_args()
    
    try:
        upgrader = PipUpgrader(requirements_file=args.requirements, quiet=args.quiet)
        
        if not args.skip_pip:
            upgrader.upgrade_pip_if_available()
            
        upgrader.upgrade_packages()
        logging.info("Script execution finished successfully.")
        
    except Exception as e:
        logging.error(f"Script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

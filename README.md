# Pip Upgrader

A Python utility to safely upgrade your pip packages while maintaining control over specific package versions.

## Features

- 🚀 Automatically upgrades all pip packages
- 🔒 Allows skipping specific packages via `skip_packages.txt`
- 📝 Maintains a log of version changes
- ⚡ Supports quiet mode for less verbose output
- 🛡️ Safe upgrading with version control
- 🔄 Automatic pip self-upgrade

## Installation

Clone this repository:
```bash
git clone https://github.com/yourusername/pip-upgrader.git
cd pip-upgrader
```

## Usage

1. Basic usage:
```bash
python pip-upgrader.py
```

2. With command line options:
```bash
python pip-upgrader.py --quiet  # For minimal output
python pip-upgrader.py --skip-pip  # Skip pip self-upgrade
python pip-upgrader.py --requirements custom_requirements.txt  # Use custom requirements file
```

3. To skip specific packages, create a `skip_packages.txt` file and list one package per line:
```
package1
package2
```

## Configuration

- `skip_packages.txt`: List packages that should not be upgraded (one per line)
- Requirements file: Default is `requirements.txt` in the current directory

## Output

The script will show:
- Current package versions
- Updated package versions
- Skipped packages
- Any errors encountered during the process

## Requirements

- Python 3.6+
- pip

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

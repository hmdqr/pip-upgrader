# Pip Upgrader

A tool to update your Python packages safely.

## What It Does
- ✅ Updates packages and makes backups automatically
- ✅ Lets you choose which packages not to update
- ✅ Shows what will change before doing it
- ✅ Shows clear before/after reports

## Before You Start
You need:
- Python 3.6 or newer
- A virtual environment (recommended)
- A requirements.txt file
  
When you run `python pip-upgrader.py`:
1. It looks for 'requirements.txt' in your folder
2. If not found: Shows error message
3. If found:
   - Makes a backup of requirements.txt
   - Updates packages (except ones you want to skip)
   - Shows what changed
   - If anything goes wrong, keeps your old files safe

To Be Safe:
1. Try first with `--dry-run` to see what will change
2. Check you have requirements.txt
3. Use a virtual environment
4. Make a backup of your project

## How to Use

### First Time Setup
```bash
git clone https://github.com/hmdqr/pip-upgrader.git
cd pip-upgrader
```

### Simple Commands
```bash
# Update everything
python pip-upgrader.py

# See what will change (safe to run)
python pip-upgrader.py --dry-run

# Use a different requirements file
python pip-upgrader.py --requirements other-requirements.txt

# Show less information
python pip-upgrader.py --quiet
```

### Skip Some Packages
Make a file called `skip_packages.txt` and list packages you don't want to update:
```
django
requests
```

## Command Options
- `--requirements`: Choose a different requirements file
- `--quiet`: Show less output
- `--skip-pip`: Don't update pip itself
- `--dry-run`: Show changes without making them

## Common Problems

### Backup Not Working?
- Check if you can write to the folder
- Check if you have enough space

### Updates Not Working?
- Look at skip_packages.txt
- Check if versions can work together

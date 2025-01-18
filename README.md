# Pip Upgrader

A simple tool to update your Python packages. It helps you keep your packages up to date while making sure nothing breaks.

## What it does

- Updates all your pip packages automatically
- Creates a backup of your packages list just in case
- Lets you choose which packages not to update
- Shows you what changed after the update
- Can run quietly without showing too much information
- Updates packages quickly and safely

## Getting Started

1. Get the code:
```bash
git clone https://github.com/hmdqr/pip-upgrader.git
cd pip-upgrader
```

2. Run it:
```bash
python pip-upgrader.py
```

That's it! The script will handle everything else.

## Other ways to use it

### Basic way
```bash
python pip-upgrader.py
```

### More options

**For less output on screen:**
```bash
python pip-upgrader.py --quiet
```

**If you don't want to update pip itself:**
```bash
python pip-upgrader.py --skip-pip
```

**If your requirements file is somewhere else:**
```bash
python pip-upgrader.py --requirements path/to/requirements.txt
```

## Don't want to update certain packages?

If you have some packages you don't want to update:

1. Make a file called `skip_packages.txt`
2. Write the package names you want to skip, one per line, like this:
```
tensorflow
django
```

## What's in the folder

```
pip-upgrader/
├── pip-upgrader.py     # The main program
├── skip_packages.txt   # List of packages you don't want to update (optional)
└── requirements.txt    # Your list of packages
```

## How it works

The script will:
- Check if pip needs an update
- Make a backup of your current packages list
- See what versions you have now
- Update everything except the packages you want to skip
- Tell you what got updated
- Keep the old versions of packages you wanted to skip

## Good to know

- The script makes a backup automatically, so you won't lose your old package versions
- It's a good idea to test your project after updating
- Use the skip list if you need specific versions of some packages

## Want to help? Please do!

Your contributions are very welcome! Here's how you can help:

**Steps to contribute:**
1. Fork the repository
2. Create your feature branch: `git checkout -b my-new-feature`
3. Make your changes
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request

Don't worry if you're new to open source - we welcome all skill levels! You can help by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Fixing typos
- Adding tests

Check out our [issues page](https://github.com/hmdqr/pip-upgrader/issues) for ways to help.

## License

This project uses the MIT License - check out the [LICENSE](https://github.com/hmdqr/pip-upgrader/blob/main/LICENSE) file to learn more.

## Need help?

If something's not working:

**First steps:**
- Look through [existing issues](https://github.com/hmdqr/pip-upgrader/issues)
- [Create a new issue](https://github.com/hmdqr/pip-upgrader/issues/new) and tell us what's wrong
- Include any error messages you see

**Other ways to engage:**
- Star the repository if you find it useful
- Watch the repository to get notified about new updates
- Share it with others who might find it helpful

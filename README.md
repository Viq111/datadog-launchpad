# datadog-launchpad

Interface datadog with the Novation Launchpad

## Supported hardware:

- [Novation Launchpad MkII](http://global.novationmusic.com/launch/launchpad)

If you have other launchpad hardware, feel free to create a similar interface to `launchpad2.py` and submit a PR.
I am looking to support different versions of the launchpad.

## Installation

For this project, you just need python 2, pygame and datadog lib
```
pip install -r requirements.txt
```

### Install pygame

- [Windows](http://www.pygame.org/download.shtml)
- Linux: `sudo apt-get install python-pygame`
- Mac:
  - Install [MacPort](https://www.macports.org/install.php)
  - Check that macport is correctly installed: `sudo port version`
  - If you can't find `port`, try exporting the path: `export PATH=$PATH:/opt/local/bin`
  - Update port `sudo port -v selfupdate`
  - Make sure that the version of python installed is the correct architecture (check 32/64 bits)
  - Install pygame: `port install py27-game +portmidi`

## Configuration

You need to get your app key and api key from datadog [here](https://app.datadoghq.com/account/settings#api)

You can then create a `datadog.conf` file contening the following:

```
{
    "api_key": "<your_api_key>",
    "app_key": "<your_app_key>"
}
```

To bind one monitor to a button, the default configuration is 1 row per monitor category, so you can have up to 8 monitors per category.
Create a `ops.conf` file with the following content:

```
[
    [
        "category_1",
        [monitor_id_1, monitor_id_2, ...]
    ],
    [
        "category_2",
        [monitor_id_1, monitor_id_2, ...]
    ],
    [
        "category_3",
        [monitor_id_1, monitor_id_2, ...]
    ]
]
```
Your file can contains up to 8 categories and up to 8 monitors per category by default.
Check `ops_mode.py` if you want to use different configurations

## Usage

Once you have configured `datadog.conf` & `ops.conf`, you can simply plug your launchpad and run:

```
python main.py
```

Use `^C` to exit the script

This is an early version, PR are welcomed !

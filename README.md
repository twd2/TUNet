# TUNet
Script for connecting to Tsinghua University Network.

## Usage

`tunet.py [-h] -u USERNAME [-p PASSWORD] [-m MD5_HASH_OF_PASSWORD]`

You can also use `crontab` to connect TUNet automatically:

`* * * * * /path/to/tunet.py -u USERNAME -m MD5_HASH_OF_PASSWORD`

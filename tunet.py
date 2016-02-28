# -*- coding: UTF-8 -*-
import sys
import time
import hashlib
import urllib
import urllib2
import argparse

def get(url, **kwargs):
    if kwargs:
        data = urllib.urlencode(kwargs) 
        request = urllib2.Request(url, data)
    else:
        request = urllib2.Request(url)

    response = urllib2.urlopen(request)
    return response.read()

def conn_net(username, password_md5):
    res_str = get('https://net.tsinghua.edu.cn/do_login.php',
                  action='login',
                  username=username,
                  ac_id='1',
                  password='{MD5_HEX}' + password_md5)

    index = res_str.find(':')
    if index == -1:
        errcode = ''
        desc = res_str
    else:
        errcode = res_str[0:index]
        desc = res_str[index + 1:]

    if errcode == 'E2531': # User not found.
        return False
    elif errcode == 'E2532': # The two authentication interval cannot be less than 10 seconds.
        time.sleep(11)
        return False
    elif errcode == 'E2553': # Password is error
        return False
    elif errcode == 'E2842': # IP address does not require authentication.
        return True
    elif errcode != '': # Other errors
        print(errcode)
        return False
    else:
        if desc == 'Login is successful.' or desc == 'IP has been online, please logout.':
            return True
        else:
            print(desc)
            return False

def logout_net():
    res_str = get('https://net.tsinghua.edu.cn/do_login.php',
                  action='logout')

    if res_str == 'Logout is successful.' or res_str == 'You are not online.':
        return True
    else:
        print(res_str)
        return False

def conn_usereg(username, password_md5):
    res_str = get('https://usereg.tsinghua.edu.cn/do.php',
                  action='login',
                  user_login_name=username,
                  user_password=password_md5)

    if res_str == 'ok':
        print('ok')
        return True
    else:
        print(res_str) # TODO
        return False

def check_login():
    res_str = get('https://net.tsinghua.edu.cn/rad_user_info.php')
    if res_str:
        return int(res_str.split(',')[6])
    else:
        return None

def format_byte(n):
    if n > 1024 * 1024 * 1024:
        return str(n / 1024.0 / 1024 / 1024) + 'GiB'
    elif n > 1024 * 1024:
        return str(n / 1024.0 / 1024) + 'MiB'
    elif n > 1024:
        return str(n / 1024.0) + 'KiB'
    else:
        return str(n) + ('Byte' if n == 1 else 'Bytes')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, dest='username')
    parser.add_argument('-p', '--password', dest='password')
    parser.add_argument('-m', '--md5', dest='md5_hash_of_password')

    args = parser.parse_args()
    if args.password:
        password_md5 = hashlib.md5(args.password.encode()).hexdigest()
    elif args.md5_hash_of_password:
        password_md5 = args.md5_hash_of_password
    else:
        print('Need password or md5 hash.')
        exit(1)

    usage = check_login()
    if usage != None:
        print(format_byte(usage))
        exit(0)
    else:
        if conn_net(args.username, password_md5):
            exit(0)
        else:
            exit(1)

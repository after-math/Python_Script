# -*-coding:utf-8-*-

import time
import re
import os


# cmd窗口形状
def cmd_window():
    os.system('color 0A')
    os.system('mode con cols=60 lines=30')
    os.system('title 自动关机')

# 验证输入的预定时间是否正确
def verify_order_time(order_time):
    result = re.fullmatch(
        r'(((202[1235679]|2030)/(((0?[13456789]|11)/0?[1-9])|((0?[469]|11)/([1-2]\d|30))|((10|12)/([1-9]|[1-2]\d|3[0-1]))|(2/([1-9]|1\d|2[0-8]))|(0?[13578]/([1-2]\d|30|31))))|(202[48]/(((0?[13456789]|11)/0?[1-9])|((0?[469]|11)/([1-2]\d|30))|((10|12)/([1-9]|[1-2]\d|30|31))|(2/([1-9]|1\d|2[0-9]))|(0?[13578]/([1-2]\d|30|31))))) (0?[0-9]|(1\d|2[0-3])):(0?[0-9]|[1-5]\d)(?P<COLON>:)?(?(COLON)(0?[0-9]|[1-5]\d))?',
        order_time)
    if result == None:
        return 1
    if order_time.count(':') == 1:
        order_time += ':0'
    order_timestamp = time.mktime(time.strptime(order_time, '%Y/%m/%d %H:%M:%S'))
    if order_timestamp <= time.time():
        return 2
    return order_timestamp


# 下面是一个根据时间进行关机的函数
def poweroff():
    while True:
        order_time = input('\n请如“2021/9/3 20:12”这种格式输入关机的时间（24小时制）。\n->')
        verify_result = verify_order_time(order_time)
        if verify_result == 1:
            print('您的输入不规范。')
            continue
        elif verify_result == 2:
            print('您输入的日期已过期。')
            continue
        break
    poweroff_time = 'shutdown /s /t {0}'.format(int(verify_result) - int(time.time()))
    os.system(poweroff_time)
    print('本机将会在{0}关机。3秒后自动退出......'.format(order_time))
    time.sleep(4)


if __name__ == '__main__':
    cmd_window()
    off_or_cancel = input('设置自动关机输入s;取消设置的自动关机输入c。\n->')
    while off_or_cancel not in ['c', 's', '']:
        off_or_cancel = input('输入不规范\n\n请输入s或c。\n->')
    if off_or_cancel == 'c':
        poweroff_computer = os.system('shutdown /a 2>nul')
        if poweroff_computer != 0:
            request = input('您还没有设置自动关机，是否要设置自动关机的时间[y/n]？')
            while request not in ['y', 'n', '']:
                request = input('输入不规范\n\n请输入y或n。\n->')
            if request == 'n':
                print('三秒后自动退出......')
                time.sleep(4)
            elif request in ['y', '']:
                poweroff()
        elif poweroff_computer == 0:
            print('已经为您取消自动关机。3秒后自动退出......')
            time.sleep(4)
    elif off_or_cancel in ['s', '']:
        poweroff()

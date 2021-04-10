#环境： python3
#用法： 在bat.py的同目录下生成xray_url.txt，根据自己的需求更改scan_command即可
#说明： command中的xray路径需要手动修改，报告生成的位置在同一目录下

#xray_scan：v1.0
#author： 想学点black技术
#time： 2020年12月16日20:27:40
#单独扫描

#xray_scan：v1.1
#更新：增加进程池机制、提高扫描效率（可根据电脑性能自行设置进程池大小）
#时间：2021/04/10 - 12点12分
#并发扫描

import re
import time
from multiprocessing import Pool
import subprocess

# 扫描
def get_url():
    print("Xray Scan Start~")
    with open("xray_url.txt", 'r') as f:
        lines = f.readlines()
        # 进度标识位
        schedule = 1
        schedules = len(lines)
        #最多四个进程
        pool = Pool(4) if (schedules >= 4) else Pool(schedules)
        # 匹配http | https请求头
        pattern = re.compile(r'^(https|http)://')
        for line in lines:
            try:
                if not pattern.match(line.strip()):
                    targeturl = "http://"+line.strip()
                else:
                    targeturl = line.strip()
                pool.apply_async(func=do_scan, args=(targeturl, schedule, schedules))
                schedule += 1
            except Exception as e:
                print(e)
        pool.close()
        pool.join()
        print("Xray Scan End~")


# 报告
def do_scan(targeturl, schedule, schedules):
    scan_command="C:/Users/Administrator/Desktop/xray_windows_amd64.exe.lnk webscan --basic-crawler {} --html-output {}.html".format(targeturl, time.time())
    result, error = subprocess.Popen(scan_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
    #如果想看输出内容的话，就取消下面的注释
    #print(result.decode("GB2312"), error)
    print("当前正在扫描第{}个任务，还剩{}条任务，程序总共执行了{:.2f}%".format(schedule, schedules - schedule, schedule / schedules * 100))


if __name__ == '__main__':
    get_url()

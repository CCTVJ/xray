#author： 想学点black技术
#用法： 在bat.py的同目录下生成xray_url.txt，根据自己的需求更改scan_command即可
#time： 2020年12月16日20:27:40
#环境： python3
#说明： command中的xray路径需要手动修改，报告生成的位置在同一目录下

import os
import hashlib
import re

# 扫描
def get_url():
    f = open("xray_url.txt")
    lines = f.readlines()
    # 匹配http | https请求头
    pattern = re.compile(r'^(https|http)://')
    for line in lines:
        try:
            if not pattern.match(line.strip()):
                targeturl="http://"+line.strip()
            else:
                targeturl=line.strip()
            # print(targeturl.strip())
            outputfilename=hashlib.md5(targeturl.encode("utf-8"))
            do_scan(targeturl.strip(), outputfilename.hexdigest())
        except Exception as e:
            print(e)
            pass
    f.close()
    print("Xray Scan End~")
    return

# 报告
def do_scan(targeturl,outputfilename="test"):
    scan_command="C:/Users/Administrator/Desktop/xray_windows_amd64.exe.lnk webscan --basic-crawler {} --html-output {}.html".format(targeturl,outputfilename)
    # scan_command = "ping 943ogg.dnslog.cn"
    # print(scan_command)
    os.system(scan_command)
    return

if __name__ == '__main__':
    get_url()
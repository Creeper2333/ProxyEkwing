import requests
import urllib3
import zipfile
import json
import sys
import os

LAUNCHER_VERSION=1000#当前启动器版本
root_url='http://openedu.vaiwan.com'#所有都使用相对路径
api={
    'update':'/api/version.php'
}
path=sys.argv[0]
debug_mode='0'
try:
    debug_mode=sys.argv[1]
    if(debug_mode=='ofcourse'):
        root_url=input('[调试模式]根请求网址:')
except:
    pass

def get_version():
    data={'aid':'1'}
    try:
        rslt=requests.post(root_url+api['update'],data=data)
        j=json.loads(rslt.text)
    except Exception as e:
        print('网络连接异常，无法检查更新')
        print('异常代码：',e.with_traceback(None))
        input('按回车退出')
        sys.exit(0)
    #print(rslt.text)
    if 'errorlog' in rslt.text:
        print('遇到错误，错误码',j['errorlog'])
        print('此错误可能是 >> aid << 参数错误导致的，请联系开发者解决')
        input('按回车退出')
        sys.exit(0)

    update_url=j['url']
    description=j['description']

    ver=int(j['version'])
    current_verion=0
    flag=True

    while(flag):
        try:
            with open('settings\\version.txt','r') as f:
                current_verion=int(f.read())
                f.close()
                flag=False
        except:
            os.system(r'mkdir settings')#如果失败，就创建文件夹
            with open('settings\\version.txt','a') as f:
                f.write('0')
                f.close()
    if current_verion<ver:
        return((False,ver,current_verion,update_url,description))
    else:
        return((True,ver,current_verion))

def download(url,version):
    flag=True
    print('正在准备下载...')
    urllib3.disable_warnings()
    res=requests.get(root_url+url,verify=False)
    while(flag):
        try:
            with open('tmp/'+str(version)+'.zip','ab') as f:
                f.write(res.content)#写入文件
                f.flush()
            flag=False
        except:
            os.system('mkdir tmp')
    print('下载完成，大小',int(len(res.content)/1024),'KiB')
    return 'tmp\\'+str(version)+'.zip'

def unzip(path,version):
    main_app=str()
    print('正在准备解压缩资源...')
    zip_file = zipfile.ZipFile(path)
    if os.path.isdir('bin'):
        pass
    else:
        os.mkdir('bin')
    for names in zip_file.namelist():
        if os.path.isdir('bin/'+version):
            pass
        else:
            os.mkdir('bin/'+version)
        print('正在解压：',names)
        if('.exe' in names):
            main_app=names
        zip_file.extract(names,'bin/'+version)#分别解压文件
    zip_file.close()
    print('资源解压缩完成')
    return main_app

if __name__=='__main__':
    print('ProxyEkwing Launcher Version.',str(LAUNCHER_VERSION))
    print('输入完命令务必按 **回车** 别愣着')

    v=get_version()
    if (v[0]==False):
        print('有新版本，版本号：',v[1],' 当前版本：',v[2],'\n','自述：',v[4])
        if(input('是否下载？输入 0 并敲回车为不下载，输入其它任意字符并敲回车为下载')!='0'):
            p=download(v[3],v[1])
            #p=download('/res/pe.zip',v[1])#测试用
            unzip(p,str(v[1]))
            with open('settings\\version.txt','w') as f:
                f.write(str(v[1]))#写入新版本号
                f.close()
    else:
        print('当前版本：',v[1],'，已经是最新版本')
    
    print('准备启动程序...')
    print('版本号',str(v[1]))
    os.system('start .\\bin\\'+str(v[1])+'\\ProxyEk.exe')
    input('启动！！')

#目录结构
#./bin  主程序目录
#   -/xxxx  小版本目录
#       -/xxx.xxx
#       -/xxx.xxx
#       -/ProxyEk.exe   主程序
#   -/xxxx  小版本目录
#       -/xxx.xxx
#       -/xxx.xxx
#       -/ProxyEk.exe   主程序
#./tmp  下载文件夹
#   -/xxxx.zip  下载文件
#   -/xxxx.zip
#./settings 设置
#   -/version.txt   软件版本（最新）
#./update.exe   更新程序
#(./update.py)

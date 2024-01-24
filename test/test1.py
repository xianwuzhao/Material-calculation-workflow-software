
'''
import paramiko
import os as os
t=paramiko.Transport(("10.17.17.238",131))
t.connect(username ="iei", password ="ccmsiei")

chan=t.open_session()   # 连接成功后打开一个channe

sftp=paramiko.SFTPClient.from_transport(t)

# linux下载到window
path_remote_down="/home/iei/lds"
path_local_down=os.path.join(os.path.abspath("."),"main.py")
sftp.get(path_remote_down,path_local_down)

# window上传到linux
path_local_up=os.path.join(os.path.abspath("."),"data_upload.csv")
path_remote_up="/home/apple/data_upload.csv"
sftp.put(path_local_up,path_remote_up)

'''


from asyncio import transports
import paramiko, sys
from forward import forward_tunnel
import threading
import os as os
remote_host = "192.168.199.131"#"10.17.17.238" 
remote_port = 22 #22
local_port  = 22 #22
ssh_host    = "10.17.17.238"#"192.168.199.131"
ssh_port    = 131 # 131

user     = "iei"
password = "ccmsiei"
'''
transport = paramiko.Transport((ssh_host, ssh_port))

# Command for paramiko-1.7.7.1
transport.connect(hostkey  = None,
                  username = user,
                  password = password,
                  pkey     = None)
                  '''
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh_client.connect(hostname=ssh_host, port=ssh_port, username=user, password=password)
# 获取传输实例
transport=ssh_client.get_transport()
#sftp=paramiko.SFTPClient.from_transport(transport)

def onupload():
    sftp=paramiko.SFTPClient.from_transport(transport)
    path_local_up=os.path.join(os.path.abspath("."),"test.py")
    path_remote_up="/home/iei/test.py"
    sftp.put(path_local_up,path_remote_up)


try:
    
    thread1 = threading.Thread(target=forward_tunnel,args = (local_port, remote_host, remote_port, transport))
   # thread2 = threading.Thread(target=onupload)
    thread1.start()
    sftp=paramiko.SFTPClient.from_transport(transport)
    #thread2.start()
    #threading.Thread(forward_tunnel(local_port, remote_host, remote_port, transport))
except KeyboardInterrupt:
    print( 'Port forwarding stopped.')
    sys.exit(0)



print(1)



    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
    # 获取传输实例
    tran=ssh_client.get_transport()
    sftp=paramiko.SFTPClient.from_transport(tran)
    sftp.put(local_dir,remote_dir)
    print("##########################上传完成###################")
    ssh_client.close()
remote_file('D:\python21\python\练习\hnf\dddd.txt','/root/aa','192.168.204.128','root','redhat','22',)

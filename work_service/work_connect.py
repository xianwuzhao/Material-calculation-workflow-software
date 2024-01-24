import paramiko
import socket


class SSHConnection(object):

    def __init__(self, host_dict, app):
        """ 初始化 """
        self.app = app
        self.host = host_dict['IP地址']
        self.port = host_dict['端口']
        self.username = host_dict['用户名']
        self.pwd = host_dict['密码']
        print(self.host,"111",self.port,"222",self.username,"333", self.pwd)

    def connect(self):
        """ 连接 """
        try:
            transport = paramiko.Transport((self.host, int(self.port),))
            transport.connect(username=self.username, password=self.pwd)
            self.trans = transport
        except paramiko.AuthenticationException:
            self.app.log.Info('认证失败，请检查用户名和密码是否正确')
            return False
        except paramiko.BadHostKeyException:
            self.app.log.Info('Host Key出错')
            return False
        except socket.error:
            self.app.log.Info('连接失败，确保是否连接了指定的服务器，请检查ip或主机名是否正确')
            return False
        except paramiko.SSHException:
            self.app.log.Info('SSH 会话建立失败，请确保服务器端是否启动了SSH服务，并确保相应的端口已经打开')
            return False
        else:
            self.app.log.Info('连接{}成功！'.format(self.host))
            return True

    def close(self):
        """ 断开连接 """
        self.trans.close()

    def run_cmd(self, command):
        """ 执行 """
        self.app.log.Info('运行中...')
        ssh = paramiko.SSHClient()
        ssh._transport = self.trans
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        # 获取命令结果
        res = to_str(stdout.read())
        # 获取错误信息
        error = to_str(stderr.read())
        # 如果有错误信息，返回error， 否则返回res
        if error.strip():
            self.app.log.Error(error)
            return error
        else:
            self.app.log.Info('计算完成！')
            return res

    def upload(self, local_path, target_path):
        """ 上传 """
        sftp = paramiko.SFTPClient.from_transport(self.trans)
        # 连接，上传
        sftp.put(local_path, target_path)
        # sftp.chmod(target_path, 0o755)
        self.app.log.Info('成功上传文件{}'.format(local_path))

    def download(self, target_path, local_path):
        """ 下载 """
        sftp = paramiko.SFTPClient.from_transport(self.trans)
        # 连接， 下载
        sftp.get(target_path, local_path)
        self.app.log.Info('成功下载文件{}'.format(target_path))

    def mkdir(self, path):
        """ 创建目录 """
        sftp = paramiko.SFTPClient.from_transport(self.trans)
        sftp.mkdir(path)

    def listdir(self, path):
        """ 列出目录下的文件 """
        sftp = paramiko.SFTPClient.from_transport(self.trans)
        return sftp.listdir(path)


    def __del__(self):
        self.close()

def to_str(bytes_or_str):
    """
    把byte类型转换为str
    :return:
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str

    return value

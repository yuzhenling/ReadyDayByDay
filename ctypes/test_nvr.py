import ctypes
from _ctypes import byref
from ctypes import Structure, POINTER, c_int, c_char_p, c_void_p

# 加载动态库
lib = ctypes.CDLL('./libvideonetclient.so')
# 定义登录参数结构体
class UserLoginPara(Structure):
    _fields_ = [
        ("szServerIP", ctypes.c_char * 16),
        ("dwCommandPort", ctypes.c_uint32),
        ("szUserName", ctypes.c_char * 32),
        ("szPassword", ctypes.c_char * 32),
    ]

# 设置函数签名
lib.VideoNetClient_Start.argtypes = []
lib.VideoNetClient_Start.restype = c_int

lib.VideoNetClient_UserLogin.argtypes = [
    POINTER(c_void_p),
    POINTER(UserLoginPara),
    c_char_p
]
lib.VideoNetClient_UserLogin.restype = c_int

lib.VideoNetClient_UserLogout.argtypes = [c_void_p]
lib.VideoNetClient_UserLogout.restype = c_int

lib.VideoNetClient_Stop.argtypes = []
lib.VideoNetClient_Stop.restype = c_int


# 使用示例
def main():
    # 1. 启动SDK
    result = lib.VideoNetClient_Start()
    if result != 0:
        print(f"启动SDK失败，错误码: {result}")
        return

    print("SDK启动成功")

    # 2. 准备登录参数
    login_para = UserLoginPara()
    login_para.szServerIP = b"<>"
    login_para.dwCommandPort = 8000
    login_para.szUserName = b""
    login_para.szPassword = b""

    # 3. 登录
    h_user = c_void_p()
    result = lib.VideoNetClient_UserLogin(
        byref(h_user),
        byref(login_para),
        None
    )

    if result == 0:
        print(f"登录成功，用户句柄: {h_user.value}")

        # 这里可以调用其他功能...
        # 例如：连接视频流、查询录像等

        # 登出
        lib.VideoNetClient_UserLogout(h_user)
    else:
        print(f"登录失败，错误码: {result}")

    # 4. 停止SDK
    lib.VideoNetClient_Stop()
    print("SDK已停止")


if __name__ == "__main__":
    main()


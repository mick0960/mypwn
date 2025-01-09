# mypwn/core.py

from pwn import *
from ctypes import *
import inspect

class Mypwn:
    def __init__(self, elf_name):
        """
        初始化 Mypwn 实例。
        :param elf_name: 目标 ELF 文件的路径
        """
        self._p = process(elf_name)
        self._elf = ELF(elf_name)
        libs = list(self._p.libs().keys())
        self._libc = libs[1] if len(libs) > 1 else None
        self._clibc = cdll.LoadLibrary(self._libc) if self._libc else None
        

    def get_p(self):
        """获取 p 对象"""
        return self._p

    def get_elf(self):
        """获取 elf 对象"""
        return self._elf

    def get_libc(self):
        """获取 libc 路径"""
        return self._libc

    def get_clibc(self):
        """获取 clibc 对象"""
        return self._clibc


def sla(p, ch, data):
    """发送数据并在接收到指定字符后发送一行数据"""
    p.sendlineafter(ch, data)

def sda(p, ch, data):
    """发送数据并在接收到指定字符后发送数据"""
    p.sendafter(ch, data)

def sd(p, data):
    """发送数据"""
    p.send(data)

def sl(p, data):
    """发送一行数据"""
    p.sendline(data)

def addr32(p):
    """接收 32 位地址"""
    return u32(p.recvuntil(b"\xf7")[-4:])

def addr64(p):
    """接收 64 位地址"""
    return u64(p.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))

def ru(p, con, drop=False, timeout=None):
    """
    接收数据直到遇到指定内容。
    :param p: 进程对象
    :param con: 匹配的内容（字符串或字节）
    :param drop: 是否丢弃匹配的内容（默认为 False，即保留匹配内容）
    :param timeout: 超时时间（单位为秒，默认为 None，即不设置超时）
    :return: 接收到的数据
    """
    if timeout is not None:
        p.settimeout(timeout)
    try:
        data = p.recvuntil(con)
        if drop:
            # 丢弃匹配的内容
            return data[:-len(con)]
        return data
    except Exception as e:
        log.error(f"接收数据时发生错误: {e}")
        return None

def lg(addr):
    """
    打印变量名及其对应的地址
    :param addr: 变量或地址
    """
    frame = inspect.currentframe().f_back
    variables = {id(val): name for name, val in frame.f_locals.items()}
    addr_name = variables.get(id(addr), "Unknown")
    log.success(f"{addr_name} --> {hex(addr) if isinstance(addr, int) else addr}")
    

def debug(p, elf, pie=0, bp=None):
    """
    用于调试程序的函数。
    :param p: 进程对象
    :param elf: ELF 对象
    :param pie: 是否启用 PIE 模式 (Position Independent Executable)
    :param bp: 断点，可以是字符串（单个断点）或列表（多个断点）
    """
    if pie:
        base = p.libs()[elf.path]
        if bp:
            if isinstance(bp, str):
                bp = f"*{hex(base + int(bp, 16))}"
            elif isinstance(bp, list):
                bp = [f"*{hex(base + int(b, 16))}" for b in bp]
        gdb.attach(p, gdbscript="\n".join(bp) if bp else None)
    else:
        if bp:
            if isinstance(bp, str):
                bp = f"b {bp}"
            elif isinstance(bp, list):
                bp = [f"b {b}" for b in bp]
        gdb.attach(p, gdbscript="\n".join(bp) if bp else None)
    pause()

def ia(p):
    """进入交互模式"""
    p.interactive()
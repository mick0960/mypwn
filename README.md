# mypwn
mypwn 是一个基于 pwntools 的 Python 库，旨在简化pwn攻击脚本的书写
以下是为 `mypwn` 库编写的 `README.md` 文件，涵盖了库的功能、安装方法、使用示例等内容。

---


## 安装

### 通过 `pip` 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/mick0960/mypwn.git
   cd mypwn
   ```

2. 安装依赖：
   ```bash
   pip install pwntools
   ```

3. 安装 `mypwn`：
   ```bash
   pip install .
   ```

---

## 使用示例

### 初始化

```python
from mypwn import Mypwn, sla, sd, ru, ia

# 初始化 Mypwn 实例
pwntools = Mypwn('./elf_name')

# 获取进程对象、ELF 对象、libc 路径等
p = pwntools.get_p()
elf = pwntools.get_elf()
libc = pwntools.get_libc()
clibc = pwntools.get_clibc()

# 打印 libc 路径
print(f"libc path: {libc}")
```

### 发送和接收数据

```python
# 发送数据
payload = b'A' * 8
sd(p, payload)

# 接收数据直到遇到指定内容
data = ru(p, b"Hello", drop=True)
print(f"Received data: {data}")
```

### 调试

```python
# 设置断点并调试
debug(p, elf, pie=1, bp="main")
```

### 进入交互模式

```python
# 进入交互模式
ia(p)
```

---

## API 文档

### `Mypwn` 类

- **`Mypwn(elf_name)`**  
  初始化 `Mypwn` 实例。  
  **参数**：
  - `elf_name`：目标 ELF 文件的路径。

- **`get_p()`**  
  获取进程对象 `p`。

- **`get_elf()`**  
  获取 ELF 对象 `elf`。

- **`get_libc()`**  
  获取 libc 路径。

- **`get_clibc()`**  
  获取 `ctypes` 加载的 libc 对象。

---

### 功能函数

- **`sla(p, ch, data)`**  
  发送数据并在接收到指定字符后发送一行数据。  
  **参数**：
  - `p`：进程对象。
  - `ch`：匹配的字符。
  - `data`：要发送的数据。

- **`sda(p, ch, data)`**  
  发送数据并在接收到指定字符后发送数据。  
  **参数**：
  - `p`：进程对象。
  - `ch`：匹配的字符。
  - `data`：要发送的数据。

- **`sd(p, data)`**  
  发送数据。  
  **参数**：
  - `p`：进程对象。
  - `data`：要发送的数据。

- **`sl(p, data)`**  
  发送一行数据。  
  **参数**：
  - `p`：进程对象。
  - `data`：要发送的数据。

- **`addr32(p)`**  
  接收 32 位地址。  
  **参数**：
  - `p`：进程对象。

- **`addr64(p)`**  
  接收 64 位地址。  
  **参数**：
  - `p`：进程对象。

- **`ru(p, con, drop=False, timeout=None)`**  
  接收数据直到遇到指定内容。  
  **参数**：
  - `p`：进程对象。
  - `con`：匹配的内容（字符串或字节）。
  - `drop`：是否丢弃匹配的内容（默认为 `False`）。
  - `timeout`：超时时间（单位为秒，默认为 `None`）。

- **`lg(addr)`**  
  打印变量名及其对应的地址。  
  **参数**：
  - `addr`：变量或地址。

- **`debug(p, elf, pie=0, bp=None)`**  
  用于调试程序的函数。  
  **参数**：
  - `p`：进程对象。
  - `elf`：ELF 对象。
  - `pie`：是否启用 PIE 模式（默认为 `0`）。
  - `bp`：断点，可以是字符串（单个断点）或列表（多个断点）。

- **`ia(p)`**  
  进入交互模式。  
  **参数**：
  - `p`：进程对象。

---

## 作者

- **mick0960**  
  GitHub: [@mick0960](https://github.com/mick0960)  
  Email: mickonly@qq.com

---


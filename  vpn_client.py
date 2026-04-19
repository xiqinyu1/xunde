"""
WireGuard VPN Client Implementation
A simple VPN client that manages WireGuard connections with Chinese UI and English code documentation.
"""

import subprocess
import json
import os
import sys
import time
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
import platform
import ipaddress


class WireGuardConfig:
    """WireGuard configuration management class"""
    
    def __init__(self, config_path: str = "wg0.conf"):
        """
        Initialize WireGuard configuration
        
        Args:
            config_path: Path to WireGuard configuration file
        """
        self.config_path = config_path
        self.config_data = {}
        self.interface_name = "wg0"
        
    def load_config(self) -> bool:
        """
        Load WireGuard configuration from file
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.config_path):
                print(f"[错误] 配置文件不存在: {self.config_path}")
                return False
                
            with open(self.config_path, 'r', encoding='utf-8') as f:
                current_section = None
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]
                        self.config_data[current_section] = {}
                    elif '=' in line and current_section:
                        key, value = line.split('=', 1)
                        self.config_data[current_section][key.strip()] = value.strip()
                        
            print(f"[成功] 配置文件已加载: {self.config_path}")
            return True
            
        except Exception as e:
            print(f"[错误] 加载配置文件失败: {e}")
            return False
    
    def validate_config(self) -> Tuple[bool, str]:
        """
        Validate WireGuard configuration
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if 'Interface' not in self.config_data:
            return False, "配置文件中缺少 [Interface] 部分"
            
        interface = self.config_data['Interface']
        
        # Check required fields
        required_fields = ['PrivateKey', 'Address']
        for field in required_fields:
            if field not in interface:
                return False, f"[Interface] 中缺少必需的字段: {field}"
        
        # Validate IP address
        try:
            ipaddress.ip_interface(interface['Address'])
        except ValueError:
            return False, f"无效的IP地址格式: {interface['Address']}"
        
        # Check for Peer section
        if 'Peer' not in self.config_data:
            return False, "配置文件中缺少 [Peer] 部分"
            
        peer = self.config_data['Peer']
        if 'PublicKey' not in peer or 'Endpoint' not in peer:
            return False, "[Peer] 中缺少 PublicKey 或 Endpoint 字段"
            
        return True, "配置验证通过"
    
    def create_sample_config(self) -> str:
        """
        Create a sample WireGuard configuration
        
        Returns:
            str: Sample configuration content
        """
        sample_config = """# WireGuard 客户端配置示例
# 请用实际的密钥和地址替换下面的值

[Interface]
# 客户端私钥 (请保密!)
PrivateKey = YOUR_CLIENT_PRIVATE_KEY_HERE
# 客户端的VPN IP地址
Address = 10.0.0.2/24
# DNS服务器 (可选)
DNS = 8.8.8.8, 8.8.4.4
# MTU大小 (可选)
MTU = 1420

[Peer]
# 服务器公钥
PublicKey = YOUR_SERVER_PUBLIC_KEY_HERE
# 服务器端点 (IP:端口)
Endpoint = vpn.example.com:51820
# 允许的IP范围 (0.0.0.0/0 表示所有流量)
AllowedIPs = 0.0.0.0/0
# 保持连接 (可选)
PersistentKeepalive = 25
"""
        return sample_config


class VPNClient:
    """Main VPN client class for managing connections"""
    
    def __init__(self, config_path: str = "wg0.conf"):
        """
        Initialize VPN client
        
        Args:
            config_path: Path to WireGuard configuration file
        """
        self.config = WireGuardConfig(config_path)
        self.is_connected = False
        self.connection_stats = {
            'start_time': None,
            'bytes_received': 0,
            'bytes_sent': 0,
            'duration': 0
        }
        
    def check_wireguard_installed(self) -> bool:
        """
        Check if WireGuard is installed on the system
        
        Returns:
            bool: True if WireGuard is installed, False otherwise
        """
        try:
            # Try to run wg command
            result = subprocess.run(['wg', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                print("[成功] WireGuard 已安装")
                return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
            
        print("[警告] WireGuard 未安装或 wg 命令不可用")
        return False
    
    def install_wireguard(self) -> bool:
        """
        Install WireGuard (platform-specific)
        
        Returns:
            bool: True if installation successful or already installed, False otherwise
        """
        system = platform.system().lower()
        
        print(f"检测到系统: {system}")
        print("请根据您的系统手动安装WireGuard:")
        
        if system == 'linux':
            print("""
Ubuntu/Debian:
    sudo apt update
    sudo apt install wireguard

CentOS/RHEL/Fedora:
    sudo yum install wireguard-tools
    # 或
    sudo dnf install wireguard-tools

Arch Linux:
    sudo pacman -S wireguard-tools
            """)
        elif system == 'darwin':  # macOS
            print("""
通过Homebrew安装:
    brew install wireguard-tools
            """)
        elif system == 'windows':
            print("""
从Microsoft Store安装WireGuard:
    https://www.wireguard.com/install/
            """)
        else:
            print(f"不支持的系统: {system}")
            return False
            
        return self.check_wireguard_installed()
    
    def setup_interface(self) -> bool:
        """
        Set up WireGuard interface
        
        Returns:
            bool: True if setup successful, False otherwise
        """
尝试:
            # Create interface
            cmd = ['sudo', 'wg', 'set', 'wg0', 'private-key', 
                   self.配置.config_path, 'listen-port', '51820']
            
            result = subprocess.跑(CMD，capture_output=正确，text=正确，timeout=10)
            
            如果结果。返回代码==0:
                打印("[成功] WireGuard 接口已设置")
                返回 正确
            其他:
                打印(f"[错误] 设置接口失败: {结果。stderr}")
                返回 假的
                
        除……之外例外作为e：
            打印(f"[错误] 设置接口时发生错误: {e}")
            返回 假的
    
    定义 连接(自己) -> bool:
        """
        Connect to VPN server
        
退货：
            bool: True if connection successful, False otherwise
        """
        打印("正在连接到VPN...")
        
        # Check WireGuard installation
        如果 not自己。check_WireGuard_installed():
            打印("[信息] 正在尝试安装WireGuard...")
            如果 not自己。install_wireguard():
                返回 假的
        
        # Load and validate configuration
        如果 not自己。配置.load_config():
            返回 假的
            
        is_valid, message = self.配置.validate_config()
        如果 not is_valid:
            打印(f"[错误] 配置验证失败: {message}")
            返回 假的
        
        打印("[信息] 配置验证通过")
        
        # Setup interface
        如果 not自己。setup_interface():
            返回 假的
        
        # Bring interface up
尝试:
CMD=['sudo', 'wg-快速', '向上'，self.配置.config_path]
结果=子流程。跑(CMD，capture_output=正确，text=正确，timeout=30)
            
            如果结果。返回代码==0:
自己。is_connected=正确
自己。connection_stats['start_time']=日期时间。现在()
                打印("[成功]VPN连接已建立")
                返回 正确
            其他:
                打印(F"[错误]连接失败：{结果。stderr}")
返回 假的
                
        除……之外例外作为e：
            打印(f"[错误] 连接时发生错误: {e}")
返回 假的
    
    定义 断开连接(自己)->bool：
        """
断开与VPN服务器的连接
        
退货：
bool：断开连接成功时为True，否则为False
        """
如果不是自己.is_connected：
            打印("[信息]当前未连接VPN")
            返回 正确
            
        打印("正在断开VPN连接...")
        
尝试:
CMD=['sudo', 'wg-快速', '向下'，self.配置.config_path]
结果=子流程。跑(CMD，capture_output=正确，text=正确，timeout=30)
            
            如果结果。返回代码==0:
自己。is_connected=假的
                
                #更新连接时长
如果自己。connection_stats['start_time']:
持续时间=日期时间。现在()-自我。connection_stats['start_time']
自己。connection_stats['持续时间']=持续时间。总计秒数(_S)()
                
                打印("[成功]VPN连接已断开")
                返回 正确
            其他:
                打印(f"[错误] 断开连接失败: {结果。stderr}")
返回 假的
                
        除……之外例外作为e：
            打印(f"[错误] 断开连接时发生错误: {e}")
返回 假的
    
    定义 get_status(自己)->口述[str，任意]:
        """
获取当前VPN连接状态
        
退货：
dict[str，Any]：状态信息
        """
状态={{
'已连接'：self.is_connected，'已连接'：self.is_connected，
'接口'：'wg0'，
    
'统计信息'：self.connection_stats。复制()
}
        
如果自己。已连接(_C)：
#考试考试详细的wireguard状态
尝试:
CMD=['sudo'，'wg'，'显示'，'wg0']
结果=子流程。跑(CMD，捕获输出=正确，text=正确，timeout=5)
                
                如果结果。返回代码==0:
状态['wg_status']=结果。stdout
除……之外：
状态['wg_status']="无法获取详细状态"
        
返回状态
    
定义show_config_sample(自己)->没有一个：
        """
显示示例配置
        """
打印("\n"+"="*50)
标记(wireguard"配置示例")
打印("="*50)
打印(自己。配置.create_sample_config())
打印("="*50)
打印("说明:")
打印("1.将your_CLIENT_PRIVATE_KEY_HERE替换为你的客户端私钥")
打印("2.将your_SERVER_PUBLIC_KEY_HERE替换为服务器公钥")
打印("3.将vpn.example.com:51820替换为实际的VPN服务器地址")
打印("4.保存为wg0.conf文件")
打印("="*50)


定义 显示菜单(_M)()->没有一个:
    """
主菜单中文显示
    """
打印("\n"+"="*50)
打印("WireGuard VPN客户端")
打印("="*50)
打印("1.连接VPN")
打印("2.断开VPN")
打印("3. 查看状态")
    打印("4. 显示配置示例")
打印("5.检查WireGuard安装")打印("5.检查WireGuard安装")
打印("6. 退出")打印("6. 退出")
打印("="*50)打印("="*50)


定义 主要的():主要的():
    运行VPN客户端的主要功能
运行VPN客户端的主要功能
    """
VPN_client=VPNClient()
    
在……期间 正确:
显示菜单(_M)()
        
尝试:
选择=输入("请求操作(1-6)：").带()
            
如果choice=='1'：
VPN客户端(_C)。连接()
Elifchoice=='2'：
vpn客户门端(_c)。断开连接()
Elifchoice=='3'：
状态=VPN_client.get_status()
打印("\nVPN状态：")
                打印(F"连接状态：{'已连接' 如果状态['已连接'] 其他 '未连接'}")
打印(F"接口名称：{状态['接口']}")
打印(F"配置文件：{状态['config_file']}")
                
如果状态['已连接']和状态['统计信息']['start_time']：
持续时间=日期时间。现在()-状态['统计信息']['start_time']
打印(F"连接时长：{持续}")
                    
如果'WG_status'在……内状态：
打印(F"\n详细状态：\n{状态['wg_status']}")
                    
Elifchoice=='4'：
vpn客门端(_C).show_config_sample()
Elifchoice=='5'：
VPN客户端(_C).check_Wireguard_installed()
Elifchoice=='6'：
如果VPN客户端(_C).is_connected：
确认=输入("VPN当前已连接，确定要退出吗？(y/N)：")。带().降低()
如果确认！='Y'：
                        继续
vpn客户门端(_c)。断开连接()
打印("感谢使用WireGuard VPN客户端！")
                打破
            其他:
                打印("无效的选项，请重新选择!")
                
        除……之外键盘中断：
打印(""\n\n检测到中断信号...")
如果VPN客户端(_C).is_connected：
vpn客户门端(_c)。断开连接()
            打印("程序已退出")
            打破
        除……之外例外作为e：
打印(f"发生错误：{e}")


如果__名称__=="__主要的__"：
#检查是否以sudo/管理员权限运行
    如果操作系统。姓名==”posix' 和操作系统。geteuid()!=0:
        打印("警告: 建议使用 sudo 运行此程序以获取必要的权限")
打印("示例：sudo python Wireguard_client.py")
    
    主要的()

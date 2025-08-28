#!/usr/bin/env python3
"""
Mobile MIDI Controller Server
提供WebSocket服务和MIDI输出功能
"""

import asyncio
import websockets
import json
import threading
import time
import webbrowser
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys
import os

# MIDI相关导入
try:
    import rtmidi
except ImportError:
    print("错误: 需要安装 python-rtmidi")
    print("请运行: pip install python-rtmidi")
    sys.exit(1)

class MIDIController:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
        self.current_port = None
        self.connected_clients = set()
        self.active_clients_by_ip = {}  # 按IP地址管理活跃客户端 {ip: websocket}
        self.debug_mode = False
        self.last_pitchbend = 8192  # 中间值
        self.last_modulation = 0
        
        # 调试信息输出控制
        self.last_debug_time = 0
        self.debug_interval = 2.0  # 2秒显示一次调试信息
        
        print("🎹 MIDI控制器服务器启动中...")
        print(f"📱 可用MIDI端口:")
        for i, port in enumerate(self.available_ports):
            print(f"   {i}: {port}")
        
        # 智能连接MIDI端口
        self.auto_connect_loopmidi()
    
    def auto_connect_loopmidi(self):
        """智能连接MIDI端口"""
        # 查找虚拟MIDI端口
        virtual_ports = []
        system_ports = ['microsoft gs wavetable synth']  # 系统端口，避免连接
        
        for i, port in enumerate(self.available_ports):
            port_lower = port.lower()
            # 排除系统端口
            if any(sys_port in port_lower for sys_port in system_ports):
                continue
                
            # 识别虚拟MIDI端口的各种可能命名
            virtual_keywords = [
                'loopmidi', 'loop midi', 'midi controller', 
                'remotecc', 'remote cc', 'virtual midi',
                'breathcontrol', 'breath control'
            ]
            
            if any(keyword in port_lower for keyword in virtual_keywords):
                virtual_ports.append((i, port))
        
        if virtual_ports and len(virtual_ports) == 1:
            # 只有一个虚拟MIDI端口，自动连接
            port_index, port_name = virtual_ports[0]
            print(f"\n✅ 自动连接到虚拟MIDI端口: {port_name}")
            self.connect_midi_port(port_index)
        else:
            # 多个端口或没有明确的虚拟端口，让用户选择
            print("\n请选择要使用的MIDI端口:")
            self.prompt_port_selection()
    
    def connect_midi_port(self, port_index):
        """连接MIDI端口"""
        try:
            if self.current_port is not None:
                self.midiout.close_port()
            
            self.midiout.open_port(port_index)
            self.current_port = port_index
            port_name = self.available_ports[port_index]
            print(f"✅ 已连接到MIDI端口: {port_name}")
            return True
        except Exception as e:
            print(f"❌ MIDI端口连接失败: {e}")
            return False
    
    def prompt_port_selection(self):
        """提示用户选择MIDI端口"""
        if not self.available_ports:
            print("❌ 没有可用的MIDI端口")
            return
        
        try:
            port_input = input(f"输入端口号 (0-{len(self.available_ports)-1}，回车跳过): ").strip()
            
            if port_input:
                port_index = int(port_input)
                if 0 <= port_index < len(self.available_ports):
                    self.connect_midi_port(port_index)
                else:
                    print("❌ 端口号无效，稍后可用 'connect' 命令选择")
            else:
                print("⭐ 跳过MIDI端口连接，稍后可用 'connect' 命令选择")
        except (ValueError, KeyboardInterrupt):
            print("⭐ 跳过MIDI端口连接，稍后可用 'connect' 命令选择")
    
    def get_client_ip(self, websocket):
        """获取客户端IP地址"""
        try:
            return websocket.remote_address[0]
        except:
            return "unknown"
    
    def set_active_client_by_ip(self, websocket):
        """基于IP地址设置活跃客户端，踢掉同一IP的其他连接"""
        client_ip = self.get_client_ip(websocket)
        old_websocket = self.active_clients_by_ip.get(client_ip)
        
        if old_websocket and old_websocket != websocket:
            # 踢掉同一IP的旧连接
            try:
                if old_websocket in self.connected_clients:
                    print(f"📱 踢下线同IP旧连接: {client_ip}")
                    # 创建异步任务来断开旧连接
                    import asyncio
                    try:
                        # 发送断开消息
                        asyncio.create_task(old_websocket.send(json.dumps({
                            'type': 'disconnect',
                            'reason': '同IP新设备已连接'
                        })))
                        # 关闭连接
                        asyncio.create_task(old_websocket.close())
                    except Exception as e:
                        if self.debug_mode:
                            print(f"发送断开消息失败: {e}")
                        # 直接强制关闭
                        try:
                            asyncio.create_task(old_websocket.close())
                        except:
                            pass
            except Exception as e:
                if self.debug_mode:
                    print(f"断开旧连接时出错: {e}")
        
        # 设置新的活跃客户端
        self.active_clients_by_ip[client_ip] = websocket
        client_id = f"{client_ip}:{websocket.remote_address[1]}"
        print(f"🎯 设置活跃控制客户端: {client_id}")
        
        # 发送归零信号，确保从干净的状态开始（静默发送，只在debug模式显示）
        if self.current_port is not None:
            try:
                # 弯音归零
                pitchbend_msg = [0xE0, 0x00, 0x40]  # 8192 = 0x2000, lsb=0, msb=64
                self.midiout.send_message(pitchbend_msg)
                # 调制归零
                cc_msg = [0xB0, 1, 0]
                self.midiout.send_message(cc_msg)
                if self.debug_mode:
                    print("🔄 新设备连接，MIDI已归零")
            except Exception as e:
                if self.debug_mode:
                    print(f"归零发送错误: {e}")
    
    def is_active_client(self, websocket):
        """检查是否是活跃客户端"""
        client_ip = self.get_client_ip(websocket)
        return self.active_clients_by_ip.get(client_ip) == websocket
    
    def remove_client_by_websocket(self, websocket):
        """根据websocket移除客户端"""
        client_ip = self.get_client_ip(websocket)
        if self.active_clients_by_ip.get(client_ip) == websocket:
            del self.active_clients_by_ip[client_ip]
            print(f"📱 活跃客户端断开: {client_ip}")
            
            # 发送归零信号（静默发送，只在debug模式显示）
            if self.current_port is not None:
                try:
                    # 弯音归零
                    pitchbend_msg = [0xE0, 0x00, 0x40]  # 8192 = 0x2000, lsb=0, msb=64
                    self.midiout.send_message(pitchbend_msg)
                    # 调制归零
                    cc_msg = [0xB0, 1, 0]
                    self.midiout.send_message(cc_msg)
                    if self.debug_mode:
                        print("🔄 客户端断开，MIDI已归零")
                except Exception as e:
                    if self.debug_mode:
                        print(f"断开归零错误: {e}")
            return True
        else:
            client_id = f"{client_ip}:{websocket.remote_address[1]}" if hasattr(websocket, 'remote_address') else client_ip
            print(f"📱 非活跃客户端断开: {client_id}")
            return False
    
    def send_pitchbend(self, value):
        """发送弯音信息 (0-16383, 8192为中间值)"""
        if self.current_port is None:
            return
        
        try:
            # 确保值在有效范围内
            value = max(0, min(16383, int(value)))
            
            # 总是发送MIDI消息
            lsb = value & 0x7F
            msb = (value >> 7) & 0x7F
            pitchbend_msg = [0xE0, lsb, msb]  # Channel 1 pitchbend
            self.midiout.send_message(pitchbend_msg)
            
            # 调试信息输出控制（只在debug模式下显示）
            if self.debug_mode:
                current_time = time.time()
                should_show_debug = (current_time - self.last_debug_time >= self.debug_interval)
                
                if should_show_debug:
                    normalized = (value - 8192) / 8192.0
                    print(f"🎵 弯音: {normalized:.3f} (MIDI: {value}) | 调制: {self.last_modulation}/127")
                    self.last_debug_time = current_time
            
            self.last_pitchbend = value
            
        except Exception as e:
            if self.debug_mode:
                print(f"弯音发送错误: {e}")
    
    def send_modulation(self, value):
        """发送调制信息 (0-127)"""
        if self.current_port is None:
            return
        
        try:
            # 确保值在有效范围内
            value = max(0, min(127, int(value)))
            
            # 总是发送MIDI消息
            cc_msg = [0xB0, 1, value]  # Channel 1, CC1 (modulation)
            self.midiout.send_message(cc_msg)
            
            # 调试信息在send_pitchbend中统一显示，这里不输出任何信息
            self.last_modulation = value
            
        except Exception as e:
            if self.debug_mode:
                print(f"调制发送错误: {e}")
    
    def get_status(self):
        """获取连接状态"""
        active_clients_info = []
        for ip, websocket in self.active_clients_by_ip.items():
            try:
                port = websocket.remote_address[1] if hasattr(websocket, 'remote_address') else "unknown"
                active_clients_info.append(f"{ip}:{port}")
            except:
                active_clients_info.append(ip)
        
        return {
            'midi_connected': self.current_port is not None,
            'midi_port': self.available_ports[self.current_port] if self.current_port is not None else None,
            'clients_connected': len(self.connected_clients),
            'active_clients': active_clients_info,
            'available_ports': self.available_ports
        }

# 全局MIDI控制器实例
midi_controller = MIDIController()

async def handle_websocket(websocket):
    """处理WebSocket连接"""
    client_ip = midi_controller.get_client_ip(websocket)
    client_id = f"{client_ip}:{websocket.remote_address[1]}"
    midi_controller.connected_clients.add(websocket)
    print(f"📱 客户端连接: {client_id} (总连接数: {len(midi_controller.connected_clients)})")
    
    try:
        # 发送初始状态
        await websocket.send(json.dumps({
            'type': 'status',
            'data': midi_controller.get_status()
        }))
        
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type')
                
                if msg_type == 'control':
                    # 检查是否是活跃客户端
                    if not midi_controller.is_active_client(websocket):
                        # 如果不是活跃客户端，设置为活跃客户端（踢掉同IP的旧连接）
                        midi_controller.set_active_client_by_ip(websocket)
                    
                    # 处理控制数据
                    pitchbend = data.get('pitchbend', 0.0)  # -1.0 to 1.0
                    modulation = data.get('modulation', 0.0)  # 0.0 to 1.0
                    is_continuous = data.get('continuous', False)  # 是否为持续发送
                    
                    # 转换为MIDI值
                    midi_pitchbend = int((pitchbend + 1.0) * 8191.5)  # 0-16383
                    midi_modulation = int(modulation * 127)  # 0-127
                    
                    # 发送MIDI消息
                    midi_controller.send_pitchbend(midi_pitchbend)
                    midi_controller.send_modulation(midi_modulation)
                    
                    # 持续发送的调试信息（减少输出）
                    if is_continuous and midi_controller.debug_mode:
                        # 只在值有明显变化时显示持续发送的调试信息
                        pass  # 减少日志输出
                
                elif msg_type == 'ping':
                    # 响应ping消息保持连接
                    await websocket.send(json.dumps({'type': 'pong'}))
                
            except json.JSONDecodeError:
                if midi_controller.debug_mode:
                    print(f"无效JSON: {message}")
            except Exception as e:
                if midi_controller.debug_mode:
                    print(f"处理消息错误: {e}")
    
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        if midi_controller.debug_mode:
            print(f"WebSocket错误: {e}")
    finally:
        midi_controller.connected_clients.discard(websocket)
        
        # 如果断开的是活跃客户端，清理并归零
        was_active = midi_controller.remove_client_by_websocket(websocket)
        
        print(f"剩余连接数: {len(midi_controller.connected_clients)}")

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器"""
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # 静默HTTP日志
        pass

def start_http_server():
    """启动HTTP服务器"""
    try:
        server = HTTPServer(('', 8000), CustomHTTPRequestHandler)
        print(f"🌐 HTTP服务器启动: http://localhost:8000")
        server.serve_forever()
    except Exception as e:
        print(f"HTTP服务器启动失败: {e}")

def get_local_ip():
    """获取本地IP地址"""
    try:
        # 连接到一个远程地址来获取本地IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "localhost"

def open_browser():
    """打开浏览器"""
    time.sleep(2)  # 等待服务器启动
    local_ip = get_local_ip()
    url = f"http://{local_ip}:8000"
    print(f"🔗 正在打开浏览器: {url}")
    webbrowser.open(url)

def command_interface():
    """命令行界面"""
    print("\n" + "="*50)
    print("🎹 MIDI控制器服务器运行中")
    print("="*50)
    
    local_ip = get_local_ip()
    print(f"📱 手机访问地址: http://{local_ip}:8000")
    print(f"🌐 本机访问地址: http://localhost:8000")
    print(f"🔌 WebSocket端口: {local_ip}:8001")
    
    print("\n可用命令:")
    print("  help    - 显示帮助信息")
    print("  status  - 显示连接状态") 
    print("  debug   - 切换调试模式")
    print("  ports   - 显示MIDI端口")
    print("  connect - 连接MIDI端口")
    print("  quit    - 退出服务器")
    print("-" * 50)
    
    while True:
        try:
            command = input("MIDI> ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 正在关闭服务器...")
                os._exit(0)
            
            elif command in ['help', 'h']:
                print("\n可用命令:")
                print("  help/h     - 显示此帮助")
                print("  status/s   - 显示连接状态")
                print("  debug/d    - 切换调试模式 (每2秒显示MIDI数据)")
                print("  ports/p    - 显示MIDI端口")
                print("  connect/c  - 连接MIDI端口")
                print("  quit/q     - 退出服务器")
            
            elif command in ['status', 's']:
                status = midi_controller.get_status()
                print(f"\n📊 服务器状态:")
                print(f"  MIDI连接: {'✅ 是' if status['midi_connected'] else '❌ 否'}")
                if status['midi_port']:
                    print(f"  MIDI端口: {status['midi_port']}")
                print(f"  总连接数: {status['clients_connected']}")
                if status['active_clients']:
                    print(f"  活跃控制端: {', '.join(status['active_clients'])}")
                else:
                    print(f"  活跃控制端: 无")
                print(f"  调试模式: {'开启' if midi_controller.debug_mode else '关闭'}")
                if midi_controller.debug_mode:
                    print(f"  调试输出: 每{midi_controller.debug_interval}秒显示一次")
                print(f"  持续发送: 已启用 (20fps)")
            
            elif command in ['debug', 'd']:
                midi_controller.debug_mode = not midi_controller.debug_mode
                if midi_controller.debug_mode:
                    print(f"🛠 调试模式: 开启 (每{midi_controller.debug_interval}秒显示一次)")
                else:
                    print(f"🛠 调试模式: 关闭")
            
            elif command in ['ports', 'p']:
                print(f"\n🎹 可用MIDI端口:")
                for i, port in enumerate(midi_controller.available_ports):
                    marker = " ← 当前" if i == midi_controller.current_port else ""
                    print(f"  {i}: {port}{marker}")
            
            elif command in ['connect', 'c']:
                print(f"\n🎹 可用MIDI端口:")
                for i, port in enumerate(midi_controller.available_ports):
                    marker = " ← 当前" if i == midi_controller.current_port else ""
                    print(f"  {i}: {port}{marker}")
                
                try:
                    port_num = input("请选择端口号 (回车取消): ").strip()
                    if port_num:
                        port_index = int(port_num)
                        if 0 <= port_index < len(midi_controller.available_ports):
                            if midi_controller.connect_midi_port(port_index):
                                print(f"✅ 成功连接到端口 {port_index}")
                            else:
                                print(f"❌ 连接端口 {port_index} 失败")
                        else:
                            print("❌ 端口号无效")
                except ValueError:
                    print("❌ 请输入有效数字")
                except KeyboardInterrupt:
                    pass
            
            elif command:
                print(f"❓ 未知命令: {command}")
                print("输入 'help' 查看可用命令")
        
        except KeyboardInterrupt:
            print("\n👋 正在关闭服务器...")
            os._exit(0)
        except EOFError:
            print("\n👋 正在关闭服务器...")
            os._exit(0)
        except Exception as e:
            print(f"命令处理错误: {e}")

def main():
    """主函数"""
    print("🚀 启动MIDI控制器服务器...")
    
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)  # 切换到脚本目录
    
    # 创建index.html如果不存在
    index_path = script_dir / 'index.html'
    if not index_path.exists():
        print("❌ 未找到 index.html 文件")
        print(f"请确保 index.html 文件位于: {script_dir}")
        input("按回车键退出...")
        return
    
    # 启动HTTP服务器线程
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    # 启动浏览器线程
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # 修复WebSocket服务器启动
    def run_websocket_server():
        # 创建新的event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def start_server():
            # 在正确的loop中创建WebSocket服务器
            server = await websockets.serve(handle_websocket, '', 8001)
            await server.wait_closed()
        
        try:
            loop.run_until_complete(start_server())
        except Exception as e:
            print(f"WebSocket服务器错误: {e}")
        finally:
            loop.close()
    
    # 在单独线程中运行WebSocket服务器
    websocket_thread = threading.Thread(target=run_websocket_server, daemon=True)
    websocket_thread.start()
    
    # 等待服务器启动
    time.sleep(1)
    print(f"🔌 WebSocket服务器启动: ws://localhost:8001")
    
    # 运行命令行界面
    command_interface()

if __name__ == "__main__":
    main()
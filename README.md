# RemoteMIDI-Controller

[![English](https://img.shields.io/badge/Language-English-blue)](#english) [![中文](https://img.shields.io/badge/语言-中文-red)](#中文)

---

## 中文

一个免费的移动MIDI控制器，将您的智能手机转换为无线MIDI设备。通过局域网将手机连接到计算机，零成本发送实时MIDI信号。

### 快速开始

1. **下载并运行**
   - 下载仓库文件
   - 首先运行 `loopMIDISetup.exe` 安装虚拟MIDI驱动（仅Windows）
   - 双击 `MIDI_Controller.exe` 启动应用程序
   - 无需额外安装

2. **设置MIDI连接**
   - 安装后启动loopMIDI应用程序并创建新端口
   - 在MIDI_Controller.exe提示时，从列表中选择loopMIDI端口
   - 虚拟MIDI端口允许您的DAW接收来自手机的MIDI信号

3. **连接您的手机**
   - 记录控制台显示的IP地址（例如：`http://192.168.1.100:8000`）
   - 在手机浏览器中打开此地址
   - 两台设备必须在同一局域网（LAN）上

4. **开始演奏**
   - 在控制界面上触摸和拖拽
   - 左右移动控制调制（CC1）
   - 上下移动控制弯音
   - 在设置菜单中调整灵敏度

### 功能特性

- **实时MIDI控制**：以最低延迟发送弯音和调制数据
- **移动端优化界面**：专为智能手机设计的响应式触控控制
- **可调节灵敏度**：根据您的演奏风格自定义控制响应
- **基于浏览器**：移动设备无需安装应用程序
- **多设备支持**：自动处理设备切换
- **零成本解决方案**：昂贵MIDI控制器的免费替代方案

### 系统要求

- **计算机**：Windows 10/11
- **移动设备**：任何具有现代网络浏览器的智能手机
- **网络**：局域网连接（两台设备在同一LAN上）
- **MIDI设备**：物理或虚拟MIDI端口

### 推荐设置

**虚拟MIDI设备（已包含）：**
- **Windows**：使用包含的 `loopMIDISetup.exe` 安装loopMIDI虚拟MIDI驱动
- **macOS**：IAC驱动（内置）

**完整设置流程：**

1. **安装虚拟MIDI驱动**（仅Windows）
   - 运行包含的 `loopMIDISetup.exe`
   - 按照安装向导操作
   - 启动loopMIDI应用程序并创建新端口（默认设置即可）

2. **启动MIDI控制器**
   - 双击 `MIDI_Controller.exe`
   - 在提示时从列表中选择loopMIDI端口

3. **配置您的DAW**
   - 设置音乐软件从loopMIDI端口接收MIDI
   - 为所需乐器启用弯音和调制（CC1）
   - 配置弯音范围（通常为±2或±12半音）

### 故障排除

**连接问题：**

*问：手机无法连接到服务器*
- 确认两台设备在同一局域网（LAN）上
- 检查Windows防火墙设置 - 允许应用程序通过防火墙
- 尝试禁用VPN或代理连接
- 如有需要，重启应用程序和网络设备

*问：连接频繁断开*
- 确保网络信号强度良好
- 关闭其他占用带宽的应用程序
- 如使用WiFi，尝试使用5GHz频段（如可用）

**MIDI问题：**

*问：DAW中没有MIDI输出*
- 首先确保已安装loopMIDI（如未安装请运行 `loopMIDISetup.exe`）
- 检查loopMIDI应用程序是否运行且至少有一个活动端口
- 验证MIDI控制器应用程序中的MIDI端口选择
- 检查DAW MIDI输入设置 - 选择loopMIDI端口
- 使用虚拟MIDI监视器应用程序测试
- 尝试使用'connect'命令重新连接MIDI端口

*问：高延迟或响应延迟*
- 使用流量最少的专用网络
- 关闭两台设备上不必要的应用程序
- 如可能，考虑为计算机使用有线连接

**应用程序问题：**

*问：应用程序无法启动*
- 如需要，以管理员身份运行
- 检查所需端口（8000, 8001）是否可用
- 暂时禁用杀毒软件进行测试

### 控制台命令

应用程序运行时，您可以使用这些控制台命令：

- `status` - 查看连接和MIDI状态
- `ports` - 列出可用MIDI端口
- `connect` - 更改MIDI端口连接
- `debug` - 切换详细日志记录
- `help` - 显示所有可用命令
- `quit` - 退出应用程序

### 网络安全

应用程序创建本地Web服务器进行通信。它只接受来自本地网络设备的连接，不会通过互联网发送数据。

---

## 开发者信息

### 项目结构

```
RemoteMIDI-Controller/
├── MIDI_Controller.exe    # 主应用程序（独立可执行文件）
├── loopMIDISetup.exe     # 虚拟MIDI驱动安装程序（已包含）
├── README.md             # 此文档
├── server.py             # 源码：主服务器应用程序
├── index.html            # 源码：Web界面
└── requirements.txt      # 源码：Python依赖项
```

### 源文件

**核心组件：**
- `server.py` - 带MIDI输出的Python WebSocket服务器
- `index.html` - 移动端优化的Web界面和触控控制
- `requirements.txt` - 开发所需的Python依赖项

### 技术架构

**后端（Python）：**
- 使用 `websockets` 库的WebSocket服务器
- 通过 `python-rtmidi` 实现MIDI输出
- 用于提供Web界面的HTTP服务器
- 多客户端连接管理
- 实时消息处理

**前端（HTML/JavaScript）：**
- 触控优化的控制界面
- 实时通信WebSocket客户端
- 适配各种屏幕尺寸的响应式设计
- 灵敏度控制和视觉反馈

**通信协议：**
```json
{
  "type": "control",
  "pitchbend": -1.0,      // 范围：-1.0 到 1.0
  "modulation": 0.5,      // 范围：0.0 到 1.0
  "continuous": false     // 连续更新时为true
}
```

### 开发环境设置

**依赖要求：**
```bash
pip install -r requirements.txt
```

**从源码运行：**
```bash
python server.py
```

源代码为构建附加功能和自定义提供了基础。

### 扩展想法

模块化设计允许轻松扩展：

**附加控件：**
- 添加更多MIDI CC控制器
- 实现程序变更选择器
- 创建虚拟键盘界面

**高级输入方法：**
- 加速度计/陀螺仪控制（设备运动）
- 多点触控手势识别
- 语音控制集成

**增强功能：**
- MIDI文件录制/播放
- 预设管理系统
- 波形视觉反馈
- 多种控制器布局

### 代码示例

**添加新MIDI控制器：**
```python
def send_custom_cc(self, cc_number, value):
    """发送自定义MIDI CC消息"""
    if self.current_port is None:
        return
    
    value = max(0, min(127, int(value)))
    cc_msg = [0xB0, cc_number, value]  # 通道1
    self.midiout.send_message(cc_msg)
```

**前端控制添加：**
```javascript
// 添加新滑块控制
function handleCustomControl(value) {
    const data = {
        type: 'custom_control',
        cc_number: 7,  // 音量
        value: value
    };
    websocket.send(JSON.stringify(data));
}
```

### API参考

**WebSocket事件：**

*客户端到服务器：*
- `control` - 发送MIDI控制数据
- `ping` - 心跳消息

*服务器到客户端：*
- `status` - 连接和MIDI状态
- `pong` - 心跳响应
- `disconnect` - 设备位移通知

**MIDI实现：**
- 通道：1（可配置）
- 弯音：完整14位分辨率（0-16383）
- 调制：CC1（0-127）
- 附加CC：易于扩展

### 构建自定义版本

要创建自定义版本或修改应用程序：

1. 安装Python开发环境
2. 从 `requirements.txt` 安装依赖项
3. 根据需要修改 `server.py` 和 `index.html`
4. 使用 `python server.py` 测试
5. 使用PyInstaller或类似工具创建可执行文件

### 性能考虑

**优化技巧：**
- 限制WebSocket消息频率以避免泛滥
- 使用高效的JSON序列化
- 实现客户端平滑处理以获得更好的用户体验
- 监控多连接时的内存使用

**可扩展性：**
- 当前设计支持约10-20个并发连接
- MIDI输出按设计是单线程的
- 对于更大的部署，考虑连接池

### 贡献

**开发工作流程：**
1. Fork仓库
2. 创建功能分支
3. 在多个设备/浏览器上测试
4. 提交拉取请求

**测试清单：**
- 验证MIDI输出准确性
- 在各种移动设备上测试
- 检查网络连接边缘情况
- 验证WebSocket重连逻辑

**代码风格：**
- Python代码遵循PEP 8
- 使用描述性变量名
- 包含网络操作的错误处理
- 记录复杂算法

### 许可证和致谢

此项目展示了基于Web的实时MIDI控制。欢迎在您自己的项目中使用、修改和扩展。

**特别感谢：**
- **Tobias Erichsen和loopMIDI团队** - 没有loopMIDI出色的虚拟MIDI驱动程序，这个项目就不可能实现。他们免费、可靠的虚拟MIDI解决方案对于在Windows上实现应用程序之间的无缝通信至关重要。访问：https://www.tobias-erichsen.de/software/loopmidi.html

**依赖项：**
- python-rtmidi：MIDI I/O库
- websockets：WebSocket实现

**灵感：**
此项目旨在为商业MIDI控制器提供免费替代方案，使音乐制作更加便民。

---

## English

A free mobile MIDI controller that transforms your smartphone into a wireless MIDI device. Connect your phone to your computer via local area network and send real-time MIDI signals with zero cost.

### For Users

#### Quick Start

1. **Download and Run**
   - Download the repository files
   - Run `loopMIDISetup.exe` first to install the virtual MIDI driver (Windows only)
   - Double-click `MIDI_Controller.exe` to launch the application
   - No additional installation required

2. **Setup MIDI Connection**
   - Launch loopMIDI application after installation and create a new port
   - When prompted in MIDI_Controller.exe, select the loopMIDI port from the list
   - The virtual MIDI port allows your DAW to receive MIDI signals from your phone

3. **Connect Your Phone**
   - Note the IP address displayed in the console (e.g., `http://192.168.1.100:8000`)
   - Open this address in your phone's web browser
   - Both devices must be on the same local area network (LAN)

4. **Start Playing**
   - Touch and drag on the control surface
   - Left-right movement controls modulation (CC1)
   - Up-down movement controls pitchbend
   - Adjust sensitivity in the settings menu

#### Features

- **Real-time MIDI Control**: Send pitchbend and modulation data with minimal latency
- **Mobile-Optimized Interface**: Responsive touch controls designed for smartphones
- **Adjustable Sensitivity**: Customize control response to your playing style
- **Browser-Based**: No app installation required on mobile device
- **Multi-Device Support**: Automatically handles device switching
- **Zero Cost Solution**: Free alternative to expensive MIDI controllers

#### System Requirements

- **Computer**: Windows 10/11
- **Mobile Device**: Any smartphone with modern web browser
- **Network**: Local area network connection (both devices on same LAN)
- **MIDI Device**: Physical or virtual MIDI port

#### Recommended Setup

**Virtual MIDI Device (Included):**
- **Windows**: Use the included `loopMIDISetup.exe` to install loopMIDI virtual MIDI driver
- **macOS**: IAC Driver (built-in)

**Complete Setup Process:**

1. **Install Virtual MIDI Driver** (Windows only)
   - Run the included `loopMIDISetup.exe`
   - Follow the installation wizard
   - Launch loopMIDI application and create a new port (default settings work fine)

2. **Launch MIDI Controller**
   - Double-click `MIDI_Controller.exe`
   - Select the loopMIDI port from the list when prompted

3. **Configure Your DAW**
   - Set your music software to receive MIDI from the loopMIDI port
   - Enable pitchbend and modulation (CC1) for the desired instrument
   - Configure pitchbend range (typically ±2 or ±12 semitones)

#### Troubleshooting

**Connection Issues:**

*Q: Phone cannot connect to the server*
- Verify both devices are on the same local area network (LAN)
- Check Windows Firewall settings - allow the application through firewall
- Try disabling VPN or proxy connections
- Restart both the application and your network equipment if needed

*Q: Connection drops frequently*
- Ensure strong network signal strength
- Close other bandwidth-intensive applications
- If using WiFi, try using 5GHz band if available

**MIDI Issues:**

*Q: No MIDI output in DAW*
- First ensure loopMIDI is installed (run `loopMIDISetup.exe` if not already done)
- Check that loopMIDI application is running with at least one active port
- Verify MIDI port selection in the MIDI Controller application
- Check DAW MIDI input settings - select the loopMIDI port
- Test with a virtual MIDI monitor application
- Try reconnecting the MIDI port using the 'connect' command

*Q: High latency or delayed response*
- Use dedicated network with minimal traffic
- Close unnecessary applications on both devices
- Consider wired connection for the computer if possible

**Application Issues:**

*Q: Application won't start*
- Run as administrator if needed
- Check if required ports (8000, 8001) are available
- Temporarily disable antivirus software to test

#### Commands

While the application is running, you can use these console commands:

- `status` - View connection and MIDI status
- `ports` - List available MIDI ports
- `connect` - Change MIDI port connection
- `debug` - Toggle detailed logging
- `help` - Show all available commands
- `quit` - Exit the application

#### Network Security

The application creates a local web server for communication. It only accepts connections from devices on your local network and does not send data over the internet.

---

### For Developers

#### Project Structure

```
RemoteMIDI-Controller/
├── MIDI_Controller.exe    # Main application (standalone executable)
├── loopMIDISetup.exe     # Virtual MIDI driver installer (included)
├── README.md             # This documentation
├── server.py             # Source: Main server application
├── index.html            # Source: Web interface
└── requirements.txt      # Source: Python dependencies
```

#### Source Files

**Core Components:**
- `server.py` - Python WebSocket server with MIDI output
- `index.html` - Mobile-optimized web interface with touch controls
- `requirements.txt` - Python dependencies for development

#### Technical Architecture

**Backend (Python):**
- WebSocket server using `websockets` library
- MIDI output via `python-rtmidi`
- HTTP server for serving web interface
- Multi-client connection management
- Real-time message processing

**Frontend (HTML/JavaScript):**
- Touch-optimized control surface
- WebSocket client for real-time communication
- Responsive design for various screen sizes
- Sensitivity controls and visual feedback

**Communication Protocol:**
```json
{
  "type": "control",
  "pitchbend": -1.0,      // Range: -1.0 to 1.0
  "modulation": 0.5,      // Range: 0.0 to 1.0
  "continuous": false     // True for continuous updates
}
```

#### Development Setup

**Requirements:**
```bash
pip install -r requirements.txt
```

**Running from Source:**
```bash
python server.py
```

The source code provides the foundation for building additional features and customizations.

#### Extension Ideas

The modular design allows for easy extension:

**Additional Controls:**
- Add more MIDI CC controllers
- Implement program change selectors
- Create virtual keyboard interface

**Advanced Input Methods:**
- Accelerometer/gyroscope control (device motion)
- Multi-touch gesture recognition
- Voice control integration

**Enhanced Features:**
- MIDI file recording/playback
- Preset management system
- Visual feedback with waveforms
- Multiple controller layouts

#### Code Examples

**Adding New MIDI Controller:**
```python
def send_custom_cc(self, cc_number, value):
    """Send custom MIDI CC message"""
    if self.current_port is None:
        return
    
    value = max(0, min(127, int(value)))
    cc_msg = [0xB0, cc_number, value]  # Channel 1
    self.midiout.send_message(cc_msg)
```

**Frontend Control Addition:**
```javascript
// Add new slider control
function handleCustomControl(value) {
    const data = {
        type: 'custom_control',
        cc_number: 7,  // Volume
        value: value
    };
    websocket.send(JSON.stringify(data));
}
```

#### API Reference

**WebSocket Events:**

*Client to Server:*
- `control` - Send MIDI control data
- `ping` - Heartbeat message

*Server to Client:*
- `status` - Connection and MIDI status
- `pong` - Heartbeat response
- `disconnect` - Device displacement notification

**MIDI Implementation:**
- Channel: 1 (configurable)
- Pitchbend: Full 14-bit resolution (0-16383)
- Modulation: CC1 (0-127)
- Additional CCs: Easily extensible

#### Building Custom Versions

To create custom versions or modify the application:

1. Install Python development environment
2. Install dependencies from `requirements.txt`
3. Modify `server.py` and `index.html` as needed
4. Test with `python server.py`
5. Use PyInstaller or similar tools to create executables

#### Performance Considerations

**Optimization Tips:**
- Limit WebSocket message frequency to avoid flooding
- Use efficient JSON serialization
- Implement client-side smoothing for better UX
- Monitor memory usage with multiple connections

**Scalability:**
- Current design supports approximately 10-20 concurrent connections
- MIDI output is single-threaded by design
- Consider connection pooling for larger deployments

#### Contributing

**Development Workflow:**
1. Fork the repository
2. Create feature branch
3. Test on multiple devices/browsers
4. Submit pull request

**Testing Checklist:**
- Verify MIDI output accuracy
- Test on various mobile devices
- Check network connectivity edge cases
- Validate WebSocket reconnection logic

**Code Style:**
- Follow PEP 8 for Python code
- Use descriptive variable names
- Include error handling for network operations
- Document complex algorithms

#### License and Credits

This project demonstrates real-time web-based MIDI control. Feel free to use, modify, and extend for your own projects.

**Special Thanks:**
- **Tobias Erichsen and the loopMIDI team** - Without loopMIDI's excellent virtual MIDI driver, this project would not be possible. Their free, reliable virtual MIDI solution is essential for enabling seamless communication between applications on Windows. Visit: https://www.tobias-erichsen.de/software/loopmidi.html

**Dependencies:**
- python-rtmidi: MIDI I/O library
- websockets: WebSocket implementation

**Inspiration:**
This project was created to provide a free alternative to commercial MIDI controllers, making music production more accessible.

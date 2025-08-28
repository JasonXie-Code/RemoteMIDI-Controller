# RemoteMIDI-Controller

A free mobile MIDI controller that transforms your smartphone into a wireless MIDI device. Connect your phone to your computer via local area network and send real-time MIDI signals with zero cost.

## For Users

### Quick Start

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

### Features

- Real-time MIDI Control: Send pitchbend and modulation data with minimal latency
- Mobile-Optimized Interface: Responsive touch controls designed for smartphones
- Adjustable Sensitivity: Customize control response to your playing style
- Browser-Based: No app installation required on mobile device
- Multi-Device Support: Automatically handles device switching
- Zero Cost Solution: Free alternative to expensive MIDI controllers

### System Requirements

- **Computer**: Windows 10/11
- **Mobile Device**: Any smartphone with modern web browser
- **Network**: Local area network connection (both devices on same LAN)
- **MIDI Device**: Physical or virtual MIDI port

### Recommended Setup

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

### Troubleshooting

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

### Commands

While the application is running, you can use these console commands:

- `status` - View connection and MIDI status
- `ports` - List available MIDI ports
- `connect` - Change MIDI port connection
- `debug` - Toggle detailed logging
- `help` - Show all available commands
- `quit` - Exit the application

### Network Security

The application creates a local web server for communication. It only accepts connections from devices on your local network and does not send data over the internet.

---

## For Developers

### Project Structure

```
RemoteMIDI-Controller/
├── MIDI_Controller.exe    # Main application (standalone executable)
├── loopMIDISetup.exe     # Virtual MIDI driver installer (included)
├── README.md             # This documentation
├── server.py             # Source: Main server application
├── index.html            # Source: Web interface
└── requirements.txt      # Source: Python dependencies
```

### Source Files

**Core Components:**
- `server.py` - Python WebSocket server with MIDI output
- `index.html` - Mobile-optimized web interface with touch controls
- `requirements.txt` - Python dependencies for development

### Technical Architecture

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

### Development Setup

**Requirements:**
```bash
pip install -r requirements.txt
```

**Running from Source:**
```bash
python server.py
```

The source code provides the foundation for building additional features and customizations.

### Extension Ideas

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

### Code Examples

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

### API Reference

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

### Building Custom Versions

To create custom versions or modify the application:

1. Install Python development environment
2. Install dependencies from `requirements.txt`
3. Modify `server.py` and `index.html` as needed
4. Test with `python server.py`
5. Use PyInstaller or similar tools to create executables

### Performance Considerations

**Optimization Tips:**
- Limit WebSocket message frequency to avoid flooding
- Use efficient JSON serialization
- Implement client-side smoothing for better UX
- Monitor memory usage with multiple connections

**Scalability:**
- Current design supports approximately 10-20 concurrent connections
- MIDI output is single-threaded by design
- Consider connection pooling for larger deployments

### Contributing

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

### License and Credits

This project demonstrates real-time web-based MIDI control. Feel free to use, modify, and extend for your own projects.

**Special Thanks:**
- **Tobias Erichsen and the loopMIDI team** - Without loopMIDI's excellent virtual MIDI driver, this project would not be possible. Their free, reliable virtual MIDI solution is essential for enabling seamless communication between applications on Windows. Visit: https://www.tobias-erichsen.de/software/loopmidi.html

**Dependencies:**
- python-rtmidi: MIDI I/O library
- websockets: WebSocket implementation

**Inspiration:**
This project was created to provide a free alternative to commercial MIDI controllers, making music production more accessible.

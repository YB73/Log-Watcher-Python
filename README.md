# Real-time Log Monitor

A real-time log monitoring system that allows users to view log file updates through a web interface. Similar to `tail -f` command but accessible via browser with support for multiple simultaneous clients.

## Features

- 🔄 Real-time log file monitoring
- 🌐 Web-based interface
- 🔌 WebSocket-based live updates
- 👥 Support for multiple concurrent clients
- 📝 Automatic encoding detection (UTF-8, UTF-16)
- 🚀 Efficient updates (sends only new lines)
- 💪 Thread-safe implementation
- 🔙 Auto-reconnect on connection loss

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/log-monitor.git
cd log-monitor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
log_monitor/
├── requirements.txt      # Project dependencies
├── main.py              # FastAPI server implementation
├── log_watcher.py       # Core log watching functionality
├── static/              # Static files directory
│   └── index.html       # Web interface
└── test_logs/          # Directory for log files
    └── sample.log      # Sample log file
```

## Usage

1. Start the server:
```bash
python main.py
```

2. Access the web interface:
   - Open your browser and navigate to `http://localhost:8000`
   - The page will display the last 10 lines of the log file
   - New log entries will appear automatically

3. Monitor different log files:
   - Modify the log file path in `main.py`:
   ```python
   log_watcher = LogWatcher("path/to/your/logfile.log")
   ```

## Testing

To test the system, you can add new entries to your log file:

```bash
# Add a test entry
echo "New log entry $(date)" >> test_logs/sample.log
```

For UTF-16 encoded logs:
```python
with open('test_logs/sample.log', 'a', encoding='utf-16') as f:
    f.write(f"New log entry {time.strftime('%m/%d/%Y %H:%M:%S')}\n")
```

## Technical Details

### Server-side Components

- **LogWatcher**: Core class that monitors log file changes
  - Thread-safe implementation using locks
  - Efficient file reading using position tracking
  - Automatic encoding detection
  - Callback-based update system

- **FastAPI Server**:
  - WebSocket endpoint for real-time updates
  - Static file serving for web interface
  - Multiple client support

### Client-side Features

- Real-time updates using WebSocket
- Auto-scrolling to latest entries
- Memory management (limits maximum displayed lines)
- Automatic reconnection on connection loss
- Clean, responsive interface

## Performance Considerations

- Only sends new log entries, not the entire file
- Uses a single thread per log file, not per client
- Implements efficient file reading using position tracking
- Memory-efficient client-side implementation
- Minimal CPU usage when idle

## Configuration Options

The following parameters can be modified in the code:

- Server port (default: 8000)
- Maximum displayed lines in UI (default: 1000)
- Initial lines shown (default: 10)
- File check interval (default: 0.1 seconds)

## Future Improvements

- Configuration file support
- Multiple log file monitoring
- Search and filter capabilities
- User authentication
- Log rotation handling
- Metrics and monitoring
- Docker support

## Common Issues

1. **Encoding Issues**
   - The system automatically detects and handles UTF-8 and UTF-16 encodings
   - If you see encoding artifacts, ensure your log file has a consistent encoding

2. **Permission Issues**
   - Ensure the application has read permissions for the log file
   - The application needs write permission if the log file doesn't exist

3. **Performance**
   - For very large log files, consider adjusting the maximum lines displayed
   - If CPU usage is high, increase the file check interval

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/name`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

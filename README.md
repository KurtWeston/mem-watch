# mem-watch

Monitor process memory usage with configurable threshold alerts and usage history tracking

## Features

- Monitor memory usage of processes by PID or process name pattern
- Real-time memory consumption display with auto-refresh
- Configurable memory threshold alerts (percentage or absolute MB/GB)
- Track multiple processes simultaneously
- Display memory usage history as ASCII graph in terminal
- Filter processes by name using regex patterns
- Export memory usage data to CSV with timestamps
- Show RSS, VMS, and percentage of total system memory
- Color-coded output (green=normal, yellow=warning, red=critical)
- Configurable sampling interval (default 1 second)
- Summary statistics (min, max, average memory usage)
- Option to monitor child processes recursively

## How to Use

Use this project when you need to:

- Quickly solve problems related to mem-watch
- Integrate python functionality into your workflow
- Learn how python handles common patterns

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/mem-watch.git
cd mem-watch

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python

## Dependencies

- `psutil`
- `click`
- `rich`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

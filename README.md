# Restaurant Booking Automation

Automation script for booking restaurants via INLINE platform (Karuizawa Hotpot).
Built for integration with N8N workflow automation platform.

## Features

- Automated form filling with customer details
- Support for date/time selection
- JSON input/output for N8N integration
- Screenshot capture for debugging
- Error handling and reporting

## Requirements

- Python 3.7+
- Selenium 4.10+
- Google Chrome browser
- ChromeDriver

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
python book_restaurant.py
```

### With Custom Booking Data (JSON)

```bash
python book_restaurant.py '{"name": "李羿", "phone": "0919077013", "email": "alleh363953@gmail.com", "date": "2025-11-15", "time": "22:00"}'
```

### N8N Integration

Use the `Execute Command` node in N8N to trigger this script:

```json
{
  "command": "python /path/to/book_restaurant.py",
  "args": ["booking_json_data"]
}
```

## Configuration

Edit the `booking_data` dictionary in `book_restaurant.py` to configure:

- `restaurant_url`: INLINE restaurant booking URL
- `name`: Reservation name
- `title`: Mr/Ms designation
- `phone`: Contact phone number
- `email`: Contact email
- `date`: Booking date (YYYY-MM-DD)
- `time`: Booking time (HH:MM)
- `party_size`: Number of people

## Output

The script returns JSON output with:

```json
{
  "status": "success|completed|error",
  "message": "Description",
  "booking_details": { ... },
  "error_type": "Exception type (if error)"
}
```

## Troubleshooting

1. **Element not found**: Update CSS selectors in the script for new website changes
2. **Timeout issues**: Increase wait time in `WebDriverWait` function
3. **Screenshot issues**: Ensure `/tmp/` directory is writable

## Author

n8n363953-crypto

## License

MIT

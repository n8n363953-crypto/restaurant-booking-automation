# N8N Integration Guide

Complete guide for integrating the Restaurant Booking Automation script with N8N workflow automation platform.

## Prerequisites

1. N8N instance running (local or cloud)
2. Python 3.7+ installed on the server running the script
3. Chrome/Chromium browser installed
4. Script files installed (see Installation section)

## Installation on Zeber (or Server)

### Step 1: Clone or Download the Repository

```bash
cd /opt/scripts
git clone https://github.com/n8n363953-crypto/restaurant-booking-automation.git
cd restaurant-booking-automation
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Verify Chrome/Chromium Installation

```bash
which google-chrome chromium chromium-browser
```

If not installed:

```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# CentOS/RHEL
sudo yum install chromium
```

### Step 4: Make Script Executable

```bash
chmod +x /opt/scripts/restaurant-booking-automation/book_restaurant.py
```

## N8N Workflow Configuration

### Step 1: Create Trigger Node

1. Add **Webhook** trigger node
2. Configure:
   - HTTP Method: POST
   - Authentication: None (or add API key if needed)
   - Set a trigger name: "Restaurant Booking Request"

### Step 2: Add Execute Command Node

1. Add **Execute Command** node
2. Configure:
   ```
   Command: /usr/bin/python3
   Arguments: /opt/scripts/restaurant-booking-automation/book_restaurant.py
   ```

### Step 3: Add JSON Data Preparation

1. Add **Function** node before Execute Command:
   ```javascript
   // Prepare booking data from webhook payload
   const bookingData = {
     restaurant_url: $('Webhook Trigger').toObject().body.restaurant_url || 'https://inline.co.jp/restaurants/...',
     name: $('Webhook Trigger').toObject().body.name || '李羿',
     title: $('Webhook Trigger').toObject().body.title || '先生',
     phone: $('Webhook Trigger').toObject().body.phone || '0919077013',
     email: $('Webhook Trigger').toObject().body.email || 'alleh363953@gmail.com',
     date: $('Webhook Trigger').toObject().body.date || '2025-11-15',
     time: $('Webhook Trigger').toObject().body.time || '22:00',
     party_size: $('Webhook Trigger').toObject().body.party_size || '2'
   };
   
   return [{ json: { booking_data: bookingData } }];
   ```

### Step 4: Pass Data to Script

Modify Execute Command node:

```
Command: /usr/bin/python3
Arguments: /opt/scripts/restaurant-booking-automation/book_restaurant.py
Input Data: '{{JSON.stringify($json.booking_data)}}'
```

### Step 5: Add Result Processing

1. Add another **Function** node to parse results:
   ```javascript
   const result = JSON.parse($('Execute Command').toObject().body);
   return [{ json: { 
     success: result.status !== 'error',
     status: result.status,
     message: result.message,
     booking_details: result.booking_details
   }}];
   ```

### Step 6: Add Response Node

1. Add **Send Response** node:
   - Set status code based on result
   - Send JSON response back

## Webhook Payload Example

When triggering the workflow via webhook:

```json
{
  "restaurant_url": "https://inline.co.jp/restaurants/karuizawa-hotpot-gongyi",
  "name": "李羿",
  "title": "先生",
  "phone": "0919077013",
  "email": "alleh363953@gmail.com",
  "date": "2025-11-15",
  "time": "22:00",
  "party_size": "2"
}
```

## Testing the Workflow

### Test 1: Manual Trigger

1. In N8N, click the test trigger
2. Provide sample payload
3. Check execution logs

### Test 2: Webhook Trigger

```bash
curl -X POST http://your-n8n-instance/webhook/restaurant-booking \
  -H "Content-Type: application/json" \
  -d '{
    "name": "李羿",
    "phone": "0919077013",
    "email": "alleh363953@gmail.com",
    "date": "2025-11-15",
    "time": "22:00"
  }'
```

## Error Handling

### Common Issues:

1. **Chrome not found**: Install chromium or update PATH
2. **Timeout errors**: Increase timeout in Execute Command node
3. **Element not found**: Website structure changed, update selectors in script
4. **Permission denied**: Check file permissions with `chmod +x`

## Monitoring

1. Set up error handling with **Error Trigger** node
2. Add **SendGrid** or **Email** node for notifications
3. Log results to database using **Database** node
4. Monitor execution history in N8N dashboard

## Security Considerations

1. Use API key authentication for webhook
2. Validate input data in Function nodes
3. Don't expose sensitive URLs in logs
4. Use environment variables for credentials
5. Run script with minimal required permissions

## Scheduling

To run automatically:

1. Add **Schedule Trigger** node
2. Set frequency (daily, weekly, etc.)
3. Configure default booking data

## Performance Tips

1. Use headless mode: Modify script with `--headless` Chrome option
2. Implement connection pooling for multiple bookings
3. Add rate limiting to prevent website blocking
4. Cache restaurant URLs

## Support

For issues or questions, refer to:
- Script README.md
- N8N documentation: https://docs.n8n.io
- GitHub Issues: https://github.com/n8n363953-crypto/restaurant-booking-automation/issues

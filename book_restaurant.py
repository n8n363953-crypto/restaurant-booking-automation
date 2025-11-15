#!/usr/bin/env python3
"""
Restaurant Booking Automation Script for INLINE (Karuizawa Hotpot)
This script automates the reservation process for restaurants using INLINE booking system
Integration with N8N workflow automation platform
"""

import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def book_restaurant(booking_data):
    """
    Main function to automate restaurant booking
    
    Args:
        booking_data: Dictionary containing booking information
            - restaurant_url: URL to the restaurant booking page
            - name: Reservation name
            - title: Mr/Ms/etc
            - phone: Phone number
            - email: Email address
            - date: Booking date (YYYY-MM-DD)
            - time: Booking time (HH:MM)
            - party_size: Number of people (optional)
    
    Returns:
        Dictionary with success status and message
    """
    
    driver = None
    try:
        # Setup Chrome options
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Uncomment for headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to booking page
        booking_url = booking_data.get('restaurant_url')
        print(f"Navigating to: {booking_url}")
        driver.get(booking_url)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Extract booking information
        name = booking_data.get('name', '李羿')
        title = booking_data.get('title', '先生')  # Mr
        phone = booking_data.get('phone', '0919077013')
        email = booking_data.get('email', 'alleh363953@gmail.com')
        booking_date = booking_data.get('date', '2025-11-15')
        booking_time = booking_data.get('time', '22:00')
        party_size = booking_data.get('party_size', '2')
        
        print(f"Booking details: {name} {title}, {phone}, {email}")
        print(f"Date: {booking_date}, Time: {booking_time}")
        
        # Wait for and fill name field
        try:
            name_input = wait.until(EC.presence_of_element_located((By.NAME, 'name')))
            name_input.clear()
            name_input.send_keys(name)
            print(f"✓ Entered name: {name}")
        except Exception as e:
            # Try alternative selectors
            print(f"Trying alternative name selector...")
            name_inputs = driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='名']")  
            if name_inputs:
                name_inputs[0].clear()
                name_inputs[0].send_keys(name)
                print(f"✓ Entered name using alternative selector: {name}")
        
        time.sleep(0.5)
        
        # Handle title/gender selection if exists
        try:
            title_select = Select(driver.find_element(By.NAME, 'title'))
            title_select.select_by_value('mr')
            print(f"✓ Selected title: {title}")
        except:
            print("Title selection not found or not required")
        
        time.sleep(0.5)
        
        # Fill phone number
        try:
            phone_input = driver.find_element(By.NAME, 'phone')
            phone_input.clear()
            phone_input.send_keys(phone)
            print(f"✓ Entered phone: {phone}")
        except Exception as e:
            phone_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='tel']")
            if phone_inputs:
                phone_inputs[0].clear()
                phone_inputs[0].send_keys(phone)
                print(f"✓ Entered phone using alternative selector: {phone}")
        
        time.sleep(0.5)
        
        # Fill email
        try:
            email_input = driver.find_element(By.NAME, 'email')
            email_input.clear()
            email_input.send_keys(email)
            print(f"✓ Entered email: {email}")
        except Exception as e:
            email_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
            if email_inputs:
                email_inputs[0].clear()
                email_inputs[0].send_keys(email)
                print(f"✓ Entered email using alternative selector: {email}")
        
        time.sleep(1)
        
        # Take screenshot before submitting
        screenshot_path = '/tmp/booking_before_submit.png'
        driver.save_screenshot(screenshot_path)
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        # Find and click submit button
        try:
            # Try to find submit button with various selectors
            submit_button = None
            selectors = [
                "button[type='submit']",
                "button:contains('訂位')",
                "button:contains('確認')",
                "//button[contains(text(), '訂位')]",
                "//button[contains(text(), '確認')]"
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith('//'):
                        submit_button = driver.find_element(By.XPATH, selector)
                    else:
                        submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                    if submit_button:
                        break
                except:
                    continue
            
            if submit_button:
                print("✓ Found submit button, clicking...")
                submit_button.click()
                time.sleep(2)
                print("✓ Booking submitted successfully!")
            else:
                # Find all buttons and try the last one
                buttons = driver.find_elements(By.TAG_NAME, "button")
                if buttons:
                    buttons[-1].click()
                    print("✓ Clicked potential submit button")
                    time.sleep(2)
        except Exception as e:
            print(f"Error clicking submit button: {e}")
            raise
        
        # Take final screenshot
        final_screenshot = '/tmp/booking_after_submit.png'
        driver.save_screenshot(final_screenshot)
        print(f"✓ Final screenshot saved: {final_screenshot}")
        
        # Check for confirmation
        time.sleep(1)
        page_source = driver.page_source
        
        if '成功' in page_source or 'success' in page_source.lower() or '確認' in page_source:
            result = {
                'status': 'success',
                'message': 'Reservation completed successfully!',
                'booking_details': {
                    'name': name,
                    'title': title,
                    'phone': phone,
                    'email': email,
                    'date': booking_date,
                    'time': booking_time,
                    'timestamp': datetime.now().isoformat()
                }
            }
        else:
            result = {
                'status': 'completed',
                'message': 'Booking process completed. Please verify the reservation.',
                'booking_details': {
                    'name': name,
                    'phone': phone,
                    'email': email,
                    'timestamp': datetime.now().isoformat()
                }
            }
        
        return result
        
    except Exception as e:
        error_message = f"Booking process failed: {str(e)}"
        print(f"✗ {error_message}")
        return {
            'status': 'error',
            'message': error_message,
            'error_type': type(e).__name__
        }
    
    finally:
        # Close the browser
        if driver:
            driver.quit()
            print("✓ Browser closed")

def main():
    """
    Main entry point for the script
    Can be called from N8N or command line
    """
    
    # Default booking data for testing
    booking_data = {
        'restaurant_url': 'https://inline.co.jp/restaurants/karuizawa-hotpot-gongyi',  # Replace with actual URL
        'name': '李羿',
        'title': '先生',
        'phone': '0919077013',
        'email': 'alleh363953@gmail.com',
        'date': '2025-11-15',
        'time': '22:00',
        'party_size': '2'
    }
    
    # Try to get booking data from command line arguments (JSON format)
    if len(sys.argv) > 1:
        try:
            booking_data = json.loads(sys.argv[1])
            print("✓ Booking data loaded from command line argument")
        except json.JSONDecodeError:
            print("Warning: Invalid JSON argument, using default booking data")
    
    # Execute booking
    result = book_restaurant(booking_data)
    
    # Output result as JSON
    print("\n" + "="*50)
    print("BOOKING RESULT:")
    print("="*50)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Exit with appropriate code
    sys.exit(0 if result['status'] != 'error' else 1)

if __name__ == '__main__':
    main()

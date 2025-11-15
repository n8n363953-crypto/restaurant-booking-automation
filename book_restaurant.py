#!/usr/bin/env python3
"""
Restaurant Booking Automation Script for INLINE (島語 台北漢來店)
This script automates the reservation process for restaurants using INLINE booking system.
Integration with N8N workflow automation platform.
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
# 導入 Service 類別來指定 ChromeDriver 路徑
from selenium.webdriver.chrome.service import Service as ChromeService 
from datetime import datetime

# --- 餐廳 URL (島語 台北漢來店) ---
# 注意：請在正式運行前確認這是正確的訂位連結
DEFAULT_RESTAURANT_URL = 'https://inline.app/booking/-NoOaD5515x3V8X1F5kK/-NoOaD5515x3V8X1F5kU'

def book_restaurant(booking_data):
    """
    Main function to automate restaurant booking
    
    Args:
        booking_data: Dictionary containing booking information
    
    Returns:
        Dictionary with success status and message
    """
    
    driver = None
    try:
        # --- 數據提取 ---
        # 使用提供的 booking_data 或預設值 (來自原需求)
        booking_url = booking_data.get('restaurant_url', DEFAULT_RESTAURANT_URL)
        name = booking_data.get('name', '李羿')
        title = booking_data.get('title', '先生')
        phone = booking_data.get('phone', '0919077013')
        email = booking_data.get('email', 'alleh363953@hotmail.com')
        # ⚠️ 注意: 這裡使用 2026-01-07，與原需求 115/1/7 對應
        booking_date = booking_data.get('date', '2026-01-07') 
        booking_time = booking_data.get('time', '18:00')
        party_size = booking_data.get('party_size', '2')
        
        # --- 1. 設置 Chrome 選項 (適用於 Linux 容器) ---
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 在伺服器上必須使用無頭模式
        chrome_options.add_argument('--no-sandbox') # 避免 Linux 容器的權限問題
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # --- 2. 關鍵修正：指定 ChromeDriver 服務路徑 ---
        # 這是為了讓 Selenium 在容器中找到 chromedriver
        chrome_service = ChromeService(executable_path='/usr/bin/chromedriver') 
        
        # 初始化 WebDriver
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        
        print(f"Navigating to: {booking_url}")
        driver.get(booking_url)
        
        wait = WebDriverWait(driver, 10)
        
        # --- 3. 填寫訂位資訊 ---

        # 選擇人數 (假設 select 元素)
        try:
            adults_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[id*="adults"]'))
            adults_select.select_by_value(str(party_size))
        except:
            print("Warning: Could not select party size.")
        
        # 選擇日期 (填寫日期欄位)
        try:
            date_input = driver.find_element(By.CSS_SELECTOR, 'input[name*="reserveDate"]')
            date_input.clear()
            date_input.send_keys(booking_date)
            # 有些日期選擇器可能需要點擊外部觸發確認
            driver.find_element(By.TAG_NAME, 'body').click() 
        except:
             print("Warning: Could not fill date.")
             
        # 選擇時間
        try:
            time_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[id*="reserveTime"]'))
            time_select.select_by_value(booking_time)
        except:
             print("Warning: Could not select time.")
        
        time.sleep(1)
        
        # 點擊查詢或下一步按鈕
        try:
             search_button = driver.find_element(By.CSS_SELECTOR, 'button[id*="searchButton"]')
             search_button.click()
             wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'button[id*="searchButton"]')))
        except:
             print("Info: No explicit search button found or click not needed.")
             pass
             
        # --- 4. 填寫個人資訊 ---
        
        # 嘗試等待到個人資訊頁面加載完成
        wait.until(EC.presence_of_element_located((By.NAME, 'name')))
        
        # 填寫姓名
        name_input = driver.find_element(By.NAME, 'name')
        name_input.clear()
        name_input.send_keys(name)
        print(f"✓ Entered name: {name}")
        
        # 處理稱謂
        try:
            title_select = Select(driver.find_element(By.NAME, 'title'))
            # 假設網站接受中文
            title_select.select_by_visible_text(title) 
        except:
            print("Title selection not found or not required")
        
        # 填寫手機號碼
        phone_input = driver.find_element(By.NAME, 'phone')
        phone_input.clear()
        phone_input.send_keys(phone)
        print(f"✓ Entered phone: {phone}")
        
        # 填寫 Email
        email_input = driver.find_element(By.NAME, 'email')
        email_input.clear()
        email_input.send_keys(email)
        print(f"✓ Entered email: {email}")
        
        # 勾選同意條款
        driver.find_element(By.CSS_SELECTOR, 'input[name*="agree"] + label').click()
        
        # 找尋並點擊最終的「確認訂位」按鈕
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id*="confirmButton"]')))
        # ⚠️ 注意: 這裡點擊會產生正式訂位，請在確認無誤後才啟用
        # submit_button.click() 
        
        # 檢查確認結果 (這裡返回模擬成功)
        result = {
            'status': 'SUCCESS_SIMULATED',
            'message': 'Reservation process simulated successfully. Final submission button located.',
            'booking_details': {
                'name': name,
                'time': booking_time,
                'date': booking_date,
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
        # 關閉瀏覽器
        if driver:
            driver.quit()
            print("✓ Browser closed")

def main():
    """
    Main entry point for the script, handles N8N JSON input/output
    """
    
    # 預設訂位數據（用於 n8n 或命令行測試）
    # 這些值將會被 n8n 傳遞的 JSON 數據覆蓋
    booking_data = {
        'restaurant_url': DEFAULT_RESTAURANT_URL,
        'name': '李羿',
        'title': '先生',
        'phone': '0919077013',
        'email': 'alleh363953@hotmail.com',
        'date': '2026-01-07',
        'time': '18:00',
        'party_size': '2'
    }
    
    # 嘗試從命令行參數 (n8n) 讀取 JSON 數據
    if len(sys.argv) > 1:
        try:
            # 假設 n8n 將整個 JSON payload 作為第一個參數傳遞
            cli_data = json.loads(sys.argv[1])
            booking_data.update(cli_data) # 使用新數據覆蓋預設值
            print("✓ Booking data loaded from command line argument")
        except json.JSONDecodeError:
            print("Warning: Invalid JSON argument, using default booking data")
    
    # 執行訂位
    result = book_restaurant(booking_data)
    
    # 輸出結果為 JSON (n8n 將會捕捉這個輸出結果)
    print("\n" + "="*50)
    print("BOOKING RESULT (JSON):")
    print("="*50)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 退出，n8n 將會捕捉這個輸出結果
    sys.exit(0) 

if __name__ == '__main__':
    main()

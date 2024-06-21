import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException



def app_getter():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    login_url = 'https://prenotami.esteri.it/Home/'

    def wait_and_find(by, value, timeout=10):
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    try:
        driver.get(login_url)
        email_field = wait_and_find(By.ID, 'login-email')
        pw_field = wait_and_find(By.ID, 'login-password')

        email_field.send_keys('npbq26@gmail.com')
        pw_field.send_keys('Quincee7')

        forward_button = wait_and_find(By.XPATH, '//button[@type="submit" and @class="button primary g-recaptcha"]')
        forward_button.click()

        while driver.title == 'Unavailable':
            time.sleep(600)
            driver.back()
            email_field = wait_and_find(By.ID, 'login-email')
            pw_field = wait_and_find(By.ID, 'login-password')
            email_field.send_keys('npbq26@gmail.com')
            pw_field.send_keys('Quincee7')
            forward_button = wait_and_find(By.XPATH, '//button[@type="submit" and @class="button primary g-recaptcha"]')
            forward_button.click()

        service_field = wait_and_find(By.ID, 'advanced')
        service_field.click()

        while True:
            time.sleep(5)
            current_url = driver.current_url
            try:
                if "/Services" in current_url and "/Booking/4996" not in current_url:
                    book_button = driver.find_element(By.XPATH, '//a[@href="/Services/Booking/4996"]')
                    book_button.click()
                    time.sleep(5)

                    try:
                        ok_button = driver.find_element(By.XPATH, '//button[@type="button" and @class="btn btn-blue"]')
                        if ok_button:
                            ok_button.click()
                    except:
                        continue
                    time.sleep(5)
                    old_page = driver.find_element(By.TAG_NAME, 'html')
                    driver.refresh()
                    WebDriverWait(driver, 10).until(EC.staleness_of(old_page))
                elif "Booking/4996" in current_url:
                    try:
                        error_message = driver.find_element(By.XPATH,
                                                            '//span[@jsselect="heading" and @jsvalues=".innerHTML:msg" and @jstcache="9"]')
                        if error_message and "This site can’t be reached" in error_message.text:
                            print('Site can’t be reached, retrying...')
                            driver.back()
                            time.sleep(5)
                        else:
                            print('Go register')
                            break
                    except NoSuchElementException:
                        # No error message, assume the page is valid and pause
                        print('Page reached, pausing...')
                        break
                else:
                    print('Go register')
                    break
            except WebDriverException as e:
                print(f"WebDriver exception: {e}")
                time.sleep(30)
                driver.refresh()

    except Exception as e:
        print(f"Exception occurred: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    app_getter()

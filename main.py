from playwright.sync_api import sync_playwright
import time
from mailtm import Email
import re
from datetime import datetime
import sys
from PIL import Image
import base64
from io import BytesIO
from PIL import Image

code_email = "lol"

def listener(message):
    global code_email  # Добавляем эту строку для указания, что мы хотим использовать глобальную переменную
    # print("\nSubject: " + message['subject'])
    # print("Content: " + message['text'] if message['text'] else message['html'])
    
    content = str(message['text'] if message['text'] else message['html'])
    
    urls_email = re.findall(r'https:\/\/[^\s"\']+', content)
    
    code_email = urls_email[0]
    
def run_parser():
    with sync_playwright() as p:
        try:
            global code_email
            # Запускаем браузер (можно использовать chromium, firefox или webkit)
            browser = p.chromium.launch(headless=True,channel="chrome")
            page = browser.new_page()
            # Переходим на нужную страницу
            page.goto("https://hotmc.ru/sign-up", wait_until="domcontentloaded")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "Register Page Loaded")
            
            # Нажимаем на кнопку с указанным XPath
        #            button_xpath = "/html/body/div/div[2]/div[2]/div/div[2]/div/div[5]/div[2]/div/a"
        #            page.click(f"xpath=/html/body/div/div[2]/div[2]/div/div[2]/div/div[5]/div[2]/div/a")
            
            # Ждём появления поля для ввода email
            email_input_xpath = '//*[@id="emailcollector-email"]'
            page.wait_for_selector(email_input_xpath)
            
            new_email = Email()
            new_email.register()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "New Email Created: " + new_email.address)  # qwerty123@1secmail.com
            
            # Вводим email (замените на нужный)
            page.fill(f"xpath={email_input_xpath}", new_email.address)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "Email Writed")
            
            # Ждём появления поля для ввода капчи
            captcha_input_xpath = '//*[@id="captchacollector-captcha"]'
            page.wait_for_selector(captcha_input_xpath)
            
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "PLEASE ENTER CAPTCHA")
            # Получаем скриншот элемента

            # Создаем изображение напрямую из байтов (без лишнего base64)
            img = Image.open(BytesIO(page.query_selector('xpath=/html/body/div/div[2]/div/form/div[2]/table/tbody/tr/td[2]/img').screenshot()))

            img = img.convert("L").resize((100, 30))  # Ч/б + уменьшение

            # Символы для градаций серого
            ascii_chars = "  ░░▒▒▓▓██"

            # Преобразуем пиксели в символы
            pixels = img.getdata()
            ascii_art = "".join([ascii_chars[pixel // 32] for pixel in pixels])

            # Выводим построчно
            for i in range(0, len(ascii_art), img.width):
                print(ascii_art[i:i+img.width])

            captcha = input("Code on the Captcha: ")  # str() не нужен, input и так возвращает строку
            page.fill(f"xpath={captcha_input_xpath}", captcha)
            # Ожидаем, пока пользователь введёт капчу вручную
            # while True:
                # captcha_value = page.input_value(captcha_input_xpath)
                # if len(captcha_value) == 4 and captcha_value.isdigit():
                    # print(f"Капча введена: {captcha_value}")
                    # break
            
            # Нажимаем кнопку отправки формы
            submit_button_xpath = "/html/body/div/div[2]/div/form/div[3]/div/button"
            page.click(f"xpath={submit_button_xpath}")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "Register Completed")
            
            new_email.start(listener)

            # Ожидаем письмо с таймаутом (например, 60 секунд)
            timeout = 60
            start_time = time.time()

            while code_email == "lol":
                if time.time() - start_time > timeout:
                    raise TimeoutError("Письмо не пришло в течение 60 секунд")
                
            
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "Link Of Activate Account: " + code_email)



            try:
                with page.expect_navigation():
                    page.goto(code_email)
            except Exception as e:
                print(f"Навигация прервана, но возможно страница загрузилась: {e}")
            
            new_email.stop()
              
            page.goto("https://hotmc.ru/minecraft-server-276854", wait_until="domcontentloaded")
            page.click(f"xpath=/html/body/div/div[2]/div[2]/div/div[2]/div/form/div[1]/div/div[1]/div/a[5]")
            page.click(f"xpath=/html/body/div/div[2]/div[2]/div/div[2]/div/div[5]/div[2]/div/a")
            
            link1 = page.locator("xpath=/html/body/div/div[2]/div[2]/div/div[2]/div/div[5]/div[2]/div/div/div[1]/a[1]").text_content()
            link2 = page.locator("xpath=/html/body/div/div[2]/div[2]/div/div[2]/div/div[5]/div[2]/div/div/div[1]/a[2]").text_content()
            link3 = page.locator("xpath=/html/body/div/div[2]/div[2]/div/div[2]/div/div[5]/div[2]/div/div/div[1]/a[3]").text_content()
            
            
            try: 
                page.goto(link1)
                time.sleep(1)
                result = page.evaluate("""
                    // Создаем интервал для проверки наличия изображения
                    () => {
                        const imgElement = document.querySelector('img.mob-collection-mob-head');

                        if (imgElement) {

                            // Создаем фиксированный элемент и регистрируем кнопку
                            const fixedElement = document.createElement('div');
                            fixedElement.style.position = 'fixed';
                            fixedElement.style.top = '0';
                            fixedElement.style.left = '0';
                            fixedElement.style.width = '100%';
                            fixedElement.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
                            fixedElement.style.textAlign = 'center';
                            fixedElement.style.padding = '10px';
                            fixedElement.style.zIndex = '1000';

                            fixedElement.innerHTML = 'MoonFarm v2.0 by ANGEL04eK ';

                            const registerButton = document.createElement('button');
                            registerButton.innerText = 'Register';
                            registerButton.style.marginLeft = '20px';
                            registerButton.style.padding = '5px 10px';

                            fixedElement.appendChild(registerButton);
                            document.body.appendChild(fixedElement);

                            imgElement.style.position = 'absolute';
                            imgElement.style.top = '40px';
                            imgElement.style.left = '472px';
                            return true;
                        }
                        else {
                            return false
                        }
                    }
                    """)
            except Exception:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "IDI HANUI " + link1 + " Created")
                
            try: 
                if result == False:
                    page.goto(link2)
                    time.sleep(1)
                    result = page.evaluate("""
                    // Создаем интервал для проверки наличия изображения
                    () => {
                        const imgElement = document.querySelector('img.mob-collection-mob-head');

                        if (imgElement) {

                            // Создаем фиксированный элемент и регистрируем кнопку
                            const fixedElement = document.createElement('div');
                            fixedElement.style.position = 'fixed';
                            fixedElement.style.top = '0';
                            fixedElement.style.left = '0';
                            fixedElement.style.width = '100%';
                            fixedElement.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
                            fixedElement.style.textAlign = 'center';
                            fixedElement.style.padding = '10px';
                            fixedElement.style.zIndex = '1000';

                            fixedElement.innerHTML = 'MoonFarm v2.0 by ANGEL04eK ';

                            const registerButton = document.createElement('button');
                            registerButton.innerText = 'Register';
                            registerButton.style.marginLeft = '20px';
                            registerButton.style.padding = '5px 10px';

                            fixedElement.appendChild(registerButton);
                            document.body.appendChild(fixedElement);

                            imgElement.style.position = 'absolute';
                            imgElement.style.top = '40px';
                            imgElement.style.left = '472px';
                            return true;
                        }
                        else {
                            return false
                        }
                    }
                    """)
            except Exception:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "IDI HANUI " + link2 + " Created")
                
            try: 
                if result == False:
                    page.goto(link3)
                    time.sleep(1)
                    result = page.evaluate("""
                    // Создаем интервал для проверки наличия изображения
                    () => {
                        const imgElement = document.querySelector('img.mob-collection-mob-head');

                        if (imgElement) {

                            // Создаем фиксированный элемент и регистрируем кнопку
                            const fixedElement = document.createElement('div');
                            fixedElement.style.position = 'fixed';
                            fixedElement.style.top = '0';
                            fixedElement.style.left = '0';
                            fixedElement.style.width = '100%';
                            fixedElement.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
                            fixedElement.style.textAlign = 'center';
                            fixedElement.style.padding = '10px';
                            fixedElement.style.zIndex = '1000';

                            fixedElement.innerHTML = 'MoonFarm v2.0 by ANGEL04eK ';

                            const registerButton = document.createElement('button');
                            registerButton.innerText = 'Register';
                            registerButton.style.marginLeft = '20px';
                            registerButton.style.padding = '5px 10px';

                            fixedElement.appendChild(registerButton);
                            document.body.appendChild(fixedElement);

                            imgElement.style.position = 'absolute';
                            imgElement.style.top = '40px';
                            imgElement.style.left = '472px';
                            return true;
                        }
                        else {
                            return false
                        }
                    }
                    """)
            except Exception:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "IDI HANUI " + link3 + " Created")
                

            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "Mob Founded")
            page.screenshot(path="screens/" + str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".png")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "Screen Created")
            page.evaluate("""() => {
                const el = document.querySelector('img.mob-collection-mob-head');
                if (el) el.click();
            }""")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "Mobs Clicked")
            time.sleep(1)
            # page.goto("https://hotmc.ru/sign-out", wait_until="domcontentloaded")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "RESTART")
            print()
            print()
            print()
            print()
            code_email = "lol"
            browser.close()
            sys.exit()  # Завершает программу с кодом 0 (успех)

 
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        # finally:
                # # Закрываем браузер
            # browser.close()
            # sys.exit()  # Завершает программу с кодом 0 (успех)

if __name__ == "__main__":
    #while True:
    run_parser()

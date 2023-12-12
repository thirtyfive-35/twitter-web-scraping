from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import time

#veriler
query = 'covid19'
baslangic = '2022-06-14' # yıl-ay-gün
son = '2022-06-28' # yıl-ay-gün


email = "deneme@gmail.com"
username = "username"
password = "123456"

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Header bilgilerini ekleyin
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    context.set_extra_http_headers(headers)

    page = context.new_page()
    page.goto("https://twitter.com/")
    page.get_by_test_id("loginButton").click()
    page.get_by_label("Telefon numarası, e-posta").click()
    page.get_by_label("Telefon numarası, e-posta").fill(email)
    page.get_by_role("button", name="İleri").click()
    page.get_by_test_id("ocfEnterTextTextInput").fill(username)
    page.get_by_test_id("ocfEnterTextNextButton").click()
    page.get_by_label("Şifre", exact=True).click()
    page.get_by_label("Şifre", exact=True).fill(password)
    page.get_by_test_id("LoginForm_Login_Button").click()
    page.get_by_test_id("SearchBox_Search_Input").click()
    page.get_by_test_id("SearchBox_Search_Input").fill(f"lang:en until:{son} since:{baslangic} {query}")
    page.get_by_test_id("SearchBox_Search_Input").press("Enter")
    page.get_by_role("tab", name="Latest").click()

    time.sleep(5)
    # Sayfa yüklenene kadar bekle
    page.wait_for_load_state('load')
    page.wait_for_load_state('domcontentloaded')
    sayac = 0

    # Dosyayı yazmak için aç
    with open(f'{baslangic}_{son}.txt', 'w', encoding='utf-8') as file:
        while True:
            # Sayfa içeriğini al
            page_content = page.content()

            # Beautiful Soup ile sayfa içeriğini işle
            soup = BeautifulSoup(page_content, 'html.parser')

            # Belirli bir class'a sahip tüm div'leri bul
            target_class = "css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim"
            target_divs = soup.find_all('div', {"class": target_class})

            # Her bir div'i dosyaya yaz
            for div in target_divs:
                file.write(div.text.strip() + '\n')

            # Sayfayı aşağı kaydır
            if sayac != 500:
                page.evaluate('window.scrollBy(0, 50000)')
                sayac += 1
                time.sleep(2)
            else:
                break

            # Bir süre bekle
            time.sleep(2)

    # Dosyayı kapat
    file.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

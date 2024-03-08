import time

from env import Env
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()

prefs = {
    'profile.default_content_setting_values':
        {
            'images': 2,
            'plugins': 2, 'popups': 2, 'geolocation': 2,
            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
            'media_stream_mic': 2, 'media_stream_camera': 2,
            'protocol_handlers': 2,
            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
            'push_messaging': 2, 'ssl_cert_decisions': 2,
            'metro_switch_to_desktop': 2,
            'protected_media_identifier': 2, 'app_banner': 2,
            'site_engagement': 2,
            'durable_storage': 2
        }
}

options.add_experimental_option('prefs', prefs)
# options.add_argument("--headless")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

logger.add("log/sms_service_log.log", format="{time:MMMM D, YYYY > HH:mm:SS.SSSS} | {level} | {message}",
           level="DEBUG",
           rotation="1 day")


@logger.catch
def auth() -> None:
    driver.get(Env.LOGIN_URL)

    logger.info("--> Auth start! <--")
    username = driver.find_element(by="id", value="login")
    password = driver.find_element(by="id", value="password")

    username.clear()
    username.send_keys(Env.USERNAME)
    logger.info("--> Username passed! <--")

    password.clear()
    password.send_keys(Env.PASSWORD)
    logger.info("--> Password passed! <--")

    # time.sleep(5)
    password.send_keys(Keys.ENTER)
    for cook in driver.get_cookies():
        driver.add_cookie(cook)
        logger.success("--> Cookie set! <--")

    logger.info("--> Auth complete! <--")


@logger.catch
def send_otp(phone_number: str, otp: str):
    try:
        logger.info("Auth by cookie")
        logger.info(f"----> Message to: {phone_number} otp: {otp} <-----")
        driver.get(Env.SMS_SEND_URL)
        sms_address = driver.find_element(by="id", value="Sms_DestinationAddress")

        sms_address.clear()
        sms_address.send_keys(phone_number)
        logger.info("---> Phone number passed! <---")

        otp_code = driver.find_element(by="id", value="Sms_Text")
        otp_code.clear()
        otp_code.send_keys(otp)
        logger.info("---> Otp passed! <---")

        btn = driver.find_element(by="id", value="apply")
        time.sleep(0.1)
        btn.send_keys(Keys.ENTER)
        logger.success(f"----> Message sent to: {phone_number} otp: {otp} <-----")
        logger.success("!!! All done !!!")
    except NoSuchElementException as ex:
        time.sleep(2)
        logger.error("!!! Cookie Expired !!!")
        auth()
        send_otp(phone_number, otp)


# driver.close()
# driver.quit()


if __name__ == "__main__":
    # auth()
    send_otp("63376556", "test")
# else:
#     phone_number, otp = sys.argv[2], sys.argv[3]
#     send_otp(phone_number, otp)

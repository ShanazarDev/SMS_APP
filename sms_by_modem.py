import time

import gammu


from loguru import logger

LOG_FOLDER = 'log/'


def error_filter(record):
    return record["level"].name == "ERROR" and not "traceback" in record["extra"]


logger.add(LOG_FOLDER + 'error.log', filter=error_filter,
           format="{time:MMMM D, YYYY > HH:mm:SS.SSSS} | {level} | {message}",
           level="ERROR",
           rotation="1 day")


def init_state_machine(filename='gammu.config'):
    sm = gammu.StateMachine()
    sm.ReadConfig(Filename=filename)
    sm.Init()
    return sm


m = init_state_machine()


@logger.catch
def send_sms(sms, number):
    sms_info = {
        "Class": -1,
        "Unicode": True,
        "Entries": [
            {
                "ID": "ConcatenatedTextLong",
                "Buffer": f"{sms}",
            }
        ],
    }

    encoded = gammu.EncodeSMS(sms_info)
    messages = []

    for message in encoded:
        message["SMSC"] = {'Number': '+99365999996'}
        message["Number"] = number
        messages.append(message)

    try:
        result = [m.SendSMS(message) for message in messages]
        print("good")
        return result and True
    except gammu.ERR_UNKNOWN as ex:
        from web import send_otp
        time.sleep(1)
        sms = """"Китайский Мост" - ваш проводник в мир выгодных покупок!

Празднуйте 8 Марта с "Китайским Мостом"!

Быстрая доставка: от 14 дней!

Скидка 15% в честь 8 Марта!

Не упустите шанс порадовать себя и близких!

С нами выгодно и удобно!

imo: +993 63854875"""
        send_otp(number.split("+993")[1], sms)
        return True


if __name__ == '__main__':
    send_sms('Hello', '+99363376556')

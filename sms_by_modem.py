import gammu


def init_state_machine(filename='gammu.config'):
    sm = gammu.StateMachine()
    sm.ReadConfig(Filename=filename)
    sm.Init()
    return sm


m = init_state_machine()


def send_sms(sms, number):
    sms_info = {
        "Class": -1,
        "Unicode": False,
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

    result = [m.SendSMS(message) for message in messages]
    return result and True


if __name__ == '__main__':
    send_sms('Hello', '99363376556')

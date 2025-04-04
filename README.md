Конечно, я добавлю элементы кода из файлов `sms_by_modem.py` и `main.py` в README.

# SMS_APP

SMS_APP is a Python-based application designed to manage and send SMS messages efficiently. It leverages various APIs to provide reliable and scalable SMS services.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Examples](#code-examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

SMS_APP is built to provide a simple and effective way to send SMS messages. It is written in Python and can be easily integrated into various systems to enhance communication capabilities.

## Features

- Send SMS messages to multiple recipients
- Schedule SMS messages
- Integration with popular SMS gateways
- Logging and monitoring of SMS delivery

## Installation

To get a local copy up and running follow these simple steps.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/ShanazarDev/SMS_APP.git
   ```
2. Navigate to the project directory:
   ```sh
   cd SMS_APP
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Set up your SMS gateway credentials in a `.env` file:
   ```sh
   USERNA<E=<username>
   PASSWORD=<password>
   ```
2. Run the main script to start the application:
   ```sh
   python main.py
   ```
3. Follow the on-screen instructions to send SMS messages.

## Code Examples

### Sending an SMS

Below is an example of how to send an SMS using the `send_sms` function from `sms_by_modem.py`:

```python
import time
import gammu
from loguru import logger

LOG_FOLDER = 'log/'

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
```

### Flet UI for Sending SMS

Below is an example of a simple Flet UI for sending SMS from `main.py`:

```python
import time
from datetime import datetime
from loguru import logger
import flet as ft
from sms_by_modem import send_sms

LOG_FOLDER = 'log/'

logger.info('Service Start')

@logger.catch
def main_ui(page: ft.Page):
    # Page Settings
    page.title = "SMS sender"
    page.window_maximizable = False
    page.window_resizable = True
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 320
    page.window_height = 600
    page.theme_mode = "light"

    def send_sms_func(e: ft.ControlEvent):
        phone = phone_number_input.value
        text = text_input.value
        if phone != '' and text != '':
            logger.info(f"Sending one message! To: +993 {phone} sms: {text}")
            if send_sms(sms=f"{text_input.value}", number=f'+993{phone_number_input.value}'):
                logger.success("Message successfully sent!")
                phone_number_input.value = ''
                text_input.value = ''
                recent_send_list_view.controls.append(
                    ft.Text(
                        value=f"[{send_sms_btn.data}]: "
                              f"\n\t\t\t[Phone]: \t\t{phone} \t\t "
                              f"\n\t\t\t[SMS]: \t\t{text} \t\t "
                              f"\n\t\t\t[TIME]: \t\t{datetime.now().strftime('%H:%M:%S')}"
                    )
                )
                send_sms_btn.data += 1
                page.update()

    # SMS to user
    header_text = ft.Container(
        ft.Text("SMS Sender by Shanazar 💸", size=20, font_family='Times New Roman'),
        alignment=ft.alignment.center, margin=20
    )

    phone_number_input = ft.TextField(width=300, height=70, bgcolor=ft.colors.ON_PRIMARY, label="Phone Number",
                                      prefix_text="+993")
    text_input = ft.TextField(width=300, bgcolor=ft.colors.ON_PRIMARY, label="Text",
                              multiline=True, min_lines=1, max_lines=8)
    recent_text = ft.Text("Recent SMS:", text_align=ft.alignment.center)
    recent_send_list_view = ft.ListView(expand=True, height=100, spacing=10, width=300)
    send_sms_btn = ft.ElevatedButton("Send SMS", bgcolor=ft.colors.GREEN, color='white', on_click=send_sms_func, data=1)
    sms_to_user_panel = ft.Row(
        [
            ft.Column(
                [
                    header_text,
                    phone_number_input,
                    text_input,
                    send_sms_btn,
                    recent_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]
    )

    page.add(sms_to_user_panel, recent_send_list_view)
    page.update()

ft.app(target=main_ui)
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

ShanazarDev - hshanazar29@mail.ru

Project Link: [https://github.com/ShanazarDev/SMS_APP](https://github.com/ShanazarDev/SMS_APP)

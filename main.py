import time
from datetime import datetime

from loguru import logger
import flet as ft

from sms_by_modem import send_sms

LOG_FOLDER = 'log/'


def info_filter(record):
    return record["level"].name == "INFO" or record["level"].name == "SUCCESS"


logger.add(LOG_FOLDER + 'info.log', filter=info_filter,
           format="{time:MMMM D, YYYY > HH:mm:SS.SSSS} | {level} | {message}",
           level="INFO",
           rotation="1 day")


def error_filter(record):
    return record["level"].name == "ERROR" and not "traceback" in record["extra"]


logger.add(LOG_FOLDER + 'error.log', filter=error_filter,
           format="{time:MMMM D, YYYY > HH:mm:SS.SSSS} | {level} | {message}",
           level="ERROR",
           rotation="1 day")

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

    def send_spam_sms_func(e: ft.ControlEvent):
        logger.info("Starting Spam message")
        text = text_input.value
        c = 0

        o_from = int(offset_from.value) if offset_from.value != '' else 0
        o_to = int(offset_to.value) if offset_to.value != '' else 0

        print(o_to)

        logger.info(f"Spam from [{o_from}] to [{o_to if o_to != 0 else '++'}] sms, [text]: {text}")

        with open('Numbers/nums.txt', 'r') as n_5:
            n_5 = n_5.readlines()

        if o_from and o_to:
            for n in n_5[o_from:o_to]:
                t = n.split('\n')[0]
                if send_sms(sms=f"{text}", number=f'+993{t}'):
                    c += 1
                    logger.success(f" [{c}] Message successfully sent to +993 {t}")
                    recent_send_list_view.controls.append(
                        ft.Text(
                            value=f"[{c}]: "
                                  f"\n\t\t\t[Phone]: \t\t+993 {t} \t\t "
                                  f"\n\t\t\t[TIME]: \t\t{datetime.now().strftime('%H:%M:%S')}"
                        )
                    )
                    time.sleep(0.7)
                page.update()

        elif o_from:
            for n in n_5[o_from:]:
                t = n.split('\n')[0]
                if send_sms(sms=f"{text}", number=f'+993{t}'):
                    c += 1
                    logger.success(f" [{c}] Message successfully sent to +993 {t}")
                    recent_send_list_view.controls.append(
                        ft.Text(
                            value=f"[{c}]: "
                                  f"\n\t\t\t[Phone]: \t\t+993 {t} \t\t "
                                  f"\n\t\t\t[TIME]: \t\t{datetime.now().strftime('%H:%M:%S')}"
                        )
                    )
                    time.sleep(0.7)
                page.update()

        logger.info("All done!")
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

    send_spam_sms_btn = ft.ElevatedButton(text="Start Spam", icon=ft.icons.SMS, on_click=send_spam_sms_func)
    offset_from = ft.TextField(helper_text="From", width=100)
    offset_to = ft.TextField(helper_text="To", width=100)

    spam_sms_panel = ft.Row(
        [
            ft.Column(
                [
                    header_text,
                    ft.Row(
                        [
                            offset_from, offset_to
                        ],
                        alignment=ft.alignment.center,
                        spacing=100
                    ),
                    text_input,
                    send_spam_sms_btn,
                    recent_text
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
    )

    def panel_navigation(e: ft.ControlEvent):
        index = page.navigation_bar.selected_index
        recent_send_list_view.controls.clear()
        page.clean()

        if index == 0:
            page.add(sms_to_user_panel, recent_send_list_view)
        elif index == 1:
            page.add(spam_sms_panel, recent_send_list_view)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.SMS, label="Send SMS to user"),
            ft.NavigationDestination(icon=ft.icons.CHAT, label="Start spam")
        ],
        on_change=panel_navigation
    )

    page.add(sms_to_user_panel, recent_send_list_view)
    page.update()


ft.app(target=main_ui)

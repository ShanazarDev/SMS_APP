# import time

# import gammu
from sms_by_modem import send_sms

import flet as ft


def main_ui(page: ft.Page):
    # Page Settings
    page.title = "SMS sender"
    page.window_maximizable = False
    page.window_resizable = False
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_bgcolor = ft.colors.BLACK
    page.window_width = 800
    page.window_height = 500

    def send_sms_from_phone_input(e):
        def send(e):
            last_sms_text = ft.Text(size=20, color=ft.colors.BLACK)
            last_sms_phone_number = ft.Text(size=20, color=ft.colors.BLACK)
            row_sms = ft.Row([last_sms_phone_number, last_sms_text])
            if phone_number_input.value != "":
                print(phone_number_input.value, text.value)
                if send_sms(sms=text.value, number=phone_number_input.value):
                    print(True)
                    last_sms_text.value = text.value
                    last_sms_phone_number.value = phone_number_input.value
                    phone_number_input.value = ''
                    text.value = ''
                    page.add(row_sms)
                    page.update()

        phone_number_input = ft.TextField(width=180, height=50, bgcolor=ft.colors.ON_PRIMARY,
                                          hint_text='+993 65 000000')
        text = ft.TextField(width=300, height=50, bgcolor=ft.colors.ON_PRIMARY, hint_text='Text...')
        send_sms_btn = ft.ElevatedButton("Send SMS", bgcolor=ft.colors.GREEN, on_click=send, color='white',
                                         data=[phone_number_input.value, text.value])
        row = ft.Row([phone_number_input, text, send_sms_btn])

        if send_one_sms.data == 1:
            page.add(row)

        send_one_sms.data += 1
        page.update()

    # Elements
    header_text = ft.Container(
        ft.Text("SMS Sender by Shanazar ❤️", size=20, color='yellow', font_family='Times New Roman'),
        alignment=ft.alignment.center, margin=20)
    send_one_sms = ft.ElevatedButton("Send sms to", bgcolor=ft.colors.SECONDARY, on_click=send_sms_from_phone_input,
                                     data=1, color=ft.colors.BLACK, icon=ft.icons.SMS_ROUNDED,
                                     icon_color=ft.colors.AMBER_ACCENT_200)
    send_one_sms_container = ft.Container(send_one_sms)
    send_one_sms_container.margin = ft.margin.only(left=20)

    page.add(header_text, send_one_sms_container)

    page.update()


ft.app(target=main_ui)

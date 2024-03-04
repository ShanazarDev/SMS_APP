import time

from sms_by_modem import send_sms

import flet as ft


def main_ui(page: ft.Page):
    # Page Settings
    page.title = "SMS sender"
    page.window_maximizable = False
    page.window_resizable = False
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 320
    page.window_height = 600
    page.theme_mode = "light"

    def send_sms_func(e: ft.ControlEvent):
        phone = phone_number_input.value
        text = text_input.value
        if phone != '' and text != '':
            if send_sms(sms=f"{text_input.value}", number=f'+993{phone_number_input.value}'):
                phone_number_input.value = ''
                text_input.value = ''
                recent_send_list_view.controls.append(
                    ft.Text(value=f"{send_sms_btn.data}\n--->  Phone: \t\t{phone}\n--->  SMS: \t\t{text}"))
                send_sms_btn.data += 1
                page.update()

    def send_spam_sms_func(e: ft.ControlEvent):
        text = text_input.value
        c = 0
        if spam_to_five_thousand.value:
            with open('Numbers/N_5.txt', 'r') as n_5:
                for n in n_5.readlines():
                    t = n.split('\n')[0]
                    if send_sms(sms=f"{text}", number=f'+993{t}'):
                        recent_send_list_view.controls.append(ft.Text(f"Message sent ---> {t}"))
                        time.sleep(1)
                        c += 1
                    page.update()

        elif spam_to_ten_thousand.value:
            with open('Numbers/N_10.txt', 'r') as n_10:
                for n in n_10.readlines():
                    t = n.split('\n')[0]
                    recent_send_list_view.controls.append(ft.Text(f"{t}"))
        elif spam_to_fifteen_thousand.value:
            with open('Numbers/N_15.txt', 'r') as n_15:
                for n in n_15.readlines():
                    t = n.split('\n')[0]
                    recent_send_list_view.controls.append(ft.Text(f"{t}"))
        elif spam_to_twenty_thousand.value:
            with open('Numbers/N_20.txt', 'r') as n_20:
                for n in n_20.readlines():
                    t = n.split('\n')[0]
                    recent_send_list_view.controls.append(ft.Text(f"{t}"))
        print(c)
        page.update()

    def checkboxes_func(e: ft.ControlEvent):
        if e.control.data == spam_to_five_thousand.data and spam_to_five_thousand.value:
            spam_to_ten_thousand.disabled = True
            spam_to_fifteen_thousand.disabled = True
            spam_to_twenty_thousand.disabled = True
        elif e.control.data == spam_to_ten_thousand.data and spam_to_ten_thousand.value:
            spam_to_five_thousand.disabled = True
            spam_to_fifteen_thousand.disabled = True
            spam_to_twenty_thousand.disabled = True
        elif e.control.data == spam_to_fifteen_thousand.data and spam_to_fifteen_thousand.value:
            spam_to_five_thousand.disabled = True
            spam_to_ten_thousand.disabled = True
            spam_to_twenty_thousand.disabled = True
        elif e.control.data == spam_to_twenty_thousand.data and spam_to_twenty_thousand.value:
            spam_to_five_thousand.disabled = True
            spam_to_ten_thousand.disabled = True
            spam_to_fifteen_thousand.disabled = True
        else:
            spam_to_five_thousand.disabled = False
            spam_to_ten_thousand.disabled = False
            spam_to_fifteen_thousand.disabled = False
            spam_to_twenty_thousand.disabled = False

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

    # Spam sms
    spam_to_five_thousand = ft.Checkbox(label="5.000", data=5, on_change=checkboxes_func)
    spam_to_ten_thousand = ft.Checkbox(label="10.000", data=10, on_change=checkboxes_func)
    spam_to_fifteen_thousand = ft.Checkbox(label="15.000", data=15, on_change=checkboxes_func)
    spam_to_twenty_thousand = ft.Checkbox(label="20.000", data=20, on_change=checkboxes_func)

    send_spam_sms_btn = ft.ElevatedButton(text="Start Spam", icon=ft.icons.SMS, on_click=send_spam_sms_func)
    spam_sms_panel = ft.Row(
        [
            ft.Column(
                [
                    header_text,
                    ft.Row(
                        [
                            spam_to_five_thousand,
                            spam_to_ten_thousand
                        ],
                    ),
                    ft.Row(
                        [
                            spam_to_fifteen_thousand,
                            spam_to_twenty_thousand
                        ]
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

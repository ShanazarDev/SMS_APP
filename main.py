# import time

# import gammu
# from sms_by_modem import send_sms

import flet as ft


def main_ui(page: ft.Page):
    page.title = "SMS sender"
    page.window_maximizable = False
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_bgcolor = ft.colors.BLACK

    page.add(
        ft.Container(
            ft.Text("Hello World"),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.RED
        )
    )

    page.update()


ft.app(target=main_ui)

#!/usr/bin/env python3

#
# mecab_executor.py
#
# Date    : 2024-05-27
# Auther  : Hirotoshi FUJIBE
# History :
#
# Copyright (c) 2024 Hirotoshi FUJIBE
#

# Import Libraries
import flet as ft
import MeCab

# Windows Size
WINDOW_RATIO = 60
WINDOW_WIDTH = 16 * WINDOW_RATIO
WINDOW_HEIGHT = 10 * WINDOW_RATIO
LIST_SPACING = 0
LIST_PADDING = 5


# Execute Mecab
def execute_mecab(page: ft.Page, check_value: bool, text_value: str) -> None:
    compo_list = ft.ListView(expand=1, spacing=LIST_SPACING, padding=LIST_PADDING)
    page.add(ft.ResponsiveRow([compo_list]))
    if check_value:
        tagger = MeCab.Tagger()
        result = tagger.parse(text_value)
    else:
        wakati = MeCab.Tagger('-Owakati')
        result = wakati.parse(text_value)
    compo_list.controls.append(ft.Text(result))
    page.update()
    return


# Main
def main(page: ft.Page) -> None:

    def yes_click(e):  # noqa
        page.window_destroy()

    def no_click(e):  # noqa
        confirm_dialog.open = False
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text('Confirm'),
        content=ft.Text('Are you sure?'),
        actions=[
            ft.ElevatedButton('Yes', on_click=yes_click),
            ft.OutlinedButton('No', on_click=no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def window_event(e):
        if e.data == 'close':
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()
            return

    def click_execute_button(e):  # noqa
        text_value = str(compo_text[len(compo_text) - 1].value).strip()
        check_value = compo_check_button.value
        if not len(text_value):
            page.snack_bar = ft.SnackBar(ft.Text('日文を入力してください。'), show_close_icon=True)
            page.snack_bar.open = True
            page.update()
            return
        compo_text[len(compo_text) - 1].read_only = True
        page.remove(compo_input)
        execute_mecab(page, check_value, '%s' % text_value)
        compo_text.append(
            ft.TextField(label='日文', hint_text="日文を入力してください。",
                         value='', text_align=ft.TextAlign.LEFT, autofocus=True)
        )
        page.add(ft.ResponsiveRow([compo_text[len(compo_text) - 1]]), compo_input)
        page.update()
        return

    def click_close_button(e):  # noqa
        page.window_destroy()
        return

    page.title = 'Mecab Executor'
    page.scroll = ft.ScrollMode.ALWAYS
    page.window_width = WINDOW_WIDTH
    page.window_height = WINDOW_HEIGHT
    page.window_prevent_close = True
    page.on_window_event = window_event
    page.add(ft.ResponsiveRow([ft.Text('[日文] テキストボックスに日文を入力し [実行] ボタンをクリックすると、MeCab を呼び出して、日文の分析結果を表示します。')]))

    compo_text = [
        ft.TextField(label='日文', hint_text="日文を入力してください。",
                     value='', text_align=ft.TextAlign.LEFT, autofocus=True)
    ]
    compo_execute_button = ft.FilledButton(text="実行", on_click=click_execute_button)
    compo_close_button = ft.OutlinedButton(text="閉じる", on_click=click_close_button)
    compo_check_button = ft.Checkbox(label="詳細表示", value=False)
    compo_input = ft.Row([compo_execute_button, compo_check_button, compo_close_button])
    page.add(ft.ResponsiveRow([compo_text[0]]), compo_input)


# Goto Main
ft.app(target=main)

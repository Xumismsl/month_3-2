import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = 'ToDo list'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)
    filter_type = 'all'

 
    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed, task_time in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, completed, task_time))
        page.update()


    def create_task_row(task_id, task_text, completed, task_time):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)
        task_time_label = ft.Text(value=task_time or "", size=12, color=ft.Colors.GREY)

        def toggle_task(e):
            main_db.update_task_status(task_id, int(e.control.value))
            load_task()

        checkbox = ft.Checkbox(value=bool(completed), on_change=toggle_task)

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            task_field.read_only = True
            task_field.update()
            load_task()

        def delete_task(_):
            main_db.delete_task(task_id)
            load_task()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Редактировать",
                                    on_click=enable_edit, icon_color=ft.Colors.ORANGE_700)
        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task)
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED)

        return ft.Row([checkbox, task_time_label, task_field, edit_button, save_button, delete_button])


    def add_task(_):
        if task_input.value:
            if len(task_input.value) > 200:
                task_input.value = task_input.value[:200]
                task_input.value = "Слишком длинная задача! Максимум 200 символов."
                task_input.update()
                return
            
            
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id, task, 0, None))
            task_input.value = ''
            page.update()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton("В работе", on_click=lambda e: set_filter('uncompleted')),
        ft.ElevatedButton("Готово", on_click=lambda e: set_filter('completed'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    task_input = ft.TextField(label='Введите новую задачу', expand=True, on_submit=add_task)
    add_button = ft.IconButton(icon=ft.Icons.ADD, tooltip='Добавить задачу', on_click=add_task)

    delete_all_button = ft.IconButton(
        icon=ft.Icons.DELETE_SWEEP,
        tooltip="Удалить все задачи",
        on_click=lambda _: [main_db.delete_all_tasks(), load_task()],
        icon_color=ft.Colors.RED_ACCENT
    )

    page.add(
        ft.Row([task_input, add_button, delete_all_button]),
        filter_buttons,
        task_list
    )

    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)

import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = 'ToDo list'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, task_time in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text, task_time=task_time))
        page.update()

    def create_task_row(task_id, task_text, task_time):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)
        task_time_label = ft.Text(value=task_time, size=12, color=ft.Colors.GREY)

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            load_task()
            page.update()

        def delete_task(_):
            main_db.delete_task(task_id)
            load_task()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Редактировать", on_click=enable_edit, icon_color=ft.Colors.ORANGE_700)
        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task)
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED)

        return ft.Row([task_time_label ,task_field, edit_button, save_button, delete_button])

    def add_task(_):
        if task_input.value:
            task = task_input.value
            main_db.add_task(task)
            task_input.value = ''
            load_task()
            page.update()

    def delete_all_tasks(_):
        main_db.delete_all_tasks()
        load_task()

    task_input = ft.TextField(label='Введите новую задачу', expand=True, on_submit=add_task)
    add_button = ft.IconButton(icon=ft.Icons.ADD, tooltip='Добавить задачу', on_click=add_task)
    delete_all_button = ft.IconButton(
    icon=ft.Icons.DELETE_SWEEP,
    tooltip="Удалить все задачи",
    on_click=delete_all_tasks,
    icon_color=ft.Colors.RED_ACCENT
)


    page.add(
        ft.Row([task_input, add_button,delete_all_button]),
        task_list,
    )

    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)

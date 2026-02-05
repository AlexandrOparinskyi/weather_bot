from aiogram_dialog import DialogManager


async def getter_confirm_msg(dialog_manager: DialogManager,
                             **kwargs) -> dict[str, str]:
    msg = dialog_manager.dialog_data.get("msg")

    return {"text": f"Проверьте текст\n\n<code>{msg}</code>",}

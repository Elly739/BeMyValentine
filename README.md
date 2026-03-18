# Be My Valentine

A playful Valentine desktop app built with Python and Tkinter.

It includes:
- a romantic Valentine prompt
- a dodging `No` button
- a cinematic `Yes` flow
- floating hearts, sparkles, and celebration effects
- a hidden surprise message

## Quick Download

The easiest way to use the app is from the GitHub Release:

1. Open the latest Release on GitHub.
2. Download `BeMyValentine.exe` or `BeMyValentine-email.zip`.
3. If you downloaded the zip, extract it first.
4. Double-click `BeMyValentine.exe` to run it on Windows.

Note:
- Windows may show a security prompt before opening an unsigned app.
- Email providers often block raw `.exe` attachments, so `BeMyValentine-email.zip` is the better file to share by email.

## Run From Source

If you want to run the Python version instead:

```powershell
git clone https://github.com/Elly739/BeMyValentine.git
cd BeMyValentine
python .\valentine_app.py
```

## Build the Executable

To build the Windows executable yourself:

```powershell
pyinstaller --clean --noconfirm --onefile --windowed --icon=heart.ico --name "BeMyValentine" valentine_app.py
```

The built app will be created in:

```text
dist\BeMyValentine.exe
```

## Share By Email

For email sharing, send:

```text
dist\BeMyValentine-email.zip
```

That is the zipped executable version and is more likely to get through email filters than a raw `.exe` file.

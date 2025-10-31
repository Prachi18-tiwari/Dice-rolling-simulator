import tkinter
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import os


def create_app() -> tkinter.Tk:
    """Create and return the Tk application root for the dice app.

    Returns the Tk root so callers can call `.mainloop()` themselves.
    """
    # Use the directory where this script lives as the base for image lookup
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    root = tkinter.Tk()
    root.geometry('400x400')
    root.title('DataFlair Roll the Dice')

    Blankline = tkinter.Label(root, text="")
    Blankline.pack()

    HeadingLabel = tkinter.Label(root,
                                 text="Hello From DataFlair!",
                                 fg="light green",
                                 bg="dark green",
                                 font="Helvetica 16 bold italic")
    HeadingLabel.pack()

    # Build a list of PIL Image objects for the six die faces.
    dice_pil = []
    for i in range(1, 7):
        path = os.path.join(BASE_DIR, f'die{i}.png')
        if os.path.isfile(path):
            try:
                dice_pil.append(Image.open(path).convert('RGBA'))
            except Exception:
                # skip file if it can't be opened
                pass

    # If no image files found, generate simple placeholder images with the face number.
    if not dice_pil:
        size = (120, 120)
        try:
            # try to get a default truetype font; fall back to default bitmap if not available
            font = ImageFont.truetype("arial.ttf", 72)
        except Exception:
            font = ImageFont.load_default()

        for i in range(1, 7):
            img = Image.new('RGBA', size, 'white')
            draw = ImageDraw.Draw(img)
            text = str(i)
            # textsize availability varies between Pillow versions; prefer textbbox then fallback
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            except Exception:
                try:
                    w, h = font.getsize(text)
                except Exception:
                    # final fallback
                    w, h = 50, 50
            draw.text(((size[0]-w)/2, (size[1]-h)/2), text, fill='black', font=font)
            dice_pil.append(img)

    # Convert one image to PhotoImage for initial display and keep a reference to avoid GC
    current_pil = random.choice(dice_pil)
    DiceImage = ImageTk.PhotoImage(current_pil)
    ImageLabel = tkinter.Label(root, image=DiceImage)
    # store reference on the widget to prevent it being garbage-collected
    ImageLabel.image = DiceImage
    ImageLabel.pack(expand=True)

    def rolling_dice():
        # pick a random PIL image and convert to PhotoImage for tkinter
        pil = random.choice(dice_pil)
        photo = ImageTk.PhotoImage(pil)
        ImageLabel.configure(image=photo)
        ImageLabel.image = photo

    button = tkinter.Button(root, text="Roll the Dice", fg='blue', command=rolling_dice)
    button.pack(expand=True)

    return root


if __name__ == '__main__':
    app = create_app()
    app.mainloop()

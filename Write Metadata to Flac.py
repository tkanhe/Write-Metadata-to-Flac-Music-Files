import glob
import os
import requests
import urllib.request
import PySimpleGUI as Sg
from PIL import Image
from mutagen.flac import Picture, FLAC
from time import sleep

files = glob.glob(r"D:\Music\flacs\*.flac")
error = 3  # abs(length_of_local_file - track_length_from_itunes) in seconds [recommended range 1 to 5]
size = 600  # size of the cover 1000x1000 [possible range 300 to 3000]


def windows(fname, titles, artists, albums):
    l1 = [[Sg.Text("File Name:"), Sg.Text(fname)]]
    l2 = [[Sg.Text(i, size=(25, 2), pad=(3, 1)) for i in titles]]
    l3 = [[Sg.Text(i, size=(25, 2), pad=(3, 1)) for i in artists]]
    l4 = [[Sg.Text(i, size=(25, 2), pad=(3, 1)) for i in albums]]
    l5 = [[Sg.Text("Your Choice:"), Sg.InputText(), Sg.Submit()]]
    l6 = [[Sg.Image(f"{i}.png") for i in range(len(titles))]]
    layout = l1 + [[Sg.Text("-" * 100)]] + l2 + [[Sg.Text("-" * 100)]] + l3 + [[Sg.Text("-" * 100)]] + l4 + l5 + l6
    window = Sg.Window("TK", layout, font="Courier 12")
    event, values = window.read()
    window.close()
    return values[0]


def setup(err=3, sizes=1000):
    for j in files:
        sleep(1)
        try:
            audio = FLAC(j)
            name = os.path.splitext(os.path.basename(j))[0]
            u = f"https://itunes.apple.com/search?term={name}"
            r = requests.get(u)
            try:
                xx = r.json()["results"]
            except (Exception,):
                sleep(3)
                r = requests.get(u)
                xx = r.json()["results"]
            if xx:
                x1 = [i for i in xx if (i["kind"] == "song") and (abs(i["trackTimeMillis"] / 1000 - audio.info.length) <= err)]
            else:
                continue

            if not x1:
                continue

            x = [[i["trackCensoredName"], i["artistName"], i["collectionName"], i["primaryGenreName"], i["releaseDate"][:10], i["artworkUrl100"]] for i in x1[:4]]

            title = [i[0] for i in x]
            artist = [i[1] for i in x]
            album = [i[2] for i in x]
            genre = [i[3] for i in x]
            dates = [i[4] for i in x]
            urls = [i[5] for i in x]

            if (len(x) == 1) & (("original" in album[0].lower()) or ("EP" in album[0]) or ("single" in album[0].lower())):
                urllib.request.urlretrieve(urls[0].replace("100x100", f"{sizes}x{sizes}"), "0.jpeg")
                audio["title"] = title[0]
                audio["artist"] = artist[0]
                audio["album"] = album[0]
                audio["genre"] = genre[0]
                audio["date"] = dates[0]

                image = Picture()
                image.type = 3  # PictureType.COVER_FRONT
                image.mime = "image/jpeg"

                with open("0.jpeg", "rb") as f:
                    image.data = f.read()

                audio.add_picture(image)
                audio.save(deleteid3=True)
                continue

            for ind, url in enumerate(urls):
                urllib.request.urlretrieve(url.replace("100x100", f"{sizes}x{sizes}"), f"{ind}.jpeg")
                Image.open(f"{ind}.jpeg").resize((250, 250), Image.ANTIALIAS).save(f"{ind}.png")

            user_input = windows(name, title, artist, album)

            if user_input == "0" or user_input == "":
                continue

            if int(user_input) < len(title) + 1:
                audio["title"] = title[int(user_input) - 1]
                audio["artist"] = artist[int(user_input) - 1]
                audio["album"] = album[int(user_input) - 1]
                audio["genre"] = genre[int(user_input) - 1]
                audio["date"] = dates[int(user_input) - 1]

                image = Picture()
                image.type = 3
                image.mime = "image/jpeg"

                with open(f"{int(user_input) - 1}.jpeg", "rb") as f:
                    image.data = f.read()

                audio.add_picture(image)
                audio.save(deleteid3=True)

            else:
                continue

        except Exception as e:
            print("Error in file:", j)
            print(e)
            sleep(5)

    print("Task completed!!!")


if __name__ == __name__:
    setup(error, size)

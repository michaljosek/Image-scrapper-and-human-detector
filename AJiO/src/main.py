import tkinter as tk
from src.human_detection import *


ensure_input_folder_exists_and_is_empty()
ensure_output_folder_exists_and_is_empty()

root = tk.Tk()

main_canvas = tk.Canvas(root, width=500, height=300, relief='raised')
main_canvas.pack()

header_label = tk.Label(root, text='Detekcja czlowieka na zdjeciach ze strony internetowej')
header_label.config(font=('times', 14))
main_canvas.create_window(250, 25, window=header_label)

inform_label = tk.Label(root, text='Podaj adres strony internetowej:')
inform_label.config(font=('times', 10))
main_canvas.create_window(250, 100, window=inform_label)

input_entry = tk.Entry(root)
main_canvas.create_window(250, 140, window=input_entry)

error_label_http_request = tk.Label(root, text='Cos poszło nie tak (byc moze adres nie istnieje)!', font=('times', 10))
error_label_human_not_found = tk.Label(root, text='Nie znaleziono czlowieka na zdjeciu', font=('times', 10))


def handle_button_click():
    global error_label_http_request
    global error_label_human_not_found

    error_label_http_request.destroy()
    error_label_human_not_found.destroy()

    url = input_entry.get()
    is_ok_http_status, content = get_website_content(url)

    if not is_ok_http_status:
        error_label_http_request = tk.Label(root, text='Cos poszło nie tak (byc moze adres nie istnieje)!', font=('times', 10))
        main_canvas.create_window(250, 210, window=error_label_http_request)
        return

    image_urls = get_image_urls_from_content(content, url)
    download_images(image_urls)

    try:
        evaluate_input_images()
    except Exception as e:
        print('Could not evaluate img', str(e))

    output_files = get_output_files()

    if len(output_files) == 0:
        error_label_human_not_found = tk.Label(root, text='Nie znaleziono czlowieka na zdjeciu', font=('times', 10))
        main_canvas.create_window(250, 210, window=error_label_human_not_found)
        return

    success_label = tk.Label(root, text='Pomyslnie przetworzono zdjecia!', font=('times', 10))
    main_canvas.create_window(250, 150, window=success_label)
    fetch_url_button.destroy()
    inform_label.destroy()
    input_entry.destroy()

    return


fetch_url_button = tk.Button(text='Pobierz obrazki', command=handle_button_click, bg='blue', fg='white',
                             font=('times', 8, 'bold'))
main_canvas.create_window(250, 180, window=fetch_url_button)

root.mainloop()

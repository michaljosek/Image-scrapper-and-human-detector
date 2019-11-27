import tkinter as tk
from src.human_detection import *


#ensure_input_folder_exists_and_is_empty()
#ensure_output_folder_exists_and_is_empty()

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

    image_urls = get_image_urls_from_content(content)
    download_images(image_urls)
    #evaluate_input_images()
    output_files = get_output_files()

    tk_images = []
    if len(output_files) == 0:
        error_label_human_not_found = tk.Label(root, text='Nie znaleziono czlowieka na zdjeciu', font=('times', 10))
        main_canvas.create_window(250, 210, window=error_label_human_not_found)
        return

    for output_file in output_files:
        # im = Image.open(os.path.join(get_input_folder_path(), output_file))
        tk_image = tk.PhotoImage(os.path.join(get_input_folder_path(), output_file))
        tk_images.append(tk_image)

    main_canvas.delete("all")

    img_label = tk.Label(image=tk_images[0])
    main_canvas.create_window(0, 0, window=img_label)

    button_back = tk.Button(root, text="Wstecz")
    button_exit = tk.Button(root, text="Wyjscie")
    button_forward = tk.Button(root, text="Dalej")

    return


fetch_url_button = tk.Button(text='Pobierz obrazki', command=handle_button_click, bg='blue', fg='white',
                             font=('times', 8, 'bold'))
main_canvas.create_window(250, 180, window=fetch_url_button)

root.mainloop()

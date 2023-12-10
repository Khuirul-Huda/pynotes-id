import PySimpleGUI as sg
import sqlite3
from PIL import Image, ImageTk
# import tkinter as tk
sg.theme('Dark Brown 1')
# daftar_tema = sg.theme_list()
connection = sqlite3.connect('data.db', isolation_level=None)
sql = connection.cursor()

def setup_database():
    with connection:
        sql.execute('CREATE TABLE IF NOT EXISTS catatan (id INTEGER PRIMARY KEY, judul TEXT, isi TEXT)')

def ambil_data_catatan():
    with connection:
        query = sql.execute('SELECT * FROM catatan')
        hasil = query.fetchall()
    return hasil

def edit_catatan(id, judul, isi):
    with connection:
        sql.execute("""
        UPDATE catatan
        SET judul = ?,
            isi = ?
        WHERE
            id IS ?
        """, (judul, isi, id))
    notif('Berhasl disimpan!')


def buka_jendela_edit():
    indeks_catatan = window.Element('-CATATAN-LIST-').get_indexes()[0]
    catatan = data_catatan[indeks_catatan]

    event_edit, values_edit = sg.Window('Catatan', [[buat_layout_edit(catatan[0], catatan[1], catatan[2])]], modal=True).read(close=True)
    if event_edit == 'Edit':
        edit_catatan(values_edit['ID-EDIT-IN'], values_edit['JUDUL-EDIT-IN'], values_edit['ISI-EDIT-IN'])

def buat_layout_edit(id, judul, isi):
    return sg.Column([

    [
        sg.Frame('Catatan', [
        [
            sg.Input(default_text=id, key='ID-EDIT-IN', readonly=True, visible=False)
        ],
        [
            sg.Text('Judul:', font=15),
            sg.Input(default_text=judul, key='JUDUL-EDIT-IN', size=(50,1), font=15)
        ],
        [
            sg.Text('Isi:     ', font=15),
            sg.Multiline(default_text=isi, key='ISI-EDIT-IN', size=(50,19), font=15)
        ],
        [
            sg.Button('Edit', font=15)
        ]
    ], size=(600,500))
    ]

])

# tambah ke db
def tambah_catatan(judul, isi):
    with connection:
        sql.execute('INSERT INTO catatan (judul, isi) VALUES (?, ?)', (judul, isi))
    notif('Berhasil ditambahkan!')

def buka_jendela_tambah():
    event_tambah, values_tambah = sg.Window('Tambah Catatan', [[buat_layout_tambah()]], modal=True).read(close=True)
    if event_tambah == 'Simpan':
        tambah_catatan(values_tambah['JUDUL-ADD-IN'], values_tambah['ISI-ADD-IN'])

# layout tambah catatan
def buat_layout_tambah():
    return sg.Column([
    [
        sg.Frame('Tambah Catatan:', [
            [
                sg.Text('Judul:', font=15),
                sg.Input(key='JUDUL-ADD-IN', size=(35,1), font=15)
            ],
            [
                sg.Text('Isi:    ', font=15),
                sg.Multiline(key='ISI-ADD-IN', size=(35,15), font=15)
            ],
            [
                sg.Button('Simpan', font=15)
            ]
        ], size=(400,400))
    ]])
    
def hapus_catatan(indeks):
    catatan = data_catatan[indeks]
    id_catatan = catatan[0]
    with connection:
        sql.execute('DELETE FROM catatan WHERE id IS ?', (id_catatan,))

def perbarui_data():
    global data_catatan
    global daftar_judul
    data_catatan = ambil_data_catatan()
    daftar_judul = [i[1] for i in data_catatan]
    perbarui_daftar_catatan(daftar_judul)
    


def perbarui_daftar_catatan(daftar_judul_baru):
    window.Element('-CATATAN-LIST-').update(daftar_judul_baru)

def notif(msg):
    sg.popup_no_buttons(msg, font=15, no_titlebar=True, auto_close=True, auto_close_duration=2)
# start
setup_database()

data_catatan = ambil_data_catatan()
daftar_judul = [i[1] for i in data_catatan]

layout_utama = sg.Column([
    [sg.Text('Catatan Anda', font=25)],
    [sg.Text('Dibuat oleh: Muhammad Khuirul Huda 2304130046', font=14)],

    [sg.Frame('Daftar Catatan:', [
        [
            sg.Listbox(values=daftar_judul, size=(100,100), enable_events=True, key='-CATATAN-LIST-', font=15)
        ]
    ], size=(800,350))],
    [
        sg.Button('Buka', font=14),
        sg.Button('Tambah', font=14),
        sg.Button('Hapus', font=14)
    ]
])

# icon= b'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'
# root = tk.Tk()
# ic = Image.open(r'./favicon.jpeg')
# ic2 = ImageTk.PhotoImage(ic)

layout = [[layout_utama]]
window = sg.Window('PyNotes-ID', layout, finalize=True)


while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Buka':
        if len(values['-CATATAN-LIST-']) > 0:
            buka_jendela_edit()
        else:
            notif('Pilih catatan untuk dibuka!')
    elif event == 'Tambah':
        buka_jendela_tambah()
    elif event == 'Hapus':
        if len(values['-CATATAN-LIST-']) > 0:
            if sg.popup_yes_no('Sebuah catatan bisa bermakna apa saja\nCatatan hanya menggunakan sepersekian persen dari penyimpananmu', 'Apakah anda yakin untuk menghapus catatan ini?', font=14, title='Perhatian') == 'Yes':
                hapus_catatan(window.Element('-CATATAN-LIST-').get_indexes()[0])
                notif('Berhasil dihapus!')
        else:
            notif('Pilih catatan untuk dihapus!')
    if event != '-CATATAN-LIST-':
        perbarui_data()
window.close()
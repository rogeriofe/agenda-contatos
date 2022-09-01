# Simples Agenda de Contatos
import PySimpleGUI as Sg

data_values = []
file_text = "contatos.txt"
encoder_text = "iso-8859-1"

def read_file():
    data_values.clear()
    try:
        with open(file_text, 'r') as reader, open(file_text, 'r+', encoding=encoder_text) as writer:
            for lin in reader.readlines():
                if lin.strip():
                    writer.write(lin) # Grava nova linha no arquivo
                    lin = lin.rstrip().split(";")
                    data_values.append(lin)
                    data_values.sort()
            writer.truncate()
    except IOError:
        open(file_text, 'a+', encoding=encoder_text)
    return data_values


def update_file(nome, email, telefone):
    try:
        with open(file_text, 'a', encoding=encoder_text) as file_read:
            file_read.write('\n' + nome + ';' + email + ';' + telefone)
    except IOError:
        pass


def remove_file(nome):
    with open(file_text, 'r+', encoding=encoder_text) as file_read:
        lins = file_read.readlines()
        file_read.seek(0)
        for lin in lins:
            if nome not in lin:
                file_read.write(lin)
        file_read.truncate()


def first_win(data_values):
    headings = ['Nome', 'Email', 'Telefone']
    layout = [
        [Sg.Image('image.png', size=(600, 50))],
        [Sg.Table(
            values=data_values,
            max_col_width=25,
            auto_size_columns=False,
            justification='left',
            num_rows=10,
            row_height=30,
            enable_click_events=True,
            expand_x=False,
            expand_y=True,
            vertical_scroll_only=False,
            headings=headings,
            key='TABLE',
            col_widths=[18,20,15]
            )
        ],
        [Sg.Button('NOVO'), Sg.Button('APAGAR')]
    ]
    return Sg.Window('Agenda de Contatos', size=(600,450), layout=layout, finalize=True, font='Helvetica 12', resizable=False)


def second_win():
    layout = [
        [Sg.Text('Digite o Nome')],
        [Sg.InputText('', key='txt_nome')],
        [Sg.Text('Digite o Email')],
        [Sg.InputText('', key='txt_email')],
        [Sg.Text('Digite o Telefone')],
        [Sg.InputText('', key='txt_fone')],
        [Sg.Button('SALVAR'), Sg.Button('CANCELAR')]
    ]
    return Sg.Window('Novo Contato', layout=layout, finalize=True)


win1, win2 = first_win(read_file()), None
while True:
    window, event, values = Sg.read_all_windows()
    if window == win1 and event == Sg.WINDOW_CLOSED:
        break

    if window == win1 and event == 'NOVO':
        win2 = second_win()

    if window == win2 and event == 'CANCELAR':
        win2.close()

    if window == win2 and event == 'SALVAR':
        update_file(values['txt_nome'], values['txt_email'], values['txt_fone'])
        win = win1.find_element(key='TABLE')
        win.update(read_file())
        win2.close()

    if window == win1 and event == 'APAGAR':
        if values['TABLE']:
            key = int(values['TABLE'][0])
            remove_file(data_values[key][0])
            win = win1.find_element(key='TABLE')
            win.update(read_file())


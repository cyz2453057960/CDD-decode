import tkinter as tk
from tkinter import filedialog, scrolledtext
from argparse import Namespace
from typing import List, Optional
import odxtools.cli.decode as decode
from odxtools.odxtypes import ParameterValue
import sys
from io import StringIO




def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDX files", "*.pdx")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)


class UtilFunctions:


    @staticmethod
    def run_decode_tool(
        data: str,
        decode_data: bool = True,
        path_to_pdx_file: str = "./examples/somersault.pdx",
        ecu_variants: Optional[List[str]] = None,
    ) -> None:
        decode_args = Namespace(
            pdx_file=path_to_pdx_file, variants=ecu_variants, data=data, decode=decode_data)

        decode.run(decode_args)


def get_display_value(v: ParameterValue) -> str:
    if isinstance(v, bytes):
        return v.hex(" ")
    elif isinstance(v, int):
        return f"{v} (0x{v:x})"
    else:
        return str(v)


def confirm():
    file_path = file_entry.get()
    input_text = text_entry.get()
    if file_path and input_text:
        try:
            # ???????????
            output = StringIO()

            # ???????
            sys.stdout = output
            UtilFunctions.run_decode_tool(data=input_text, path_to_pdx_file=file_path)
            result = output.getvalue()

            # ??????
            sys.stdout = sys.__stdout__
            # ??????????
            result = str(result)

            # ???????
            output_textbox.delete(1.0, tk.END)

            # ??????
            for line in result.splitlines():
                parts = line.split(',')
                for part in parts:
                    if 'STRUCTURE' in part:
                        index = part.index('STRUCTURE') + len('STRUCTURE')
                        output_textbox.insert(tk.END, part[:index + 2].strip() + "\n" + part[index + 2:].strip() + "\n")
                    elif 'True' in part:
                        output_textbox.insert(tk.END, part.strip() + "\n", 'red')
                    else:
                        output_textbox.insert(tk.END, part.strip() + "\n")
        except Exception as e:
            output_textbox.delete(1.0, tk.END)
            output_textbox.insert(tk.END, f"An error occurred: {e}")
    else:
        output_textbox.delete(1.0, tk.END)
        output_textbox.insert(tk.END, "Please select a file and enter text.")



root = tk.Tk()




root.title("PDX File Selector")


file_label = tk.Label(root, text="Select PDX file:")
file_label.pack(pady=5)
file_entry = tk.Entry(root, width=100)
file_entry.pack(pady=5)
file_button = tk.Button(root, text="Browse", command=select_file)
file_button.pack(pady=5)


text_label = tk.Label(root, text="Input text:")
text_label.pack(pady=5)
text_entry = tk.Entry(root, width=100)
text_entry.pack(pady=5)


confirm_button = tk.Button(root, text="Confirm", command=confirm)
confirm_button.pack(pady=5)


output_label = tk.Label(root, text="Output:")
output_label.pack(pady=5)
output_textbox = scrolledtext.ScrolledText(root, width=100, height=40)
output_textbox.pack(pady=5)


signature=tk.Label(root, text="V0.1 Provided by Chiyuze")
signature.pack(pady=0)

output_textbox.tag_configure('red', foreground='red')


root.mainloop()

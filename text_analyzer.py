"""Analyze a text file and save its statistics to a report."""

import re
import tkinter as tk
from collections import Counter
from pathlib import Path
from tkinter import filedialog, messagebox


ENCODINGS = ("utf-8-sig", "utf-8", "cp1251")
STATISTIC_TYPES = (
    "Полная статистика",
    "Символы",
    "Строки",
    "Слова",
    "Частые слова",
)


def read_text_file(file_path: Path) -> str:
    """Read a text file using the first supported encoding."""
    for encoding in ENCODINGS:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue

    raise UnicodeError("Не удалось определить кодировку файла.")


def analyze_text(text: str, statistic_type: str) -> str:
    """Return the selected text statistics as a formatted report."""
    words = re.findall(r"[а-яёa-z0-9]+", text.lower())
    frequent_words = Counter(words).most_common(10)

    if statistic_type == "Символы":
        return f"Количество символов: {len(text)}"

    if statistic_type == "Строки":
        return f"Количество строк: {len(text.splitlines())}"

    if statistic_type == "Слова":
        return (
            f"Количество слов: {len(words)}\n"
            f"Количество уникальных слов: {len(set(words))}"
        )

    report_lines = []
    if statistic_type == "Полная статистика":
        report_lines.extend(
            [
                f"Количество символов: {len(text)}",
                f"Количество строк: {len(text.splitlines())}",
                f"Количество слов: {len(words)}",
                f"Количество уникальных слов: {len(set(words))}",
            ]
        )

    if statistic_type in ("Полная статистика", "Частые слова"):
        report_lines.extend(["", "Самые частые слова:"])
        if frequent_words:
            for word, count in frequent_words:
                report_lines.append(f"{word}: {count}")
        else:
            report_lines.append("В файле нет слов.")

    return "\n".join(report_lines)


class TextAnalyzerApp:
    """The application window and its button actions."""

    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.window.title("Text File Statistics Analyzer")
        self.window.geometry("620x480")

        self.file_path: Path | None = None
        self.text = ""
        self.report = ""

        tk.Label(
            window,
            text="Text File Statistics Analyzer",
            font=("Arial", 14, "bold"),
        ).pack(pady=12)

        tk.Button(window, text="Выбрать файл", command=self.select_file).pack()

        self.file_name_label = tk.Label(window, text="Файл не выбран")
        self.file_name_label.pack(pady=8)

        self.statistic_type = tk.StringVar(value=STATISTIC_TYPES[0])
        tk.OptionMenu(
            window,
            self.statistic_type,
            *STATISTIC_TYPES,
            command=self.show_statistics,
        ).pack()

        self.result_box = tk.Text(window, height=17, width=70)
        self.result_box.pack(padx=12, pady=8, fill="both", expand=True)

        tk.Button(
            window,
            text="Сохранить отчёт",
            command=self.save_report,
        ).pack(pady=10)

    def select_file(self) -> None:
        selected_path = filedialog.askopenfilename(
            title="Выберите текстовый файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
        )
        if not selected_path:
            return

        try:
            self.text = read_text_file(Path(selected_path))
        except (OSError, UnicodeError) as error:
            messagebox.showerror("Ошибка чтения", str(error))
            return

        self.file_path = Path(selected_path)
        self.file_name_label.config(text=self.file_path.name)
        self.show_statistics()

    def show_statistics(self, selected_type: str | None = None) -> None:
        if self.file_path is None:
            return

        self.report = analyze_text(self.text, self.statistic_type.get())
        print(self.report)
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, self.report)

    def save_report(self) -> None:
        if not self.report or self.file_path is None:
            messagebox.showinfo("Нет отчёта", "Сначала выберите текстовый файл.")
            return

        default_name = f"{self.file_path.stem}_статистика.txt"
        save_path = filedialog.asksaveasfilename(
            title="Сохранить отчёт",
            initialfile=default_name,
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt")],
        )
        if not save_path:
            return

        try:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(self.report)
        except OSError as error:
            messagebox.showerror("Ошибка сохранения", str(error))
            return

        messagebox.showinfo("Готово", "Отчёт сохранён.")


def main() -> None:
    window = tk.Tk()
    TextAnalyzerApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()

import hashlib
import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import urllib.request

# Наша резервная локальная база (если вдруг пропадет интернет)
LOCAL_BAD_HASHES = {
    "44d88612fea8a8f36de82e1278abb02f": "EICAR-Test-File (Тестовый вирус)",
    "5d41402abc4b2a76b9719d911017c592": "Trojan.Generic.Example (Наш тест с hello)",
    "0d796bf911ea09abf1a0c88b5674b9a8": "Suspicious.Image.Detected (Твоя прошлая фотка)",
    "d5ce547e24549152b1b7264ba61edddf": "Malware.Torrent.SuspiciousSetup (Твой торрент-файл)",
}

QUARANTINE_DIR = "C:\\Antivirus_Quarantine"
cloud_database = {}  # Сюда скачаются хэши из интернета


def init_quarantine():
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)


def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None


class AegisAntivirusApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Aegis Cloud Antivirus v2.5")
        self.root.geometry("650x480")
        self.root.configure(bg="#1e1e2e")  # Глубокий темно-синий/серый цвет
        self.root.resizable(False, False)

        # Главный заголовок
        self.title_label = tk.Label(
            root,
            text="🛡️ AEGIS SECURITY CORE",
            font=("Arial", 20, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4",
        )
        self.title_label.pack(pady=15)

        # Статус системы
        self.status_label = tk.Label(
            root,
            text="Подключение к облаку...",
            font=("Arial", 12, ),
            bg="#1e1e2e",
            fg="#f9e2af",
        )
        self.status_label.pack(pady=5)

        # Текстовая консоль для красивого вывода логов
        self.log_box = tk.Text(
            root,
            width=70,
            height=14,
            bg="#11111b",
            fg="#a6e3a1",
            font=("Consolas", 10),
            state="disabled",
            bd=0,
            highlightthickness=1,
            highlightbackground="#45475a",
        )
        self.log_box.pack(pady=15)

        # Кнопка «Выбрать и проверить файл»
        self.scan_file_btn = tk.Button(
            root,
            text="📁 Проверить подозрительный файл",
            font=("Arial", 11, "bold"),
            bg="#89b4fa",
            fg="#11111b",
            activebackground="#b4befe",
            cursor="hand2",
            bd=0,
            width=35,
            height=2,
            command=self.browse_and_scan,
            state="disabled",  # Пока облако не загрузится, кнопка спит
        )
        self.scan_file_btn.pack(pady=10)

        # Подпись внизу
        self.footer = tk.Label(
            root,
            text="Threat Intelligence Cloud Connected | CyberSecurity Project",
            font=("Arial", 9),
            bg="#1e1e2e",
            fg="#585b70",
        )
        self.footer.pack(side="bottom", pady=10)

        # Запускаем фоновую загрузку облачной базы, чтобы окно не зависало при старте
        threading.Thread(target=self.load_cloud, daemon=True).start()

    def log_message(self, text):
        """Красиво дописывает строки в нашу внутреннюю консоль программы"""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def load_cloud(self):
        global cloud_database
        self.log_message(
            "[*] Инициализация сетевых модулей...\n[*] Подключение к облачной базе угроз (MalwareBazaar)..."
        )
        url = "https://abuse.ch"

        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode("utf-8")

            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if len(line) == 32:
                    cloud_database[line] = (
                        "Cloud.Malware.RecentThreat (Свежая угроза из сети)"
                    )

            self.log_message(
                f"[✓] Глобальное облако подключено успешно!\n[✓] В оперативную память загружено {len(cloud_database)} актуальных вирусов за сегодня."
            )
            self.status_label.configure(
                text="Статус: Защищено (Облачная база активна)", fg="#a6e3a1"
            )
            self.scan_file_btn.configure(state="normal")  # Активируем кнопку

        except Exception as e:
            self.log_message(
                f"[⚠️ Предупреждение] Не удалось связаться с облаком: {e}"
            )
            self.log_message("[*] Антивирус перешел на локальную мини-базу.")
            cloud_database = LOCAL_BAD_HASHES
            self.status_label.configure(
                text="Статус: Защищено (Локальная база)", fg="#f38ba8"
            )
            self.scan_file_btn.configure(state="normal")

    def browse_and_scan(self):
        """Открывает красивое окно Windows для выбора файла"""
        file_selected = filedialog.askopenfilename(
            title="Выбери файл для проверки антивирусом Aegis"
        )
        if not file_selected:
            return  # Если пользователь просто закрыл окно выбора

        file_name = os.path.basename(file_selected)
        self.log_message(f"\n[*] Анализ файла: {file_name}")

        file_hash = get_file_hash(file_selected)
        self.log_message(f"[*] Вычислен цифровой отпечаток (MD5): {file_hash}")

        # Проверка по базам данных
        if file_hash in cloud_database:
            self.log_message(
                f"[🚨 ВНИМАНИЕ] ОБЛАКО ОБНАРУЖИЛО ВИРУС: {cloud_database[file_hash]}"
            )
            self.quarantine_process(file_selected, file_name)
        elif file_hash in LOCAL_BAD_HASHES:
            self.log_message(
                f"[🚨 ВНИМАНИЕ] ЛОКАЛЬНАЯ БАЗА ОБНАРУЖИЛА ВИРУС: {LOCAL_BAD_HASHES[file_hash]}"
            )
            self.quarantine_process(file_selected, file_name)
        else:
            self.log_message(
                "[✓] Сканирование завершено. Угрозы не найдены. Файл чист!"
            )
            messagebox.showinfo(
                "Aegis Сканер", f"Файл {file_name} успешно проверен. Он безопасен."
            )

    def quarantine_process(self, file_path, file_name):
        """Изолирует опасный файл"""
        try:
            init_quarantine()
            quarantine_path = os.path.join(
                QUARANTINE_DIR, file_name + ".locked"
            )
            shutil.move(file_path, quarantine_path)
            self.log_message(
                f"[🔒 КАРАНТИН] Опасный объект изолирован в: {quarantine_path}"
            )
            messagebox.showwarning(
                "🚨 УГРОЗА ОБНАРУЖЕНА",
                f"Внимание! Файл {file_name} распознан как вредоносный и перемещен в безопасный карантин!",
            )
        except Exception as e:
            self.log_message(f"[❌ Ошибка карантина]: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AegisAntivirusApp(root)
    root.mainloop()

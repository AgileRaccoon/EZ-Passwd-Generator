import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip
import json
import os

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("パスワード生成アプリ")
        
        # 設定ファイルのパス
        self.config_file = "config.json"
        
        # 安全な記号と特殊記号の定義
        self.safe_symbols = "-._@"
        self.special_symbols = "".join(c for c in string.punctuation if c not in self.safe_symbols)
        
        # メインフレーム
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 変数の初期化
        self.length_var = tk.StringVar(value="12")
        self.use_safe_symbols = tk.BooleanVar(value=True)
        self.use_special_symbols = tk.BooleanVar(value=False)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_numbers = tk.BooleanVar(value=True)
        self.auto_copy = tk.BooleanVar(value=False)
        
        # 保存された設定の読み込み
        self.load_settings()
        
        # パスワードの長さ設定
        ttk.Label(main_frame, text="パスワードの長さ:").grid(row=0, column=0, sticky=tk.W)
        self.length_entry = ttk.Entry(main_frame, textvariable=self.length_var, width=10)
        self.length_entry.grid(row=0, column=1, sticky=tk.W)
        
        # オプションフレーム
        option_frame = ttk.LabelFrame(main_frame, text="オプション", padding="5")
        option_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 記号の説明
        ttk.Label(option_frame, text="安全な記号: " + self.safe_symbols).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(option_frame, text="特殊記号: " + self.special_symbols[:10] + "...").grid(row=1, column=0, columnspan=2, sticky=tk.W)
        
        # チェックボックス
        ttk.Checkbutton(option_frame, text="安全な記号を含める", variable=self.use_safe_symbols, command=self.save_settings).grid(row=2, column=0, sticky=tk.W)
        ttk.Checkbutton(option_frame, text="特殊記号を含める", variable=self.use_special_symbols, command=self.save_settings).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(option_frame, text="大文字を含める", variable=self.use_uppercase, command=self.save_settings).grid(row=4, column=0, sticky=tk.W)
        ttk.Checkbutton(option_frame, text="数字を含める", variable=self.use_numbers, command=self.save_settings).grid(row=5, column=0, sticky=tk.W)
        ttk.Checkbutton(option_frame, text="生成時に自動コピー", variable=self.auto_copy, command=self.save_settings).grid(row=6, column=0, sticky=tk.W)
        
        # パスワード表示エリア
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, width=30)
        password_entry.grid(row=2, column=0, columnspan=2, pady=10)
        
        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        # ボタン
        ttk.Button(button_frame, text="生成", command=self.generate_password).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="コピー", command=self.copy_to_clipboard).grid(row=0, column=1, padx=5)
        
        # 長さが変更されたときの保存
        self.length_var.trace_add("write", lambda *args: self.save_settings())
        
        # ウィンドウが閉じられたときの処理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_settings(self):
        """設定をJSONファイルから読み込む"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                self.length_var.set(settings.get('length', '12'))
                self.use_safe_symbols.set(settings.get('use_safe_symbols', True))
                self.use_special_symbols.set(settings.get('use_special_symbols', False))
                self.use_uppercase.set(settings.get('use_uppercase', True))
                self.use_numbers.set(settings.get('use_numbers', True))
                self.auto_copy.set(settings.get('auto_copy', False))
        except Exception as e:
            print(f"設定の読み込みエラー: {e}")
            
    def save_settings(self):
        """現在の設定をJSONファイルに保存"""
        try:
            settings = {
                'length': self.length_var.get(),
                'use_safe_symbols': self.use_safe_symbols.get(),
                'use_special_symbols': self.use_special_symbols.get(),
                'use_uppercase': self.use_uppercase.get(),
                'use_numbers': self.use_numbers.get(),
                'auto_copy': self.auto_copy.get()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"設定の保存エラー: {e}")
            
    def on_closing(self):
        """ウィンドウが閉じられるときの処理"""
        self.save_settings()
        self.root.destroy()
        
    def generate_password(self):
        try:
            length = int(self.length_var.get())
            if length <= 0:
                self.password_var.set("長さは正の整数を指定してください")
                return
        except ValueError:
            self.password_var.set("有効な数値を入力してください")
            return
            
        # 使用する文字セットの準備
        chars = string.ascii_lowercase
        if self.use_uppercase.get():
            chars += string.ascii_uppercase
        if self.use_numbers.get():
            chars += string.digits
        if self.use_safe_symbols.get():
            chars += self.safe_symbols
        if self.use_special_symbols.get():
            chars += self.special_symbols
            
        if not chars:
            self.password_var.set("少なくとも1つのオプションを選択してください")
            return
            
        # パスワード生成
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
        
        # 自動コピーが有効な場合
        if self.auto_copy.get():
            self.copy_to_clipboard()
        
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password and not password.startswith("長さ") and not password.startswith("有効"):
            pyperclip.copy(password)

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
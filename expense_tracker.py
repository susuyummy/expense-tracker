import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar

# 設定 matplotlib 中文字型
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STHeiti', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳小工具")
        
        # 設定字型
        self.default_font = ('PingFang SC', 10)
        self.title_font = ('PingFang SC', 16, 'bold')
        
        # 設定視窗大小和位置
        window_width = 1200
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 設定預設字型
        self.root.option_add('*Font', self.default_font)
        
        # 建立主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立標題
        title_label = ttk.Label(
            main_frame,
            text="記帳小工具",
            font=self.title_font
        )
        title_label.pack(pady=10)
        
        # 建立左右分欄
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左側框架（輸入區域）
        left_frame = ttk.Frame(paned_window, padding="10")
        paned_window.add(left_frame, weight=1)
        
        # 右側框架（統計和圖表）
        right_frame = ttk.Frame(paned_window, padding="10")
        paned_window.add(right_frame, weight=1)
        
        # 建立輸入區域
        self.create_input_area(left_frame)
        
        # 建立統計區域
        self.create_statistics_area(right_frame)
        
        # 初始化資料
        self.data_file = "expense_data.json"
        self.load_data()
        
        # 更新顯示
        self.update_statistics()
    
    def create_input_area(self, parent):
        """建立輸入區域"""
        # 建立輸入框架
        input_frame = ttk.LabelFrame(parent, text="新增記錄", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # 使用 Grid 布局管理器
        input_frame.columnconfigure(1, weight=1)
        
        # 日期選擇
        ttk.Label(input_frame, text="日期:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=20)
        date_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 類型選擇
        ttk.Label(input_frame, text="類型:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="支出")
        type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, values=["收入", "支出"], width=20)
        type_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 分類選擇
        ttk.Label(input_frame, text="分類:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, width=20)
        self.category_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 金額輸入
        ttk.Label(input_frame, text="金額:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, width=20)
        amount_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # 備註輸入
        ttk.Label(input_frame, text="備註:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.note_var = tk.StringVar()
        note_entry = ttk.Entry(input_frame, textvariable=self.note_var, width=40)
        note_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # 新增按鈕
        add_button = ttk.Button(
            input_frame,
            text="新增記錄",
            command=self.add_record
        )
        add_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # 建立記錄列表
        list_frame = ttk.LabelFrame(parent, text="記錄列表", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 建立表格
        columns = ("日期", "類型", "分類", "金額", "備註")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # 設定欄位標題和寬度
        self.tree.heading("日期", text="日期")
        self.tree.heading("類型", text="類型")
        self.tree.heading("分類", text="分類")
        self.tree.heading("金額", text="金額")
        self.tree.heading("備註", text="備註")
        
        self.tree.column("日期", width=100)
        self.tree.column("類型", width=80)
        self.tree.column("分類", width=100)
        self.tree.column("金額", width=100)
        self.tree.column("備註", width=200)
        
        # 加入捲動條
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置表格和捲動條
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 綁定刪除事件
        self.tree.bind("<Delete>", self.delete_record)
        
        # 更新分類選項
        self.update_categories()
    
    def create_statistics_area(self, parent):
        """建立統計區域"""
        # 建立統計框架
        stats_frame = ttk.LabelFrame(parent, text="統計資訊", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)
        
        # 使用 Grid 布局管理器
        stats_frame.columnconfigure(1, weight=1)
        
        # 總收入
        ttk.Label(stats_frame, text="總收入:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.total_income_var = tk.StringVar(value="0")
        ttk.Label(stats_frame, textvariable=self.total_income_var).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 總支出
        ttk.Label(stats_frame, text="總支出:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.total_expense_var = tk.StringVar(value="0")
        ttk.Label(stats_frame, textvariable=self.total_expense_var).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 結餘
        ttk.Label(stats_frame, text="結餘:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.balance_var = tk.StringVar(value="0")
        ttk.Label(stats_frame, textvariable=self.balance_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 建立圖表框架
        chart_frame = ttk.LabelFrame(parent, text="支出分類統計", padding="10")
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 建立圖表
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_categories(self):
        """更新分類選項"""
        categories = {
            "收入": ["薪資", "獎金", "投資", "其他收入"],
            "支出": ["飲食", "交通", "住宿", "娛樂", "購物", "醫療", "教育", "其他支出"]
        }
        self.category_combo["values"] = categories[self.type_var.get()]
        if not self.category_var.get() in categories[self.type_var.get()]:
            self.category_var.set(categories[self.type_var.get()][0])
    
    def add_record(self):
        """新增記錄"""
        try:
            # 獲取輸入值
            date = self.date_var.get()
            type_ = self.type_var.get()
            category = self.category_var.get()
            amount = float(self.amount_var.get())
            note = self.note_var.get()
            
            # 驗證輸入
            if not all([date, type_, category, amount]):
                raise ValueError("請填寫所有必要欄位")
            
            # 新增記錄
            record = {
                "date": date,
                "type": type_,
                "category": category,
                "amount": amount,
                "note": note
            }
            
            self.records.append(record)
            self.save_data()
            self.update_display()
            self.update_statistics()
            
            # 清空輸入
            self.amount_var.set("")
            self.note_var.set("")
            
        except ValueError as e:
            messagebox.showerror("錯誤", str(e))
    
    def delete_record(self, event):
        """刪除記錄"""
        selected = self.tree.selection()
        if not selected:
            return
        
        if messagebox.askyesno("確認", "確定要刪除選中的記錄嗎？"):
            for item in selected:
                index = self.tree.index(item)
                self.records.pop(index)
            
            self.save_data()
            self.update_display()
            self.update_statistics()
    
    def update_display(self):
        """更新顯示"""
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 加入記錄
        for record in self.records:
            self.tree.insert("", tk.END, values=(
                record["date"],
                record["type"],
                record["category"],
                f"{record['amount']:.2f}",
                record["note"]
            ))
    
    def update_statistics(self):
        """更新統計資訊"""
        # 計算總收入
        total_income = sum(
            record["amount"]
            for record in self.records
            if record["type"] == "收入"
        )
        
        # 計算總支出
        total_expense = sum(
            record["amount"]
            for record in self.records
            if record["type"] == "支出"
        )
        
        # 計算結餘
        balance = total_income - total_expense
        
        # 更新顯示
        self.total_income_var.set(f"{total_income:.2f}")
        self.total_expense_var.set(f"{total_expense:.2f}")
        self.balance_var.set(f"{balance:.2f}")
        
        # 更新圖表
        self.update_chart()
    
    def update_chart(self):
        """更新圖表"""
        # 清空圖表
        self.ax.clear()
        
        # 統計支出分類
        categories = {}
        for record in self.records:
            if record["type"] == "支出":
                category = record["category"]
                amount = record["amount"]
                categories[category] = categories.get(category, 0) + amount
        
        if categories:
            # 繪製圓餅圖
            labels = list(categories.keys())
            sizes = list(categories.values())
            
            self.ax.pie(sizes, labels=labels, autopct="%1.1f%%")
            self.ax.set_title("支出分類統計", fontproperties='PingFang SC')
            
            # 更新畫布
            self.canvas.draw()
    
    def load_data(self):
        """載入資料"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
            except:
                self.records = []
        else:
            self.records = []
    
    def save_data(self):
        """儲存資料"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

def main():
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random

# --- 1. ฐานข้อมูลพนักงาน (จำลอง 500 คน) ---
def get_employees():
    first = ["สมชาย", "วิชัย", "มานะ", "อารี", "นงลักษณ์", "ประเสริฐ", "วิภา", "เกียรติ", "สุรพล", "ดาริน"]
    last = ["ใจดี", "รักเรียน", "พูนทรัพย์", "ศรีสุข", "มั่งมี", "รุ่งเรือง", "ทองดี", "ขยันยิ่ง", "มั่นคง"]
    return {i: f"{random.choice(first)}{random.choice(last)}" for i in range(1, 501)}

EMPLOYEES = get_employees()

class FinalLuckyDraw:
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบสุ่มสลากรางวัล (Credit Version)")
        self.root.geometry("1150x850")
        self.root.configure(bg="#F8F9FA")

        self.current_event = ""
        self.available_tickets = [] 
        self.normal_winners = []   
        self.jackpot_winners = []  
        self.algo_choice = tk.IntVar(value=1)

        self.main_container = tk.Frame(self.root, bg="#F8F9FA")
        self.main_container.pack(fill="both", expand=True)

        self.show_home_page()

    # --- หน้าที่ 1: หน้าแรก ---
    def show_home_page(self):
        self.clear_frame()
        
        # กล่องเมนูหลักกลางหน้าจอ
        home = tk.Frame(self.main_container, bg="white", padx=60, pady=50, highlightthickness=1, highlightbackground="#DEE2E6")
        home.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(home, text="LUCKY DRAW", font=("Segoe UI", 32, "bold"), bg="white", fg="#4E73DF").pack(pady=(0, 10))
        tk.Label(home, text="โปรดเลือกระบบและกิจกรรมที่ต้องการ", font=("Tahoma", 12), bg="white", fg="#6C757D").pack(pady=(0, 20))

        # ส่วนเลือกโปรแกรม
        algo_frame = tk.LabelFrame(home, text=" เลือกรูปแบบโปรแกรม ", bg="white", font=("Tahoma", 10, "bold"), padx=20, pady=15, fg="#4E73DF")
        algo_frame.pack(pady=10, fill="x")
        tk.Radiobutton(algo_frame, text="โปรแกรม 1: สุ่มตัวเลขแล้วตัดชื่อออก", variable=self.algo_choice, value=1, bg="white", font=("Tahoma", 11)).pack(anchor="w", pady=5)
        tk.Radiobutton(algo_frame, text="โปรแกรม 2: เรียงตามลำดับ 1, 2, 3...", variable=self.algo_choice, value=2, bg="white", font=("Tahoma", 11)).pack(anchor="w", pady=5)

        # ปุ่มเลือกกิจกรรม
        btn_box = tk.Frame(home, bg="white")
        btn_box.pack(pady=20)
        
        tk.Button(btn_box, text="เข้าสู่ระบบ: งานปีใหม่ แผนก A", command=lambda: self.start_app("งานปีใหม่ A"), 
                  bg="#4E73DF", fg="white", font=("Tahoma", 12, "bold"), width=30, pady=12, relief="flat", cursor="hand2").pack(pady=5)
        tk.Button(btn_box, text="เข้าสู่ระบบ: งานปีใหม่ แผนก B", command=lambda: self.start_app("งานปีใหม่ B"), 
                  bg="#1CC88A", fg="white", font=("Tahoma", 12, "bold"), width=30, pady=12, relief="flat", cursor="hand2").pack(pady=5)

        # --- ส่วนเครดิตมุมขวาล่าง ---
        credit_lbl = tk.Label(self.main_container, text="จัดทำโดย นายอดิศร ทองแดง 684245018", 
                             font=("Tahoma", 10), bg="#F8F9FA", fg="#AAB7B8")
        credit_lbl.place(relx=0.98, rely=0.98, anchor="se")

    def start_app(self, event_name):
        self.current_event = event_name
        self.available_tickets = list(EMPLOYEES.keys())
        self.normal_winners = []
        self.jackpot_winners = []
        self.show_draw_page()

    # --- หน้าที่ 2: หน้าสุ่มหลัก ---
    def show_draw_page(self):
        self.clear_frame()
        header = tk.Frame(self.main_container, bg="#4E73DF", pady=15)
        header.pack(fill="x")
        tk.Button(header, text=" กลับหน้าแรก ", command=self.show_home_page, bg="#2E59D9", fg="white", relief="flat").pack(side="left", padx=20)
        tk.Label(header, text=f"EVENT: {self.current_event}", font=("Tahoma", 16, "bold"), bg="#4E73DF", fg="white").pack(side="left", padx=20)

        body = tk.Frame(self.main_container, bg="#F8F9FA", padx=20, pady=20)
        body.pack(fill="both", expand=True)

        # ฝั่งซ้าย: เครื่องสุ่ม
        left_side = tk.Frame(body, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#DEE2E6")
        left_side.pack(side="left", fill="both", expand=True, padx=10)

        self.lbl_id = tk.Label(left_side, text="000", font=("Arial", 120, "bold"), bg="white", fg="#4E73DF")
        self.lbl_id.pack(pady=(40, 0))

        self.lbl_name = tk.Label(left_side, text="เตรียมพร้อมดึงรายชื่อ", font=("Tahoma", 24), bg="white", fg="#5A5C69")
        self.lbl_name.pack(pady=20)

        self.btn_draw = tk.Button(left_side, text="ดึงรายชื่อ", command=self.run_main_draw, 
                                 bg="#1CC88A", fg="white", font=("Tahoma", 18, "bold"), pady=15, relief="flat")
        self.btn_draw.pack(fill="x", pady=20)

        self.lbl_count = tk.Label(left_side, text=f"คงเหลือในระบบ: {len(self.available_tickets)} ใบ", bg="white", font=("Tahoma", 11))
        self.lbl_count.pack()

        # ฝั่งขวา: ตารางรายชื่อและปุ่มลบ
        right_side = tk.Frame(body, bg="#F8F9FA", width=420)
        right_side.pack(side="right", fill="both", padx=10)
        right_side.pack_propagate(False)

        tk.Label(right_side, text="📋 รายชื่อผู้ได้รับรางวัล", font=("Tahoma", 11, "bold"), bg="#4E73DF", fg="white", pady=8).pack(fill="x")
        self.tree_normal = ttk.Treeview(right_side, columns=("id", "name"), show="headings", height=10)
        self.tree_normal.heading("id", text="ID")
        self.tree_normal.heading("name", text="ชื่อ-นามสกุล")
        self.tree_normal.column("id", width=60, anchor="center")
        self.tree_normal.pack(fill="x")
        
        tk.Button(right_side, text="🗑️ ลบรายชื่อที่เลือกและคืนสิทธิ์", command=self.delete_normal_winner, 
                  bg="#E74A3B", fg="white", font=("Tahoma", 9), relief="flat", pady=5).pack(fill="x", pady=(5, 15))

        tk.Label(right_side, text="🏆 รายชื่อรางวัลพิเศษ (Jackpot)", font=("Tahoma", 11, "bold"), bg="#F6C23E", fg="#5A5C69", pady=8).pack(fill="x")
        self.tree_jackpot = ttk.Treeview(right_side, columns=("id", "name"), show="headings", height=6)
        self.tree_jackpot.heading("id", text="ID")
        self.tree_jackpot.heading("name", text="ชื่อ-นามสกุล")
        self.tree_jackpot.column("id", width=60, anchor="center")
        self.tree_jackpot.pack(fill="x")

        tk.Button(right_side, text="🗑️ ลบรายชื่อแจ็คพอตที่เลือก", command=self.delete_jackpot_winner, 
                  bg="#E74A3B", fg="white", font=("Tahoma", 9), relief="flat", pady=5).pack(fill="x", pady=(5, 10))

        self.repopulate_tables()

        footer_btn = tk.Frame(right_side, bg="#F8F9FA")
        footer_btn.pack(fill="x", pady=10)
        tk.Button(footer_btn, text="💾 บันทึกผล", command=self.export_all, bg="#36B9CC", fg="white", relief="flat", width=12).pack(side="left")
        tk.Button(footer_btn, text="⭐ สุ่มแจ็คพอต", command=self.go_to_jackpot_page, bg="#F6C23E", fg="white", relief="flat", width=20, font=("Tahoma", 9, "bold")).pack(side="right")

    # --- ฟังก์ชันช่วยเหลือ ---
    def delete_normal_winner(self):
        selected = self.tree_normal.selection()
        if not selected: return
        if messagebox.askyesno("ยืนยัน", "ลบรายชื่อนี้และคืนสิทธิ์สุ่มใหม่?"):
            for item in selected:
                val = self.tree_normal.item(item, "values")
                wid = int(val[0])
                self.normal_winners = [w for w in self.normal_winners if w[0] != wid]
                if wid not in self.available_tickets:
                    self.available_tickets.append(wid)
                    self.available_tickets.sort()
                self.tree_normal.delete(item)
                self.lbl_count.config(text=f"คงเหลือในระบบ: {len(self.available_tickets)} ใบ")

    def delete_jackpot_winner(self):
        selected = self.tree_jackpot.selection()
        if not selected: return
        if messagebox.askyesno("ยืนยัน", "ต้องการลบรายชื่อแจ็คพอตนี้?"):
            for item in selected:
                val = self.tree_jackpot.item(item, "values")
                wid = int(val[0])
                self.jackpot_winners = [w for w in self.jackpot_winners if w[0] != wid]
                self.tree_jackpot.delete(item)

    def repopulate_tables(self):
        for item in reversed(self.normal_winners):
            self.tree_normal.insert("", "end", values=(f"{item[0]:03d}", item[1]))
        for item in reversed(self.jackpot_winners):
            self.tree_jackpot.insert("", "end", values=(f"{item[0]:03d}", item[1]))

    def run_main_draw(self):
        if not self.available_tickets:
            messagebox.showinfo("เสร็จสิ้น", "ดึงรายชื่อครบทุกคนแล้ว")
            return
        self.btn_draw.config(state="disabled")
        self.animate_roll(15)

    def animate_roll(self, count):
        if count > 0:
            rid = random.randint(1, 500)
            self.lbl_id.config(text=f"{rid:03d}")
            self.lbl_name.config(text=EMPLOYEES[rid])
            self.root.after(60, lambda: self.animate_roll(count - 1))
        else:
            self.finalize_main_draw()

    def finalize_main_draw(self):
        winner_id = random.choice(self.available_tickets) if self.algo_choice.get() == 1 else min(self.available_tickets)
        self.available_tickets.remove(winner_id)
        winner_name = EMPLOYEES[winner_id]
        self.normal_winners.append((winner_id, winner_name))
        self.tree_normal.insert("", 0, values=(f"{winner_id:03d}", winner_name))
        self.lbl_id.config(text=f"{winner_id:03d}", fg="#1CC88A")
        self.lbl_name.config(text=winner_name)
        self.lbl_count.config(text=f"คงเหลือในระบบ: {len(self.available_tickets)} ใบ")
        self.btn_draw.config(state="normal")

    def go_to_jackpot_page(self):
        if not self.normal_winners: return
        self.show_jackpot_ui()

    def show_jackpot_ui(self):
        self.clear_frame()
        header = tk.Frame(self.main_container, bg="#F6C23E", pady=15)
        header.pack(fill="x")
        tk.Button(header, text=" กลับ ", command=self.show_draw_page, bg="#D4AC0D", fg="white", relief="flat").pack(side="left", padx=20)
        tk.Label(header, text="กิจกรรมพิเศษ: รอบแจ็คพอต", font=("Tahoma", 16, "bold"), bg="#F6C23E", fg="white").pack(side="left", padx=20)
        content = tk.Frame(self.main_container, bg="#F8F9FA")
        content.pack(expand=True, fill="both")
        card = tk.Frame(content, bg="white", padx=50, pady=50, highlightthickness=2, highlightbackground="#F6C23E")
        card.place(relx=0.5, rely=0.4, anchor="center")
        self.jk_id = tk.Label(card, text="---", font=("Arial", 120, "bold"), bg="white", fg="#E74A3B")
        self.jk_id.pack()
        self.jk_name = tk.Label(card, text="สุ่มรางวัลใหญ่จากผู้มีรายชื่อ", font=("Tahoma", 24), bg="white", fg="#5A5C69")
        self.jk_name.pack(pady=20)
        self.btn_jk = tk.Button(card, text="🏆 เริ่มสุ่มแจ็คพอต", command=self.run_jackpot_draw, bg="#F6C23E", fg="white", font=("Tahoma", 18, "bold"), pady=15, padx=40, relief="flat")
        self.btn_jk.pack()

    def run_jackpot_draw(self):
        if not self.normal_winners: return
        self.btn_jk.config(state="disabled")
        self.animate_jk(20)

    def animate_jk(self, count):
        if count > 0:
            temp = random.choice(self.normal_winners)
            self.jk_id.config(text=f"{temp[0]:03d}")
            self.jk_name.config(text=temp[1])
            self.root.after(80, lambda: self.animate_jk(count - 1))
        else:
            winner = random.choice(self.normal_winners)
            self.normal_winners.remove(winner)
            self.jackpot_winners.append(winner) 
            self.jk_id.config(text=f"{winner[0]:03d}", fg="#1CC88A")
            self.jk_name.config(text=f"🎊 {winner[1]} 🎊")
            self.btn_jk.config(state="normal")

    def export_all(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"สรุปผล: {self.current_event}\nจัดทำโดย: 684245018 นายอดิศร ทองแดง\n\n[รางวัลพิเศษ]\n")
                for wid, wname in self.jackpot_winners: f.write(f"{wid:03d} - {wname}\n")
                f.write("\n[รายชื่อทั่วไป]\n")
                for wid, wname in self.normal_winners: f.write(f"{wid:03d} - {wname}\n")
            messagebox.showinfo("สำเร็จ", "บันทึกผลเรียบร้อย")

    def clear_frame(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinalLuckyDraw(root)
    root.mainloop()
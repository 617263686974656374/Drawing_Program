import tkinter
from tkinter import ttk

class KresliaciProgram:
    def __init__(self, koren):
        self.koren = koren
        self.koren.title("Kresliaci Program")

        # Plátno (Canvas)
        self.platno = tkinter.Canvas(koren, width=800, height=600, bg="white")
        self.platno.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        # Ovládací panel
        self.ovladaci_panel = tkinter.Frame(koren)
        self.ovladaci_panel.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # Popis pre súradnice myši
        self.suradnice_label = tkinter.Label(self.ovladaci_panel, text="Súradnice: X= , Y= ", font=("Arial", 12))
        self.suradnice_label.pack(pady=10)

        # Výber režimu kreslenia
        self.rezim = tkinter.StringVar(value="ciara")
        ttk.Label(self.ovladaci_panel, text="Vyber typ kreslenia:", font=("Arial", 12)).pack(pady=5)
        self.ciara_button = ttk.Radiobutton(self.ovladaci_panel, text="Čiara", variable=self.rezim, value="ciara")
        self.ciara_button.pack(anchor=tkinter.W)
        self.obdlznik_button = ttk.Radiobutton(self.ovladaci_panel, text="Obdĺžnik", variable=self.rezim,
                                               value="obdlznik")
        self.obdlznik_button.pack(anchor=tkinter.W)

        # Tlačidlo na manuálne zadávanie súradníc
        ttk.Button(self.ovladaci_panel, text="Zadať súradnice", command=self.manualne_suradnice).pack(pady=10)

        # Tlačidlo na vymazanie
        ttk.Button(self.ovladaci_panel, text="Vymazať všetko", command=self.vymazat_platno).pack(pady=20)

        # Tlačidlo na zobrazenie/vypnutie mriežky
        ttk.Button(self.ovladaci_panel, text="Zobraziť/Vypnúť mriežku", command=self.vykresli_mriezku).pack(pady=10)

        # Stav kreslenia
        self.zaciatok_x = None
        self.zaciatok_y = None
        self.aktualny_objekt = None
        self.aktualny_text = None

        # Udalosti
        self.platno.bind("<Motion>", self.zobraz_suradnice)
        self.platno.bind("<Button-1>", self.zaciatok_kreslenia)
        self.platno.bind("<B1-Motion>", self.kresli_dynamicne)
        self.platno.bind("<ButtonRelease-1>", self.ukonci_kreslenie)

    def zobraz_suradnice(self, udalost):
        """Zobrazí aktuálne súradnice myši."""
        x, y = udalost.x, udalost.y
        self.suradnice_label.config(text=f"Súradnice: X={x}, Y={y}")

    def zaciatok_kreslenia(self, udalost):
        """Začne kreslenie podľa vybraného režimu."""
        self.zaciatok_x, self.zaciatok_y = udalost.x, udalost.y

    def kresli_dynamicne(self, udalost):
        """Dynamicky vykresľuje objekt počas ťahania myšou."""
        if self.zaciatok_x is None or self.zaciatok_y is None:
            return

        koniec_x, koniec_y = udalost.x, udalost.y

        # Vymaže predchádzajúci dynamický objekt a text
        if self.aktualny_objekt:
            self.platno.delete(self.aktualny_objekt)
        if self.aktualny_text:
            self.platno.delete(self.aktualny_text)

        if self.rezim.get() == "ciara":
            # Dynamické kreslenie čiary
            self.aktualny_objekt = self.platno.create_line(
                self.zaciatok_x, self.zaciatok_y, koniec_x, koniec_y, fill="black", width=2
            )
            body = [(self.zaciatok_x, self.zaciatok_y), (koniec_x, koniec_y)]
        elif self.rezim.get() == "obdlznik":
            # Dynamické kreslenie obdĺžnika
            self.aktualny_objekt = self.platno.create_rectangle(
                self.zaciatok_x, self.zaciatok_y, koniec_x, koniec_y, fill="lightblue", outline="black", width=2
            )
            body = [(self.zaciatok_x, self.zaciatok_y), (koniec_x, koniec_y)]
        else:
            body = []

        # Dynamicky zobraz aktuálne súradnice
        if body:
            self.zobraz_suradnice_objektu(body, dynamicky=True)

    def ukonci_kreslenie(self, udalost):
        """Dokončí kreslenie objektu a zobrazí jeho súradnice."""
        if self.zaciatok_x is None or self.zaciatok_y is None:
            return

        koniec_x, koniec_y = udalost.x, udalost.y

        # Odstránenie dynamického textu (ak existuje)
        if self.aktualny_text:
            self.platno.delete(self.aktualny_text)
            self.aktualny_text = None

        if self.rezim.get() == "ciara":
            # Dokončenie kreslenia čiary
            self.platno.create_line(self.zaciatok_x, self.zaciatok_y, koniec_x, koniec_y, fill="black", width=2)
            # Zvýraznenie bodov
            self.platno.create_oval(self.zaciatok_x - 3, self.zaciatok_y - 3, self.zaciatok_x + 3, self.zaciatok_y + 3,
                                    fill="green")
            self.platno.create_oval(koniec_x - 3, koniec_y - 3, koniec_x + 3, koniec_y + 3, fill="red")
            body = [(self.zaciatok_x, self.zaciatok_y), (koniec_x, koniec_y)]
        elif self.rezim.get() == "obdlznik":
            # Dokončenie kreslenia obdĺžnika
            self.platno.create_rectangle(self.zaciatok_x, self.zaciatok_y, koniec_x, koniec_y, fill="lightblue",
                                         outline="black", width=2)
            # Zvýraznenie bodov
            self.platno.create_oval(self.zaciatok_x - 3, self.zaciatok_y - 3, self.zaciatok_x + 3, self.zaciatok_y + 3,
                                    fill="green")
            self.platno.create_oval(koniec_x - 3, koniec_y - 3, koniec_x + 3, koniec_y + 3, fill="red")
            body = [(self.zaciatok_x, self.zaciatok_y), (koniec_x, koniec_y)]

        # Zobraz finálne farebné súradnice
        self.zobraz_farebne_suradnice(body)
        self.aktualny_objekt = None
        self.zaciatok_x, self.zaciatok_y = None, None

    def vykresli_mriezku(self):
        """Zobrazí alebo odstráni mriežku na plátne."""
        if hasattr(self, "mriezka_zobrazená") and self.mriezka_zobrazená:
            # Vymaže existujúcu mriežku
            self.platno.delete("mriezka")
            self.mriezka_zobrazená = False
        else:
            # Vykreslí mriežku
            velkost_mriezky = 50  # Veľkosť štvorcov v mriežke
            sirka = int(self.platno.cget("width"))
            vyska = int(self.platno.cget("height"))

            # Vodorovné čiary
            for i in range(0, vyska, velkost_mriezky):
                self.platno.create_line(0, i, sirka, i, fill="gray", tags="mriezka", dash=(2, 2))
                self.platno.create_text(5, i + 5, text=f"{i}", font=("Arial", 8), fill="gray", tags="mriezka",
                                        anchor="nw")

            # Zvislé čiary
            for i in range(0, sirka, velkost_mriezky):
                self.platno.create_line(i, 0, i, vyska, fill="gray", tags="mriezka", dash=(2, 2))
                self.platno.create_text(i + 5, 5, text=f"{i}", font=("Arial", 8), fill="gray", tags="mriezka",
                                        anchor="nw")

            self.mriezka_zobrazená = True

    def zobraz_farebne_suradnice(self, body):
        """Zobrazí farebné súradnice počiatočného a koncového bodu."""
        x1, y1 = body[0]
        x2, y2 = body[1]

        # Počiatočný bod (zelený text)
        self.platno.create_text(x1, y1 - 15, text=f"({x1}, {y1})", font=("Arial", 10), fill="green")

        # Koncový bod (červený text)
        self.platno.create_text(x2, y2 - 15, text=f"({x2}, {y2})", font=("Arial", 10), fill="red")

    def zobraz_suradnice_objektu(self, body, dynamicky=False):
        """Zobrazí súradnice objektu na plátne."""
        if len(body) == 2:  # Ak ide o čiaru
            x1, y1 = body[0]
            x2, y2 = body[1]
            priemer_x = (x1 + x2) // 2
            priemer_y = min(y1, y2) - 10  # Text umiestni 10 pixelov nad čiaru
        else:  # Ak ide o obdĺžnik
            priemer_x = sum(x for x, y in body) // len(body)
            priemer_y = sum(y for x, y in body) // len(body)

        text_suradnic = ", ".join(f"({x}, {y})" for x, y in body)

        # Ak je text dynamický, odstráni sa pri ďalšom pohybe
        if dynamicky:
            self.aktualny_text = self.platno.create_text(priemer_x, priemer_y, text=text_suradnic, font=("Arial", 10),
                                                         fill="red")
        else:
            self.platno.create_text(priemer_x, priemer_y, text=text_suradnic, font=("Arial", 10), fill="blue")

    def manualne_suradnice(self):
        """Umožňuje užívateľovi manuálne zadať súradnice cez vstupné polia."""

        def potvrdit_suradnice():
            """Potvrdí zadanie súradníc a vykreslí objekt."""
            try:
                x1 = int(vstup_x1.get())
                y1 = int(vstup_y1.get())
                x2 = int(vstup_x2.get())
                y2 = int(vstup_y2.get())

                if self.rezim.get() == "ciara":
                    # Vykresli čiaru
                    self.platno.create_line(x1, y1, x2, y2, fill="black", width=2)
                    self.zobraz_farebne_suradnice([(x1, y1), (x2, y2)])
                elif self.rezim.get() == "obdlznik":
                    # Vykresli obdĺžnik
                    self.platno.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black", width=2)
                    self.zobraz_farebne_suradnice([(x1, y1), (x2, y2)])

                okno.destroy()
            except ValueError:
                chybova_label.config(text="Chyba: Zadajte platné číselné hodnoty!")

        # Vytvor nové okno
        okno = tkinter.Toplevel(self.koren)
        okno.title("Zadajte súradnice")

        # Popisy pre vstupné polia
        tkinter.Label(okno, text="X1:").grid(row=0, column=0, padx=5, pady=5)
        tkinter.Label(okno, text="Y1:").grid(row=1, column=0, padx=5, pady=5)
        tkinter.Label(okno, text="X2:").grid(row=2, column=0, padx=5, pady=5)
        tkinter.Label(okno, text="Y2:").grid(row=3, column=0, padx=5, pady=5)

        # Vstupné polia
        vstup_x1 = tkinter.Entry(okno)
        vstup_y1 = tkinter.Entry(okno)
        vstup_x2 = tkinter.Entry(okno)
        vstup_y2 = tkinter.Entry(okno)

        vstup_x1.grid(row=0, column=1, padx=5, pady=5)
        vstup_y1.grid(row=1, column=1, padx=5, pady=5)
        vstup_x2.grid(row=2, column=1, padx=5, pady=5)
        vstup_y2.grid(row=3, column=1, padx=5, pady=5)

        # Chybové hlásenie
        chybova_label = tkinter.Label(okno, text="", fg="red")
        chybova_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Tlačidlo na potvrdenie
        potvrdit_button = tkinter.Button(okno, text="Potvrdiť", command=potvrdit_suradnice)
        potvrdit_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Nastavenie veľkosti okna
        okno.geometry("200x200")
        okno.resizable(False, False)

    def vymazat_platno(self):
        """Vymaže všetky objekty z plátna."""
        self.platno.delete("all")
        self.aktualny_objekt = None
        self.aktualny_text = None


# Spustenie aplikácie
if __name__ == "__main__":
    koren = tkinter.Tk()
    program = KresliaciProgram(koren)
    koren.mainloop()

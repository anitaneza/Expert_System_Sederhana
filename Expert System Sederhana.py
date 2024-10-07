import os
import time

# Fungsi untuk membersihkan layar
def clear_screen():
    if os.name == 'nt':  # Untuk Windows
        os.system('cls')
    else:  # Untuk Mac/Linux
        os.system('clear')

# Class Rule tetap
class Rule:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def get_antecedent(self):
        return self.antecedent
    
    def get_consequent(self):
        return self.consequent

# Class UI yang menampilkan pertanyaan berdasarkan kelompok gejala
class UI:
    def __init__(self):
        # Kelompok penyakit dan gejalanya
        self.disease_symptoms = {
            'Bulai': [
                'Daun jagung berubah menjadi warna klorotik', 'Pertumbuhan tanaman mengalami hambatan',
                'Terdapat warna putih seperti tepung pada permukaan daun', 'Daun menggulung dan terpuntir',
                'Pembentukan tongkol terganggu'
            ],
            'Blight': [
                'Daun terlihat layu', 'Terdapat bercak kecil yang bersatu membentuk bercak yang lebih besar',
                'Bercak berwarna coklat muda dan berbentuk memanjang menyerupai kumparan atau perahu', 'Terdapat bercak berwarna coklat berbentuk elips',
                'Daun terlihat kering'
            ],
            'Leaf Rust': [
                'Daun jagung terlihat kering', 'Terdapat bercak-bercak kecil berwarna coklat atau kuning pada permukaan daun',
                'Terdapat bercak merah pada tulang daun', 'Muncul benang tidak beraturan yang awalnya berwarna putih, lalu berubah menjadi coklat', 
                'Daun mengeluarkan serbuk yang menyerupai tepung berwarna kuning kecoklatan'
            ],
            'Burn': [
                'Terdapat pembengkakan pada tongkol jagung', 'Muncul jamur berwarna putih hingga hitam pada biji jagung',
                'Biji jagung terlihat menggembung', 'Terdapat kelenjar yang terbentuk pada biji', 
                'Kelobot (lapisan luar tongkol) terbuka, dan muncul banyak jamur berwarna putih hingga hitam'
            ],
            'Stem Borer': [
                'Terdapat lubang kecil pada daun', 'Terdapat celah pada batang',
                'Bunga jantan atau pangkal tongkol terlihat rusak', 'Batang dan tassel (bunga jantan) mudah patah', 
                'Terdapat tumpukan tassel yang patah', 'Bunga jantan tidak terbentuk', 'Terdapat serbuk/dirt di sekitar pangkal tongkol', 
                'Daun terlihat agak kuning'
            ],
            'Cob Borer': [
                'Terdapat lubang melintang pada daun saat fase vegetatif', 'Rambut tongkol jagung terlihat terpotong atau mengering',
                'Ujung tongkol terlihat berlubang atau terdapat gerekan', 'Sering ditemukan larva di sekitar tongkol'
            ]
        }
        self.answers = [] 

    def show_symptoms(self):
        
        print("============================================")
        print("Mari Identifikasi Tanaman Jagung Anda !")
        print("============================================")
        input("\n(tekan enter untuk mulai)")
        
        clear_screen()

        idx = 1
        for x, (disease, symptoms) in enumerate(self.disease_symptoms.items(), 1):
            print(f"Pertanyaan ke-{x}")
            print(f"Apakah tanaman Anda memiliki ciri-ciri berikut?")
            for i, symptom in enumerate(symptoms, 1):
                print(f"{i}. {symptom}")
            print("\nCiri-ciri mana yang sesuai dengan tanaman Anda? (masukkan nomor sesuai, misal: 1 3 5, atau 0 jika tidak ada yang cocok)")

            user_input = input("Masukkan pilihan Anda: ").strip()  # Ambil input sebagai string dan hapus spasi
            selected_symptoms = []

            while True:
                try:
                    # Pisahkan input berdasarkan spasi dan konversi ke integer
                    selected_symptoms = list(map(int, user_input.split()))

                    # Validasi bahwa semua input ada dalam rentang yang sesuai
                    if all(num in range(len(symptoms) + 1) for num in selected_symptoms):  
                        break  # Keluar dari loop jika input valid
                    else:
                        print("Input tidak sesuai. Mohon masukkan nomor yang valid.")
                except ValueError:
                    print("Input tidak valid. Mohon masukkan angka.")

                user_input = input("Masukkan pilihan Anda: ").strip()  # Ambil input lagi
                    
            if user_input != '0':    
                selected_symptoms = list(map(int, user_input.split()))
                for selected in selected_symptoms:
                    if 1 <= selected <= len(symptoms):
                        self.answers.append(f"G{idx + (selected - 1)}")

            idx += len(symptoms)
            # time.sleep(3)
            clear_screen()

    def get_facts(self):
        return set(self.answers)
    
    def show_conclusion(self, facts, inferred_facts):
        penyakit = []
        print(f"Fakta yang didapat: {facts}\n")
        print(f'Fakta yang disimpulkan: {inferred_facts}\n')

        if 'P001' in inferred_facts:
            penyakit.append('Bulai')
        if 'P002' in inferred_facts:
            penyakit.append('Blight')
        if 'P003' in inferred_facts:
            penyakit.append('Leaf Rust')
        if 'P004' in inferred_facts:
            penyakit.append('Burn')
        if 'P005' in inferred_facts:
            penyakit.append('Stem borer')
        if 'P006' in inferred_facts:
            penyakit.append('Cob borer')

        if penyakit:
            print(f'Tanaman anda menderita: {", ".join(penyakit)}')
        else:
            print('Tanaman anda tidak teridentifikasi penyakit apapun')

# Class ForwardChaining tetap
class ForwardChaining:
    @staticmethod
    def do_forward_chaining(rules, facts):
        inferred_facts = set()
        while True:
            inferred = False
            for rule in rules:
                if set(rule.get_antecedent()).issubset(facts) and rule.get_consequent() not in inferred_facts:
                    facts.add(rule.get_consequent())
                    inferred_facts.add(rule.get_consequent())
                    inferred = True
                    break
            if not inferred:
                break
        return inferred_facts

# Fungsi untuk membaca basis pengetahuan
def get_knowledge():
    file_path = "knowledge_base.txt"
    rules = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split("-")
                antecedent = parts[0].split(",")
                consequent = parts[1]
                rules.append(Rule(antecedent, consequent))
    return rules

# Eksekusi program
tampilan = UI()
tampilan.show_symptoms()

facts = tampilan.get_facts()
fakta = tuple(facts)
rules = get_knowledge()
inferred_facts = ForwardChaining.do_forward_chaining(rules, facts)

tampilan.show_conclusion(fakta, inferred_facts)

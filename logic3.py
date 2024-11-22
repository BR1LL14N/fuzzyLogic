# Fuzzy Curve
def kurva_linear_naik(a, b, x):
    if x <= a:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return 1

def kurva_linear_turun(a, b, x):
    if x <= a:
        return 1
    elif a < x <= b:
        return (b - x) / (b - a)
    else:
        return 0

def segitiga(a, b, c, x):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

# Fuzzy Banyak Beras
def FBB(x):
    return {
        "sedikit": kurva_linear_turun(100, 500, x),  # Mengubah range ke 100-500 gram
        "sedang": segitiga(200, 600, 1000, x),  # Mengubah range ke 200-1000 gram
        "banyak": kurva_linear_naik(500, 1000, x),  # Mengubah range ke 500-1000 gram
    }

# Fuzzy Komposisi Air
def FKA(x):
    return {
        "kurang": kurva_linear_turun(10, 200, x),  # Mengubah range ke 10-200 mL
        "pas": segitiga(100, 300, 800, x),  # Mengubah range ke 100-800 mL
        "berlebih": kurva_linear_naik(300, 1000, x),  # Mengubah range ke 300-1000 mL
    }

# Fuzzy Lama Masak
def FLM(x):
    return {
        "sebentar": kurva_linear_turun(5, 10, x),  # Mengubah range ke 5-10 menit
        "cukup": segitiga(8, 15, 25, x),  # Mengubah range ke 8-25 menit
        "lama": kurva_linear_naik(20, 30, x),  # Mengubah range ke 20-30 menit
    }

# Fungsi Z
def naik(a, b, alpha):
    return b - (alpha * (b - a))

def turun(a, b, alpha):
    return (alpha * (b - a)) + a

def defuzzify(alpha, z):
    alpha_values = [a["alpha"] for a in alpha]
    pembilang = sum(alpha_values[i] * z[i] for i in range(len(alpha)))
    penyebut = sum(alpha_values)
    if penyebut == 0:  # Cegah pembagian nol
        return sum(z) / len(z)  # Nilai default (rata-rata domain output)
    return pembilang / penyebut

# Mesin Inferensi
def inferensi(BB_val, KA_val, LM_val):
    BB = FBB(BB_val)
    KA = FKA(KA_val)
    LM = FLM(LM_val)

    # Rules untuk Porsi
    alphaPorsi = [
        {"alpha": min(BB["sedikit"], KA["kurang"]), "out": "sedikit"},
        {"alpha": min(BB["sedikit"], KA["pas"]), "out": "sedikit"},
        {"alpha": min(BB["sedikit"], KA["berlebih"]), "out": "sedang"},
        {"alpha": min(BB["sedang"], KA["kurang"]), "out": "sedang"},
        {"alpha": min(BB["sedang"], KA["pas"]), "out": "sedang"},
        {"alpha": min(BB["sedang"], KA["berlebih"]), "out": "banyak"},
        {"alpha": min(BB["banyak"], KA["kurang"]), "out": "banyak"},
        {"alpha": min(BB["banyak"], KA["pas"]), "out": "banyak"},
        {"alpha": min(BB["banyak"], KA["berlebih"]), "out": "banyak"},
    ]

    # Rules untuk Tingkat Kematangan
    alphaKematangan = [
        {"alpha": min(LM["sebentar"], KA["kurang"]), "out": "kurang matang"},
        {"alpha": min(LM["cukup"], KA["pas"]), "out": "matang"},
        {"alpha": min(LM["lama"], KA["berlebih"]), "out": "terlalu matang"},
    ]

    # Fuzzy Output
    zPorsi = [turun(1, 5, rule["alpha"]) if rule["out"] == "sedikit" else 
                naik(5, 10, rule["alpha"]) if rule["out"] == "banyak" else 7 for rule in alphaPorsi]
    zKematangan = [turun(0, 50, rule["alpha"]) if rule["out"] == "kurang matang" else 
                    naik(50, 100, rule["alpha"]) if rule["out"] == "terlalu matang" else 75 for rule in alphaKematangan]

    # Defuzzification
    Porsi = defuzzify(alphaPorsi, zPorsi)
    Kematangan = defuzzify(alphaKematangan, zKematangan)

    return Porsi, Kematangan

# Input Data
BB_val = float(input("Masukkan banyak beras (gram, 100-1000): "))
KA_val = float(input("Masukkan komposisi air (mL, 1-1000): "))
LM_val = float(input("Masukkan lama masak (menit, 1-30): "))

# Output Hasil
Porsi, Kematangan = inferensi(BB_val, KA_val, LM_val)
print(f"Porsi Nasi: {Porsi:.2f}")
print(f"Tingkat Kematangan Nasi: {Kematangan:.2f}%")

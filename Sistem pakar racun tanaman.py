"""
SISTEM PAKAR DETEKSI RACUN TANAMAN
===================================
Menggunakan metode Forward Chaining dengan logika IF-THEN
Berdasarkan gejala klinis untuk mendeteksi jenis racun tanaman
"""

# ============================================================
# BASIS PENGETAHUAN (KNOWLEDGE BASE)
# ============================================================

GEJALA = {
    # Gejala Gastrointestinal
    "G01": "Mual dan muntah-muntah (lebih dari 2 kali)",
    "G02": "Diare / mencret",
    "G03": "Sakit / kram perut",
    "G04": "Air liur berlebihan (hipersalivasi)",
    "G05": "Mual tanpa muntah",

    # Gejala Neurologis
    "G06": "Pusing / kepala berputar",
    "G07": "Kejang-kejang",
    "G08": "Bingung / disorientasi",
    "G09": "Pingsan / kehilangan kesadaran",
    "G10": "Kelumpuhan / sulit menggerakkan anggota badan",
    "G11": "Tremor / gemetar",
    "G12": "Penglihatan kabur atau ganda",

    # Gejala Kardiovaskular
    "G13": "Tekanan darah rendah (hipotensi)",
    "G14": "Detak jantung tidak normal (terlalu cepat/lambat)",
    "G15": "Kulit pucat atau kebiruan (sianosis)",

    # Gejala Pernapasan
    "G16": "Sesak napas / sulit bernapas",
    "G17": "Napas berbunyi / mengi",

    # Gejala Kulit & Lokal
    "G18": "Ruam atau kemerahan pada kulit",
    "G19": "Rasa terbakar di mulut, tenggorokan, atau kulit",
    "G20": "Gatal-gatal",
    "G21": "Bengkak pada bibir, lidah, atau tenggorokan",

    # Gejala Lain
    "G22": "Demam / suhu tubuh tinggi",
    "G23": "Keringat dingin",
    "G24": "Penglihatan berwarna kuning (ikterus / mata kuning)",
    "G25": "Pupil mata melebar (midriasis)",
    "G26": "Pupil mata mengecil (miosis)",
}

PENYAKIT = {
    "P01": "Keracunan Alkaloid (mis. Atropa belladonna / Kecubung)",
    "P02": "Keracunan Glikosida Jantung (mis. Digitalis / Oleander)",
    "P03": "Keracunan Oksalat (mis. Dieffenbachia / Keladi Hias)",
    "P04": "Keracunan Solanin (mis. Kentang Hijau / Tomat Mentah)",
    "P05": "Keracunan Sianida Tanaman (mis. Singkong Liar / Biji Apel)",
    "P06": "Keracunan Pirolizidine Alkaloid (mis. Daun Comfrey)",
    "P07": "Keracunan Tanin & Fitotoksin (mis. Buah Beri Liar)",
    "P08": "Keracunan Resin & Terpenoid (mis. Euphorbia / Getah Karet)",
}

# ============================================================
# ATURAN (RULES) - Logika IF-THEN
# Format: {penyakit_id: [gejala_wajib, gejala_tambahan, bobot_per_gejala]}
# ============================================================

RULES = {
    "P01": {
        "nama": "Keracunan Alkaloid (Atropa belladonna / Kecubung)",
        "gejala_utama": ["G25", "G08", "G12"],   # pupil melebar, bingung, penglihatan kabur
        "gejala_pendukung": ["G07", "G09", "G06", "G14"],
        "bobot_utama": 20,
        "bobot_pendukung": 10,
        "saran": "Segera bawa ke UGD. Hindari memberi apapun lewat mulut. Dokter mungkin akan memberikan antidot physostigmine.",
        "tanaman": ["Kecubung (Datura stramonium)", "Belladonna (Atropa belladonna)", "Henbane (Hyoscyamus niger)"],
    },
    "P02": {
        "nama": "Keracunan Glikosida Jantung (Digitalis / Oleander)",
        "gejala_utama": ["G14", "G01", "G03"],   # detak jantung abnormal, mual muntah, sakit perut
        "gejala_pendukung": ["G06", "G12", "G09", "G13"],
        "bobot_utama": 20,
        "bobot_pendukung": 10,
        "saran": "Darurat medis! Segera ke RS. Jangan telat — glikosida jantung dapat menyebabkan henti jantung.",
        "tanaman": ["Oleander (Nerium oleander)", "Digitalis (Foxglove)", "Lily of the Valley", "Bungur"],
    },
    "P03": {
        "nama": "Keracunan Oksalat (Dieffenbachia / Keladi Hias)",
        "gejala_utama": ["G19", "G21", "G04"],   # terbakar di mulut, bengkak, hipersalivasi
        "gejala_pendukung": ["G01", "G16", "G17"],
        "bobot_utama": 20,
        "bobot_pendukung": 10,
        "saran": "Bilas mulut dengan air bersih. Minum air atau susu untuk mengencerkan. Jangan paksa muntah. Segera ke dokter jika ada pembengkakan di tenggorokan.",
        "tanaman": ["Dieffenbachia (Dumb Cane)", "Keladi hias (Caladium)", "Philodendron", "Colocasia"],
    },
    "P04": {
        "nama": "Keracunan Solanin (Kentang Hijau / Tomat Mentah)",
        "gejala_utama": ["G01", "G02", "G03"],   # mual muntah, diare, sakit perut
        "gejala_pendukung": ["G06", "G08", "G07", "G22"],
        "bobot_utama": 20,
        "bobot_pendukung": 10,
        "saran": "Istirahat dan minum banyak air. Hindari dehidrasi. Kunjungi dokter jika gejala memburuk atau berlangsung lebih dari 24 jam.",
        "tanaman": ["Kentang hijau / bertunas", "Tomat mentah (dalam jumlah besar)", "Terong mentah", "Leunca"],
    },
    "P05": {
        "nama": "Keracunan Sianida Tanaman (Singkong Liar / Biji Apel)",
        "gejala_utama": ["G16", "G09", "G07"],   # sesak napas, pingsan, kejang
        "gejala_pendukung": ["G06", "G15", "G13", "G23"],
        "bobot_utama": 20,
        "bobot_pendukung": 10,
        "saran": "DARURAT! Hubungi 119 segera. Sianida sangat mematikan. Bawa ke UGD untuk antidot hydroxocobalamin atau natrium tiosulfat.",
        "tanaman": ["Singkong liar (Manihot esculenta var. liar)", "Biji apel/pir", "Biji ceri/peach", "Bambu muda mentah"],
    },
    "P06": {
        "nama": "Keracunan Pirolizidine Alkaloid (Daun Comfrey)",
        "gejala_utama": ["G24", "G01", "G03"],   # mata kuning, mual muntah, sakit perut
        "gejala_pendukung": ["G22", "G13", "G09"],
        "bobot_utama": 20,
        "bobot_pendukung": 10,
        "saran": "Segera ke dokter. Keracunan ini menyerang hati secara perlahan (kronis). Perlu pemeriksaan fungsi hati (SGOT/SGPT).",
        "tanaman": ["Comfrey (Symphytum officinale)", "Tansy ragwort", "Heliotrope", "Tussilago"],
    },
    "P07": {
        "nama": "Keracunan Tanin & Fitotoksin (Buah Beri Liar)",
        "gejala_utama": ["G01", "G18", "G20"],   # mual muntah, ruam kulit, gatal
        "gejala_pendukung": ["G02", "G03", "G05"],
        "bobot_utama": 20,
        "bobot_pendukung": 10,
        "saran": "Minum air banyak. Berikan antihistamin untuk reaksi kulit. Kunjungi dokter jika reaksi alergi parah.",
        "tanaman": ["Elderberry mentah (Sambucus)", "Biji mistletoe", "Holly berry (Ilex)", "Pokeweed"],
    },
    "P08": {
        "nama": "Keracunan Resin & Terpenoid (Euphorbia / Getah)",
        "gejala_utama": ["G19", "G18", "G21"],   # terbakar, ruam, bengkak
        "gejala_pendukung": ["G20", "G01", "G04", "G16"],
        "bobot_utama": 20,
        "bobot_pendukung": 10,
        "saran": "Bilas area terkena dengan air mengalir minimal 15 menit. Jangan sentuh mata. Konsultasi ke dokter untuk steroid topikal jika perlu.",
        "tanaman": ["Euphorbia (Jarak pagar)", "Getah karet (Ficus elastica)", "Poinsettia", "Manchineel"],
    },
}

# ============================================================
# MESIN INFERENSI (INFERENCE ENGINE)
# ============================================================

def hitung_persentase(penyakit_id, gejala_pasien):
    """Hitung persentase kemiripan gejala dengan aturan penyakit."""
    rule = RULES[penyakit_id]
    skor = 0
    skor_maks = (len(rule["gejala_utama"]) * rule["bobot_utama"] +
                 len(rule["gejala_pendukung"]) * rule["bobot_pendukung"])

    for g in rule["gejala_utama"]:
        if g in gejala_pasien:
            skor += rule["bobot_utama"]

    for g in rule["gejala_pendukung"]:
        if g in gejala_pasien:
            skor += rule["bobot_pendukung"]

    if skor_maks == 0:
        return 0.0
    return round((skor / skor_maks) * 100, 2)


def diagnosa(gejala_pasien):
    """Jalankan inferensi forward chaining dan kembalikan hasil diagnosa."""
    hasil = []
    for pid in RULES:
        persen = hitung_persentase(pid, gejala_pasien)
        if persen > 0:
            hasil.append((pid, persen))

    hasil.sort(key=lambda x: x[1], reverse=True)
    return hasil


# ============================================================
# ANTARMUKA KONSOL
# ============================================================




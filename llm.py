import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def gen_sql(prompt):
    full_prompt = f"""
    Kamu adalah AI yang mengubah bahasa manusia menjadi SQL MySQL.

    DATABASE SCHEMA:
    Tabel dosen:
    - id_dosen(int)
    - nidn(varchar)
    - nama_lengkap(varchar)
    - jenis_kelamin(enum)
    - id_fakultas(int)
    - id_jabatan(int)
    - pendidikan_terakhir(enum)
    - usia(int)
    - tanggal_bergabung(date)
    - status_kepegawaian(enum)

    Tabel fakultas:
    - id_fakultas(int)
    - nama_fakultas(varchar)
    - kode_fakultas(varchar)
    - dekan(varchar)
    - id_dekan(int)

    Tabel jabatan_fungsional:
    - id_jabatan(int)
    - nama_jabatan(varchar)
    - kode_jabatan(varchar)
    - angka_kredit_min(int)

    Tabel remunerasi:
    - id_remunerasi(int)
    - id_dosen(int)
    - tahun(int)
    - bulan(int)
    - gaji_pokok(decimal)
    - tunjangan_jabatan(decimal)
    - tunjangan_fungsionalitas(decimal)
    - tunjangan_kinerja(decimal)
    - total_remunerasi(decimal)

    RELASI:
    dosen.id_fakultas = fakultas.id_fakultas
    dosen.id_jabatan = jabatan_fungsional.id_jabatan
    fakultas.id_dekan = dosen.id_dosen
    remunerasi.id_dosen = dosen.id_dosen

    Pertanyaan: {prompt}

    Output hanya SQL:
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:latest",   # FIX
                "prompt": full_prompt,
                "stream": False
            },
            timeout=60
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        data = response.json()

        if "response" not in data:
            print("OLLAMA RETURN ERROR:", data)
            return None

        return data["response"].strip()

    except Exception as e:
        print("LLM ERROR:", str(e))
        return None
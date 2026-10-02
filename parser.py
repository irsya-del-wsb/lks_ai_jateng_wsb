def parse_nl(pertanyaan):
    pertanyaan = pertanyaan.lower()

    if "jumlah dosen" in pertanyaan:
        return {
            "intent": "count_dosen",
            "group_by": "fakultas"
        }
    if "usia dosen" in pertanyaan:
        return{
            "intent": "average_dosen",
            "group_by": "fakultas"
        }
    if "jabatan dosen" in pertanyaan:
        return{
            "intent": "sum_jabatan",
        }
    if "status kepegawaian" in pertanyaan:
        return{
            "intent": "sta_peg"
        }
    return {"intent": "unknown"}
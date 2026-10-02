def generate_sql(parsed):
    
    
    if parsed["intent"] == "count_dosen":
        return """
        SELECT f.nama_fakultas, COUNT(*) as total
        FROM dosen d
        JOIN fakultas f ON d.id_fakultas = f.id_fakultas
        GROUP BY f.nama_fakultas
        """
    if parsed["intent"] == "average_dosen":
        return """
        SELECT AVG(usia) as rata_usia FROM dosen
        """
    if parsed["intent"] == "sum_jabatan":
        return """
        SELECT DISTINCT j.nama_jabatan
        FROM dosen d
        JOIN jabatan_fungsional j 
        ON d.id_jabatan = j.id_jabatan;
        """
    if parsed["intent"] == "sta_peg":
        return """
        SELECT dosen.status_kepegawaian
        FROM dosen
        GROUP BY status_kepegawaian
        """
    
    return None

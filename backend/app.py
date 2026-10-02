from parser import parse_nl
from mapping import generate_sql
from query import run_query
from llm import gen_sql

def is_safe_sql(sql):
    sql = sql.lower()
    
    forbidden = ["drop", "delete", "truncate", "update", "insert"]
    
    for word in forbidden:
        if word in sql:
            return False
        
    if not sql.strip().startswith("select"):
        return False
    
    return True

def detect_chart(sql, pertanyaan):
    p = pertanyaan.lower()
    sql = sql.lower()
    
    if "grafik" in p or "chart" in p or "diagram" in p:
        return True
    
    if "group by" in sql or "count(" in sql or "sum(" in sql:
        return True

    return False

def detect_chart_type(sql):
    sql = sql.lower()
    
    if "group by" in sql:
        return "bar"
    elif "avg" in sql:
        return "line"
    elif "count" in sql:
        return "bar"
    elif "sum" in sql:
        return "bar"

    return "table"

def generate_title(pertanyaan):
    return "Hasil: " + pertanyaan.capitalize()

cache = {}

def process(pertanyaan):
    parsed = parse_nl(pertanyaan)
    sql = generate_sql(parsed)
    
    if pertanyaan in cache:
        print("CACHE HIT")
        sql = cache[pertanyaan]
    else:
        parsed = parse_nl(pertanyaan)
        sql = generate_sql(parsed)
    
    if parsed["intent"] == ["unknown"] or sql is None:
    
        if "semua dosen" in pertanyaan.lower():
            sql = "SELECT * FROM dosen"
        
        elif "semua fakultas" in pertanyaan.lower():
            sql = "SELECT * FROM fakultas"
        
        else:
            print("Pakai LLM")
            sql = gen_sql(pertanyaan)
            
    if sql is None or sql.strip() == "":
        return {"error":"LLM gagal Generate"}
        
    print("DEBUG SQL FINAL:", sql)
        
    if not is_safe_sql(sql):
        return {"error": "SQL tidak valid / berbahaya"}

    data = run_query(sql)
    print("DEBUG DATA:", data)

    chart = detect_chart(sql, pertanyaan)

    if "group by" in sql.lower():
        chart = True
        
    # VALIDASI DATA UNTUK CHART
    if not data or len(data) == 0:
        chart = False
    elif len(data[0].keys()) > 2:
        chart = False
        
    chartType = None
    chartTitle = None

    if chart:
        chartType = detect_chart_type(sql)
        chartTitle = generate_title(pertanyaan)

    return {
        "sql": sql,
        "chart": chart,
        "chartType": chartType,
        "chartTitle": chartTitle,
        "data": data
    }
    
if __name__ == "__main__":
    while True:
        user_input = input("Tanya: ")
        if user_input.lower() == "exit":
            break

        hasil = process(user_input)
        print("\n=== HASIL ===")
        print("SQL:", hasil["sql"])
        print("DATA:", hasil["data"])
        print("JSON:", hasil)
        print("================\n")

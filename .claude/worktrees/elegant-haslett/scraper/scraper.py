import pandas as pd
import json
import os

files = {
    2016: ("fase1_16.ods", "ods"),
    2017: ("fase1_17.ods", "ods"),
    2018: ("fase1_18.ods", "ods"),
    2019: ("fase1_19.xls", "xls"),
    2020: ("fase1_20.xls", "xls"),
    2021: ("fase1_21.xls", "xls"),
    2022: ("fase1_22.xls", "xls"),
    2023: ("fase1_23.xlsx", "xlsx"),
    2024: ("fase1_24.xlsx", "xlsx"),
    2025: ("fase1_25.xlsx", "xlsx25"),
}

def read_file(path, filetype):
    if filetype == "xlsx":
        return pd.read_excel(path, skiprows=4)
    elif filetype == "xlsx25":
        return pd.read_excel(path, sheet_name="Concurso Nacional")
    elif filetype == "xls":
        df = pd.read_excel(path, engine="xlrd", skiprows=4)
        mask = df.apply(lambda row: row.astype(str).str.contains(r'^\(1\)$').any(), axis=1)
        return df[~mask]
    elif filetype == "ods":
        for skip in [4, 2]:
            df = pd.read_excel(path, engine="odf", skiprows=skip)
            mask = df.apply(lambda row: row.astype(str).str.contains(r'^\(1\)$').any(), axis=1)
            df = df[~mask]
            grade_cols = [c for c in df.columns if "colocado" in str(c).lower()]
            if grade_cols:
                return df
        return df

# Build a dict: key = (universidade, curso), value = {year: grade}
all_courses = {}

for year, (filename, filetype) in files.items():
    print(f"Processing {year}...")
    try:
        df = read_file(filename, filetype)

        if filetype == "xlsx25":
            grade_col = "NOTA ULTIMO COLOCADO REGIME GERAL DE ACESSO 2025/2026"
            uni_col = "IES UO"
            curso_col = "CURSO"
            vagas_col = "REGIME GERAL DE ACESSO  2025/2026"
            grau_col = "TIPO CURSO"
        else:
            grade_col = [c for c in df.columns if "colocado" in str(c).lower() and "não" not in str(c).lower()][-1]

            uni_col = next((c for c in df.columns if "nome da inst" in str(c).lower()),
                      next((c for c in df.columns if "instituição de ensino" in str(c).lower()),
                      next((c for c in df.columns if "instituição" in str(c).lower() and "código" not in str(c).lower()),
                      next((c for c in df.columns if "instit" in str(c).lower() and "código" not in str(c).lower()), None))))

            curso_col = next((c for c in df.columns if "nome do curso" in str(c).lower()),
                        next((c for c in df.columns if "curso" in str(c).lower() and "código" not in str(c).lower()), None))

            vagas_col = [c for c in df.columns if "vaga" in str(c).lower() and "adic" not in str(c).lower()][0]

            grau_col = next((c for c in df.columns if "grau" in str(c).lower()), None)

        for _, row in df.iterrows():
            uni = str(row[uni_col]).strip()
            curso = str(row[curso_col]).strip()
            grade = row[grade_col]
            vagas = row[vagas_col]
            grau = str(row[grau_col]).strip() if grau_col else None

            if pd.isna(grade) or uni == "nan" or curso == "nan":
                continue

            try:
                vagas_val = int(vagas) if not pd.isna(vagas) else None
            except:
                vagas_val = None

            key = (uni, curso)
            if key not in all_courses:
                all_courses[key] = {
                    "universidade": uni,
                    "curso": curso,
                    "vagas": vagas_val,
                    "notas": {},
                    "grau": grau if filetype != "xlsx25" else None,
                }
            else:
                if vagas_val is not None:
                    all_courses[key]["vagas"] = vagas_val
                if filetype != "xlsx25" and grau:
                    all_courses[key]["grau"] = grau
                # Don't update grau from 2025 file — it reclassifies MI as L1
                if filetype != "xlsx25" and grau:
                    all_courses[key]["grau"] = grau
            all_courses[key]["notas"][year] = round(float(grade), 1)

    except Exception as e:
        print(f"  Error: {e}")

# Convert to list
courses = [c for c in all_courses.values() if 2025 in c["notas"] or 2024 in c["notas"]]

# Save
os.makedirs("../src/data", exist_ok=True)
with open("../src/data/courses.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, ensure_ascii=False, indent=2)

print(f"\nDone! {len(courses)} courses saved.")
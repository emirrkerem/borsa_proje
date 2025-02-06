import pandas as pd

# Google Drive'daki dosya yolu (kendi yolunu yaz!)
file_path = r"G:\Drive'ım\Trade.xlsx"
sheet_name = "Hisseler"  # Sayfa adı

# Verileri oku
df = pd.read_excel(file_path, sheet_name=sheet_name)

# JSON formatına çevir ve ekrana yazdır
print(df.to_json(orient="records", indent=4))

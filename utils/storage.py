import os
import csv
from datetime import date

def save_vector(user_vector, base_dir="data"):
    try:
        # Nombre del archivo CSV
        filename = f"{user_vector['source']}_{user_vector['language']}_{date.today().isoformat()}.csv"
        
        # Directorio donde guardar (por idioma/vectors)
        csv_dir = os.path.join(base_dir, user_vector["language"], "vectors")
        os.makedirs(csv_dir, exist_ok=True)
        
        csv_path = os.path.join(csv_dir, filename)

        # Columnas del CSV
        fieldnames = [
            "user_id",
            "source",
            "language",
            "text",
            "account_age_days",
            "popularity_score",
            "engagement_score",
            "reach_score",
            "personality",
            "professional"
        ]

        # Modo de apertura
        file_exists = os.path.isfile(csv_path)
        mode = "a" if file_exists else "w"

        with open(csv_path, mode=mode, newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({field: user_vector.get(field, "") for field in fieldnames})

        return True

    except Exception as e:
        return False

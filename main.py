from utils.vectorization import generate_vector
from api.reddit import fetch_all_posts
from gui.screens.bow_screen import BowScreen

if __name__ == "__main__":
    data = generate_vector(source="reddit", limit=100, language="es")

    # data = fetch_all_posts(limit=1)
    # Mostrar BOW final
    #for user in bow:
    #    print(f"🧍 Usuario: {user}")
    #    print(dict(bow[user]))
    #    print("=" * 60)
    
    #vectorization.show_bow(bow)
    print(data[0])

    #window = show_viewer(data[0])
    # Agregar el porcentaje de cambios al vector de usuario
    # Pasarle al viewer como parametro el vector completo (columnas: text, porcentaje de cambios ?)
    app = BowScreen(data)
    app.mainloop()
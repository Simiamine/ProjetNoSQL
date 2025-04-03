import os
import pytesseract
from PIL import Image
import shutil

DOSSIER_CAPTURES = "captures"
FICHIER_SORTIE = "ocr_resultats.txt"

def generer_nom_disponible(nom_base, extension, dossier):
    i = 1
    while True:
        nom_fichier = f"{i}.{extension}"
        chemin = os.path.join(dossier, nom_fichier)
        if not os.path.exists(chemin):
            return nom_fichier
        i += 1

# Lister les fichiers .png à renommer
fichiers = [f for f in os.listdir(DOSSIER_CAPTURES) if f.lower().endswith(".png") and not f.split('.')[0].isdigit()]
fichiers = sorted(fichiers, key=lambda x: os.path.getctime(os.path.join(DOSSIER_CAPTURES, x)))

print("🔄 Renommage sécurisé des fichiers...")

index_disponible = 1
for fichier in fichiers:
    while os.path.exists(os.path.join(DOSSIER_CAPTURES, f"{index_disponible}.png")):
        index_disponible += 1
    ancien_chemin = os.path.join(DOSSIER_CAPTURES, fichier)
    nouveau_nom = f"{index_disponible}.png"
    nouveau_chemin = os.path.join(DOSSIER_CAPTURES, nouveau_nom)
    shutil.move(ancien_chemin, nouveau_chemin)
    print(f"{fichier} → {nouveau_nom}")
    index_disponible += 1

# Re-trier tous les fichiers numériques (déjà renommés ou non)
fichiers_tries = sorted(
    [f for f in os.listdir(DOSSIER_CAPTURES) if f.lower().endswith(".png") and f.split('.')[0].isdigit()],
    key=lambda x: int(x.split('.')[0])
)

print("\n🧠 Extraction OCR en cours...")

with open(FICHIER_SORTIE, "w", encoding="utf-8") as f:
    for fichier in fichiers_tries:
        chemin_image = os.path.join(DOSSIER_CAPTURES, fichier)
        image = Image.open(chemin_image)
        texte = pytesseract.image_to_string(image, lang="eng+fra")

        f.write(f"\n--- {fichier} ---\n")
        f.write(texte.strip() + "\n")
        f.write("-" * 40 + "\n")
        print(f"✅ {fichier} traité.")

print(f"\n📁 Résultat OCR enregistré dans : {FICHIER_SORTIE}")
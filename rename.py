import os
import string

folder_path = "dataset"   # change if needed

# Get A-Z letters
letters = list(string.ascii_uppercase)

# Get sorted image list
images = sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1].split('.')[0]))

for i, img in enumerate(images):
    old_path = os.path.join(folder_path, img)
    
    # Only rename first 26 safely
    if i < len(letters):
        new_name = f"{letters[i]}.png"
        new_path = os.path.join(folder_path, new_name)
        
        os.rename(old_path, new_path)
        print(f"{img} → {new_name}")

print("✅ Done bro 🔥")
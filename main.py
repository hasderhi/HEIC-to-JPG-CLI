try: 
    from PIL import Image
    import pillow_heif
    from tqdm import tqdm
    import os
except:
    print("Could not resolve imports")
    exit()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def get_all_heic_files(folder):
    heic_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.heic'):
                heic_files.append(os.path.join(root, file))
    return heic_files

def convert_heic_to_jpg(folder, delete_heic=False):
    pillow_heif.register_heif_opener()

    heic_files = get_all_heic_files(folder)
    total_files = len(heic_files)

    if total_files == 0:
        print(bcolors.WARNING + "No .heic files found." + bcolors.ENDC)
        return

    print(bcolors.OKCYAN + f"Found {total_files} .heic file(s).\n" + bcolors.ENDC)

    for index, heic_path in enumerate(tqdm(heic_files, desc="Converting", unit="file")):
        file = os.path.basename(heic_path)
        jpg_path = os.path.splitext(heic_path)[0] + ".jpg"

        try:
            image = Image.open(heic_path)
            image.save(jpg_path, "JPEG")
            tqdm.write(bcolors.OKGREEN + f"Converted: {file} → {os.path.basename(jpg_path)} ({index + 1} / {total_files})" + bcolors.ENDC)

            if delete_heic:
                os.remove(heic_path)
                tqdm.write(bcolors.OKBLUE + f"Deleted original: {file}" + bcolors.ENDC)

        except Exception as e:
            tqdm.write(bcolors.FAIL + f"Failed to convert {file}: {e}" + bcolors.ENDC)

if __name__ == "__main__":
    print(bcolors.HEADER + "HEIC to JPG CLI\nWritten by Tobias Kisling using the pillow_heif library\n" + bcolors.ENDC)
    folder_path = input("Enter the absolute folder path containing .heic files: ").strip()
    delete_input = input("Delete original .heic files after conversion? (Y/N): ").strip().lower()
    delete_heic = delete_input == "y"

    if os.path.isdir(folder_path):
        convert_heic_to_jpg(folder_path, delete_heic)
        print(bcolors.WARNING + "Conversion finished!" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Invalid folder path." + bcolors.ENDC)

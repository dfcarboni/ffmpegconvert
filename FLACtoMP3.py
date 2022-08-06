import os
import glob
import pathlib
import readline
import subprocess

def complete_path(text, state):
    incomplete_path = pathlib.Path(text)
    if incomplete_path.is_dir():
        completions = [p.as_posix() for p in incomplete_path.iterdir()]
    elif incomplete_path.exists():
        completions = [incomplete_path]
    else:
        exists_parts = pathlib.Path('.')
        for part in incomplete_path.parts:
            test_next_part = exists_parts / part
            if test_next_part.exists():
                exists_parts = test_next_part

        completions = []
        for p in exists_parts.iterdir():
            p_str = p.as_posix()
            if p_str.startswith(text):
                completions.append(p_str)
    return completions[state]

def getuserinput(message):
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete_path)
    userinput= input(f'{message}')
    return userinput

def main():
    while True:
        folder= getuserinput('Digite o caminho da pasta: \n')
        os.makedirs(os.path.join(folder, 'MP3'), exist_ok= True)
        folder_path= os.path.join('./', folder, '*.flac')
        
        # print(glob.glob(folder_path))
        item_list= glob.glob(folder_path)
        
        for item in item_list:
            # os.system ("ffmpeg -i input.flac -ab 320k -map_metadata 0 -id3v2_version 3 output.mp3")
            cleanname= os.path.basename(item)[:-4]
            flac_file= item 
            cmd = ['./ffmpeg/bin/ffmpeg', '-y', '-i', f'{flac_file}', '-ab', '320k', '-map_metadata', '0', f"./{folder}/MP3/{cleanname}.mp3"]
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
            
        # os.system('cls' if os.name == 'nt' else 'clear')
        
        quit= input('Continuar (Y/n): ')
        while True:
            if quit == 'Y' or quit == 'y':
                break
            elif quit == 'n':
                exit()
            else:
                quit= input('Continuar (Y/n): ')
        
    # os.system()
    
if __name__ == '__main__':
    main()

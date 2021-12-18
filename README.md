# Write-Metadata-to-Flac-Music-Files

This script takes the metadata from https://itunes.apple.com.  
Following metadata is being added: Title, Artist, Album, Genre, Date, Cover.

### Inputs:
- Path to folder containing flac files
- [Optional] size: Cover size (possible range 300 to 3000)
- [Optional] error: tolerance in seconds for the track == abs(length_of_local_file - track_length_from_itunes)  
***The recommended range for error is 1 to 5. Higher the error more will be the False Positives (reduces accuracy). Lower the error results in False Negatives (reduces the number metadata written files).***

### Requirements:
- Mutagen ```pip install mutagen```
- PySimpleGUI ```pip install PySimpleGUI```
- Pillow ```pip install Pillow```

### How it works:
- You will get GUI as shown below.
- The first row is the file name; the second row shows titles, the third row shows artists, fourth row shows albums for the track.
- Find which column is right for you from the maximum four columns shown.
- Write column number {1,2,3,4} in the box next to 'Your Choice' text.
- Click the 'Submit' button OR press 'Enter' on the keyboard.
- If you find that none of the columns are correct for you, write input as 0 or keep it blank, then click 'Submit'.

![alt text](https://github.com/tkanhe/Write-Metadata-to-Flac-Music-Files/blob/main/Capture.png?raw=true)

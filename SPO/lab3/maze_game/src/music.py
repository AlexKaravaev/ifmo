import glob

class Music:
    def __init__(self):
        self.path ="/home/alexander/dev/ifmo/SPO/lab3/maze_game/src/ost/"
    
    def find_files(self, directory):
        files = [f for f in glob.glob(self.path + directory + "/*.wav")]
        song_names = []
        for name in files:
            begin = len(self.path)
            end = name.find(".wav")
            song_names.append(name[begin:end])
        return song_names
    
    def shuffle_lib(self, directory):
        songs = self.find_files(directory)
        return [song+".wav" for song in songs]

if __name__ == "__main__":
    mus = Music()
    print(mus.find_files('game'))

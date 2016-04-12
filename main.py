import argparse
import audioToolkit as at


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="mp3 file to analyze.")
    parser.add_argument("-b", help="Block size.", default=44100)

    args = parser.parse_args()

    blockSize = args.b

    if args.filename != "":
        wavFile = at.convert_mp3_to_wav(args.filename, 44100)
        X, Y = at.convert_wav_files_to_nptensor(wavFile, blockSize)

    return 0




if __name__ == "__main__":
    main()

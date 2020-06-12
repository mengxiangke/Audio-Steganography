import wave
import pysftp
import sys
from Crypto.Cipher import AES
import random
import string


def encode():
    song = wave.open("song.wav", mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    string = input("Enter your secret message: ")
    string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))

    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)

    with wave.open('song_embedded.wav', 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()
    print("Secret message encoded to audio file thorugh LSB Steganography")


def decode():
    #dirpath = "C:/Users/ayu/PycharmProjects/AudioSteg/"
    file_to_open ="song_embedded.wav"
    song = wave.open(file_to_open, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    decoded = string.split("###")[0]

    print("Decoded message: " + decoded)
    song.close()


def transfer():
    #host = input("Enter SFTP host server IP address: ")
    #username = input("Enter SFTP username: ")
    #password = input("Enter SFTP password: ")
    with pysftp.Connection(host='enter hostname here', username='enter username here', password='enter password here') as sftp:
        print("Connection created, now transferring...")
        with sftp.cd('/'):
            sftp.put('song_embedded.wav')


def encrypt():
    AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
    AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
    input_file = 'song_embedded.wav'
    text_file = open("aes_key.txt", "wt")
    n = text_file.write(AES_KEY)
    text_file.close()
    text_file = open("aes_iv.txt", "wt")
    n = text_file.write(AES_IV)
    text_file.close()
    encrypted_audio_file = '(encrypted)' + input_file
    with open(input_file, 'rb') as fd:
        contents = fd.read()
    encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    encrypted_audio = encryptor.encrypt(contents)
    with open(encrypted_audio_file, 'wb') as fd:
        fd.write(encrypted_audio)
    print('Audio file encrypted')


def decrypt():
    AES_KEY = input("Enter your randomly generated AES Key: ")
    AES_IV = input("Enter your randomly generated IV: ")
    decrypted_audio_file = '(decrypted)' + input_file
    decryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    decrypted_audio = decryptor.decrypt('(encrypted)song_embedded.wav')
    with open(decrypted_audio_file, 'wb') as fd:
        fd.write(decrypted_audio)
    print('Encrypted audio file decrypted')


def main():
    choice = input("""
        A: Encode message in audio (LSB)
        B: Decode Message from audio (LSB)
        C: Transfer embedded audio through SFTP
        D: Decrypt audio file
        E: Encrypt audio file
        Q: Quit
        Please enter your choice: """)
    if choice == "A" or choice == "a":
        encode()
    elif choice == "B" or choice == "b":
        decode()
    elif choice == "C" or choice == "c":
        transfer()
    elif choice == "D" or choice == "d":
        decrypt()
    elif choice == "E" or choice == "e":
        encrypt()
    elif choice == "Q" or choice == "q":
        sys.exit()
    else:
        print("You must only select either A,B,C,D,E or Q.")
        print("Please try again")
        main()


print("Welcome to Audio Steganography Project!")
print("******************************************************")
if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Sat May 23 14:39:56 2020

@author: amaury
"""
import numpy as np
import scipy.io as sio   #matlab
import scipy.io.wavfile
import scipy.signal as ss
import matplotlib.pyplot as plt
#import h5py as h5
import pyaudio
import wave
  
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024#22050
RECORD_SECONDS = 6#30
  
audio = pyaudio.PyAudio() 

                                        # Debut enregistrement
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
 

frames=[]

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #frames.append(data)
    amplitude = np.fromstring(data,np.int16)
    
fig = plt.figure() #créer une nouvelle grille d'affichage
    
plt.plot(amplitude)

plt.title('Amplitude du signal en fonction du temps')#Fréquence en fonction du temps
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')

#amplitude = np.fromstring(frames,np.int16


stream.stop_stream()
stream.close()
audio.terminate()


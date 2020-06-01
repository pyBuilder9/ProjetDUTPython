# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:42:27 2020

@author: amaury
"""
import numpy as np
#import scipy.io as sio   #matlab
#import scipy.io.wavfile
import scipy.signal as ss
import matplotlib.pyplot as plt
import pyaudio

#var globales
RATE = 44100  # nombre d'échantillons/s
duree_signal=4
dt = duree_signal/(RATE) # Periode d'echantillonnage
t = np.arange(RATE) * dt # Vecteur temps
FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 22050  # tronçon de 22050 correspond à une durée de 0,5 s
RECORD_SECONDS = 0.5#30


def capture_son():
    audio = pyaudio.PyAudio() 
    # Debut enregistrement
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
    #frames=[]
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        #frames.append(data)
        signal = np.fromstring(data,np.int16)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return signal
    

def calcul_fft(signal):
    # Calcul de la TFD (Transfo Fourrier Discrète)
    Nfft = 4096 # nombre de points de caclul de la FFT 
    axe_frequence, Pow = ss.welch(x=signal, fs=RATE, nfft=Nfft)
    # SPECTRE DU SIGNAL EN DB
    spec_db = 20*np.log10(Pow)
    return axe_frequence,spec_db

def affichage_des_3graph(axe_frequence, spec_db,signal):
    # Affichage de la courbe du signal        
    plt.subplot(221) #211=2 lignes, 1 colonne, index=1=affichera sur la 1ère case
    plt.title('Amplitude du signal en fonction du temps')#Fréquence en fonction du temps
    plt.xlabel('Temps (s)')
    plt.ylabel('Unite arbitraire')
    
    #Affichage du spectre du signal
    plt.subplot(122) #212  affichera sur la 2ème case
    plt.plot(axe_frequence, spec_db)
    plt.title('Spectre')
    plt.xlabel('frequence (Hz)')
    plt.ylabel('Unite arbitraire/sqrt(Hz)')
    #fig.tight_layout() #Automatically adjust subplot parameters to give specified padding.
    
    # Affichage du sonogramme du signal
    frequencies, times, spectrogram = ss.spectrogram(signal,RATE,nfft=2048) 
    plt.gcf().subplots_adjust(wspace=0.3)
    plt.subplot(223)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    #plt.ylim() # 0,fmax_obs
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.show()

################### main ###########################
fig=plt.figure()
for i in range(0,int(duree_signal/RECORD_SECONDS)):        
    signal=capture_son()
    axe_frequence, spec_db=calcul_fft(signal)
    affichage_des_3graph(axe_frequence, spec_db,signal)


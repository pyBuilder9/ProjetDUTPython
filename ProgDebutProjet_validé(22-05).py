# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:00:52 2020
@author: amaury
"""

# programme du projet encadré (16/05)


#######################################################################
# PROGRAMME POUR L'ANALYSE TEMPS-REEL DE SIGNAUX AUDIO : 
# PRODUCTION DE SPECTRE ET SONOGRAMME A PARTIR D'UNE ENTREE AUDIO
#######################################################################

# Analyse spectrale d'un signal sinusoïdal
import numpy as np
import scipy.io as sio   #matlab
import scipy.io.wavfile
import scipy.signal as ss
import matplotlib.pyplot as plt
#import h5py as h5

plt.close ('all') # ferme toutes les figures

# DIMENSIONNEMENT DE LA TFD
# 1.	Creer un vecteur echantillonnage de N points d'une duree T.
T = 1 # Duree du signal
N  = 50001 # Nombre de d'echantillons
dt = T/(N-1) # Periode d'echantillonnage
t = np.arange(N) * dt # Vecteur temps

## 2.	Quelle est la frequence d'echantillonnage ?
fe = 1/dt # Frequence d'echantillonnage
## 3 Quelle frequence maximale peut-on analyser ?
fmax = fe/2
print('Frequence d\'échantillonnage : %.1f Hz'% fe)
print('Frequence max d\'analyse : %.1f Hz'% fmax)

# chirp: choix = 2; signal modulé en fréquence: choix = 2
choix = 2

## Cas du sinus glissant ("chirp")
if choix == 1:

    fini = 1000
    Deltaf =  1000 #demi-accroissement de la frequence instantanée qui variera 
    # de fini à fini + 2*Deltaf
    pas_frequence = (Deltaf)/N
    matrice_frequence = np.arange(fini,fini+Deltaf, pas_frequence)
    frequence_instantanee = np.arange(fini,fini+2*Deltaf, 2*pas_frequence)
    sig = np.sin(2*np.pi*matrice_frequence* t)#
else:
     
# cas de la modulation de fréquence sinusoïdale
    fini=1000
    alfa = 100 # indice de modulation
    fmod = 2   # frequence de modulation
    freqmodulee= alfa*np.sin(2*np.pi*fmod* t)
    sig = np.sin(2*np.pi*fini* t + freqmodulee)
    frequence_instantanee = fini + alfa * fmod * np.cos(2*np.pi*fmod* t)
#plt.subplot(212)
#plt.plot(t,sig)

#creation bruit
noise = np.random.normal(0,0.5,N)
# 0 is the mean of the normal distribution you are choosing from
# 1 is the standard deviation of the normal distribution
# 100 is the number of elements you get in array noise

#signal bruité
sigb = sig + noise

## 5.	Tracer et legender le signal.
fig = plt.figure(figsize=(15,10)) #créer une nouvelle grille d'affichage
plt.gcf().subplots_adjust(wspace=0.1) #ajuste l'espace intergraphes
plt.subplot(221) #211=2 lignes, 1 colonne, index=1 => affichera sur la 1ère case
plt.plot(t,sigb)
plt.title('Amplitude du signal en fonction du temps')#Fréquence en fonction du temps
plt.xlabel('Temps (s)')
plt.ylabel('Unite arbitraire')

## 7.	Calculer la TFD. Transfo Fourrier Discrète
Nfft = 4096 # 4096 =nombre de points de caclul de la FFT 
f, Pow = ss.welch(x=sigb, fs=fe, nfft=Nfft) 
#spec=np.fft.fft(sigb, n=Nfft)
## 6.	Determiner le vecteur frequence associe.
df = fe/Nfft #1/(Nfft*dt) #Resolution spectrale
print('Résolution en fréquence : %.1f Hz'% df)

# axe des fréquences associé à la FFT
freq = np.arange(Nfft)*df

# SPECTRE DU SIGNAL EN DB
spec_db = 20*np.log10(Pow)# /Pow.max()
plt.subplot(122) #212  affichera sur la 2ème case
plt.plot(f, spec_db) #freq, abs(spec)
plt.title('Spectre')
plt.xlabel('frequence (Hz)')
plt.ylabel('Unite arbitraire/sqrt(Hz)')
fig.tight_layout() #Automatically adjust subplot parameters to give specified padding.
Deltaf=1000
fmax_obs=fini+ 2*(Deltaf) #fe/2  # fréquence de Shannon
plt.xlim(0, fmax_obs+1000)
plt.ylim(-150,0)

#sample_rate, samples = scipy.io.wavfile.read('Note_PianoB.wav')
#frequencies, times, spectrogram = ss.spectrogram(samples, sample_rate)

frequencies, times, spectrogram = ss.spectrogram(sigb, fe,nfft=2048)#,nperseg=32,,noverlap=30)
plt.gcf().subplots_adjust(wspace=0.3)

plt.subplot(223)
##plt.imshow(spectrogram)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.ylim(0,fmax_obs)
plt.pcolormesh(times, frequencies, spectrogram)
 
plt.show()

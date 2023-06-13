import pandas as pd
from models.transmission import Transmission
import numpy as np
import matplotlib.pyplot as plt
import utils


filename = '17-02-2023.csv'
df = pd.read_csv(filename, sep='\t', lineterminator='\n')
splitted_df = utils.split_data(df)
txs = [Transmission(s_df) for s_df in  splitted_df]


N = len(txs)         
cmap = plt.cm.get_cmap("hsv", N+1)

deltaf = 312.5       # sampling resolution or subcarrier bandwidth [kHz] 
K = 104              # number of carriers
B = K*deltaf         # channel bandwidth 
t0 = 0               # assuming that starts from zero
deltat = 1/B

plt.rcParams.update({'font.size': 22})
# Plotting the amplitude of H(f)
plt.figure(0)
for index, tx in enumerate(txs):
    Hest_abs = np.mean(tx.csi.amplitude, axis=0)
    all_carriers = np.arange(K)
    if tx.receiver_id == 'ca04': 
        linestyle='solid'
    else:
        linestyle='dashed'
    plt.plot(all_carriers, Hest_abs, label=tx.self_description(), linestyle=linestyle, c=cmap(index))
    plt.grid(True); plt.xlabel('Carrier index'); plt.ylabel(r'$|\hat{H}(f)|$ '); plt.legend(fontsize=10)
    plt.title('Amplitude (Null subcarriers removed)')
# plt.show()


# Plotting the phase of H(f)
plt.figure(1)
for index, tx in enumerate(txs):
    Hest_phase = np.mean(tx.csi.phase, axis=0)*180/np.pi
    all_carriers = np.arange(K)
    if tx.receiver_id == 'ca04': 
        linestyle='solid'
    else:
        linestyle='dashed'
    plt.plot(all_carriers, Hest_phase, label=tx.self_description(), linestyle=linestyle, c=cmap(index))
    plt.grid(True); plt.xlabel('Carrier index'); plt.ylabel(r'$\angle \hat{H}(f)$ [degrees]'); plt.legend(fontsize=10, ncol=2)
    plt.title('Phase (Null subcarriers removed)')
# plt.show()



# # Plotting the channel impulse response h(t)
plt.figure(2)
for index, tx in enumerate(txs):
    Hest_abs = np.mean(tx.csi.amplitude, axis=0)
    Hest_phase = np.mean(tx.csi.phase, axis=0)
    Hest = Hest_abs * np.exp(1j*Hest_phase)
    hest = np.fft.ifft(Hest)
    time = t0 + np.arange(K)*deltat*1000
    if tx.receiver_id == 'ca04': 
        linestyle='solid'
    else:
        linestyle='dashed'
    plt.plot(time, hest, label=tx.self_description(), linestyle=linestyle, c=cmap(index))
    plt.grid(True); plt.xlabel(r'time [$\mu$s]'); plt.ylabel(r'$\hat{h}(t)$'); plt.legend(fontsize=10)
    plt.title(r'Estimated channel impulse response $\hat{h}(t)$')
# plt.show()


# Plotting the power delay profile norm(h(t))
plt.figure(3)
for index, tx in enumerate(txs):
    Hest_abs = np.mean(tx.csi.amplitude, axis=0)
    Hest_phase = np.mean(tx.csi.phase, axis=0)
    Hest = Hest_abs * np.exp(1j*Hest_phase)
    hest = np.fft.ifft(Hest)
    pdpest = 20*np.log10(np.abs(hest)/1000)
    time = t0 + np.arange(K)*deltat*1000
    if tx.receiver_id == 'ca04': 
        linestyle='solid'
    else:
        linestyle='dashed'
    plt.plot(time, pdpest, label=tx.self_description(), linestyle=linestyle, c=cmap(index))
    # plt.stem(time, pdpest, label=tx.self_description())
    plt.grid(True); plt.xlabel(r'time [$\mu$s]'); plt.ylabel('Power delay profile [dBm]'); plt.legend(fontsize=10, ncol=2)
    plt.title('Power delay profile')
# plt.show()


# Plotting the RSSI vs distance
plt.figure(4)
for index, tx in enumerate(txs):
    distance = tx.distance*1000  # mts
    rssi_mean = tx.data.rssi.mean()
    if tx.receiver_id == 'ca04': 
        marker='o'
    else:
        marker='s'
    plt.plot(distance, rssi_mean, label=tx.self_description(), marker=marker, markersize=12, c=cmap(index))
    # plt.stem(time, pdpest, label=tx.self_description())
    plt.grid(True); plt.xlabel(r'Distance [$m$]'); plt.ylabel('RSSI'); plt.legend(fontsize=10)
    plt.title('RSSI vs distance')
# plt.show()

# Plotting the power of the direct path vs distance
plt.figure(5)
for index, tx in enumerate(txs):
    distance = tx.distance*1000  # mts
    Hest_abs = np.mean(tx.csi.amplitude, axis=0)
    Hest_phase = np.mean(tx.csi.phase, axis=0)
    Hest = Hest_abs * np.exp(1j*Hest_phase)
    hest = np.fft.ifft(Hest)
    pdpest = 20*np.log10(np.abs(hest)/1000)
    fmc = np.max(pdpest)

    if tx.receiver_id == 'ca04': 
        marker='o'
    else:
        marker='s'
    plt.plot(distance, fmc, label=tx.self_description(), marker=marker, markersize=12, c=cmap(index))
    # plt.stem(time, pdpest, label=tx.self_description())
    plt.grid(True); plt.xlabel(r'Distance [$m$]'); plt.ylabel('Power of the direct path [dBm]'); plt.legend(fontsize=10)
    plt.title('Power of the direct path vs distance')

# Plotting the power of the direct path vs distance
plt.show()
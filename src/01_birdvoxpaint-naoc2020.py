import datetime
import birdvoxpaint as bvp
import glob
import h5py
import librosa
import os
import sys

date_str = sys.argv[1]

indices = [
    bvp.acoustic_complexity_index,
    bvp.entropy_based_concentration,
    bvp.acoustic_event_count,
    bvp.average_energy,
    bvp.maximum_pcen
]

# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Saving BirdVoxPaint features to HDF5 format.")
print("birdvoxpaint version: {:s}".format(bvp.__version__))
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("")

data_dir = "/beegfs/vl1019/drucker2020naoc_data"
in_dir = os.path.join(data_dir, "BOGOTA_NFCs_2018")
swift_dir = os.path.join(in_dir, "SWIFT_" + date_str)
glob_regexp = os.path.join(swift_dir, "*.wav")
wav_paths = glob.glob(glob_regexp)

out_dir = os.path.join(data_dir, "BOGOTA_NFCs_2018_bvp-features")
os.makedirs(out_dir, exist_ok=True)
h5_name = "SWIFT_" + date_str + ".h5"
h5_path = os.path.join(out_dir, h5_name)


with h5py.File(h5_path, "w") as h5py_file:
    X = h5py_file.create_group("bvp_features")
    for wav_path in wav_paths:
        wav_name = os.path.split(wav_path)[1]
        X[wav_name] = bvp.transform(
            wav_path, indices=indices, verbose=False,
            frame_length=512, hop_length=256,
            segment_duration=60)


# Print elapsed time.
print(str(datetime.datetime.now()) + " Finish.")
elapsed_time = time.time() - int(start_time)
elapsed_hours = int(elapsed_time / (60 * 60))
elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
elapsed_seconds = elapsed_time % 60.
elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                               elapsed_minutes,
                                               elapsed_seconds)
print("Total elapsed time: " + elapsed_str + ".")

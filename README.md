# PyQt5_with_docker

# As of 2021.05.14 

## Create environment from scratch
# Use Nvidia docker image that contains CUDA and CUDANN
- options for display, sound (not sure), opengl are included.
`docker run --gpus all -it --name gui1 -v /home/hayoung/Desktop/:/data -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native -v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native --group-add $(getent group audio | cut -d: -f3) --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -e NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute nvidia/cuda:11.2.2-cudnn8-devel-ubuntu18.04`

# Install gl library
`apt install -y -qq --no-install-recommends libglvnd0 libgl1 libglx0 libegl1 libxext6 libx11-6`
`rm -rf /var/lib/apt/lists/*`

# Set option outside of a docker container (i.e., host)
`xhost +local:'docker inspect --format='{{.Config.Hostname}}' bdba249440d4'`

# Install PyQt5
`pip isntall PyQt5`
(You may also need `apt install python3-pyqt5`)
`apt install qttools5-dev-tools`
`apt install libpulse-dev`
`apt install libqtSmultimediaS-plugins`
`apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio`

# Create .ui file
You need to create an .ui file which contains widgets that have specific names for demo, so downloading demo .ui file from [here](https://drive.google.com/file/d/1ODFZsKrKH_h8IXUzQUikT4Zfsl20s4JT/view?usp=sharing) or from this git repo is recommanded.

# Run demo code
`python test.py`

## Use docker image
# Download docker image
`docker pull hyformal/gui_cuda11.2cudnn8:tagname'

# Start docker container
`docker run --gpus all -it --name gui1 -v /home/hayoung/Desktop/:/data -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native -v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native --group-add $(getent group audio | cut -d: -f3) --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -e NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute nvidia/cuda:11.2.2-cudnn8-devel-ubuntu18.04`

# Set option outside of a docker container
`xhost +local:'docker inspect --format='{{.Config.Hostname}}' bdba249440d4'`

# Clone this repo
`git clone https://github.com/Hayoung93/PyQt5_with_docker.git`

# Start demo
`python test.py`

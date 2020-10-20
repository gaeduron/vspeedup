# Video Auto SpeedUp

Video Auto SpeedUp is a script that **speedup the silent parts of a video.**

## Installation

Download the project

```
git clone https://github.com/gduron/vspeedup
```

To use this project you will need [Python3](https://www.python.org/downloads/), [pipenv](https://pypi.org/project/pipenv/), [ffmpeg](https://ffmpeg.org/download.html) and [Jupiter Notebook](https://jupyter.org/install)

Once they are installed you can install the python libraries with:

```
pipenv install
```

## Usage

You can open the script interface in **jupiter notebook** with:
```
jupyter notebook Video_Auto_SpeedUp.ipynb
```

Inside the notebook you can select the **path of the file** you want to speed up.
You can also change 3 options:
1. The **volume threshold** for the silence
2. The **speed** of the fast forward
3. **Verbose** to see which part of the video correspond to silence

### Interface

![interface](https://i.ibb.co/y6qZG6r/Screen-Shot-2020-10-20-at-18-26-13.png)
![audio analysis](https://i.ibb.co/Lz4bSD8/Screen-Shot-2020-10-20-at-18-26-24.png)

## Info

This project is not actively maintained.

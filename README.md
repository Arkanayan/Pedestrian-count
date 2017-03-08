# Pedestrian detection and graphing

Detect number of pedestrians in a frame and graph show it in a graph

## Getting Started

Run the script by specifying the video
```
python[3] detect.py -v "path to the video"
```

### Prerequisites

The script is coded using ```python 3.6```, ```opencv 3```. And you will need opencv compiled with `ffmpeg` to read video

### Installing

Install opencv3 on anaconda
```
conda install -c menpo opencv3

```
Or to compile opencv3 with ffmpeg follow instructions here [https://github.com/menpo/conda-opencv3](https://github.com/menpo/conda-opencv3) or run these commands

```
$ conda install conda-build
$ git clone https://github.com/menpo/conda-opencv3
$ cd conda-opencv3
$ conda config --add channels menpo
$ conda build conda/
$ conda install /PATH/TO/OPENCV3/PACKAGE.tar.gz
```

Before compiling change the flag ```-DWITH_FFMPEG=0 ``` to ```1``` on file ```conda/build.sh```.

Then install other libraries using ```pip``` or ```pip3```
```
pip[3] install matplotlib rx imutils
```

## Built With

* [Visual Studio Code](https://code.visualstudio.com/) - The web framework used
* [Anaconda](https://www.continuum.io/) - Dependency Management


## Authors

* **Arka Nayan** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Built as per instructions given by Navin Manaswi


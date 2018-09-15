# Carpat Climate Data Webapp

Display climate data for given location or whole area in given time

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

See deployment for notes on how to deploy the project on a live system.

#### Prerequisites
- python 3.6.5 (3.5.2 works also)

- Cartopy dependencies:
* [proj4](https://proj4.org/install.html#install)

```bash
sudo apt-get install libproj-dev proj-data proj-bin
```
* [geos](https://github.com/googlecolab/colabtools/issues/85)
```bash
sudo apt-get install libgeos-dev
```


Climate Data files:
```
CARPATGRID_TA_D.ser
CARPATGRID_TA_M.ser
CARPATGRID_TA_Y.ser
PredtandfilaGrid.dat
```


### Installing
Create python virtual enviroment and activate it. Update pip if needed.
```bash
python -m pip install --upgrade pip
```


##### Install python packages:

```bash
pip install -f requirements.txt
```

or with conda:
```bash
conda install -n carpatclim --file requirements_conda.txt
```

##### Matplotlib
Force matplotlib to not use any Xwindows backend. Set backend to Agg in matplotlib rc file.
```bash
python -c "import matplotlib; print(matplotlib.matplotlib_fname())"
vi ./myvenv/lib/python3.5/site-packages/matplotlib/mpl-data/matplotlibrc
```
```
backend : Agg
```

##### Copy Climate data files into static/data

##### Test run
Run django test server with:
```bash
python manage.py runserver 0.0.0.0:8000
```

Open 127.0.0.1:8000/carpatclim/ in browser

## Running the tests
run tests in tests directory with
```bash
python -m unittest run
```

## TODO
- [ ] Fetch climate data for specific coordinates and time

## Deployment
Add additional notes about how to deploy this on a live system

## Built With

* [python](https://www.python.org/) - Language used
* [django](https://www.djangoproject.com/) - The web framework used
* [matplotlib](https://matplotlib.org/) - Python 2D plotting library
* [numpy](https://www.numpy.org) - Package for scientific computing with Python
* [pandas](https://pandas.pydata.org/) - Data structures and data analysis tools for the Python
* [cartopy](https://scitools.org.uk/cartopy/) - Python package designed for geospatial data processing
* [metpy](https://github.com/Unidata/MetPy) - Tools in Python for reading, visualizing and performing calculations with weather data

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Martin** - *Initial work* - [meteorolog90](https://github.com/meteorolog90)
* **dstojakovic** [dstojakovic](https://github.com/dstojakovic)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


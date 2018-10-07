### Installing
Create python virtual enviroment and activate it. Update pip if needed.
```bash
python -m pip install --upgrade pip
```


##### Install python packages:

```bash
pip install -f requirements.txt
pip install cartopy
```

or with conda:
```bash
conda create --name carpatclim python=3.6.4
conda install --channel anaconda --name carpatclim geos==3.6.2
conda install --channel anaconda --name carpatclim shapely==1.6.4
conda install --channel conda-forge --name carpatclim metpy==0.9.1
conda install --name carpatclim --file requirements_conda.txt
```

##### Copy Climate data files into data directory:
```
CARPATGRID_TA_D.ser
CARPATGRID_TA_M.ser
CARPATGRID_TA_Y.ser
PredtandfilaGrid.dat
```

##### Matplotlib
If not using GUI, force matplotlib to not use any Xwindows backend. Set backend to Agg in matplotlib rc file.
```bash
python -c "import matplotlib; print(matplotlib.matplotlib_fname())"
vi ./myvenv/lib/python3.5/site-packages/matplotlib/mpl-data/matplotlibrc
```
```
backend : Agg
```

##### Import climate data files into dataabse

```bash
python carpatclimapp/sqlite_import.py -i
```

##### Django Test Server run
Generate secret key
```bash
python -c 'import random; import string; print("".join([random.SystemRandom().choice(string.digits + string.ascii_letters + string.punctuation) for i in range(100)]))' > secret_key.txt
```

Apply database migrations
```bash
python manage.py migrate
```

Run Django test server with:
```bash
python manage.py runserver 0.0.0.0:8000
```

Open 127.0.0.1:8000/ in browser

## Running the tests
Run tests in tests directory with
```bash
python -m unittest run
```

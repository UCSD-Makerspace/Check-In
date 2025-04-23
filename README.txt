# Check-In

Check-in for the DIB 4th floor.

The entrepreneurship center's colors are #70983f.

## Installation

Create a python virtual environment:
```
python3 -m venv --system-site-packages Check-In
```

Clone the repo:
```
git clone https://github.com/UCSD-Makerspace/Check-In
cd Check-In
git checkout entrepreneur-ship-center
```

Install dependencies:
sudo apt-get install swig pcscd

Install pyscard:
```
sudo apt-get install pcscd swig gcc libpcsclite-dev
git clone https://github.com/LudovicRousseau/pyscard.git 
cd pyscard
sudo ../bin/python setup.py build_ext install
```

Install other dependencies:
```
./bin/python -m pip install -r requirements.txt
```
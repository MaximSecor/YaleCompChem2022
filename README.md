# Submit Gaussian16 jobs for Yale's Chem 426/526

This will install `gausub`, which is an easy submitter for Gaussian jobs on Grace.

## Install

In your home directory (if you aren't sure, just type `cd`), type 

```
git clone https://github.com/jjgoings/YaleCompChem.git
cd YaleCompChem
python setup.py install --user
``` 

This should install the submitter `gausub`.

## Usage

Say we have a G16 job: `water.com`, which is a water molecule (you can find this in `examples/water.com`)

To submit it, just

```
gausub water.com
```

This will prepare a submission script for you and send it to the queue to run. You can check on it by typing 

```
squeue -u <Your NetID>
```

Once complete, the output will be written to `water.log`.

If you want to inspect the submission script, it will have the same name as your input, but with a `.sh` extension (e.g. `water.sh`)

## Options and help

Type `gausub --help` for a list of command-line options. You can change the time given to the job and number of CPUs here. 

(Note that if you want to use more CPUs, you must *also* change the input file to request a greater number of CPUs. In the Gaussian `.com` or `.gjf` file, you must edit `%NprocShared=<num CPUs>`.)



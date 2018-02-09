import os
import MetaTagTypes as tt
import metaunidec.mudeng as mudeng
import unidec_modules.mzmlparse_auto as mzparse
from unidec_modules.mzMLimporter import *

try:
    from unidec_modules.data_reader import *
except:
    print "Could not import data reader: meta_data_importer"


def parse_file(file_path, exp_type='Time', collision=None, dir=None):
    file_name = os.path.split(file_path)[1]
    exedir = dir

    out = {tt.FILE_PATH: file_path,
           tt.FILE_NAME: file_name,
           tt.V1: None,
           tt.V2: None,
           tt.TIME_START: None,
           tt.TIME_END: None,
           tt.TYPE: exp_type,
           tt.SCAN_START: None,
           tt.SCAN_END: None}

    return out


def auto_from_wizard(data, filename, mode):
    # print data
    eng = mudeng.MetaUniDec()
    eng.data.new_file(filename)
    v1s = []
    v2s = []
    for i, d in enumerate(data):
        v1 = d[1]
        v2 = d[2]
        v1s.append(v1)
        v2s.append(v2)
        try:
            start = float(d[3])
        except:
            start = None
        try:
            stop = float(d[4])
        except:
            stop = None
        path = d[5]

        if start is None or stop is None:
            eng.data.add_file(path=path)
        else:
            print start, stop
            if os.path.splitext(path)[1] == ".mzML":
                d = mzMLimporter(path)
            else:
                d = DataImporter(path)
            if mode == 1:
                data = d.get_data(scan_range=(start, stop))
            elif mode == 0:
                data = d.get_data(time_range=(start, stop))
            eng.data.add_data(data, path)
        eng.data.spectra[-1].var1 = v1
        eng.data.spectra[-1].var2 = v2
    eng.data.export_hdf5()



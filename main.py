# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from fileUtilities import readConfigFile
from pymeasure.adapters import VISAAdapter
from pymeasure.instruments.eurotest.eurotestHPP120256 import EurotestHPP120256
from pymeasure.instruments.keithley import Keithley2400


def check_presence(inst):
    response = inst.id
    print(response)
    time.sleep(1)

def getInstruments(k2400_gpibAddress, hvSource_gpibAddress):

    hpp120256 = None
    k2400 = None

    hpp120256_adapter = VISAAdapter("GPIB0::"+str(hvSource_gpibAddress)+"::INSTR",
                          write_termination="\n",
                          read_termination="",
                          send_end=True)

    hpp120256_adapter.connection.timeout = 5000
    response_encoding = "iso-8859-2"  # In my case, instrument uses this encoding on response, so take it into account
    query_delay = 0.2  # Delay in s to sleep between the write and read occuring in a query
    hpp120256 = EurotestHPP120256(hpp120256_adapter, response_encoding, query_delay, includeSCPI=False)

    check_presence(hpp120256)

    k2400_adapter = VISAAdapter("GPIB0::" + str(k2400_gpibAddress) + "::INSTR",
                                    write_termination="\n",
                                    read_termination="",
                                    send_end=True)

    k2400 = Keithley2400(k2400_adapter)
    check_presence(k2400)

    return k2400, hpp120256


def initializeK2400(k2400, compliance, nplcs, range):
    pass

def initializeHVSource(hv_source, rampVoltage, outputCurrentLimit, enableKill):
    pass

def start_process(K2400_gpibAddress,
                  HVSource_gpibAddress,
                  initialVoltage,
                  finalVoltage,
                  pointsVoltage,
                  measureDelay_ms,
                  rampVoltage,
                  outputCurrentLimit,
                  enableKill,
                  ammeterRange,
                  ammeterCompliance,
                  ammeterNPLCs,
                  resultsFilePath):


    k2400, hv_source = getInstruments(K2400_gpibAddress, HVSource_gpibAddress)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    process_config_file_path = "process_config_file.json"
    dut_reference = ""

    K2400_gpibAddress, \
    HVSource_gpibAddress, \
    initialVoltage, \
    finalVoltage, \
    pointsVoltage, \
    measureDelay_ms, \
    rampVoltage, \
    outputCurrentLimit, \
    enableKill, \
    ammeterRange, \
    ammeterCompliance, \
    ammeterNPLCs, \
    resultsFilePath, \
    resultsFilePathExtension = readConfigFile(process_config_file_path)

    start_process(K2400_gpibAddress,
                  HVSource_gpibAddress,
                  initialVoltage,
                  finalVoltage,
                  pointsVoltage,
                  measureDelay_ms,
                  rampVoltage,
                  outputCurrentLimit,
                  enableKill,
                  ammeterRange,
                  ammeterCompliance,
                  ammeterNPLCs,
                  resultsFilePath + str(dut_reference) + "." + resultsFilePathExtension)

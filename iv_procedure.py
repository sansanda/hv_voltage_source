# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.eurotest.eurotestHPP120256 import EurotestHPP120256

from pymeasure.experiment import Procedure, Results, Worker
from pymeasure.experiment import IntegerParameter, FloatParameter
from time import sleep
import logging
import numpy as np
from pymeasure.log import console_log

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class IVProcedure(Procedure):

    data_points = IntegerParameter('Data points', default=50)
    averages = IntegerParameter('Averages', default=50)
    max_voltage = FloatParameter('Maximum Voltage', units='kV', default=1.0)
    min_voltage = FloatParameter('Minimum Voltage', units='kV', default=0.0)
    voltage_ramp = 100.0 #V/s
    voltage

    DATA_COLUMNS = ['Voltage (kV)', 'Current (A)', 'Current Std (A)']

    def startup(self):
        log.info("Connecting and configuring the instruments...")
        log.info("Connecting to the Keithley 2400..............")
        self.sourcemeter = Keithley2400("GPIB::25")
        self.sourcemeter.reset()
        self.sourcemeter.source_mode = "voltage"
        self.sourcemeter.measure_current(nplc=1, current=1.05e-6, auto_range=False)
        self.sourcemeter.compliance_current = 1.05e-3
        self.sourcemeter.use_rear_terminals()
        self.sourcemeter.source_enabled = True
        sleep(0.1) # wait here to give the instrument time to react
        self.sourcemeter.set_buffer(IVProcedure.averages)

        log.info("Connecting to the Euro Test HV Source........")
        self.hv_source = EurotestHPP120256("GPIB::20")
        self.hv_source.voltage_ramp = IVProcedure.voltage_ramp

        self.hv_source.voltage = 0.0
        self.hv_source.wait_for_voltage_output_set()

    def execute(self):
        voltages = np.linspace(
            self.min_voltage,
            self.max_voltage,
            num=self.data_points
        )

        # Loop through each current point, measure and record the voltage
        for voltage in voltages:
            log.info("Setting the voltage to %g A" % voltage)
            self.hv_source.voltage = voltage
            self.hv_source.wait_for_voltage_output_set()
            self.sourcemeter.reset_buffer()
            sleep(0.1)
            self.sourcemeter.start_buffer()
            log.info("Waiting for the buffer to fill with measurements")
            self.sourcemeter.wait_for_buffer()
            data = {
                'Voltage (kV)': voltage,
                'Current (A)': self.sourcemeter.means,
                'Current Std (A)': self.sourcemeter.standard_devs
            }
            self.emit('results', data)
            sleep(0.01)
            if self.should_stop():
                log.info("User aborted the procedure")
                break

    def shutdown(self):
        self.sourcemeter.shutdown()
        log.info("Finished measuring")

if __name__ == "__main__":
    console_log(log)

    log.info("Constructing an IVProcedure")
    procedure = IVProcedure()
    procedure.data_points = 100
    procedure.averages = 50
    procedure.max_voltage = 1.0
    procedure.min_voltage = 0.0

    data_filename = 'example.csv'
    log.info("Constructing the Results with a data file: %s" % data_filename)
    results = Results(procedure, data_filename)

    log.info("Constructing the Worker")
    worker = Worker(results)
    worker.start()
    log.info("Started the Worker")

    log.info("Joining with the worker in at most 1 hr")
    worker.join(timeout=3600) # wait at most 1 hr (3600 sec)
    log.info("Finished the measurement")

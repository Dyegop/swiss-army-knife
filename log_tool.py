# Objetivo: programa que reciba un error y genere un archivo de log

# El nombre del fichero debe ser "registro_log_fechaActual"
# El modo de escritura debe ser "w" la primera vez que se abra el fichero en el día y "a" las sucesivas
# veces en ese mismo día

import time
import sys

class Log:
    def __init__(self, error, file_name):
        self.error = error
        self.file_name = file_name

    def generate_log(self):
        with open(self.file_name, 'a') as log_file:
            # Get line where error happens
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            # Write the text to the logfile and move to next line
            log_file.write(f'{time.strftime("%d/%m/%Y %H:%M:%S")} - {self.error}\n')
            log_file.write(f'{time.strftime("%d/%m/%Y %H:%M:%S")} - Error at line {line}\n\n')


"""
Execution example
log = Log("Error example", '.\\Error_log.txt')
log.generate_log()
"""


"""
/* Copyright (C) Dired Proyectos e Instalaciones, S.L. - Todos los derechos reservados
 * Queda totalmente prohibida la distribución de este contenido sin el consentimiento expreso
 * de Dired Proyectos e Instalaciones S.L.
 *
 *
 * En caso de consultas sobre el funcionamiento del código
 * Por favor escriba a: info@diredproyectos.com, o visite https://diredproyectos.com
 */
"""
# Librería para leer archivos CSV
import csv
# Librería utilizada para la automatización de procesos en Chrome
import rpa as r



copyright_str = """/* Copyright (C) Dired Proyectos e Instalaciones, S.L. - Todos los derechos reservados
                    * Queda totalmente prohibida la distribución de este contenido sin el consentimiento expreso
                    * de Dired Proyectos e Instalaciones S.L.
                    *
                    *
                    * En caso de consultas sobre el funcionamiento del código
                    * Por favor escriba a: info@diredproyectos.com, o visite https://diredproyectos.com
                    */"""

# URLS donde ejecutar login
urls = ['http://fd##############?errorType=logoff', 'htt##################ogin.jsp', 
        'http://fdt###############ndex.jsp']


def login(user, password):
    r.type('//*[@name="user"]', user)
    r.type('//*[@name="password"]', password + '[enter]')


def rezonificar_finca(uuii):
    r.url(uuii)
    r.timeout(120)
    if r.read('//*[@id="mySubmit"]'):
        r.select('//*[@name="new_central_office_id"]', '391')
        r.timeout(120)
        r.select('//*[@name="new_creg_id"]', '86093')
        r.timeout(120)
        r.select('//*[@name="new_zone_id"]', '835260')
        r.timeout(120)
        r.click('//*[@id="mySubmit"]')
        r.wait(10)
        r.timeout(120)
        if r.url('htt####################tchMethod=submit'):
            print('Finca Rezonificada')
        elif r.timeout() > 120:
            print('Finca NO Rezonificada')



# Print copyright
print(copyright_str)

# Inicio del programa
r.init()

# Pide usuario y contraseña
# Suponemos que los introduciria bien y que siempre es el mismo user/pass,
# de manera que solo los tiene que poner una vez
user = input("Introduce el usuario de FDTT: ")
password = input("Introduce el password: ")
file = open(input("Introduce la ruta del archivo de fincas: "), "rt")
ui = [row[0] for row in csv.reader(file)]


# Si no me equivoco, aqui ya te abre el link
# En caso de no estar logueado, se loguea



while r.url() in urls:
    try:
        login(user, password)
        for value in ui:
            rezonificar_finca(ui)
    # TODO Añadir una excepcion de la libreria por si falla el login en lugar de usar la general
    except Exception:
        # Mensaje para el usuario
        print("Usuario o contraseña incorrectos\n")
        # Raise lanza la excepcion
        # Si falla, tendría que reejecutar el script
        raise

import subprocess
import os
import zmq
import sys
import glob
import pickle
import netifaces as ni

# Imprime la tabla.
print "-------------------------------------------------------------"
print "|                                                           |"
print "| Elija una de las opciones disponibles:                    |"
print "-------------------------------------------------------------"
print "|                                                           |"
print "|  1. Actuar como servidor de archivos                      |"
print "|  2. Pedir archivos a los servidores disponibles.          |"
print "|                                                           |"
print "-------------------------------------------------------------"


print

# Pide una respuesta concreta y la guarda en la variable "respuesta"
respuesta = input("Respuesta (1/2): ")

print


# Si la respuesta es 2 (Pedir ficheros a los servidores)
if respuesta == 2:

    # Muestra la tabla 
    print "-------------------------------------------------------------"
    print "|                                                           |"
    print "|  1. Elegir una IP concreta                                |"
    print "|  2. Escanear la red en busca de servidores disponibles    |"
    print "|     (puede resultar algo mas lento)                       |"
    print "|                                                           |"
    print "-------------------------------------------------------------"

    # Pide al usuario una respuesta
    respIp = input("Elija una respuesta (1/2): ")

    # Si el usuario quiere escanear la red
    if(respIp == 2):
        print
        # Pide la interfaz por la que escanear
        interf = raw_input("Seleccione la interfaz a escanear (wlan0/eth0): ")

        print
        print "Servidores disponibles:"
        print

        # "Recorta" la IP actual para buscar solo en dicho rango de direcciones
        ipActual = ni.ifaddresses(interf)[2][0]['addr']
        ipCortada = ipActual[:-4]

        # Lista las IP activas de un rango de direcciones concreto, mostrando "Activo" si puede hacerse ping y "Inactivo" en otro caso.
        with open(os.devnull, "wb") as limbo:
            listaip = []
            for n in xrange(1, 255):
                ip=ipCortada+".{0}".format(n)
                result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip], stdout=limbo, stderr=limbo).wait()
                if result == False:
                    print ip + "- Activo"
                    listaip.append(ip)
                else:
                    print ip + "- Inactivo"

        # Muestra los servidores activos.
        print "Los servidores disponibles son:"
        for nlista in xrange(0,len(listaip)):
            print " -  ", listaip[nlista]

        print
        ipElegida = raw_input("Elija un servidor de la lista: ")


    elif respIp == 1:
        ipElegida = raw_input("Introduzca la IP elegida: ")


    # Pone en marcha los sockets que permitiran conectar con el servidor

    context = zmq.Context()

    # Este socket es un socket de tipo REQUEST, que realizara una peticion de tipo "consulta" al servidor
    socket = context.socket(zmq.REQ)
    # Este socket es de tipo REPONSE, y permitira recibir por parte del servidor una respuesta
    socket2 = context.socket(zmq.REP)
    # Conecta los sockets y envia "consulta" al servidor
    socket.connect('tcp://'+ipElegida+':4545')
    socket.send('consulta')
    socket2.connect('tcp://'+ipElegida+':4546')

    # Recibe informacion por parte del servidor 
    while True:
        data = pickle.loads(socket2.recv())
        if not socket.getsockopt(zmq.RCVMORE):
            break

    print
    # Muestra los ficheros disponibles
    print "Los ficheros disponibles de "+ ipElegida+" son los siguientes: "

    for ndata in xrange(0,len(data)):
        print " -  ", data[ndata]

    # Pide al usuario que elija uno de los ficheros
    respuestaFichero = raw_input("Elija uno de los ficheros (ruta completa): ")

    # Abre en el mismo directorio que el fichero ".py" un fichero con el nombre.
    destino = open(os.path.basename(respuestaFichero), 'w+')

    # Usa dos sockets mas. Uno para enviar la ruta que quiere conseguir (socket3) y otro para
    # recibir la informacion.
    socket3 = context.socket(zmq.REQ)
    socket3.connect('tcp://'+ipElegida+":4547")
    socket3.send(respuestaFichero)

    socket4 = context.socket(zmq.REP)
    socket4.connect('tcp://'+ipElegida+":4548")
    
    # Recibe la informacion
    while True:
        data2 = socket4.recv()
        destino.write(data)
        if not socket.getsockopt(zmq.RCVMORE):
            break

    # Imprime la ruta del fichero recibido.
    print "Recibido "+respuestaFichero+". "



elif respuesta == 1:

    ruta = raw_input("Escriba la ruta del directorio a compartir: ")

    context = zmq.Context(1)
    socketrep = context.socket(zmq.REP)
    socketrep.bind('tcp://*:4545')


    sockc = context.socket(zmq.REQ)
    sockc.bind('tcp://*:4546')

    socket3 = context.socket(zmq.REP)
    socket3.bind('tcp://*:4547')

    socket4 = context.socket(zmq.REQ)
    socket4.bind('tcp://*:4548')

    msg = socketrep.recv();

    if msg == 'consulta':
        print "Recibida consulta. Procesando..."
        lista = glob.glob(ruta+"/*")
        stream = pickle.dumps(lista)

        sockc.send(stream)
        msg = socket3.recv();
        if not os.path.isfile(msg):
            sockc.send('')

        fn = open(msg, 'rb')
        stream = True
        while stream:
            stream = fn.read()
            if stream:
                socket4.send(stream, zmq.SNDMORE)
            else:
                socket4.send(stream)

        print "Enviado "+msg+". "

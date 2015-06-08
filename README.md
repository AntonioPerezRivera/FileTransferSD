## FileTransferSD

### Introducción

Aplicación que, mediante su ejecución permite la transferencia de ficheros entre máquinas dentro del mismo rango de direcciones.

Los ficheros pueden ser de cualquier tipo (imágenes, documentos, ficheros de texto plano, texto enriquecido, ficheros comprimidos, etcétera).

El cliente podrá escanear los ficheros que un servidor concreto ponga a disposición de los clientes y elegir el deseado.

### Desarrollo y uso de la aplicación:

Es tan simple como ejecutar nuestro código "main.py" mediante la sentencia 'python main.py'. Como es lógico y debido a que está basado en una transferencia de ficheros entre máquinas dentro del mismo rango de direcciones, debemos elegir según muestra el programa mediante un menú, actuar como servidor o cliente, pidiendo archivos a un servidor en éste último caso.

* Si elegimos la opción de cliente:

Tenemos dos opciones, elegir una IP concreta de manera directa o pedir que escanee dentro de la subred, los servidores disponibles, de los cuáles posteriormente elegiremos uno. A éste elegido se le preguntará por sus archivos disponibles en cierto directorio que se utilice y responderá de vuelta al cliente con el resultado. Tras esto, el cliente le solicitará la transferencia de dicho archivo en cuestión al servidor. Todo ello mediante una comunicación síncrona podría decirse.

* Si elegimos la opción de servidor:

Éste actuará de tal modo que se mantendrá a la espera de que un cliente en la misma subred le realice una petición, de la cuál responderá diciéndole que archivos disponibles tiene, y posterior a ello de ser respondido por el cliente por cuál quiere, le enviará dicho fichero. 

Todo ello se encuentra de manera detallada y comentada en el fichero de código, dentro del cuál tenemos las dos opciones comentadas previamente, siendo éstas servidor y cliente y su correspondiente actuación.

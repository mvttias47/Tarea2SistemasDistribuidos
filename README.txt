# Tarea 2 - Sistemas Distribuidos

Este proyecto es una implementación de un sistema distribuido que gestiona y monitorea el estado de los pedidos realizados a través de un ecommerce. Utiliza diversas tecnologías como Kafka para la mensajería, gRPC para la comunicación entre microservicios, y Elasticsearch para almacenar métricas de rendimiento. 

## Estructura del Proyecto

La estructura del repositorio es la siguiente:

- **client**: Contiene el cliente que simula el envío de pedidos al servicio de gestión de pedidos a través de gRPC.
- **docker**: Incluye archivos de configuración para levantar los servicios con Docker, tales como Kafka, Zookeeper, y Elasticsearch.
- **email**: Módulo que se encarga de enviar correos electrónicos de confirmación al usuario.
- **fsm**: Implementación de una máquina de estados finita (FSM) para gestionar el ciclo de vida de los pedidos.
- **kafka**: Contiene el código relacionado con el consumidor de Kafka, que procesa los mensajes de pedidos y los envía a los módulos correspondientes.
- **metrics**: Funciones y módulos para enviar métricas a Elasticsearch, permitiendo el monitoreo del sistema.
- **order-service**: Implementación del servicio gRPC que recibe los pedidos y los procesa.
- **venv**: Entorno virtual de Python que contiene las dependencias necesarias para ejecutar el proyecto.
- **locustfile.py**: Archivo de configuración de Locust para ejecutar pruebas de carga, simulando múltiples usuarios realizando pedidos en el sistema.

## Instalación

### Requisitos

- Docker y Docker Compose
- Python 3.8 o superior
- [Locust](https://locust.io/) para las pruebas de carga
- [gRPC](https://grpc.io/) y [Elasticsearch](https://www.elastic.co/es/elasticsearch/)

### Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/mvttias47/Tarea2SistemasDistribuidos.git
   cd Tarea2SistemasDistribuidos


2. **Crear y Activar el entorno virtual**:

python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows


3. **Levantar Docker**:
    docker-compose up -d



4. **Ejecutar el servicio gRPC**:
        Desde el directorio raíz, ejecuta:

        bash

    python3 order-service/order_service.py

5. **Ejecutar el consumidor de Kafka**:

    Para procesar los mensajes de los pedidos:

    bash

    python3 kafka/consumer.py

6. **Enviar pedidos simulados**:

    Ejecuta el archivo locustfile.py para simular múltiples usuarios enviando pedidos:

    bash

        locust -f locustfile.py

        Accede a http://localhost:8089 en tu navegador para configurar y lanzar la prueba de carga.

Descripción de Componentes
Docker Compose

El archivo docker-compose.yml configura y levanta los servicios necesarios: Zookeeper, Kafka y Elasticsearch, que permiten el correcto funcionamiento del sistema de mensajería y almacenamiento de métricas.
order-service

Servicio gRPC que recibe pedidos de los clientes y los publica en Kafka, además de registrar métricas de latencia en Elasticsearch.
Kafka Consumer

Un consumidor de Kafka que procesa los pedidos publicados, pasando por varios estados en una máquina de estados finita (FSM) y enviando correos electrónicos de confirmación.
Locust

Herramienta para simular pruebas de carga, donde varios usuarios realizan pedidos concurrentes, permitiendo evaluar el rendimiento del sistema en condiciones de alta demanda.
Métricas y Monitoreo

El sistema registra métricas de latencia y throughput en Elasticsearch, lo que permite analizar el rendimiento del sistema en tiempo real y detectar posibles cuellos de botella.
Contribuciones

Si deseas contribuir, realiza un fork del proyecto y envía tus propuestas a través de un pull request.
    
Licencia

Este `README.md` proporciona una visión general del proyecto, instrucciones de instalación, y una breve descripción de cada componente clave del sistema. Esto facilitará a otros desarrolladores entender y colaborar en tu proyecto.


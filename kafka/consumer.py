import sys
import os
import time
import smtplib
from kafka import KafkaConsumer
import json
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Timer


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fsm.order_fsm import OrderFSM 

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


processed_requests = 0
interval = 60  
def log_to_elasticsearch(data, load_test_type):
    data['load_test_type'] = load_test_type  
    url = 'http://localhost:9200/metrics/_doc'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Métricas enviadas a Elasticsearch con estado: {response.status_code}")

def calculate_throughput():
    global processed_requests
    throughput = processed_requests / interval * 60  
    log_to_elasticsearch({
        'throughput': throughput,
        'event': 'ThroughputCalculation'
    }, load_test_type="bajo")  
    

    processed_requests = 0
    

    Timer(interval, calculate_throughput).start()


calculate_throughput()

def send_email(order_data):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "matixd123423@gmail.com"  
    smtp_password = "mgvv xhuy kgms jfnw"  

    to_email = order_data['email']
    subject = f"Confirmación de pedido: {order_data['product_name']}"
    body = f"""
    Estimado cliente,

    Su pedido del producto {order_data['product_name']} ha sido procesado exitosamente.
    Estado actual: {order_data['status']}

    Detalles del pedido:
    - Producto: {order_data['product_name']}
    - Precio: {order_data['price']}
    - Método de pago: {order_data['payment_gateway']}
    - Dirección de envío: {order_data['shipping_address']}
    
    Gracias por su compra.

    Saludos,
    El equipo de ventas
    """

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

for message in consumer:
    order_data = message.value
    print(f"Pedido recibido de Kafka: {order_data}")

    start_time = time.time()


    order_fsm = OrderFSM(order_data)

 
    order_fsm.preparar()
    print(f"Estado del pedido actualizado: {order_fsm.state}")
    
    time.sleep(2) 

  
    order_fsm.enviar()
    print(f"Estado del pedido actualizado: {order_fsm.state}")

    time.sleep(2)  

    order_fsm.entregar()
    print(f"Estado del pedido actualizado: {order_fsm.state}")

    time.sleep(2) 

    
    order_fsm.finalizar()
    print(f"Estado del pedido actualizado: {order_fsm.state}")

 
    send_email(order_data)

    end_time = time.time()
    processing_time = end_time - start_time  

    
    processed_requests += 1

    log_to_elasticsearch({
        'latency': processing_time,
        'state': order_fsm.state,
        'event': 'UpdateState'
    }, load_test_type="bajo")  

import time
import grpc
from concurrent import futures
import order_pb2
import order_pb2_grpc
from kafka import KafkaProducer
import json
import requests

class OrderService(order_pb2_grpc.OrderServiceServicer):
    def PlaceOrder(self, request, context):
        start_time = time.time()  # Registro de tiempo al inicio del pedido

        # Procesamiento del pedido
        order_data = {
            "product_name": request.product_name,
            "price": request.price,
            "payment_gateway": request.payment_gateway,
            "card_brand": request.card_brand,
            "bank": request.bank,
            "shipping_address": request.shipping_address,
            "region": request.region,
            "email": request.email,
            "status": "Procesando"  # Estado inicial del pedido
        }

        # Publicar el pedido en un topic de Kafka
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send('orders', order_data)
        producer.flush()

        end_time = time.time()  # Registro del tiempo cuando termina de procesar el pedido
        latency = end_time - start_time  # Latencia en segundos
        
        # Enviar la métrica a Elasticsearch
        self.log_to_elasticsearch({
            'latency': latency,
            'state': 'Procesando',
            'event': 'PlaceOrder'
        })

        return order_pb2.OrderResponse(status="Procesando", order_id="ORD12345")

    def log_to_elasticsearch(self, data):
        url = 'http://localhost:9200/metrics/_doc'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Métricas enviadas a Elasticsearch con estado: {response.status_code}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC para pedidos iniciado...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

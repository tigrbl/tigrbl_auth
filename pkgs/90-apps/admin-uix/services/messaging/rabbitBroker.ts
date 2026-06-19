
import { MessageBroker, BrokerStatus } from './baseBroker';

export class RabbitMQBroker extends MessageBroker {
  private url: string;

  constructor(url: string = "amqp://guest:guest@localhost:5672") {
    super();
    this.url = url;
  }

  async connect(): Promise<void> {
    this.status = BrokerStatus.CONNECTING;
    return new Promise((resolve) => {
      setTimeout(() => {
        this.status = BrokerStatus.CONNECTED;
        console.log(`[RabbitMQ] Connected to AMQP instance`);
        resolve();
      }, 800);
    });
  }

  async disconnect(): Promise<void> {
    this.status = BrokerStatus.DISCONNECTED;
  }

  async publish(topic: string, message: any): Promise<void> {
    if (this.status !== BrokerStatus.CONNECTED) throw new Error("RabbitMQ not connected");
    console.debug(`[RabbitMQ] Routing to exchange: ${topic}`, message);
    this.notify(topic, message);
  }
}

export const global_rabbit = new RabbitMQBroker();

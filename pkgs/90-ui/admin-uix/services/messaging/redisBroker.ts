
import { MessageBroker, BrokerStatus } from './baseBroker';

export class RedisBroker extends MessageBroker {
  private host: string;

  constructor(host: string = "localhost:6379") {
    super();
    this.host = host;
  }

  async connect(): Promise<void> {
    this.status = BrokerStatus.CONNECTING;
    return new Promise((resolve) => {
      setTimeout(() => {
        this.status = BrokerStatus.CONNECTED;
        console.log(`[Redis] Connected to ${this.host}`);
        resolve();
      }, 500);
    });
  }

  async disconnect(): Promise<void> {
    this.status = BrokerStatus.DISCONNECTED;
  }

  async publish(topic: string, message: any): Promise<void> {
    if (this.status !== BrokerStatus.CONNECTED) throw new Error("Redis not connected");
    console.debug(`[Redis] Publish to ${topic}`, message);
    this.notify(topic, message);
  }
}

export const global_redis = new RedisBroker();

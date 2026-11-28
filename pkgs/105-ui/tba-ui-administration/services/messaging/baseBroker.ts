
export enum BrokerStatus {
  CONNECTED = "CONNECTED",
  DISCONNECTED = "DISCONNECTED",
  CONNECTING = "CONNECTING",
  ERROR = "ERROR",
}

export abstract class MessageBroker {
  protected status: BrokerStatus = BrokerStatus.DISCONNECTED;
  protected listeners: Map<string, Function[]> = new Map();

  abstract connect(): Promise<void>;
  abstract disconnect(): Promise<void>;
  abstract publish(topic: string, message: any): Promise<void>;

  async subscribe(topic: string, callback: (message: any) => void): Promise<void> {
    const topic_listeners = this.listeners.get(topic) || [];
    topic_listeners.push(callback);
    this.listeners.set(topic, topic_listeners);
    console.debug(`[Broker] Subscribed to ${topic}`);
  }

  get_status(): BrokerStatus {
    return this.status;
  }

  protected notify(topic: string, message: any) {
    const topic_listeners = this.listeners.get(topic) || [];
    topic_listeners.forEach(cb => cb(message));
  }
}

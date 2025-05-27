# Apache Kafka: From Introduction to Advanced Topics

## Introduction

Apache Kafka is a distributed event streaming platform used for building real-time data pipelines and streaming applications. Kafka is designed for high throughput, scalability, durability, and fault tolerance. It decouples data streams and enables asynchronous communication between producers and consumers.

---

## Core Concepts (In-Depth)

### Topics and Partitions

- **Topic:** Logical channel to which data is published. Topics are always multi-subscriber; data written to a topic is distributed to all consumers.
- **Partition:** Each topic is split into partitions, which are ordered, immutable sequences of records. Partitions allow Kafka to scale horizontally and provide parallelism.
- **Offset:** Each record in a partition has a unique sequential ID called an offset. Consumers use offsets to track their position.

#### Partitioning Strategies
- **Round Robin:** Default, distributes messages evenly.
- **Key-based:** Messages with the same key go to the same partition, ensuring order for that key.
- **Custom:** Implement your own partitioner for advanced use cases.

### Producers and Consumers

- **Producer:** Sends records to Kafka topics. Producers can choose which partition to send a record to, either randomly, by key, or using a custom partitioner.
- **Producer Configurations:**
  - `acks`: Controls durability (`0`, `1`, `all`).
  - `batch.size`, `linger.ms`: Control batching for throughput.
  - `compression.type`: `none`, `gzip`, `snappy`, `lz4`, `zstd`.
  - `retries`, `retry.backoff.ms`: Control retry behavior.
- **Consumer:** Reads records from topics. Consumers are grouped into consumer groups for scalability and fault tolerance.
- **Consumer Configurations:**
  - `group.id`: Consumer group identifier.
  - `auto.offset.reset`: What to do when there is no initial offset (`earliest`, `latest`).
  - `enable.auto.commit`: Whether offsets are committed automatically.
  - `max.poll.records`: Controls the maximum records returned in a single poll.

### Brokers and Clusters

- **Broker:** Kafka server that stores data and serves client requests. Each broker has a unique ID.
- **Cluster:** A group of brokers. Topics are distributed across brokers for scalability and fault tolerance.
- **Replication:** Each partition has one leader and zero or more followers. Leaders handle all reads/writes; followers replicate data.

### Zookeeper

- Used for metadata management, leader election, and cluster coordination.
- Kafka is moving towards KRaft mode (Kafka Raft Metadata mode), removing Zookeeper dependency.

---

## Kafka Architecture

### Indexing

- Kafka maintains two indexes per partition:
  - **Offset Index:** Maps logical offsets to physical file positions.
  - **Time Index:** Maps timestamps to offsets for time-based retrieval.
- Indexes enable fast lookups and efficient log segment management.

### Sharding and Partitioning

- **Sharding:** Achieved via partitioning. Each partition is a shard of the topic.
- **Partitioning:** Enables parallelism and scalability. The number of partitions determines the maximum consumer parallelism and throughput.

#### Best Practices
- Choose partition count based on throughput and consumer parallelism needs.
- Avoid too many partitions (can increase overhead).
- Use keys for ordering guarantees.

---

## Advanced Topics

### Kafka Streams

- Java library for building stream processing applications.
- Supports stateless and stateful operations (map, filter, join, windowing).
- Handles fault tolerance and scaling internally.

### Kafka Connect

- Framework for integrating Kafka with external systems (databases, file systems, etc.).
- **Source Connectors:** Ingest data into Kafka.
- **Sink Connectors:** Push data from Kafka to external systems.
- Supports distributed and standalone modes.

### Exactly-Once Semantics

- Ensures records are neither lost nor processed more than once.
- Requires idempotent producers and transactional writes.
- Configurations: `enable.idempotence=true`, use transactions API.

### Security

- **Authentication:** SSL, SASL/PLAIN, SASL/SCRAM, SASL/GSSAPI.
- **Authorization:** Access Control Lists (ACLs) for topics, groups, clusters.
- **Encryption:** TLS for data in transit; at-rest encryption via disk encryption.

### Monitoring and Management

- **Metrics:** Exposed via JMX.
- **Tools:** Prometheus, Grafana, Confluent Control Center.
- **Key Metrics:** Broker health, consumer lag, throughput, disk usage.

### Schema Registry

- Manages Avro/JSON/Protobuf schemas for Kafka topics.
- Enables schema evolution and compatibility checks.

### Performance Tuning

- **Producer:** Tune `batch.size`, `linger.ms`, `compression.type`.
- **Consumer:** Tune `fetch.min.bytes`, `max.poll.records`.
- **Broker:** Tune `num.network.threads`, `num.io.threads`, `log.segment.bytes`.
- **Partition Count:** More partitions = higher parallelism, but more overhead.

---

## Use Cases

- Real-time analytics (e.g., user activity tracking)
- Event sourcing and CQRS
- Log aggregation
- Data integration and ETL pipelines
- Messaging backbone for microservices

---

## Troubleshooting Q&A

**Q: Why are my consumers lagging behind?**  
A: Check consumer group health, increase consumer parallelism, tune `max.poll.records`, and ensure brokers are not overloaded.

**Q: What causes "Leader Not Available" errors?**  
A: Partition leader may be down or Zookeeper/KRaft issues. Check broker status and cluster metadata.

**Q: How do I recover from unclean leader election?**  
A: Set `unclean.leader.election.enable=false` for safety, but may cause unavailability. Investigate broker failures and restore replicas.

**Q: Why are messages not being delivered in order?**  
A: Ordering is guaranteed only within a partition. Use keys to ensure related messages go to the same partition.

**Q: How do I increase throughput?**  
A: Increase partition count, tune producer/consumer configs, use compression, and optimize hardware.

**Q: How to handle schema evolution?**  
A: Use Schema Registry and set compatibility mode (`BACKWARD`, `FORWARD`, `FULL`).

**Q: What to do if disk usage is high?**  
A: Adjust retention policies (`retention.ms`, `retention.bytes`), add more brokers/disks, or archive old data.

---

## Resources

- [Kafka Official Documentation](https://kafka.apache.org/documentation/)
- [Confluent Kafka Tutorials](https://developer.confluent.io/learn-kafka/)
- [Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/)
- [Kafka Connect Documentation](https://kafka.apache.org/documentation/#connect)
- [Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)
## Problems and Solutions List
### Content Delivery and Streaming
    1. Design Spotify/Music Streaming.
        a. https://www.geeksforgeeks.org/design-spotify-premium-system-design
        b. https://blog.algomaster.io/p/design-spotify-system-design-interview
    Key:
        Streaming Service, Search Service, Recommendations Service, Ad Service, Users Service

    2. Design Netflix/Prime Video
        a. https://medium.com/@lazygeek78/system-design-of-netflix-8a31bf9ca53f
        b. https://www.geeksforgeeks.org/system-design-netflix-a-complete-architecture
    Key:
        Open Connect Appliances, ZUUL, EVCache, Chukwa, Critical/Stateless service, file chunker, GRPC(LLD) Workflows, Cassandra/MySQL

    3. Design Youtube
        a. https://www.geeksforgeeks.org/system-design-of-youtube-a-complete-architecture
        b. https://medium.com/@lazygeek78/design-of-youtube-cf77b4cc47d9
    Key:
        Transcoding FlowDiagram, GOP/DAG scheduler, Resource Manager, Task, Video Streaming Flow, LLD Services


### Payment Systems - UPI/Paytm/PayPal

    1. In-App Payment System
        a. https://newsletter.pragmaticengineer.com/p/designing-a-payment-system
    Key: 
        HLD: Pay-In/Out Flow, Payment service, Payment executor, Payment service provider, Card schemes, Ledger, Wallet, Double-entry ledger system, Hosted payment page
        LLD: PSP integration, Reconciliation(Settlement File), Handling payment processing delays, Communication among internal services, Handling failed payments, Exact-once delivery, Consistency, Security

    2. UPI/Paytm/PayPal
        b. https://www.geeksforgeeks.org/designing-upi-system-design    
    key: 
##### 
        ⚙️ Core API Design
        1. Registration API
        POST /register
        Body: {
        phone: "9876543210",
        upi_id: "alice@upi",
        bank_account: {
            ifsc: "HDFC0001234",
            account_number: "123456789"
        }
        }
        2. Money Transfer API
        POST /transfer
        Body: {
        sender_upi: "alice@upi",
        receiver_upi: "bob@upi",
        amount: 500,
        txn_note: "Dinner",
        txn_id: "txn-uuid"
        }
        3. Collect Request API
        POST /collect
        Body: {
        requestor_upi: "merchant@upi",
        payer_upi: "user@upi",
        amount: 1000,
        expiry: "10m"
        }

        ⚙️ Database Design

        Users Table:

        - user_id (PK)
        - vpa (unique)
        - linked_bank_accounts (FK to bank_accounts)
        - mpin_hash
        - device_info
        - created_at
        - last_login
        Bank Accounts Table:

        - account_id (PK)
        - user_id (FK)
        - bank_id (FK)
        - account_number
        - ifsc_code
        - is_primary
        - balance
        Transactions Table:

        - transaction_id (PK)
        - sender_vpa
        - receiver_vpa
        - amount
        - status (initiated/processing/completed/failed)
        - timestamp
        - reference_id
        - settlement_batch_id (nullable)
        4.3. APIs Design

        Authentication APIs:

        /auth/register - Register new UPI user
        /auth/login - Authenticate user
        /auth/reset_mpin - Reset MPIN
        Transaction APIs:

        /transaction/initiate - Start new transaction
        /transaction/status - Check transaction status
        /transaction/history - Get user transaction history
        Bank APIs:

        /bank/link - Link new bank account
        /bank/accounts - List linked accounts
        /bank/set_primary - Set primary account

### Booking System
    1. BookMyShow - Ticket
        a. https://medium.com/@prithwish.samanta/online-movie-ticket-booking-platform-system-design-e-g-bookmyshow-69048440901c
        b. https://www.geeksforgeeks.org/design-bookmyshow-a-system-design-interview-question
    
    2. AirBnb/Oyo - Hotel
        a. https://medium.com/@seetharamugn/designing-a-scalable-and-resilient-hotel-reservation-system-architecture-4ede2916893b
        b. https://medium.com/@neo678/design-airbnb-hotel-booking-system-25ebf154d8de
        b. https://medium.com/nerd-for-tech/system-design-architecture-for-hotel-booking-apps-like-airbnb-oyo-6efb4f4dddd7

### Food Delivery Application
    1. Swiggy/Zomato
        a. https://www.swiftanytime.com/blog/design-food-delivery-app-mobile-system-design
        LLD Program: https://github.com/ashishps1/awesome-low-level-design/tree/main/solutions/java/src/fooddeliveryservice
####
    Capacity Estimation
    To estimate the system's capacity, let's make some assumptions based on a large-scale food delivery platform:

    Users:
        10 million daily active users (DAU).
        Each user places ~0.2 orders/day → 2 million orders/day.
    Orders:
        Average order size: 1 KB (order details, items, customer info).
        Storage for orders: 2 million orders * 1 KB = 2 GB/day.
        Assuming 1 year of data retention: 2 GB * 365 = 730 GB/year.
    Search and Read Operations:
        10 million users * 10 searches/day = 100 million searches/day.
        Peak search QPS (queries per second): 100 million / (24 * 3600) ≈ 1,157 QPS.
    Write Operations:
        Order placement: 2 million orders / (24 * 3600) ≈ 23 QPS.
        Peak order QPS (during lunch/dinner): ~100 QPS.
    Real-Time Tracking:
        2 million orders with ~10 updates/order (e.g., order placed, accepted, delivered).
        Tracking updates: 2 million * 10 / (24 * 3600) ≈ 231 QPS.
    Storage:
        User data: 10 million users * 1 KB/user = 10 GB.
        Restaurant data: 100,000 restaurants * 10 KB/restaurant (menu, details) = 1 GB.
        Total storage (including orders, images, etc.): ~1 TB initially, growing with order history.
    Network Bandwidth:
        Average API response size: 1 KB.
        Search bandwidth: 1,157 QPS * 1 KB = 1.16 MB/s.
        Peak bandwidth (with images, tracking): ~10 MB/s.

    ⚖️ 8. Scalability

    Component	                         Strategy
    API Gateway	            Horizontally scalable via load balancer
    Search & Catalog	    Elasticsearch + Redis cache
    Orders & State	        Kafka for event flow, Redis for status
    Menu Storage	        CDN for images, S3 for static assets
    Location Tracking	    Kafka → TSDB (e.g., InfluxDB, Cassandra)
    Payments	            Async callbacks, idempotent operations
    DB Sharding	            Per-region/user_id modulo for writes
    Caching	                Redis/Memcached for menu, configs

    ✅ 9. Reliability

    Use retry queues for failed order state transitions
    Circuit breakers to avoid retry storms on failures
    Outbox pattern for atomic DB-write + event-publish
    Dead letter queues to isolate unprocessable messages
    Replication & backup of critical databases
    Health checks and auto-healing on all services
    Monitoring and Alerts:

    Bottlenecks and Mitigation
    Bottleneck: Database Write Overload:
        Problem: High order volume during peak hours can overwhelm the database.
        Mitigation: Shard the database by user_id or order_id. Use Kafka to buffer writes and process them asynchronously.

    Bottleneck: Search Latency:
        Problem: High search QPS can slow down restaurant discovery.
        Mitigation: Use Elasticsearch with inverted indices for fast search. Cache popular search results in Redis.

    Bottleneck: Delivery Partner Assignment:
        Problem: Assigning delivery partners in real-time for millions of orders is compute-intensive.
        Mitigation: Use a precomputed index of available delivery partners by location. Optimize assignment with a lightweight scoring algorithm.

    Bottleneck: Payment Processing:
        Problem: Payment gateway failures can block order placement.
        Mitigation: Implement a fallback payment gateway and retry logic. Queue failed payments for asynchronous retries.

    Bottleneck: Real-Time Tracking:
        Problem: High-frequency location updates from delivery partners can overload WebSocket servers.
        Mitigation: Use a scalable WebSocket framework like Socket.IO. Aggregate updates to reduce frequency (e.g., update every 5 seconds).


### Location Ride Services:
    1. Ola/Uber
        a. https://github.com/karanpratapsingh/system-design?tab=readme-ov-file#uber
        b. https://www.geeksforgeeks.org/system-design-of-uber-app-uber-system-architecture
    
    2. Google Maps
        a. https://medium.com/@jyoti1308/designing-google-maps-d9865c3506ba
        b. https://www.geeksforgeeks.org/designing-google-maps-system-design
        c.https://mecha-mind.medium.com/system-design-google-maps-c9dddca72df5
        d. https://systemdesignschool.io/problems/google-map/solution
####
    Capacity Estimation
    Assume the platform operates in a large market with the following estimates:

    Users: 10M riders, 1M drivers.
    Daily Active Users (DAU): 1M riders, 100K drivers.
    Ride Requests: 5M rides/day (~58 rides/second average, ~580 rides/second peak).
    Location Updates: 100K drivers updating location every 5 seconds (~20K updates/second).
    Storage:
    User data: 10M users × 1KB/user = 10GB.
    Ride data: 5M rides/day × 5KB/ride × 30 days = 750GB/month.
    Historical data: 100TB over 5 years (assuming growth).
    Network: 1MB/ride for real-time updates (location, notifications) = 5TB/day.

    HLD
    +------------------+       +---------------------+       +----------------------+
    | Mobile App       | <---> | API Gateway         | <---> | Auth Service         |
    +------------------+       +---------------------+       +----------------------+
                                    |
    +---------------------+   +------------------------+   +----------------------+
    | Ride Matching Svc   |   | Trip Management Svc    |   | Payment Service      |
    +---------------------+   +------------------------+   +----------------------+
            |                        |                             |
            |                        v                             |
    +-------------------+   +-------------------------+   +--------------------+
    | Location Service  |   | Notification Service    |   | Fraud Detection    |
    +-------------------+   +-------------------------+   +--------------------+

    +----------------------+     +---------------------+
    | Analytics & Logging  |     | Admin Dashboard     |
    +----------------------+     +---------------------+

    10. Bottlenecks & Solutions

    Bottleneck	Solution
    High DB load during peaks	Caching, read replicas
    Driver matching latency	    Geospatial indexing (Redis, QuadTree)
    Surge pricing calculations	Pre-compute pricing zones
    Real-time location updates	WebSockets + edge caching


### Design E-commerce System

    1. Amazon/Flipkart
        a. https://medium.com/@vaibhavkansagara/high-level-system-design-for-amazon-1aa18f3efd15
        b. https://dzone.com/articles/scalable-ecommerce-platform-system-design
####
    System Design: E-Commerce Platform (Amazon/Flipkart)
    1. Functional Requirements

    1.1 User Management

    User registration/login (email, phone, OTP, social login)
    Profile management (addresses, payment methods, wishlist)
    1.2 Product Catalog

    Product listing (categories, filters, search)
    Product details (images, descriptions, reviews, ratings)
    1.3 Order Management

    Shopping cart (add/remove items, quantity updates)
    Checkout (COD, online payment, coupons)
    Order tracking (real-time status updates)
    1.4 Payment System

    Multiple payment options (UPI, cards, wallets, net banking)
    Refund processing (failed/cancelled orders)
    1.5 Inventory Management

    Stock updates in real-time
    Notifications for low stock
    1.6 Reviews & Ratings

    Rate products & sellers (1-5 stars with feedback)
    1.7 Notifications

    Order confirmations, shipping updates, offers (SMS, push, email)
    1.8 Seller Portal

    Seller onboarding (product listing, pricing, inventory)
    Order fulfillment (shipping, returns)
    2. Non-Functional Requirements

    2.1 Scalability

    Handle millions of users & products
    Peak traffic during sales (Big Billion Days, Prime Day)
    2.2 Low Latency

    Fast product search (<500ms)
    Smooth checkout experience
    2.3 High Availability

    99.99% uptime (minimal downtime)
    2.4 Data Consistency

    Strong consistency for inventory & orders
    2.5 Security

    PCI-DSS compliance for payments
    Encrypted user data (PII protection)
    2.6 Fault Tolerance

    Handle payment gateway failures
    Retry mechanisms for failed orders
    3. Capacity Estimation

    3.1 Traffic Estimates

    Daily Active Users (DAU): 20M
    Orders per day: 10M (~120 orders/sec peak)
    Read:Write Ratio: 20:1 (heavy reads for browsing)
    3.2 Storage Estimates

    Products: 100M × 5KB = 500GB
    Orders: 10M/day × 2KB = 20GB/day (~7TB/year)
    User Data: 200M users × 2KB = 400GB
    3.3 Bandwidth

    Per Product Page Load: ~1MB (images + data)
    Peak Traffic: 10,000 req/sec × 1MB = 10GB/sec
    4. Data Models

    4.1 User Schema

    json
    {
    "user_id": "uuid",
    "name": "string",
    "email": "string",
    "addresses": [{
        "address_id": "uuid",
        "street": "string",
        "city": "string",
        "pincode": "string"
    }],
    "payment_methods": ["upi_id", "card_id"],
    "wishlist": ["product_id1", "product_id2"]
    }
    4.2 Product Schema

    json
    {
    "product_id": "uuid",
    "name": "string",
    "category": "Electronics | Fashion",
    "price": "float",
    "seller_id": "uuid",
    "stock": "int",
    "images": ["url1", "url2"],
    "reviews": [{
        "review_id": "uuid",
        "user_id": "uuid",
        "rating": "int",
        "comment": "string"
    }]
    }
    4.3 Order Schema

    json
    {
    "order_id": "uuid",
    "user_id": "uuid",
    "items": [{
        "product_id": "uuid",
        "quantity": "int",
        "price": "float"
    }],
    "total_amount": "float",
    "status": "PLACED | SHIPPED | DELIVERED | CANCELLED",
    "payment_status": "PENDING | SUCCESS | FAILED",
    "shipping_address": "address_id",
    "created_at": "timestamp"
    }
    4.4 Inventory Schema

    json
    {
    "product_id": "uuid",
    "seller_id": "uuid",
    "stock": "int",
    "last_updated": "timestamp"
    }
    5. API Models

    5.1 Search Products

    GET /api/products/search?query=iPhone&category=Electronics  
    Response: { products: [ {...} ], pagination: {...} }  
    5.2 Add to Cart

    POST /api/cart/add  
    Request: { user_id, product_id, quantity }  
    Response: { success, cart_id }  
    5.3 Place Order

    POST /api/orders  
    Request: { user_id, cart_id, payment_method, shipping_address }  
    Response: { order_id, estimated_delivery }  
    5.4 Track Order

    GET /api/orders/{order_id}  
    Response: { status, shipping_details }  

    HLD: 

        [ Mobile/Web App ]
            |
        [ API Gateway ]
            |
    +--------------------+
    | Authentication Svc |
    +--------------------+
            |
    +-------------------------+
    | Product Catalog Service |
    +-------------------------+
            |
    +--------------------+     +--------------------+     +------------------------+
    | Search Service     |     | Cart Service       |     | Order Management Svc   |
    +--------------------+     +--------------------+     +------------------------+
                                                            |
                                                    +------------------+
                                                    | Inventory Service|
                                                    +------------------+
                                                            |
    +----------------+   +-----------------+         +--------------------+
    | Payment Svc    |   | NotificationSvc |         | Shipping/Logistics |
    +----------------+   +-----------------+         +--------------------+

    +----------------------+   +---------------------+
    | Analytics & Logging  |   | Admin Dashboard     |
    +----------------------+   +---------------------+

    ⚖️ 8. Scalability Strategies

    Component	Strategy
    Catalog	Partitioned by category ID, region
    Search	ElasticSearch with sharding + denormalized index
    Cart	Stored in Redis, expiration policy
    Orders	Write-ahead log (Kafka) + NoSQL for scale
    Payment	Idempotent retry-safe API with queues
    Media assets (images)	Stored in S3 with CDN (e.g., CloudFront)
    Cache	Product info, user sessions (Redis)
    DB Sharding	Per user_id, product_id

    ✅ 9. Reliability Techniques

    Circuit Breakers for critical services (payment, shipping)
    Idempotency Tokens for retry-safe payment/order APIs
    Eventual Consistency for inventory updates and notifications
    Kafka for event-driven updates (cart, order, review pipelines)
    Retry Queues for failed orders/notifications
    Backfill Scripts for compensations (e.g., stock rollback)
    Global and local replicas for high availability
    Blue-green deployment for zero downtime rollouts

    🧨 10. Bottlenecks & Mitigation

    Bottleneck	Solution
    Flash sale spikes	Redis queue + async inventory decrements
    Search overload	Caching + precomputed top results
    Checkout concurrency	Optimistic locking or atomic inventory API
    Payment gateway delays	Async payment verification + polling
    Large catalog indexing	Batched ingestion & background sync to ES
    Order fraud	ML anomaly detection + rule-based scoring


### Design Cloud Storage

    1. Google Drive/DropBox
        a. https://www.geeksforgeeks.org/design-dropbox-a-system-design-interview-question/
        b. https://github.com/gitgik/distributed-system-design/blob/master/designing-cloud-storage.ipynb
        c. https://www.pankajtanwar.in/blog/system-design-how-to-design-google-drive-dropbox-a-cloud-file-storage-service
    Key: 
        Presigned URL, Upload/Metadata/Sync Service, Client Chunk/Watcher, Edge Wrapper










### Design Chatting System
    1. Whatsapp
        a. https://www.geeksforgeeks.org/designing-whatsapp-messenger-system-design
        b. https://github.com/karanpratapsingh/system-design?tab=readme-ov-file#whatsapp

    2. Instagram
        a. https://www.geeksforgeeks.org/design-instagram-a-system-design-interview-question
        b. https://medium.com/@lazygeek78/system-design-series-cfa60db16c27

    3. Facebook
        a. https://www.geeksforgeeks.org/design-facebook-system-design
    
    4. Twitter
        a. https://www.geeksforgeeks.org/design-twitter-a-system-design-interview-question
        b. https://github.com/karanpratapsingh/system-design?tab=readme-ov-file#twitter


### Design Zoom

### Design Leaderboard

### Miscellenous

###

Ref:
    https://github.com/gitgik/distributed-system-design/tree/master

https://github.com/ashishps1/awesome-system-design-resources
## 🔹 Real-World App-Based System Design Problems / Pending

1. Design LRU Cache  
2. Design LFU Cache  
3. Design an ATM System: Support balance checks, withdrawals, and deposits with security and consistency.  
4. Design a Snake and Ladder Game: Build a multiplayer game with low-latency updates and fair gameplay.  
5. Design a URL Shortener (like TinyURL) Use Alex Xu *
6. Design a Distributed Cache (like Redis): Support low-latency data access with high availability and scalability.  
7. Design a Message Queue (like Kafka): Handle high-throughput message processing with fault tolerance and scalability.  
8. Design a Distributed Key-Value Store (like DynamoDB): Support high availability, consistency, and partition tolerance.  
9. Design a Web Crawler Use Alex Xu 
10. Design a Search Engine (like Google): Handle query processing, indexing, and ranking for billions of web pages.  
11. Design a Recommendation System: Create a system for personalized recommendations (e.g., Netflix, Amazon).  
12. Design Typeahead/Autocomplete: Support real-time search suggestions with personalization and low latency.  
13. Design a News Feed System: Generate personalized feeds with ranking and real-time updates (e.g., Facebook, LinkedIn).  *
14. Design Ad Aggregator  
15. Design a Parking Lot System: Manage parking spot allocation, payments, and real-time availability.  
16. Design a Content Delivery Network (CDN): Optimize content delivery with edge servers, caching, and low-latency distribution.  
17. Design a Live Streaming Service (like Twitch): Support real-time video streaming, chat, and low-latency interactions.  
18. Design Swiggy / Zomato / DoorDash  *
19. Design Paytm / Google Pay / PhonePe  *
20. Design a Leaderboard System  
21. Design Google Maps  *
22. Design Uber/Ola  *
23. Design BookMyShow / Ticketmaster  *
24. Design Airbnb / OYO  *
25. Design Amazon Order Management System / Flipkart / Paytm Mall  *
26. Design a Warehouse Management System  *
27. Design a WhatsApp-like Chat App  
28. Design Email Scheduling System  
29. Design Push Notification Service  
30. Design Real-Time Dashboard (like Grafana/Prometheus)  
31. Design Google Docs (Real-Time Editing)  
32. Design Job Recommendation Engine (like LinkedIn)  
33. Design a Rate Limiter (Token Bucket / Sliding Window)  *
34. Design CAPTCHA Verification System  
35. Design a Digital Locker (Govt. or Edu App)

### Monitoring and Analytics
36. Design a Metrics Monitoring System (like Prometheus): Collect, store, and visualize system metrics in real time.
37. Design a Logging System: Handle high-volume log collection, storage, and querying for debugging and analytics.
38. Design a Request Monitoring Service: Track API request counts per time window with scalability and low latency.[](https://www.geeksforgeeks.org/top-10-system-design-interview-questions-and-answers/)
39. Design an Analytics System (like Google Analytics): Process and visualize user behavior data for millions of events.
40. Design a Fraud Detection System: Detect and prevent fraudulent transactions in real time for payment systems.


## LLD Programming
https://github.com/ashishps1/awesome-low-level-design

## Curated List
### Social Media and Messaging Platforms
1. *** Design Twitter/X: Build a system to handle tweets, timelines, followers, and real-time updates (500M daily active users, 140-character limit).[](https://medium.com/javarevisited/top-30-system-design-interview-questions-and-problems-for-programmers-417e89eadd67)
2. *** Design Instagram: Create a system for photo/video sharing, stories, and feeds with high-resolution media and real-time interactions.
3. *** Design Facebook: Design a social network with friend connections, news feeds, groups, and event handling for billions of users.
4. *** Design WhatsApp: Build a messaging app with end-to-end encryption, group chats, and media sharing for low-latency communication.
5. *** Design a Chat Application (like Slack/Discord): Support real-time messaging, channels, and notifications with high availability.

### Content Delivery and Streaming
6. *** Design YouTube: Create a video streaming service with upload, transcoding, and playback for millions of concurrent users.[](https://dev.to/fahimulhaq/cracking-amazon-system-design-interview-top-questions-and-answer-45i1)
7. *** Design Netflix: Build a streaming platform with personalized recommendations, low-latency playback, and global content delivery.
8. *** Design Spotify: Design a music streaming service with playlists, offline mode, and low-latency audio streaming.


### E-Commerce and Payment Systems
11. *** Design Amazon: Build an e-commerce platform with product catalog, cart, checkout, and order tracking for high scalability.
12. Design an Online Bookstore: Create a system for book searches, reviews, and purchases with inventory management.
13. *** Design a Payment Gateway (like Stripe/PayPal): Handle secure transactions, refunds, and fraud detection for millions of payments.
14. *** Design a Food Delivery System (like Zomato/Swiggy): Support restaurant listings, order placement, and real-time delivery tracking.
15. Design an Auction System (like eBay): Build a system for real-time bidding, auctions, and payment processing.

### Ride-Sharing and Location-Based Systems
16. *** Design Uber: Create a ride-sharing system with driver matching, GPS-based routing, ETA calculations, and payment integration.[](https://www.geeksforgeeks.org/top-10-system-design-interview-questions-and-answers/)
17. Design a Location-Based Service (like Google Maps): Support route planning, traffic updates, and geolocation for millions of users.
18. Design a Cab Dispatch System: Optimize driver allocation, ride requests, and real-time location updates.
19. *** Design a Parking Lot System: Manage parking spot allocation, payments, and real-time availability.
20. *** Design a Logistics System (like FedEx): Handle package tracking, routing, and delivery optimization.

### File Storage and Collaboration
21. Design Dropbox: Build a file storage and sharing system with real-time sync, versioning, and access control.[](https://www.joinleland.com/library/a/20-common-system-design-interview-questions-with-sample-answers)
22. Design Google Drive: Create a cloud storage system with file sharing, collaboration, and differential sync.[](https://www.indeed.com/career-advice/interviewing/system-design-interview-questions)
23. Design a Collaborative Editor (like Google Docs): Support real-time document editing, conflict resolution, and versioning.
24. Design a File Sharing System: Handle large file uploads, downloads, and secure sharing with access controls.
25. Design an In-Memory File System: Create data structures and algorithms for a file system with low-latency operations.[](https://in.indeed.com/career-advice/interviewing/low-level-design-interview-questions)

### Search and Recommendation Systems
26. Design a Web Crawler: Build a scalable system to index web content for search engines like Google or Bing.[](https://www.coursera.org/articles/system-design-interview-questions)
27. Design a Search Engine (like Google): Handle query processing, indexing, and ranking for billions of web pages.
28. Design a Recommendation System: Create a system for personalized recommendations (e.g., Netflix, Amazon).[](https://www.coursera.org/articles/system-design-interview-questions)
29. Design Typeahead/Autocomplete: Support real-time search suggestions with personalization and low latency.[](https://medium.com/javarevisited/top-30-system-design-interview-questions-and-problems-for-programmers-417e89eadd67)
30. Design a News Feed System: Generate personalized feeds with ranking and real-time updates (e.g., Facebook, LinkedIn).

### Distributed Systems and Infrastructure
31. Design a URL Shortener (like TinyURL): Create a system for generating and redirecting short URLs with high availability.[](https://www.geeksforgeeks.org/top-10-system-design-interview-questions-and-answers/)[](https://in.indeed.com/career-advice/interviewing/system-design-interview-questions)
32. Design an API Rate Limiter: Build a system to limit API requests per user/window for platforms like Firebase or GitHub.[](https://www.educative.io/blog/system-design-interview-questions)
33. Design a Distributed Cache (like Redis): Support low-latency data access with high availability and scalability.
34. Design a Message Queue (like Kafka): Handle high-throughput message processing with fault tolerance and scalability.
35. Design a Distributed Key-Value Store (like DynamoDB): Support high availability, consistency, and partition tolerance.[](https://www.interviewbit.com/system-design-interview-questions/)


### Miscellaneous Systems
41. *** Design a Movie Ticket Booking System: Handle seat selection, payments, and real-time availability for high concurrency.[](https://in.indeed.com/career-advice/interviewing/low-level-design-interview-questions)
42. Design an ATM System: Support balance checks, withdrawals, and deposits with security and consistency.[](https://www.interviewbit.com/system-design-interview-questions/)
43. Design a Traffic Control System: Manage traffic lights, sensors, and real-time optimization for urban areas.[](https://in.indeed.com/career-advice/interviewing/low-level-design-interview-questions)
44. Design a Snake and Ladder Game: Build a multiplayer game with low-latency updates and fair gameplay.[](https://in.indeed.com/career-advice/interviewing/low-level-design-interview-questions)
45. Design a Vending Machine System: Handle inventory, payments, and dispensing with fault tolerance.

### Advanced and Niche Systems
46. Design a Distributed File System (like HDFS): Support large-scale data storage and processing with fault tolerance.
47. Design a Blockchain-Based System: Build a decentralized ledger for secure transactions and consensus.
48. Design a Notification System: Handle push notifications, emails, and SMS for millions of users with low latency.
49. Design a Job Scheduler (like Kubernetes): Manage task scheduling, resource allocation, and fault tolerance.
50. Design a Social Graph System: Model relationships and interactions for social networks with high scalability.
51. Design LeaderBoard
52. Design Webhooks Processing System
53. Design Ad Aggregrator
54. Design LRU Cache
55. Design LFU Cache

### Notes on Preparation
- FAAMNG+ Expectations in India: Interviews focus on scalability, trade-offs, and communication. Amazon emphasizes leadership principles, Google tests deep database knowledge, and Meta/Netflix prioritize real-world problem-solving.[](https://www.tryexponent.com/blog/system-design-interview-guide)
- Approach: Use a structured framework like RESHADED (Requirements, Estimation, Scope, High-level design, APIs, Data model, Evaluation, Detailed design) to break down problems systematically.[](https://dev.to/fahimulhaq/cracking-amazon-system-design-interview-top-questions-and-answer-45i1)
- Key Concepts: Master scalability (horizontal vs. vertical), load balancing, caching, database design (SQL vs. NoSQL), sharding, CAP theorem, and microservices.[](https://www.interviewbit.com/system-design-interview-questions/)[](https://www.coursera.org/articles/system-design-interview-questions)
- Practice Tips: Study real-world architectures (e.g., Uber, Netflix), use mock interviews, and draw clear diagrams. Resources like Educative’s *Grokking the System Design Interview* and Gaurav Sen’s YouTube playlist are highly recommended.[](https://www.educative.io/blog/system-design-interview-questions)[](https://www.techinterviewhandbook.org/system-design/)

### Sources
This list is compiled from recent articles and candidate experiences shared on platforms like GeeksforGeeks, Educative.io, InterviewBit, and Medium, reflecting 2024-2025 trends in India.[](https://www.geeksforgeeks.org/top-10-system-design-interview-questions-and-answers/)[](https://www.educative.io/blog/system-design-interview-questions)[](https://www.interviewbit.com/system-design-interview-questions/)

If you’d like detailed solutions or a breakdown of how to approach any specific question, let me know!

### Additional


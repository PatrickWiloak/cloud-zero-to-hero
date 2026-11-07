# IBM Cloud Developer (C1000-177) - Data, AI Services & Monitoring

## Table of Contents
- [Database Services](#database-services)
- [Watson AI Services](#watson-ai-services)
- [Data Analytics](#data-analytics)
- [Application Monitoring](#application-monitoring)
- [Logging and Observability](#logging-and-observability)
- [Performance Optimization](#performance-optimization)
- [Security Monitoring](#security-monitoring)

---

## Database Services

### IBM Cloud Databases for PostgreSQL

#### Creating a Database Instance

```bash
# Create PostgreSQL instance
ibmcloud resource service-instance-create \
  my-postgres \
  databases-for-postgresql \
  standard \
  us-south \
  -p '{
    "members_memory_allocation_mb": "4096",
    "members_disk_allocation_mb": "20480",
    "members_cpu_allocation_count": "2",
    "version": "15"
  }'

# Get connection strings
ibmcloud resource service-key-create \
  postgres-credentials \
  Manager \
  --instance-name my-postgres

# Retrieve credentials
ibmcloud resource service-key postgres-credentials --output json
```

#### Connecting to PostgreSQL

```javascript
// postgres-connection.js
const { Client } = require('pg');

const client = new Client({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  ssl: {
    rejectUnauthorized: true,
    ca: process.env.DB_CA_CERT
  }
});

async function connectDB() {
  try {
    await client.connect();
    console.log('Connected to PostgreSQL');

    // Execute query
    const result = await client.query('SELECT NOW()');
    console.log('Current time:', result.rows[0]);

    // Create table
    await client.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Insert data with parameterized query
    const insertResult = await client.query(
      'INSERT INTO users (username, email) VALUES ($1, $2) RETURNING *',
      ['john_doe', 'john@example.com']
    );
    console.log('Inserted user:', insertResult.rows[0]);

    // Query with transaction
    await performTransaction();

  } catch (err) {
    console.error('Database error:', err);
  } finally {
    await client.end();
  }
}

async function performTransaction() {
  try {
    await client.query('BEGIN');

    await client.query(
      'UPDATE users SET email = $1 WHERE username = $2',
      ['newemail@example.com', 'john_doe']
    );

    await client.query(
      'INSERT INTO audit_log (action, username) VALUES ($1, $2)',
      ['email_update', 'john_doe']
    );

    await client.query('COMMIT');
    console.log('Transaction committed');
  } catch (err) {
    await client.query('ROLLBACK');
    console.error('Transaction rolled back:', err);
  }
}

connectDB();
```

#### Connection Pooling

```javascript
// postgres-pool.js
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  ssl: {
    rejectUnauthorized: true,
    ca: process.env.DB_CA_CERT
  },
  max: 20, // Maximum connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

pool.on('error', (err, client) => {
  console.error('Unexpected error on idle client', err);
});

async function queryDatabase(text, params) {
  const start = Date.now();
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: res.rowCount });
    return res;
  } catch (err) {
    console.error('Query error:', err);
    throw err;
  }
}

// Usage
async function getUsers() {
  const result = await queryDatabase(
    'SELECT * FROM users WHERE created_at > $1',
    [new Date(Date.now() - 86400000)] // Last 24 hours
  );
  return result.rows;
}

module.exports = { pool, queryDatabase };
```

### IBM Cloudant (NoSQL)

#### Creating Cloudant Instance

```bash
# Create Cloudant instance
ibmcloud resource service-instance-create \
  my-cloudant \
  cloudantnosqldb \
  standard \
  us-south

# Create service credentials
ibmcloud resource service-key-create \
  cloudant-credentials \
  Manager \
  --instance-name my-cloudant
```

#### Working with Cloudant

```javascript
// cloudant-client.js
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const authenticator = new IamAuthenticator({
  apikey: process.env.CLOUDANT_API_KEY
});

const client = CloudantV1.newInstance({
  authenticator,
  serviceUrl: process.env.CLOUDANT_URL
});

// Create database
async function createDatabase(dbName) {
  try {
    await client.putDatabase({ db: dbName });
    console.log(`Database ${dbName} created`);
  } catch (err) {
    if (err.status === 412) {
      console.log('Database already exists');
    } else {
      throw err;
    }
  }
}

// Insert document
async function insertDocument(dbName, document) {
  try {
    const response = await client.postDocument({
      db: dbName,
      document
    });
    console.log('Document created:', response.result);
    return response.result;
  } catch (err) {
    console.error('Error inserting document:', err);
    throw err;
  }
}

// Query documents
async function queryDocuments(dbName, selector) {
  try {
    const response = await client.postFind({
      db: dbName,
      selector,
      limit: 100
    });
    return response.result.docs;
  } catch (err) {
    console.error('Error querying documents:', err);
    throw err;
  }
}

// Create index
async function createIndex(dbName, indexDef) {
  try {
    await client.postIndex({
      db: dbName,
      index: indexDef
    });
    console.log('Index created');
  } catch (err) {
    console.error('Error creating index:', err);
    throw err;
  }
}

// Usage example
async function run() {
  const dbName = 'orders';

  await createDatabase(dbName);

  // Create index for efficient queries
  await createIndex(dbName, {
    fields: ['customerId', 'createdAt']
  });

  // Insert document
  const order = {
    customerId: 'cust-123',
    items: [
      { productId: 'prod-1', quantity: 2, price: 29.99 },
      { productId: 'prod-2', quantity: 1, price: 49.99 }
    ],
    totalAmount: 109.97,
    status: 'pending',
    createdAt: new Date().toISOString()
  };

  const result = await insertDocument(dbName, order);

  // Query documents
  const recentOrders = await queryDocuments(dbName, {
    customerId: 'cust-123',
    createdAt: { $gt: '2024-01-01' }
  });

  console.log('Recent orders:', recentOrders);
}

run().catch(console.error);
```

#### Cloudant Views

```javascript
// Create design document with views
async function createViews(dbName) {
  const designDoc = {
    _id: '_design/orders',
    views: {
      by_customer: {
        map: function(doc) {
          if (doc.customerId) {
            emit(doc.customerId, {
              orderId: doc._id,
              totalAmount: doc.totalAmount,
              status: doc.status
            });
          }
        }.toString(),
        reduce: '_sum'
      },
      by_status: {
        map: function(doc) {
          if (doc.status) {
            emit(doc.status, 1);
          }
        }.toString(),
        reduce: '_count'
      }
    }
  };

  await client.putDesignDocument({
    db: dbName,
    designDocument: designDoc,
    ddoc: 'orders'
  });

  console.log('Views created');
}

// Query view
async function queryView(dbName, ddoc, viewName, options) {
  const response = await client.postView({
    db: dbName,
    ddoc,
    view: viewName,
    ...options
  });
  return response.result.rows;
}

// Usage
const customerOrders = await queryView('orders', 'orders', 'by_customer', {
  key: 'cust-123',
  includeDocs: true
});
```

### IBM Databases for MongoDB

```javascript
// mongodb-connection.js
const { MongoClient } = require('mongodb');

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri, {
  useUnifiedTopology: true,
  tls: true,
  tlsCAFile: process.env.MONGODB_CA_CERT
});

async function connectMongoDB() {
  try {
    await client.connect();
    console.log('Connected to MongoDB');

    const db = client.db('myapp');
    const collection = db.collection('users');

    // Insert document
    const result = await collection.insertOne({
      username: 'john_doe',
      email: 'john@example.com',
      profile: {
        firstName: 'John',
        lastName: 'Doe',
        age: 30
      },
      tags: ['developer', 'nodejs'],
      createdAt: new Date()
    });

    console.log('Inserted document:', result.insertedId);

    // Query documents
    const users = await collection.find({
      'profile.age': { $gte: 25 }
    }).toArray();

    console.log('Users:', users);

    // Update document
    await collection.updateOne(
      { username: 'john_doe' },
      {
        $set: { 'profile.age': 31 },
        $push: { tags: 'mongodb' }
      }
    );

    // Aggregation
    const stats = await collection.aggregate([
      { $match: { 'profile.age': { $gte: 25 } } },
      {
        $group: {
          _id: null,
          avgAge: { $avg: '$profile.age' },
          count: { $sum: 1 }
        }
      }
    ]).toArray();

    console.log('Stats:', stats);

  } finally {
    await client.close();
  }
}

connectMongoDB().catch(console.error);
```

### IBM Databases for Redis

```javascript
// redis-connection.js
const redis = require('redis');

const client = redis.createClient({
  socket: {
    host: process.env.REDIS_HOST,
    port: process.env.REDIS_PORT,
    tls: true,
    ca: process.env.REDIS_CA_CERT
  },
  password: process.env.REDIS_PASSWORD
});

client.on('error', (err) => console.error('Redis error:', err));
client.on('connect', () => console.log('Connected to Redis'));

async function useRedis() {
  await client.connect();

  // String operations
  await client.set('user:1000', JSON.stringify({
    id: 1000,
    username: 'john_doe',
    email: 'john@example.com'
  }));

  // Set expiration
  await client.expire('user:1000', 3600); // 1 hour

  // Get value
  const userData = await client.get('user:1000');
  console.log('User data:', JSON.parse(userData));

  // Hash operations
  await client.hSet('user:1001', {
    username: 'jane_doe',
    email: 'jane@example.com',
    age: '28'
  });

  const username = await client.hGet('user:1001', 'username');
  console.log('Username:', username);

  // List operations
  await client.lPush('notifications:user:1000', 'New message');
  await client.lPush('notifications:user:1000', 'Friend request');

  const notifications = await client.lRange('notifications:user:1000', 0, -1);
  console.log('Notifications:', notifications);

  // Set operations
  await client.sAdd('tags:post:1', ['nodejs', 'javascript', 'tutorial']);
  const tags = await client.sMembers('tags:post:1');
  console.log('Tags:', tags);

  // Sorted set operations
  await client.zAdd('leaderboard', [
    { score: 100, value: 'player1' },
    { score: 85, value: 'player2' },
    { score: 92, value: 'player3' }
  ]);

  const topPlayers = await client.zRange('leaderboard', 0, 2, {
    REV: true,
    WITHSCORES: true
  });
  console.log('Top players:', topPlayers);

  await client.disconnect();
}

useRedis().catch(console.error);
```

---

## Watson AI Services

### Watson Assistant

```javascript
// watson-assistant.js
const AssistantV2 = require('ibm-watson/assistant/v2');
const { IamAuthenticator } = require('ibm-watson/auth');

const assistant = new AssistantV2({
  version: '2023-06-15',
  authenticator: new IamAuthenticator({
    apikey: process.env.WATSON_ASSISTANT_API_KEY
  }),
  serviceUrl: process.env.WATSON_ASSISTANT_URL
});

const assistantId = process.env.WATSON_ASSISTANT_ID;

// Create session
async function createSession() {
  try {
    const response = await assistant.createSession({
      assistantId
    });
    return response.result.session_id;
  } catch (err) {
    console.error('Error creating session:', err);
    throw err;
  }
}

// Send message
async function sendMessage(sessionId, messageText) {
  try {
    const response = await assistant.message({
      assistantId,
      sessionId,
      input: {
        message_type: 'text',
        text: messageText
      }
    });

    return response.result;
  } catch (err) {
    console.error('Error sending message:', err);
    throw err;
  }
}

// Chatbot conversation
async function runConversation() {
  const sessionId = await createSession();

  try {
    // First message
    let result = await sendMessage(sessionId, 'Hello');
    console.log('Assistant:', result.output.generic[0].text);

    // Follow-up message
    result = await sendMessage(sessionId, 'What are your business hours?');
    console.log('Assistant:', result.output.generic[0].text);

    // Extract entities and intents
    console.log('Intents:', result.output.intents);
    console.log('Entities:', result.output.entities);

  } finally {
    // Delete session
    await assistant.deleteSession({
      assistantId,
      sessionId
    });
  }
}

runConversation().catch(console.error);
```

### Watson Natural Language Understanding

```javascript
// watson-nlu.js
const NaturalLanguageUnderstandingV1 = require('ibm-watson/natural-language-understanding/v1');
const { IamAuthenticator } = require('ibm-watson/auth');

const nlu = new NaturalLanguageUnderstandingV1({
  version: '2022-04-07',
  authenticator: new IamAuthenticator({
    apikey: process.env.WATSON_NLU_API_KEY
  }),
  serviceUrl: process.env.WATSON_NLU_URL
});

async function analyzeText(text) {
  try {
    const response = await nlu.analyze({
      text,
      features: {
        entities: {
          emotion: true,
          sentiment: true,
          limit: 10
        },
        keywords: {
          emotion: true,
          sentiment: true,
          limit: 10
        },
        categories: {
          limit: 5
        },
        concepts: {
          limit: 5
        },
        emotion: {
          targets: ['IBM Cloud', 'Watson']
        },
        sentiment: {
          targets: ['IBM Cloud', 'Watson']
        }
      }
    });

    return response.result;
  } catch (err) {
    console.error('Error analyzing text:', err);
    throw err;
  }
}

// Usage
const text = `
  IBM Cloud offers a comprehensive suite of AI services including Watson.
  The platform provides excellent scalability and security features.
  Developers love the ease of integration and robust API documentation.
`;

analyzeText(text).then(result => {
  console.log('Sentiment:', JSON.stringify(result.sentiment, null, 2));
  console.log('Entities:', JSON.stringify(result.entities, null, 2));
  console.log('Keywords:', JSON.stringify(result.keywords, null, 2));
  console.log('Categories:', JSON.stringify(result.categories, null, 2));
}).catch(console.error);
```

### Watson Language Translator

```javascript
// watson-translator.js
const LanguageTranslatorV3 = require('ibm-watson/language-translator/v3');
const { IamAuthenticator } = require('ibm-watson/auth');

const translator = new LanguageTranslatorV3({
  version: '2018-05-01',
  authenticator: new IamAuthenticator({
    apikey: process.env.WATSON_TRANSLATOR_API_KEY
  }),
  serviceUrl: process.env.WATSON_TRANSLATOR_URL
});

async function translateText(text, source, target) {
  try {
    const response = await translator.translate({
      text: [text],
      source,
      target
    });
    return response.result.translations[0].translation;
  } catch (err) {
    console.error('Error translating text:', err);
    throw err;
  }
}

async function identifyLanguage(text) {
  try {
    const response = await translator.identify({ text });
    return response.result.languages;
  } catch (err) {
    console.error('Error identifying language:', err);
    throw err;
  }
}

// Usage
async function translate() {
  const text = 'Hello, how are you?';

  // Identify language
  const languages = await identifyLanguage(text);
  console.log('Detected languages:', languages);

  // Translate to Spanish
  const spanish = await translateText(text, 'en', 'es');
  console.log('Spanish:', spanish);

  // Translate to French
  const french = await translateText(text, 'en', 'fr');
  console.log('French:', french);

  // Translate to German
  const german = await translateText(text, 'en', 'de');
  console.log('German:', german);
}

translate().catch(console.error);
```

### Watson Speech to Text

```javascript
// watson-stt.js
const SpeechToTextV1 = require('ibm-watson/speech-to-text/v1');
const { IamAuthenticator } = require('ibm-watson/auth');
const fs = require('fs');

const speechToText = new SpeechToTextV1({
  authenticator: new IamAuthenticator({
    apikey: process.env.WATSON_STT_API_KEY
  }),
  serviceUrl: process.env.WATSON_STT_URL
});

async function transcribeAudio(audioFile) {
  try {
    const params = {
      audio: fs.createReadStream(audioFile),
      contentType: 'audio/mp3',
      model: 'en-US_BroadbandModel',
      timestamps: true,
      wordAlternativesThreshold: 0.9,
      keywords: ['IBM', 'Cloud', 'Watson'],
      keywordsThreshold: 0.5
    };

    const response = await speechToText.recognize(params);
    return response.result;
  } catch (err) {
    console.error('Error transcribing audio:', err);
    throw err;
  }
}

// WebSocket streaming
function transcribeStream(audioStream) {
  const recognizeStream = speechToText.recognizeUsingWebSocket({
    contentType: 'audio/l16; rate=44100',
    interimResults: true
  });

  recognizeStream.on('data', (event) => {
    if (event.results[0].final) {
      console.log('Final transcript:', event.results[0].alternatives[0].transcript);
    } else {
      console.log('Interim transcript:', event.results[0].alternatives[0].transcript);
    }
  });

  recognizeStream.on('error', (err) => {
    console.error('Stream error:', err);
  });

  audioStream.pipe(recognizeStream);
}
```

### Watson Text to Speech

```javascript
// watson-tts.js
const TextToSpeechV1 = require('ibm-watson/text-to-speech/v1');
const { IamAuthenticator } = require('ibm-watson/auth');
const fs = require('fs');

const textToSpeech = new TextToSpeechV1({
  authenticator: new IamAuthenticator({
    apikey: process.env.WATSON_TTS_API_KEY
  }),
  serviceUrl: process.env.WATSON_TTS_URL
});

async function synthesizeSpeech(text, outputFile) {
  try {
    const params = {
      text,
      voice: 'en-US_AllisonV3Voice',
      accept: 'audio/mp3'
    };

    const response = await textToSpeech.synthesize(params);
    const audio = await textToSpeech.repairWavHeaderStream(response.result);

    audio.pipe(fs.createWriteStream(outputFile));

    audio.on('finish', () => {
      console.log(`Audio written to ${outputFile}`);
    });
  } catch (err) {
    console.error('Error synthesizing speech:', err);
    throw err;
  }
}

// SSML support
async function synthesizeWithSSML(outputFile) {
  const ssml = `
    <speak>
      Hello! <break time="1s"/>
      Welcome to <emphasis level="strong">IBM Cloud</emphasis>.
      <prosody rate="slow">This text is spoken slowly.</prosody>
      <prosody pitch="high">This text has a higher pitch.</prosody>
    </speak>
  `;

  const params = {
    text: ssml,
    voice: 'en-US_AllisonV3Voice',
    accept: 'audio/mp3'
  };

  const response = await textToSpeech.synthesize(params);
  const audio = await textToSpeech.repairWavHeaderStream(response.result);
  audio.pipe(fs.createWriteStream(outputFile));
}
```

### Watson Visual Recognition (Replaced by Watson Studio)

```javascript
// watson-visual.js
const VisualRecognitionV4 = require('ibm-watson/visual-recognition/v4');
const { IamAuthenticator } = require('ibm-watson/auth');
const fs = require('fs');

const visualRecognition = new VisualRecognitionV4({
  version: '2021-04-01',
  authenticator: new IamAuthenticator({
    apikey: process.env.WATSON_VR_API_KEY
  }),
  serviceUrl: process.env.WATSON_VR_URL
});

async function analyzeImage(imagePath, collectionId) {
  try {
    const params = {
      collectionIds: [collectionId],
      features: ['objects'],
      imagesFile: [
        {
          data: fs.createReadStream(imagePath),
          contentType: 'image/jpeg'
        }
      ]
    };

    const response = await visualRecognition.analyze(params);
    return response.result;
  } catch (err) {
    console.error('Error analyzing image:', err);
    throw err;
  }
}
```

---

## Data Analytics

### IBM Cloud SQL Query

```bash
# Create SQL Query instance
ibmcloud resource service-instance-create \
  my-sql-query \
  sql-query \
  standard \
  us-south

# Query data in Cloud Object Storage
ibmcloud sql query \
  "SELECT * FROM cos://us-south/my-bucket/data.csv STORED AS CSV" \
  --output cos://us-south/my-bucket/results/
```

### IBM Db2 Warehouse

```javascript
// db2-connection.js
const ibmdb = require('ibm_db');

const connStr = `
  DATABASE=${process.env.DB2_DATABASE};
  HOSTNAME=${process.env.DB2_HOSTNAME};
  PORT=${process.env.DB2_PORT};
  PROTOCOL=TCPIP;
  UID=${process.env.DB2_UID};
  PWD=${process.env.DB2_PASSWORD};
  Security=SSL;
`;

async function queryDb2() {
  try {
    const conn = await ibmdb.open(connStr);

    // Execute query
    const result = await conn.query('SELECT * FROM SALES WHERE AMOUNT > 1000');
    console.log('Results:', result);

    // Prepared statement
    const stmt = await conn.prepare('INSERT INTO SALES (ID, AMOUNT) VALUES (?, ?)');
    await stmt.execute([123, 1500]);

    // Close connection
    await conn.close();
  } catch (err) {
    console.error('Db2 error:', err);
  }
}

queryDb2();
```

---

## Application Monitoring

### IBM Cloud Monitoring (Sysdig)

#### Setting Up Monitoring

```bash
# Create monitoring instance
ibmcloud resource service-instance-create \
  my-monitoring \
  sysdig-monitor \
  graduated-tier \
  us-south

# Get access key
ibmcloud resource service-key-create \
  monitoring-key \
  Manager \
  --instance-name my-monitoring

# Install Sysdig agent on Kubernetes
kubectl create namespace ibm-observe
kubectl create secret generic sysdig-agent \
  --from-literal=access-key=$SYSDIG_ACCESS_KEY \
  --namespace ibm-observe

kubectl apply -f https://ibm.biz/sysdig-agent-yaml -n ibm-observe
```

#### Custom Metrics

```javascript
// sysdig-metrics.js
const StatsD = require('node-statsd');

const statsd = new StatsD({
  host: 'localhost',
  port: 8125,
  prefix: 'myapp.'
});

// Counter
statsd.increment('requests.total');
statsd.increment('orders.created');

// Gauge
statsd.gauge('users.active', 150);
statsd.gauge('memory.usage', process.memoryUsage().heapUsed);

// Timing
statsd.timing('api.response_time', 250);

// Histogram
statsd.histogram('order.value', 99.99);

// Set
statsd.set('unique.visitors', 'user-123');

// Custom metrics
function recordMetrics() {
  const metrics = {
    cpu: process.cpuUsage(),
    memory: process.memoryUsage(),
    uptime: process.uptime()
  };

  statsd.gauge('cpu.user', metrics.cpu.user);
  statsd.gauge('cpu.system', metrics.cpu.system);
  statsd.gauge('memory.heap_used', metrics.memory.heapUsed);
  statsd.gauge('memory.heap_total', metrics.memory.heapTotal);
  statsd.gauge('uptime.seconds', metrics.uptime);
}

// Record metrics every 10 seconds
setInterval(recordMetrics, 10000);
```

#### Prometheus Integration

```javascript
// prometheus-metrics.js
const prometheus = require('prom-client');
const express = require('express');

const app = express();

// Create a Registry
const register = new prometheus.Registry();

// Add default metrics
prometheus.collectDefaultMetrics({ register });

// Custom counter
const httpRequestsTotal = new prometheus.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status']
});
register.registerMetric(httpRequestsTotal);

// Custom histogram
const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
});
register.registerMetric(httpRequestDuration);

// Custom gauge
const activeConnections = new prometheus.Gauge({
  name: 'active_connections',
  help: 'Number of active connections'
});
register.registerMetric(activeConnections);

// Middleware to track metrics
app.use((req, res, next) => {
  const start = Date.now();
  activeConnections.inc();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestsTotal.inc({
      method: req.method,
      route: req.route?.path || req.path,
      status: res.statusCode
    });
    httpRequestDuration.observe(
      {
        method: req.method,
        route: req.route?.path || req.path,
        status: res.statusCode
      },
      duration
    );
    activeConnections.dec();
  });

  next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(3000);
```

### IBM Cloud Activity Tracker

```bash
# Create Activity Tracker instance
ibmcloud resource service-instance-create \
  my-activity-tracker \
  logdnaat \
  7-day \
  us-south

# Configure routing
ibmcloud atracker route create \
  --name my-route \
  --target-id $TARGET_ID \
  --locations us-south

# View events
ibmcloud atracker event list \
  --from "2024-01-01T00:00:00Z" \
  --to "2024-01-31T23:59:59Z"
```

---

## Logging and Observability

### IBM Log Analysis (LogDNA)

> **Retired service:** IBM Log Analysis (LogDNA) and IBM Cloud Activity Tracker are retired. IBM Cloud Logs provides replacement functions for both (per [IBM's Cloud Logs announcement](https://www.ibm.com/new/product-blog/ibm-cloud-logs-observability)). Read the Log Analysis material below as the legacy model and map it to IBM Cloud Logs.

```bash
# Create Log Analysis instance
ibmcloud resource service-instance-create \
  my-log-analysis \
  logdna \
  7-day \
  us-south

# Configure Kubernetes logging
kubectl create namespace ibm-observe
kubectl create secret generic logdna-agent-key \
  --from-literal=logdna-ingestion-key=$LOGDNA_KEY \
  --namespace ibm-observe

kubectl apply -f https://assets.us-south.logging.cloud.ibm.com/clients/logdna-agent-ds.yaml
```

#### Structured Logging

```javascript
// winston-logger.js
const winston = require('winston');
const { LogDNA } = require('logdna-winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'my-app',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new LogDNA({
      key: process.env.LOGDNA_KEY,
      hostname: process.env.HOSTNAME,
      app: 'my-app',
      env: process.env.NODE_ENV
    })
  ]
});

// Usage
logger.info('Application started', {
  port: 3000,
  version: '1.0.0'
});

logger.warn('High memory usage detected', {
  heapUsed: process.memoryUsage().heapUsed,
  threshold: 500000000
});

logger.error('Database connection failed', {
  error: new Error('Connection timeout'),
  database: 'postgresql',
  host: 'db.example.com'
});

// Request logging middleware
function requestLogger(req, res, next) {
  const start = Date.now();

  res.on('finish', () => {
    logger.info('HTTP request', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: Date.now() - start,
      userAgent: req.get('user-agent'),
      ip: req.ip
    });
  });

  next();
}

module.exports = { logger, requestLogger };
```

### Distributed Tracing

```javascript
// opentelemetry-tracing.js
const opentelemetry = require('@opentelemetry/api');
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');

// Create provider
const provider = new NodeTracerProvider();

// Configure Jaeger exporter
const exporter = new JaegerExporter({
  endpoint: process.env.JAEGER_ENDPOINT,
  serviceName: 'my-app'
});

provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

// Register instrumentations
registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation()
  ]
});

// Get tracer
const tracer = opentelemetry.trace.getTracer('my-app');

// Create custom span
async function processOrder(orderId) {
  const span = tracer.startSpan('processOrder');
  span.setAttribute('order.id', orderId);

  try {
    // Simulate processing
    await validateOrder(orderId);
    await chargePayment(orderId);
    await shipOrder(orderId);

    span.setStatus({ code: opentelemetry.SpanStatusCode.OK });
  } catch (err) {
    span.setStatus({
      code: opentelemetry.SpanStatusCode.ERROR,
      message: err.message
    });
    span.recordException(err);
    throw err;
  } finally {
    span.end();
  }
}

async function validateOrder(orderId) {
  const span = tracer.startSpan('validateOrder', {
    parent: opentelemetry.trace.getActiveSpan()
  });

  try {
    // Validation logic
    span.addEvent('Order validated');
  } finally {
    span.end();
  }
}
```

---

## Performance Optimization

### Caching Strategies

```javascript
// redis-cache.js
const redis = require('redis');

const cache = redis.createClient({
  socket: {
    host: process.env.REDIS_HOST,
    port: process.env.REDIS_PORT
  }
});

await cache.connect();

// Cache middleware
function cacheMiddleware(duration) {
  return async (req, res, next) => {
    const key = `cache:${req.originalUrl}`;

    try {
      const cachedData = await cache.get(key);

      if (cachedData) {
        return res.json(JSON.parse(cachedData));
      }

      res.originalJson = res.json;
      res.json = async (data) => {
        await cache.setEx(key, duration, JSON.stringify(data));
        res.originalJson(data);
      };

      next();
    } catch (err) {
      console.error('Cache error:', err);
      next();
    }
  };
}

// Usage
app.get('/api/products', cacheMiddleware(300), async (req, res) => {
  const products = await getProducts();
  res.json(products);
});
```

### Connection Pooling

```javascript
// connection-pool.js
const { Pool } = require('pg');
const redis = require('redis');

// PostgreSQL pool
const pgPool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

// Redis connection pool
const redisPool = [];
const poolSize = 10;

for (let i = 0; i < poolSize; i++) {
  const client = redis.createClient({
    socket: {
      host: process.env.REDIS_HOST,
      port: process.env.REDIS_PORT
    }
  });
  await client.connect();
  redisPool.push(client);
}

function getRedisClient() {
  return redisPool[Math.floor(Math.random() * poolSize)];
}

module.exports = { pgPool, getRedisClient };
```

---

## Security Monitoring

### Security Advisor

```bash
# Get security findings
ibmcloud security-advisor findings list \
  --account-id $ACCOUNT_ID

# Create custom finding
ibmcloud security-advisor finding create \
  --account-id $ACCOUNT_ID \
  --provider-id custom-security \
  --finding-id suspicious-activity-001 \
  --severity HIGH \
  --certainty HIGH
```

### Vulnerability Scanning

```bash
# Scan container image
ibmcloud cr vulnerability-assessment us.icr.io/mynamespace/myapp:latest

# View vulnerability report
ibmcloud cr vulnerability-assessment us.icr.io/mynamespace/myapp:latest --output json

# Set exemption policy
ibmcloud cr exemption-add \
  --scope us.icr.io/mynamespace/myapp \
  --issue-id CVE-2021-12345 \
  --reason "False positive - already patched"
```

### Exam Tips

1. **Databases**
   - Know when to use SQL vs NoSQL
   - Understand connection pooling
   - Practice with PostgreSQL, Cloudant, MongoDB, Redis
   - Study backup and recovery procedures

2. **Watson AI**
   - Master Watson Assistant conversation flows
   - Understand NLU capabilities
   - Practice with Speech-to-Text and Text-to-Speech
   - Know Language Translator use cases

3. **Monitoring**
   - Understand Sysdig metrics and alerts
   - Know Prometheus/Grafana integration
   - Study Activity Tracker event types
   - Practice custom metrics creation

4. **Logging**
   - Master structured logging with Winston
   - Understand LogDNA querying
   - Know distributed tracing concepts
   - Practice with OpenTelemetry

5. **Performance**
   - Understand caching strategies
   - Know connection pooling best practices
   - Study CDN usage
   - Practice load testing

### Common Scenarios

**Scenario 1**: Implement caching for high-traffic API
```javascript
// Use Redis for caching with appropriate TTL
// Implement cache-aside pattern
// Monitor cache hit ratio
```

**Scenario 2**: Set up monitoring for microservices
```javascript
// Deploy Sysdig agent to Kubernetes
// Configure Prometheus metrics
// Set up distributed tracing
// Create dashboards and alerts
```

**Scenario 3**: Integrate Watson AI into application
```javascript
// Use Watson Assistant for chatbot
// Implement NLU for sentiment analysis
// Add Language Translator for i18n
// Monitor API usage and performance
```

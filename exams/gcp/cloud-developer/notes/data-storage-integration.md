# Data Storage and Integration - GCP Professional Cloud Developer

## Overview

Integrating applications with GCP data services, messaging systems, and implementing data access patterns for cloud-native applications. This guide covers production-ready patterns for Cloud Storage, Cloud SQL, Cloud Spanner, Firestore, Bigtable, Memorystore, and Pub/Sub integration.

## Cloud Storage for Developers

### Client Library Integration

**Python Client Library**:
```python
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
import os
from datetime import timedelta

class CloudStorageClient:
    def __init__(self, project_id=None):
        """Initialize Cloud Storage client with optional project ID"""
        self.client = storage.Client(project=project_id)

    def upload_file(self, bucket_name, source_file_name, destination_blob_name):
        """Upload file to bucket with error handling"""
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)

            # Upload with metadata
            blob.metadata = {
                'uploaded_by': 'app-service',
                'original_name': os.path.basename(source_file_name)
            }
            blob.upload_from_filename(source_file_name)

            print(f"File {source_file_name} uploaded to {destination_blob_name}")
            return blob.public_url
        except GoogleCloudError as e:
            print(f"Error uploading file: {e}")
            raise

    def upload_from_memory(self, bucket_name, data, destination_blob_name, content_type='application/octet-stream'):
        """Upload data from memory"""
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(data, content_type=content_type)
        return blob.public_url

    def download_file(self, bucket_name, source_blob_name, destination_file_name):
        """Download file from bucket"""
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
            print(f"Downloaded {source_blob_name} to {destination_file_name}")
        except GoogleCloudError as e:
            print(f"Error downloading file: {e}")
            raise

    def download_to_memory(self, bucket_name, source_blob_name):
        """Download file contents to memory"""
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        return blob.download_as_bytes()

    def list_blobs(self, bucket_name, prefix=None):
        """List all blobs in bucket with optional prefix filter"""
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    def delete_blob(self, bucket_name, blob_name):
        """Delete a blob from bucket"""
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        print(f"Blob {blob_name} deleted")
```

**Node.js Client Library**:
```javascript
const {Storage} = require('@google-cloud/storage');

class CloudStorageClient {
    constructor(projectId) {
        this.storage = new Storage({projectId});
    }

    async uploadFile(bucketName, sourceFileName, destinationBlobName) {
        try {
            const options = {
                destination: destinationBlobName,
                metadata: {
                    metadata: {
                        uploadedBy: 'app-service',
                        originalName: sourceFileName
                    }
                }
            };

            await this.storage.bucket(bucketName).upload(sourceFileName, options);
            console.log(`${sourceFileName} uploaded to ${destinationBlobName}`);
        } catch (error) {
            console.error('Error uploading file:', error);
            throw error;
        }
    }

    async uploadFromMemory(bucketName, data, destinationBlobName, contentType = 'application/octet-stream') {
        const bucket = this.storage.bucket(bucketName);
        const file = bucket.file(destinationBlobName);

        await file.save(data, {
            contentType: contentType,
            metadata: {
                cacheControl: 'public, max-age=31536000'
            }
        });

        return `gs://${bucketName}/${destinationBlobName}`;
    }

    async downloadFile(bucketName, sourceBlobName, destinationFileName) {
        const options = {
            destination: destinationFileName
        };

        await this.storage.bucket(bucketName).file(sourceBlobName).download(options);
        console.log(`Downloaded ${sourceBlobName} to ${destinationFileName}`);
    }

    async downloadToMemory(bucketName, sourceBlobName) {
        const contents = await this.storage
            .bucket(bucketName)
            .file(sourceBlobName)
            .download();
        return contents[0];
    }

    async listFiles(bucketName, prefix = null) {
        const options = prefix ? {prefix} : {};
        const [files] = await this.storage.bucket(bucketName).getFiles(options);
        return files.map(file => file.name);
    }

    async deleteFile(bucketName, fileName) {
        await this.storage.bucket(bucketName).file(fileName).delete();
        console.log(`File ${fileName} deleted`);
    }
}

module.exports = CloudStorageClient;
```

**Go Client Library**:
```go
package storage

import (
    "context"
    "fmt"
    "io"
    "time"

    "cloud.google.com/go/storage"
    "google.golang.org/api/iterator"
)

type CloudStorageClient struct {
    client *storage.Client
    ctx    context.Context
}

func NewCloudStorageClient(ctx context.Context) (*CloudStorageClient, error) {
    client, err := storage.NewClient(ctx)
    if err != nil {
        return nil, fmt.Errorf("failed to create client: %v", err)
    }

    return &CloudStorageClient{
        client: client,
        ctx:    ctx,
    }, nil
}

func (c *CloudStorageClient) UploadFile(bucketName, objectName string, data []byte) error {
    ctx, cancel := context.WithTimeout(c.ctx, time.Second*50)
    defer cancel()

    wc := c.client.Bucket(bucketName).Object(objectName).NewWriter(ctx)
    wc.ContentType = "application/octet-stream"
    wc.Metadata = map[string]string{
        "uploaded_by": "app-service",
    }

    if _, err := wc.Write(data); err != nil {
        return fmt.Errorf("failed to write: %v", err)
    }

    if err := wc.Close(); err != nil {
        return fmt.Errorf("failed to close: %v", err)
    }

    return nil
}

func (c *CloudStorageClient) DownloadFile(bucketName, objectName string) ([]byte, error) {
    ctx, cancel := context.WithTimeout(c.ctx, time.Second*50)
    defer cancel()

    rc, err := c.client.Bucket(bucketName).Object(objectName).NewReader(ctx)
    if err != nil {
        return nil, fmt.Errorf("failed to read object: %v", err)
    }
    defer rc.Close()

    data, err := io.ReadAll(rc)
    if err != nil {
        return nil, fmt.Errorf("failed to read data: %v", err)
    }

    return data, nil
}

func (c *CloudStorageClient) ListObjects(bucketName, prefix string) ([]string, error) {
    ctx, cancel := context.WithTimeout(c.ctx, time.Second*30)
    defer cancel()

    var names []string
    it := c.client.Bucket(bucketName).Objects(ctx, &storage.Query{Prefix: prefix})

    for {
        attrs, err := it.Next()
        if err == iterator.Done {
            break
        }
        if err != nil {
            return nil, fmt.Errorf("failed to iterate: %v", err)
        }
        names = append(names, attrs.Name)
    }

    return names, nil
}

func (c *CloudStorageClient) DeleteObject(bucketName, objectName string) error {
    ctx, cancel := context.WithTimeout(c.ctx, time.Second*10)
    defer cancel()

    if err := c.client.Bucket(bucketName).Object(objectName).Delete(ctx); err != nil {
        return fmt.Errorf("failed to delete object: %v", err)
    }

    return nil
}

func (c *CloudStorageClient) Close() error {
    return c.client.Close()
}
```

### Signed URLs for Temporary Access

**Signed URL Generation (Python)**:
```python
from google.cloud import storage
from datetime import datetime, timedelta

def generate_signed_url(bucket_name, blob_name, expiration_minutes=60, method='GET'):
    """Generate signed URL for temporary access"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Generate signed URL valid for specified minutes
    url = blob.generate_signed_url(
        version='v4',
        expiration=timedelta(minutes=expiration_minutes),
        method=method,
        # Optional: specify content type for uploads
        content_type='application/octet-stream' if method == 'PUT' else None
    )

    return url

def generate_upload_url(bucket_name, blob_name, content_type='application/octet-stream'):
    """Generate signed URL for file upload"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version='v4',
        expiration=timedelta(hours=1),
        method='PUT',
        content_type=content_type
    )

    return url

# Usage example
download_url = generate_signed_url('my-bucket', 'documents/report.pdf', expiration_minutes=30)
upload_url = generate_upload_url('my-bucket', 'uploads/user-123/photo.jpg', 'image/jpeg')
```

**Signed URL with Policy (Node.js)**:
```javascript
const {Storage} = require('@google-cloud/storage');
const storage = new Storage();

async function generateV4ReadSignedUrl(bucketName, fileName) {
    const options = {
        version: 'v4',
        action: 'read',
        expires: Date.now() + 15 * 60 * 1000, // 15 minutes
    };

    const [url] = await storage
        .bucket(bucketName)
        .file(fileName)
        .getSignedUrl(options);

    return url;
}

async function generateV4UploadSignedUrl(bucketName, fileName, contentType) {
    const options = {
        version: 'v4',
        action: 'write',
        expires: Date.now() + 60 * 60 * 1000, // 1 hour
        contentType: contentType
    };

    const [url] = await storage
        .bucket(bucketName)
        .file(fileName)
        .getSignedUrl(options);

    return url;
}

// Usage with Express.js
app.get('/api/upload-url', async (req, res) => {
    try {
        const fileName = `uploads/${req.user.id}/${Date.now()}-${req.query.filename}`;
        const url = await generateV4UploadSignedUrl('my-bucket', fileName, req.query.contentType);
        res.json({uploadUrl: url, fileName: fileName});
    } catch (error) {
        res.status(500).json({error: error.message});
    }
});
```

### Resumable Uploads

**Resumable Upload Implementation (Python)**:
```python
from google.cloud import storage
from google.resumable_media import requests, common
import requests as standard_requests

def resumable_upload_large_file(bucket_name, source_file_name, destination_blob_name):
    """Upload large file with resumable upload"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Configure resumable upload with chunk size
    chunk_size = 5 * 1024 * 1024  # 5 MB chunks
    blob.chunk_size = chunk_size

    # Upload with progress tracking
    with open(source_file_name, 'rb') as file_obj:
        total_bytes = os.path.getsize(source_file_name)
        bytes_uploaded = 0

        # Custom upload with retry
        blob.upload_from_file(
            file_obj,
            rewind=True,
            size=total_bytes,
            num_retries=3
        )

    print(f"File {source_file_name} uploaded with resumable upload")

def resumable_upload_with_progress(bucket_name, source_file_name, destination_blob_name):
    """Resumable upload with progress callback"""
    from google.cloud.storage import Blob
    from google.cloud.storage.blob import _DEFAULT_CHUNKSIZE

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Set custom chunk size (must be multiple of 256 KB)
    blob.chunk_size = 5 * 1024 * 1024  # 5 MB

    file_size = os.path.getsize(source_file_name)

    with open(source_file_name, 'rb') as file_obj:
        # Create a custom upload session
        blob.upload_from_file(
            file_obj,
            size=file_size,
            num_retries=5,
            if_generation_match=None
        )

    print(f"Upload completed: {destination_blob_name}")
```

**Resumable Upload (Node.js)**:
```javascript
const {Storage} = require('@google-cloud/storage');
const fs = require('fs');

async function resumableUpload(bucketName, fileName, destFileName) {
    const storage = new Storage();
    const bucket = storage.bucket(bucketName);
    const file = bucket.file(destFileName);

    const options = {
        resumable: true,
        validation: 'crc32c',
        metadata: {
            contentType: 'application/octet-stream'
        }
    };

    await new Promise((resolve, reject) => {
        fs.createReadStream(fileName)
            .pipe(file.createWriteStream(options))
            .on('error', reject)
            .on('finish', resolve);
    });

    console.log(`${fileName} uploaded to ${destFileName}`);
}

async function resumableUploadWithProgress(bucketName, fileName, destFileName) {
    const storage = new Storage();
    const options = {
        destination: destFileName,
        resumable: true,
        validation: 'crc32c'
    };

    const fileSize = fs.statSync(fileName).size;
    let uploadedBytes = 0;

    const uploadStream = storage
        .bucket(bucketName)
        .file(destFileName)
        .createWriteStream(options);

    uploadStream.on('progress', (progress) => {
        uploadedBytes = progress.bytesWritten;
        const percent = ((uploadedBytes / fileSize) * 100).toFixed(2);
        console.log(`Upload progress: ${percent}%`);
    });

    await new Promise((resolve, reject) => {
        fs.createReadStream(fileName)
            .pipe(uploadStream)
            .on('error', reject)
            .on('finish', resolve);
    });
}

module.exports = {resumableUpload, resumableUploadWithProgress};
```

### Parallel Composite Uploads

**Parallel Upload for Large Files (Python)**:
```python
from google.cloud import storage
import os
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

def parallel_composite_upload(bucket_name, source_file_name, destination_blob_name, chunk_size=32*1024*1024):
    """Upload large file using parallel composite uploads"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get file size
    file_size = os.path.getsize(source_file_name)
    num_chunks = math.ceil(file_size / chunk_size)

    # Upload chunks in parallel
    chunk_blobs = []

    def upload_chunk(chunk_num, start, end):
        chunk_blob_name = f"{destination_blob_name}_chunk_{chunk_num}"
        blob = bucket.blob(chunk_blob_name)

        with open(source_file_name, 'rb') as f:
            f.seek(start)
            chunk_data = f.read(end - start)
            blob.upload_from_string(chunk_data)

        return blob

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, file_size)
            future = executor.submit(upload_chunk, i, start, end)
            futures.append(future)

        for future in as_completed(futures):
            chunk_blobs.append(future.result())

    # Compose chunks into final blob
    destination_blob = bucket.blob(destination_blob_name)
    destination_blob.compose(chunk_blobs)

    # Clean up chunk blobs
    for blob in chunk_blobs:
        blob.delete()

    print(f"Parallel upload completed: {destination_blob_name}")

def parallel_upload_large_file(bucket_name, source_file_name, destination_blob_name):
    """Simplified parallel upload for files > 100MB"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Cloud Storage handles parallel upload automatically for large files
    # Just configure appropriate chunk size
    blob.chunk_size = 10 * 1024 * 1024  # 10 MB chunks

    blob.upload_from_filename(source_file_name)
    print(f"Large file uploaded: {destination_blob_name}")
```

### Streaming Operations

**Stream Upload and Download (Python)**:
```python
from google.cloud import storage
import io

def stream_upload(bucket_name, destination_blob_name, data_generator):
    """Upload data from a generator/stream"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload from file-like object
    with blob.open('wb') as f:
        for chunk in data_generator:
            f.write(chunk)

    print(f"Stream upload completed: {destination_blob_name}")

def stream_download(bucket_name, source_blob_name, process_chunk):
    """Download and process data as stream"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    # Download as stream
    with blob.open('rb') as f:
        while True:
            chunk = f.read(1024 * 1024)  # 1 MB chunks
            if not chunk:
                break
            process_chunk(chunk)

    print(f"Stream download completed: {source_blob_name}")

# Example: Stream CSV processing
def process_csv_stream(bucket_name, blob_name):
    """Process CSV file without loading into memory"""
    import csv

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open('r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            # Process each row
            process_row(row)

def process_row(row):
    """Process individual CSV row"""
    print(f"Processing: {row}")
```

**Stream Processing (Node.js)**:
```javascript
const {Storage} = require('@google-cloud/storage');
const csv = require('csv-parser');

async function streamDownload(bucketName, fileName, processFn) {
    const storage = new Storage();
    const file = storage.bucket(bucketName).file(fileName);

    return new Promise((resolve, reject) => {
        file.createReadStream()
            .on('error', reject)
            .on('data', chunk => processFn(chunk))
            .on('end', resolve);
    });
}

async function streamUpload(bucketName, destFileName, dataStream) {
    const storage = new Storage();
    const file = storage.bucket(bucketName).file(destFileName);

    return new Promise((resolve, reject) => {
        dataStream
            .pipe(file.createWriteStream({
                resumable: false,
                validation: false
            }))
            .on('error', reject)
            .on('finish', resolve);
    });
}

// CSV streaming example
async function processCsvStream(bucketName, fileName) {
    const storage = new Storage();
    const file = storage.bucket(bucketName).file(fileName);

    return new Promise((resolve, reject) => {
        const results = [];
        file.createReadStream()
            .pipe(csv())
            .on('data', (row) => {
                // Process each row
                results.push(processRow(row));
            })
            .on('end', () => resolve(results))
            .on('error', reject);
    });
}

function processRow(row) {
    console.log('Processing row:', row);
    return row;
}

module.exports = {streamDownload, streamUpload, processCsvStream};
```

## Cloud SQL Integration

### Connection Methods

**Cloud SQL Proxy Connection (Python)**:
```python
import sqlalchemy
from google.cloud.sql.connector import Connector
import pg8000

def create_connection_pool_with_connector():
    """Create connection pool using Cloud SQL Python Connector"""
    connector = Connector()

    def getconn():
        conn = connector.connect(
            "project:region:instance",
            "pg8000",
            user="db-user",
            password="db-password",
            db="database-name"
        )
        return conn

    # Create SQLAlchemy engine
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True  # Verify connections before using
    )

    return pool, connector

# Usage
pool, connector = create_connection_pool_with_connector()

try:
    with pool.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT NOW()"))
        print(result.fetchone())
finally:
    connector.close()
```

**Unix Socket Connection for App Engine**:
```python
import sqlalchemy
import os

def create_unix_socket_pool():
    """Create connection pool using Unix socket (App Engine)"""
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    instance_connection_name = os.environ.get("INSTANCE_CONNECTION_NAME")

    db_socket_dir = "/cloudsql"

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_sock": f"{db_socket_dir}/{instance_connection_name}/.s.PGSQL.5432"}
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True
    )

    return pool
```

**Private IP Connection**:
```python
import sqlalchemy
import os

def create_private_ip_pool():
    """Create connection pool using private IP (VPC)"""
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    db_host = os.environ.get("PRIVATE_IP")  # Private IP of Cloud SQL instance

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=5432,
            database=db_name
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True
    )

    return pool
```

**Public IP with SSL (Node.js)**:
```javascript
const {Sequelize} = require('sequelize');
const fs = require('fs');

const sequelize = new Sequelize({
    dialect: 'postgres',
    host: process.env.DB_HOST,
    port: 5432,
    username: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME,
    dialectOptions: {
        ssl: {
            ca: fs.readFileSync('/path/to/server-ca.pem'),
            key: fs.readFileSync('/path/to/client-key.pem'),
            cert: fs.readFileSync('/path/to/client-cert.pem')
        }
    },
    pool: {
        max: 5,
        min: 0,
        acquire: 30000,
        idle: 10000
    },
    logging: false
});

module.exports = sequelize;
```

### Connection Pooling Best Practices

**Advanced Connection Pool Configuration (Python)**:
```python
import sqlalchemy
from sqlalchemy.pool import NullPool, QueuePool
from google.cloud.sql.connector import Connector
import logging

class DatabaseConnection:
    def __init__(self):
        self.connector = Connector()
        self.engine = self._create_engine()

    def _create_engine(self):
        """Create optimized database engine with connection pooling"""
        def getconn():
            conn = self.connector.connect(
                "project:region:instance",
                "pg8000",
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASS"),
                db=os.environ.get("DB_NAME"),
                # Enable faster IAM authentication
                enable_iam_auth=False
            )
            return conn

        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
            # Pool configuration for Cloud Run/Functions
            pool_size=5,  # Core pool size
            max_overflow=2,  # Additional connections when pool is full
            pool_timeout=30,  # Timeout waiting for connection
            pool_recycle=1800,  # Recycle connections after 30 min
            pool_pre_ping=True,  # Verify connection before using
            echo=False,  # Set to True for SQL debugging
            pool_use_lifo=True  # Use LIFO for better connection reuse
        )

        return engine

    def get_connection(self):
        """Get database connection from pool"""
        return self.engine.connect()

    def execute_query(self, query, params=None):
        """Execute query with automatic connection management"""
        with self.engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(query), params or {})
            return result.fetchall()

    def execute_transaction(self, operations):
        """Execute multiple operations in a transaction"""
        with self.engine.begin() as conn:
            results = []
            for operation in operations:
                result = conn.execute(
                    sqlalchemy.text(operation['query']),
                    operation.get('params', {})
                )
                results.append(result)
            return results

    def close(self):
        """Close all connections and cleanup"""
        self.engine.dispose()
        self.connector.close()

# Usage
db = DatabaseConnection()

try:
    # Simple query
    users = db.execute_query("SELECT * FROM users WHERE active = :active", {"active": True})

    # Transaction
    operations = [
        {"query": "UPDATE accounts SET balance = balance - :amount WHERE id = :id",
         "params": {"amount": 100, "id": 1}},
        {"query": "UPDATE accounts SET balance = balance + :amount WHERE id = :id",
         "params": {"amount": 100, "id": 2}}
    ]
    db.execute_transaction(operations)
finally:
    db.close()
```

**Connection Pool for Serverless (Node.js)**:
```javascript
const {Sequelize} = require('sequelize');
const {Connector} = require('@google-cloud/cloud-sql-connector');

class DatabasePool {
    constructor() {
        this.connector = new Connector();
        this.sequelize = null;
    }

    async initialize() {
        const clientOpts = await this.connector.getOptions({
            instanceConnectionName: process.env.INSTANCE_CONNECTION_NAME,
            ipType: 'PUBLIC'
        });

        this.sequelize = new Sequelize({
            dialect: 'postgres',
            username: process.env.DB_USER,
            password: process.env.DB_PASS,
            database: process.env.DB_NAME,
            ...clientOpts,
            pool: {
                max: 5,
                min: 1,
                acquire: 30000,
                idle: 10000,
                evict: 10000
            },
            logging: false,
            dialectOptions: {
                connectTimeout: 10000,
                keepAlive: true,
                statement_timeout: 30000
            }
        });

        await this.sequelize.authenticate();
        console.log('Database connection established');
    }

    async query(sql, options = {}) {
        return await this.sequelize.query(sql, {
            type: Sequelize.QueryTypes.SELECT,
            ...options
        });
    }

    async transaction(callback) {
        return await this.sequelize.transaction(callback);
    }

    async close() {
        await this.sequelize.close();
        this.connector.close();
    }

    getSequelize() {
        return this.sequelize;
    }
}

// Singleton instance for serverless
let dbPool = null;

async function getDbPool() {
    if (!dbPool) {
        dbPool = new DatabasePool();
        await dbPool.initialize();
    }
    return dbPool;
}

module.exports = {DatabasePool, getDbPool};
```

### ORM Integration

**SQLAlchemy with Cloud SQL (Python)**:
```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from google.cloud.sql.connector import Connector

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_amount = Column(Integer)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders")

# Database setup
connector = Connector()

def getconn():
    return connector.connect(
        "project:region:instance",
        "pg8000",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        db=os.environ["DB_NAME"]
    )

engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=2
)

Session = sessionmaker(bind=engine)

# CRUD Operations
def create_user(email, name):
    """Create new user"""
    session = Session()
    try:
        user = User(email=email, name=name)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def get_user_with_orders(user_id):
    """Get user with all orders"""
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            # Eagerly load orders
            orders = user.orders
            return {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'orders': [{'id': o.id, 'total': o.total_amount, 'status': o.status} for o in orders]
            }
        return None
    finally:
        session.close()

def create_order_with_transaction(user_id, total_amount):
    """Create order with transaction"""
    session = Session()
    try:
        # Verify user exists
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Create order
        order = Order(user_id=user_id, total_amount=total_amount, status='pending')
        session.add(order)
        session.commit()
        return order
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
```

**Sequelize ORM (Node.js)**:
```javascript
const {Sequelize, DataTypes} = require('sequelize');
const {Connector} = require('@google-cloud/cloud-sql-connector');

// Initialize Sequelize with Cloud SQL
async function initializeSequelize() {
    const connector = new Connector();
    const clientOpts = await connector.getOptions({
        instanceConnectionName: process.env.INSTANCE_CONNECTION_NAME,
        ipType: 'PUBLIC'
    });

    const sequelize = new Sequelize({
        dialect: 'postgres',
        username: process.env.DB_USER,
        password: process.env.DB_PASS,
        database: process.env.DB_NAME,
        ...clientOpts,
        pool: {max: 5, min: 1, idle: 10000}
    });

    return sequelize;
}

// Define Models
const sequelize = await initializeSequelize();

const User = sequelize.define('User', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    email: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: false,
        validate: {
            isEmail: true
        }
    },
    name: {
        type: DataTypes.STRING(100)
    }
}, {
    tableName: 'users',
    timestamps: true
});

const Order = sequelize.define('Order', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    userId: {
        type: DataTypes.INTEGER,
        allowNull: false,
        field: 'user_id'
    },
    totalAmount: {
        type: DataTypes.INTEGER,
        field: 'total_amount'
    },
    status: {
        type: DataTypes.STRING(50),
        defaultValue: 'pending'
    }
}, {
    tableName: 'orders',
    timestamps: true
});

// Define associations
User.hasMany(Order, {foreignKey: 'userId'});
Order.belongsTo(User, {foreignKey: 'userId'});

// CRUD Operations
async function createUser(email, name) {
    try {
        const user = await User.create({email, name});
        return user;
    } catch (error) {
        console.error('Error creating user:', error);
        throw error;
    }
}

async function getUserWithOrders(userId) {
    const user = await User.findByPk(userId, {
        include: [{
            model: Order,
            attributes: ['id', 'totalAmount', 'status', 'createdAt']
        }]
    });
    return user;
}

async function createOrderWithTransaction(userId, totalAmount) {
    const t = await sequelize.transaction();

    try {
        const user = await User.findByPk(userId, {transaction: t});
        if (!user) {
            throw new Error('User not found');
        }

        const order = await Order.create({
            userId,
            totalAmount,
            status: 'pending'
        }, {transaction: t});

        await t.commit();
        return order;
    } catch (error) {
        await t.rollback();
        throw error;
    }
}

module.exports = {sequelize, User, Order, createUser, getUserWithOrders, createOrderWithTransaction};
```

### Database Migrations

**Alembic Migrations (Python)**:
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from google.cloud.sql.connector import Connector
import os

# Import your models
from myapp.models import Base

config = context.config

# Setup connector for migrations
connector = Connector()

def getconn():
    return connector.connect(
        os.environ["INSTANCE_CONNECTION_NAME"],
        "pg8000",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        db=os.environ["DB_NAME"]
    )

def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = "postgresql+pg8000://"

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        creator=getconn
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata
        )

        with context.begin_transaction():
            context.run_migrations()

    connector.close()

run_migrations_online()
```

**Sequelize Migrations (Node.js)**:
```javascript
// migrations/20240101000000-create-users.js
module.exports = {
    up: async (queryInterface, Sequelize) => {
        await queryInterface.createTable('users', {
            id: {
                type: Sequelize.INTEGER,
                primaryKey: true,
                autoIncrement: true
            },
            email: {
                type: Sequelize.STRING(255),
                unique: true,
                allowNull: false
            },
            name: {
                type: Sequelize.STRING(100)
            },
            created_at: {
                type: Sequelize.DATE,
                allowNull: false,
                defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
            },
            updated_at: {
                type: Sequelize.DATE,
                allowNull: false,
                defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
            }
        });

        await queryInterface.addIndex('users', ['email'], {
            unique: true,
            name: 'users_email_unique'
        });
    },

    down: async (queryInterface, Sequelize) => {
        await queryInterface.dropTable('users');
    }
};

// config/database.js for migrations
const {Connector} = require('@google-cloud/cloud-sql-connector');

module.exports = {
    development: {
        dialect: 'postgres',
        username: process.env.DB_USER,
        password: process.env.DB_PASS,
        database: process.env.DB_NAME,
        host: process.env.DB_HOST,
        pool: {max: 5, min: 1}
    }
};
```

## Cloud Spanner for Applications

### Client Library Setup

**Spanner Client (Python)**:
```python
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

class SpannerClient:
    def __init__(self, instance_id, database_id):
        self.spanner_client = spanner.Client()
        self.instance = self.spanner_client.instance(instance_id)
        self.database = self.instance.database(database_id)

    def read_data(self, table, columns, key_set):
        """Read data using primary key"""
        with self.database.snapshot() as snapshot:
            results = snapshot.read(
                table=table,
                columns=columns,
                keyset=key_set
            )
            return [dict(zip(columns, row)) for row in results]

    def query_data(self, query, params=None, param_types_dict=None):
        """Execute SQL query"""
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(
                query,
                params=params,
                param_types=param_types_dict
            )
            return [dict(row) for row in results]

    def insert_data(self, table, columns, values):
        """Insert data using mutation"""
        with self.database.batch() as batch:
            batch.insert(
                table=table,
                columns=columns,
                values=values
            )

    def update_data(self, table, columns, values):
        """Update data using mutation"""
        with self.database.batch() as batch:
            batch.update(
                table=table,
                columns=columns,
                values=values
            )

    def delete_data(self, table, key_set):
        """Delete data using mutation"""
        with self.database.batch() as batch:
            batch.delete(table=table, keyset=key_set)
```

**Spanner with Node.js**:
```javascript
const {Spanner} = require('@google-cloud/spanner');

class SpannerClient {
    constructor(instanceId, databaseId) {
        this.spanner = new Spanner();
        this.instance = this.spanner.instance(instanceId);
        this.database = this.instance.database(databaseId);
    }

    async readData(table, columns, keys) {
        const [rows] = await this.database.read({
            table: table,
            columns: columns,
            keys: keys
        });

        return rows.map(row => row.toJSON());
    }

    async queryData(query) {
        const [rows] = await this.database.run(query);
        return rows.map(row => row.toJSON());
    }

    async insertData(table, data) {
        await this.database.runTransactionAsync(async (transaction) => {
            await transaction.insert(table, data);
            await transaction.commit();
        });
    }

    async updateData(table, data) {
        await this.database.runTransactionAsync(async (transaction) => {
            await transaction.update(table, data);
            await transaction.commit();
        });
    }

    async deleteData(table, keys) {
        await this.database.runTransactionAsync(async (transaction) => {
            await transaction.deleteRows(table, keys);
            await transaction.commit();
        });
    }
}

module.exports = SpannerClient;
```

### Session Management

**Session Pool Configuration (Python)**:
```python
from google.cloud import spanner

def create_spanner_database_with_pool(instance_id, database_id):
    """Create Spanner database with optimized session pool"""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    # Configure session pool
    pool = spanner.BurstyPool(
        target_size=10,  # Target number of sessions
        max_size=30,  # Maximum sessions
        min_size=5  # Minimum sessions to maintain
    )

    database = instance.database(
        database_id,
        pool=pool
    )

    return database

# Usage with session management
database = create_spanner_database_with_pool('my-instance', 'my-database')

# Sessions are automatically managed by the pool
def execute_query_with_session():
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT * FROM Users WHERE active = @active",
            params={"active": True},
            param_types={"active": param_types.BOOL}
        )
        return list(results)
```

**Session Pool (Node.js)**:
```javascript
const {Spanner} = require('@google-cloud/spanner');

const spanner = new Spanner({
    projectId: 'my-project'
});

const instance = spanner.instance('my-instance');
const database = instance.database('my-database', {
    min: 5,  // Minimum sessions
    max: 30,  // Maximum sessions
    incStep: 5,  // Step to increase sessions
    writes: 0.2,  // 20% of sessions for writes
    keepAlive: 30  // Keep alive interval in minutes
});

// Database handles session pool automatically
async function executeQuery() {
    const query = {
        sql: 'SELECT * FROM Users WHERE active = @active',
        params: {
            active: true
        }
    };

    const [rows] = await database.run(query);
    return rows;
}

module.exports = {database, executeQuery};
```

### Transaction Handling

**Read-Write Transactions (Python)**:
```python
from google.cloud import spanner

database = instance.database('my-database')

def transfer_funds(from_account_id, to_account_id, amount):
    """Transfer funds between accounts with transaction"""
    def update_in_transaction(transaction):
        # Read current balances
        row = list(transaction.read(
            table='Accounts',
            columns=['account_id', 'balance'],
            keyset=spanner.KeySet(keys=[[from_account_id]])
        ))[0]

        from_balance = row[1]

        if from_balance < amount:
            raise ValueError("Insufficient funds")

        # Update balances
        transaction.update(
            table='Accounts',
            columns=['account_id', 'balance'],
            values=[
                [from_account_id, from_balance - amount],
                [to_account_id, from_balance + amount]  # Simplified - should read to_account balance
            ]
        )

    database.run_in_transaction(update_in_transaction)

def batch_update_with_retry(updates):
    """Batch update with automatic retry"""
    from google.api_core import retry

    @retry.Retry(predicate=retry.if_transactional_error)
    def update_in_transaction(transaction):
        for update in updates:
            transaction.update(
                table=update['table'],
                columns=update['columns'],
                values=update['values']
            )

    database.run_in_transaction(update_in_transaction)
```

### Batch Operations and Query Optimization

**Batch Operations (Python)**:
```python
from google.cloud import spanner

def batch_insert_users(database, users_data):
    """Batch insert multiple users"""
    with database.batch() as batch:
        batch.insert(
            table='Users',
            columns=['user_id', 'email', 'name', 'created_at'],
            values=users_data
        )

def batch_operations_transaction(database):
    """Multiple operations in single transaction"""
    def run_batch(transaction):
        # Batch read
        rows = transaction.read(
            table='Users',
            columns=['user_id', 'email'],
            keyset=spanner.KeySet(all_=True),
            index='EmailIndex'
        )

        # Process and update
        updates = []
        for row in rows:
            updates.append([row[0], row[1], 'verified'])

        # Batch update
        transaction.update(
            table='Users',
            columns=['user_id', 'email', 'status'],
            values=updates
        )

    database.run_in_transaction(run_batch)

def optimized_query_with_index(database):
    """Query optimization with index hints"""
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            """
            SELECT u.user_id, u.name, o.order_id, o.total
            FROM Users@{FORCE_INDEX=UserNameIndex} u
            JOIN Orders o ON u.user_id = o.user_id
            WHERE u.name LIKE @pattern
            LIMIT 100
            """,
            params={"pattern": "John%"},
            param_types={"pattern": param_types.STRING}
        )
        return list(results)
```

## Firestore/Datastore Integration

### Document Model and Operations

**Firestore Client Setup (Python)**:
```python
from google.cloud import firestore
from google.cloud.firestore_v1 import ArrayUnion, ArrayRemove, Increment
from datetime import datetime

db = firestore.Client()

# Add document with auto-generated ID
def create_user(user_data):
    """Create user document with auto-generated ID"""
    doc_ref = db.collection('users').document()
    user_data['created_at'] = firestore.SERVER_TIMESTAMP
    doc_ref.set(user_data)
    return doc_ref.id

# Set document with custom ID
def create_user_with_id(user_id, user_data):
    """Create user with specific ID"""
    doc_ref = db.collection('users').document(user_id)
    doc_ref.set(user_data, merge=True)
    return user_id

# Update document
def update_user(user_id, updates):
    """Update user document"""
    doc_ref = db.collection('users').document(user_id)
    doc_ref.update(updates)

# Update with field transformations
def update_user_array_and_counter(user_id, new_tag):
    """Update arrays and increment counters"""
    doc_ref = db.collection('users').document(user_id)
    doc_ref.update({
        'tags': ArrayUnion([new_tag]),  # Add to array
        'login_count': Increment(1),  # Increment counter
        'last_login': firestore.SERVER_TIMESTAMP
    })

# Delete document
def delete_user(user_id):
    """Delete user document"""
    db.collection('users').document(user_id).delete()

# Delete field
def remove_user_field(user_id, field_name):
    """Remove specific field from document"""
    doc_ref = db.collection('users').document(user_id)
    doc_ref.update({field_name: firestore.DELETE_FIELD})
```

**Firestore with Node.js**:
```javascript
const {Firestore, FieldValue} = require('@google-cloud/firestore');

const db = new Firestore();

async function createUser(userData) {
    const docRef = db.collection('users').doc();
    userData.createdAt = FieldValue.serverTimestamp();
    await docRef.set(userData);
    return docRef.id;
}

async function createUserWithId(userId, userData) {
    const docRef = db.collection('users').doc(userId);
    await docRef.set(userData, {merge: true});
    return userId;
}

async function updateUser(userId, updates) {
    const docRef = db.collection('users').doc(userId);
    await docRef.update(updates);
}

async function updateUserArrayAndCounter(userId, newTag) {
    const docRef = db.collection('users').doc(userId);
    await docRef.update({
        tags: FieldValue.arrayUnion(newTag),
        loginCount: FieldValue.increment(1),
        lastLogin: FieldValue.serverTimestamp()
    });
}

async function deleteUser(userId) {
    await db.collection('users').doc(userId).delete();
}

async function removeUserField(userId, fieldName) {
    const docRef = db.collection('users').doc(userId);
    await docRef.update({
        [fieldName]: FieldValue.delete()
    });
}

module.exports = {createUser, createUserWithId, updateUser, updateUserArrayAndCounter, deleteUser, removeUserField};
```

### Queries and Indexes

**Complex Queries (Python)**:
```python
from google.cloud import firestore

db = firestore.Client()

def simple_query():
    """Simple where query"""
    users_ref = db.collection('users')
    query = users_ref.where('age', '>=', 18).where('active', '==', True)
    docs = query.stream()
    return [doc.to_dict() for doc in docs]

def compound_query():
    """Compound query with multiple conditions"""
    users_ref = db.collection('users')
    query = (users_ref
             .where('status', '==', 'active')
             .where('age', '>=', 18)
             .order_by('created_at', direction=firestore.Query.DESCENDING)
             .limit(20))

    return [doc.to_dict() for doc in query.stream()]

def array_contains_query():
    """Query with array-contains"""
    users_ref = db.collection('users')
    query = users_ref.where('interests', 'array_contains', 'coding')
    return [doc.to_dict() for doc in query.stream()]

def array_contains_any_query():
    """Query with array-contains-any"""
    users_ref = db.collection('users')
    query = users_ref.where('roles', 'array_contains_any', ['admin', 'moderator'])
    return [doc.to_dict() for doc in query.stream()]

def in_query():
    """Query with IN operator"""
    users_ref = db.collection('users')
    query = users_ref.where('status', 'in', ['active', 'pending', 'verified'])
    return [doc.to_dict() for doc in query.stream()]

def range_query_with_composite_index():
    """Range query requiring composite index"""
    orders_ref = db.collection('orders')
    query = (orders_ref
             .where('user_id', '==', 'user123')
             .where('total', '>=', 100)
             .where('total', '<=', 500)
             .order_by('total')
             .order_by('created_at', direction=firestore.Query.DESCENDING))

    return [doc.to_dict() for doc in query.stream()]

def pagination_query(page_size=10, last_doc=None):
    """Paginated query"""
    users_ref = db.collection('users')
    query = users_ref.order_by('created_at').limit(page_size)

    if last_doc:
        query = query.start_after(last_doc)

    docs = list(query.stream())
    return {
        'data': [doc.to_dict() for doc in docs],
        'last_doc': docs[-1] if docs else None
    }

def collection_group_query():
    """Query across all collections with same name"""
    # Query all 'orders' subcollections across all users
    orders_ref = db.collection_group('orders')
    query = (orders_ref
             .where('status', '==', 'completed')
             .where('total', '>=', 100)
             .order_by('total', direction=firestore.Query.DESCENDING)
             .limit(50))

    return [doc.to_dict() for doc in query.stream()]
```

**Advanced Queries (Node.js)**:
```javascript
const {Firestore} = require('@google-cloud/firestore');
const db = new Firestore();

async function simpleQuery() {
    const usersRef = db.collection('users');
    const snapshot = await usersRef
        .where('age', '>=', 18)
        .where('active', '==', true)
        .get();

    return snapshot.docs.map(doc => doc.data());
}

async function compoundQuery() {
    const usersRef = db.collection('users');
    const snapshot = await usersRef
        .where('status', '==', 'active')
        .where('age', '>=', 18)
        .orderBy('createdAt', 'desc')
        .limit(20)
        .get();

    return snapshot.docs.map(doc => ({id: doc.id, ...doc.data()}));
}

async function arrayContainsQuery() {
    const snapshot = await db.collection('users')
        .where('interests', 'array-contains', 'coding')
        .get();

    return snapshot.docs.map(doc => doc.data());
}

async function arrayContainsAnyQuery() {
    const snapshot = await db.collection('users')
        .where('roles', 'array-contains-any', ['admin', 'moderator'])
        .get();

    return snapshot.docs.map(doc => doc.data());
}

async function inQuery() {
    const snapshot = await db.collection('users')
        .where('status', 'in', ['active', 'pending', 'verified'])
        .get();

    return snapshot.docs.map(doc => doc.data());
}

async function paginationQuery(pageSize = 10, lastDoc = null) {
    let query = db.collection('users')
        .orderBy('createdAt')
        .limit(pageSize);

    if (lastDoc) {
        query = query.startAfter(lastDoc);
    }

    const snapshot = await query.get();

    return {
        data: snapshot.docs.map(doc => ({id: doc.id, ...doc.data()})),
        lastDoc: snapshot.docs[snapshot.docs.length - 1]
    };
}

async function collectionGroupQuery() {
    const snapshot = await db.collectionGroup('orders')
        .where('status', '==', 'completed')
        .where('total', '>=', 100)
        .orderBy('total', 'desc')
        .limit(50)
        .get();

    return snapshot.docs.map(doc => ({id: doc.id, ...doc.data()}));
}

module.exports = {simpleQuery, compoundQuery, arrayContainsQuery, arrayContainsAnyQuery, inQuery, paginationQuery, collectionGroupQuery};
```

### Transactions

**Firestore Transactions (Python)**:
```python
from google.cloud import firestore

db = firestore.Client()

@firestore.transactional
def transfer_balance(transaction, from_user_id, to_user_id, amount):
    """Transfer balance between users with transaction"""
    from_ref = db.collection('users').document(from_user_id)
    to_ref = db.collection('users').document(to_user_id)

    # Read both documents
    from_snapshot = from_ref.get(transaction=transaction)
    to_snapshot = to_ref.get(transaction=transaction)

    if not from_snapshot.exists or not to_snapshot.exists:
        raise ValueError("User not found")

    from_balance = from_snapshot.get('balance')
    to_balance = to_snapshot.get('balance')

    if from_balance < amount:
        raise ValueError("Insufficient funds")

    # Update both documents
    transaction.update(from_ref, {'balance': from_balance - amount})
    transaction.update(to_ref, {'balance': to_balance + amount})

# Execute transaction
transaction = db.transaction()
transfer_balance(transaction, 'user1', 'user2', 100)

def create_order_with_inventory_check(user_id, product_id, quantity):
    """Create order and update inventory atomically"""
    @firestore.transactional
    def transaction_func(transaction):
        product_ref = db.collection('products').document(product_id)
        product_snap = product_ref.get(transaction=transaction)

        if not product_snap.exists:
            raise ValueError("Product not found")

        available = product_snap.get('inventory')
        if available < quantity:
            raise ValueError("Insufficient inventory")

        # Update inventory
        transaction.update(product_ref, {
            'inventory': available - quantity
        })

        # Create order
        order_ref = db.collection('orders').document()
        transaction.set(order_ref, {
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'status': 'pending',
            'created_at': firestore.SERVER_TIMESTAMP
        })

        return order_ref.id

    transaction = db.transaction()
    return transaction_func(transaction)
```

**Firestore Transactions (Node.js)**:
```javascript
const {Firestore} = require('@google-cloud/firestore');
const db = new Firestore();

async function transferBalance(fromUserId, toUserId, amount) {
    return await db.runTransaction(async (transaction) => {
        const fromRef = db.collection('users').doc(fromUserId);
        const toRef = db.collection('users').doc(toUserId);

        const fromDoc = await transaction.get(fromRef);
        const toDoc = await transaction.get(toRef);

        if (!fromDoc.exists || !toDoc.exists) {
            throw new Error('User not found');
        }

        const fromBalance = fromDoc.data().balance;
        const toBalance = toDoc.data().balance;

        if (fromBalance < amount) {
            throw new Error('Insufficient funds');
        }

        transaction.update(fromRef, {balance: fromBalance - amount});
        transaction.update(toRef, {balance: toBalance + amount});
    });
}

async function createOrderWithInventoryCheck(userId, productId, quantity) {
    return await db.runTransaction(async (transaction) => {
        const productRef = db.collection('products').doc(productId);
        const productDoc = await transaction.get(productRef);

        if (!productDoc.exists) {
            throw new Error('Product not found');
        }

        const available = productDoc.data().inventory;
        if (available < quantity) {
            throw new Error('Insufficient inventory');
        }

        // Update inventory
        transaction.update(productRef, {
            inventory: available - quantity
        });

        // Create order
        const orderRef = db.collection('orders').doc();
        transaction.set(orderRef, {
            userId,
            productId,
            quantity,
            status: 'pending',
            createdAt: FieldValue.serverTimestamp()
        });

        return orderRef.id;
    });
}

module.exports = {transferBalance, createOrderWithInventoryCheck};
```

### Real-time Listeners

**Real-time Listeners (Python)**:
```python
from google.cloud import firestore

db = firestore.Client()

def listen_to_document(doc_id):
    """Listen to single document changes"""
    doc_ref = db.collection('users').document(doc_id)

    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f'Document data: {doc.to_dict()}')

    # Start listening
    doc_watch = doc_ref.on_snapshot(on_snapshot)

    # Stop listening (call when needed)
    # doc_watch.unsubscribe()

    return doc_watch

def listen_to_collection():
    """Listen to collection changes"""
    col_ref = db.collection('users').where('active', '==', True)

    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                print(f'New user: {change.document.to_dict()}')
            elif change.type.name == 'MODIFIED':
                print(f'Modified user: {change.document.to_dict()}')
            elif change.type.name == 'REMOVED':
                print(f'Removed user: {change.document.id}')

    col_watch = col_ref.on_snapshot(on_snapshot)
    return col_watch

# Error handling for listeners
def listen_with_error_handling():
    """Listener with error handling"""
    def on_snapshot(docs, changes, read_time):
        try:
            for doc in docs:
                process_document(doc.to_dict())
        except Exception as e:
            print(f'Error processing document: {e}')

    def on_error(error):
        print(f'Listener error: {error}')

    doc_ref = db.collection('users').document('user123')
    doc_watch = doc_ref.on_snapshot(on_snapshot, on_error)

    return doc_watch
```

**Real-time Listeners (Node.js)**:
```javascript
const {Firestore} = require('@google-cloud/firestore');
const db = new Firestore();

function listenToDocument(docId) {
    const docRef = db.collection('users').doc(docId);

    const unsubscribe = docRef.onSnapshot(
        (docSnapshot) => {
            if (docSnapshot.exists) {
                console.log('Document data:', docSnapshot.data());
            } else {
                console.log('Document does not exist');
            }
        },
        (error) => {
            console.error('Listener error:', error);
        }
    );

    return unsubscribe;
}

function listenToCollection() {
    const colRef = db.collection('users').where('active', '==', true);

    const unsubscribe = colRef.onSnapshot(
        (snapshot) => {
            snapshot.docChanges().forEach((change) => {
                if (change.type === 'added') {
                    console.log('New user:', change.doc.data());
                } else if (change.type === 'modified') {
                    console.log('Modified user:', change.doc.data());
                } else if (change.type === 'removed') {
                    console.log('Removed user:', change.doc.id);
                }
            });
        },
        (error) => {
            console.error('Listener error:', error);
        }
    );

    return unsubscribe;
}

function listenWithFilter() {
    const query = db.collection('orders')
        .where('status', '==', 'pending')
        .orderBy('createdAt', 'desc')
        .limit(10);

    const unsubscribe = query.onSnapshot((snapshot) => {
        const orders = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        }));
        console.log('Pending orders:', orders);
    });

    return unsubscribe;
}

module.exports = {listenToDocument, listenToCollection, listenWithFilter};
```

### Offline Support

**Offline Persistence (JavaScript)**:
```javascript
const {Firestore} = require('@google-cloud/firestore');

// Enable offline persistence
const db = new Firestore({
    ignoreUndefinedProperties: true
});

// For web/mobile clients (using Firebase SDK)
// firebase.firestore().enablePersistence()
//     .catch((err) => {
//         if (err.code == 'failed-precondition') {
//             // Multiple tabs open
//         } else if (err.code == 'unimplemented') {
//             // Browser doesn't support
//         }
//     });

// Offline-aware operations
async function createWithOfflineSupport(userId, data) {
    try {
        const docRef = db.collection('users').doc(userId);
        await docRef.set(data);
        console.log('Data saved (online or offline)');
    } catch (error) {
        console.error('Error:', error);
    }
}

// Listen with offline support
function listenWithOfflineSupport() {
    const unsubscribe = db.collection('users')
        .onSnapshot(
            {includeMetadataChanges: true},
            (snapshot) => {
                snapshot.docChanges().forEach((change) => {
                    const source = snapshot.metadata.fromCache ? 'local cache' : 'server';
                    console.log(`Data from ${source}`);

                    if (change.type === 'added') {
                        console.log('New:', change.doc.data());
                    }
                });
            }
        );

    return unsubscribe;
}

module.exports = {createWithOfflineSupport, listenWithOfflineSupport};
```

## Bigtable Integration

### Client Library Setup

**Bigtable Client (Python)**:
```python
from google.cloud import bigtable
from google.cloud.bigtable import column_family, row_filters

class BigtableClient:
    def __init__(self, project_id, instance_id, table_id):
        self.client = bigtable.Client(project=project_id, admin=True)
        self.instance = self.client.instance(instance_id)
        self.table = self.instance.table(table_id)

    def write_row(self, row_key, column_family_id, column_name, value):
        """Write single row"""
        row = self.table.direct_row(row_key)
        row.set_cell(
            column_family_id,
            column_name,
            value,
            timestamp=None  # Use server timestamp
        )
        row.commit()

    def write_batch(self, rows_data):
        """Batch write multiple rows"""
        rows = []
        for row_data in rows_data:
            row = self.table.direct_row(row_data['key'])
            row.set_cell(
                row_data['family'],
                row_data['column'],
                row_data['value']
            )
            rows.append(row)

        # Commit all rows
        statuses = self.table.mutate_rows(rows)
        failed = [i for i, status in enumerate(statuses) if status.code != 0]
        return failed

    def read_row(self, row_key):
        """Read single row"""
        row = self.table.read_row(row_key)
        if row:
            return self._row_to_dict(row)
        return None

    def read_rows_with_filter(self, start_key, end_key, limit=100):
        """Read rows with key range and filter"""
        row_set = bigtable.row_set.RowSet()
        row_set.add_row_range_from_keys(
            start_key=start_key,
            end_key=end_key
        )

        # Create filter
        filter = row_filters.CellsColumnLimitFilter(1)  # Latest version only

        rows = self.table.read_rows(
            row_set=row_set,
            filter_=filter,
            limit=limit
        )

        return [self._row_to_dict(row) for row in rows]

    def read_with_prefix(self, prefix):
        """Read rows with key prefix"""
        row_set = bigtable.row_set.RowSet()
        row_set.add_row_range_with_prefix(prefix)

        rows = self.table.read_rows(row_set=row_set)
        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row):
        """Convert row to dictionary"""
        result = {'row_key': row.row_key.decode()}
        for family_id, columns in row.cells.items():
            for column_id, cells in columns.items():
                key = f"{family_id}:{column_id.decode()}"
                result[key] = cells[0].value.decode()  # Latest cell
        return result
```

**Bigtable with Node.js**:
```javascript
const {Bigtable} = require('@google-cloud/bigtable');

class BigtableClient {
    constructor(projectId, instanceId, tableId) {
        this.bigtable = new Bigtable({projectId});
        this.instance = this.bigtable.instance(instanceId);
        this.table = this.instance.table(tableId);
    }

    async writeRow(rowKey, columnFamilyId, columnName, value) {
        const row = this.table.row(rowKey);
        await row.save({
            [columnFamilyId]: {
                [columnName]: value
            }
        });
    }

    async writeBatch(rowsData) {
        const rows = rowsData.map(data => {
            const row = this.table.row(data.key);
            return row.save({
                [data.family]: {
                    [data.column]: data.value
                }
            });
        });

        await Promise.all(rows);
    }

    async readRow(rowKey) {
        const [row] = await this.table.row(rowKey).get();
        if (!row) return null;

        return this.rowToObject(row);
    }

    async readRowsWithFilter(startKey, endKey, limit = 100) {
        const options = {
            start: startKey,
            end: endKey,
            limit: limit,
            filter: [{
                column: {
                    cellLimit: 1  // Latest version only
                }
            }]
        };

        const [rows] = await this.table.getRows(options);
        return rows.map(row => this.rowToObject(row));
    }

    async readWithPrefix(prefix) {
        const options = {
            prefix: prefix
        };

        const [rows] = await this.table.getRows(options);
        return rows.map(row => this.rowToObject(row));
    }

    rowToObject(row) {
        const result = {rowKey: row.id};
        const data = row.data;

        for (const [family, columns] of Object.entries(data)) {
            for (const [column, cells] of Object.entries(columns)) {
                const key = `${family}:${column}`;
                result[key] = cells[0].value;  // Latest cell
            }
        }

        return result;
    }
}

module.exports = BigtableClient;
```

### Row Key Design for Applications

**Row Key Design Patterns (Python)**:
```python
import hashlib
from datetime import datetime

class RowKeyDesigner:
    @staticmethod
    def time_series_key(entity_id, timestamp):
        """Time series data with reverse timestamp for recent-first access"""
        # Reverse timestamp for most recent first
        reverse_ts = 9999999999 - int(timestamp.timestamp())
        return f"{entity_id}#{reverse_ts}"

    @staticmethod
    def user_activity_key(user_id, activity_type, timestamp):
        """User activity with salting to prevent hotspots"""
        # Salt based on user_id to distribute writes
        salt = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 100
        reverse_ts = 9999999999 - int(timestamp.timestamp())
        return f"{salt:02d}#{user_id}#{activity_type}#{reverse_ts}"

    @staticmethod
    def composite_key(components):
        """Composite key from multiple components"""
        return "#".join(str(c) for c in components)

    @staticmethod
    def metric_key(metric_name, timestamp, dimensions):
        """Metrics with dimensions"""
        # Format: metricName#timestamp#dimension1=value1#dimension2=value2
        dim_str = "#".join(f"{k}={v}" for k, v in sorted(dimensions.items()))
        ts = int(timestamp.timestamp())
        return f"{metric_name}#{ts}#{dim_str}"

# Usage examples
designer = RowKeyDesigner()

# Time series
ts_key = designer.time_series_key("sensor_123", datetime.now())
# Output: sensor_123#9999990123

# User activity
activity_key = designer.user_activity_key("user_456", "login", datetime.now())
# Output: 42#user_456#login#9999990123

# Composite
comp_key = designer.composite_key(["order", "user_123", "2024-01-15"])
# Output: order#user_123#2024-01-15

# Metrics
metric_key = designer.metric_key("cpu_usage", datetime.now(), {"host": "server1", "region": "us-east"})
# Output: cpu_usage#1704374400#host=server1#region=us-east
```

### Batch Operations and Filters

**Advanced Batch Operations (Python)**:
```python
from google.cloud import bigtable
from google.cloud.bigtable import row_filters
from concurrent.futures import ThreadPoolExecutor

def batch_write_with_timestamp(table, rows_data):
    """Batch write with custom timestamps"""
    rows = []
    timestamp = datetime.utcnow()

    for data in rows_data:
        row = table.direct_row(data['key'])
        row.set_cell(
            data['family'],
            data['column'],
            data['value'],
            timestamp=timestamp
        )
        rows.append(row)

    # Batch commit with retry
    statuses = table.mutate_rows(rows)

    # Check for failures
    failed_rows = []
    for i, status in enumerate(statuses):
        if status.code != 0:
            failed_rows.append(rows_data[i])

    return failed_rows

def conditional_update(table, row_key, family, column, old_value, new_value):
    """Conditional update using check-and-mutate"""
    row = table.row(row_key)

    # Create filter to check current value
    filter = row_filters.ValueRangeFilter(
        start_value=old_value,
        end_value=old_value,
        inclusive_start=True,
        inclusive_end=True
    )

    # Conditional mutation
    row.set_cell(family, column, new_value)
    result = row.commit_modifications(filter_=filter)

    return result  # True if mutation applied, False otherwise

def read_with_complex_filter(table, start_key, end_key):
    """Read with complex filter chain"""
    # Create filter chain
    filter_chain = row_filters.RowFilterChain([
        # Only latest version
        row_filters.CellsColumnLimitFilter(1),
        # Only specific column family
        row_filters.FamilyNameRegexFilter('cf1'),
        # Only columns matching pattern
        row_filters.ColumnQualifierRegexFilter(b'metric_.*'),
        # Value range filter
        row_filters.ValueRangeFilter(start_value=b'0', end_value=b'100')
    ])

    row_set = bigtable.row_set.RowSet()
    row_set.add_row_range_from_keys(start_key=start_key, end_key=end_key)

    rows = table.read_rows(row_set=row_set, filter_=filter_chain)
    return list(rows)

def parallel_batch_read(table, row_keys, num_workers=10):
    """Parallel batch read for better performance"""
    def read_chunk(keys_chunk):
        row_set = bigtable.row_set.RowSet()
        for key in keys_chunk:
            row_set.add_row_key(key)

        return list(table.read_rows(row_set=row_set))

    # Split keys into chunks
    chunk_size = len(row_keys) // num_workers
    chunks = [row_keys[i:i + chunk_size] for i in range(0, len(row_keys), chunk_size)]

    # Read in parallel
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(read_chunk, chunks)

    # Flatten results
    all_rows = []
    for chunk_rows in results:
        all_rows.extend(chunk_rows)

    return all_rows
```

## Memorystore Integration (Redis/Memcached)

### Client Integration

**Redis Client (Python)**:
```python
import redis
import json
from datetime import timedelta

class RedisClient:
    def __init__(self, host, port=6379):
        self.client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True,
            health_check_interval=30
        )

    def set_value(self, key, value, ttl=None):
        """Set key-value with optional TTL"""
        if ttl:
            self.client.setex(key, ttl, json.dumps(value))
        else:
            self.client.set(key, json.dumps(value))

    def get_value(self, key):
        """Get value by key"""
        value = self.client.get(key)
        return json.loads(value) if value else None

    def delete_key(self, key):
        """Delete key"""
        self.client.delete(key)

    def set_hash(self, key, mapping, ttl=None):
        """Set hash map"""
        self.client.hset(key, mapping=mapping)
        if ttl:
            self.client.expire(key, ttl)

    def get_hash(self, key):
        """Get all hash fields"""
        return self.client.hgetall(key)

    def increment_counter(self, key, amount=1):
        """Increment counter"""
        return self.client.incrby(key, amount)

    def add_to_set(self, key, *values):
        """Add values to set"""
        self.client.sadd(key, *values)

    def get_set_members(self, key):
        """Get all set members"""
        return self.client.smembers(key)

    def push_to_list(self, key, *values):
        """Push values to list"""
        self.client.lpush(key, *values)

    def get_list_range(self, key, start=0, end=-1):
        """Get list range"""
        return self.client.lrange(key, start, end)

    def set_with_nx(self, key, value, ttl):
        """Set if not exists (distributed lock pattern)"""
        return self.client.set(key, value, ex=ttl, nx=True)
```

**Redis with Node.js**:
```javascript
const redis = require('redis');

class RedisClient {
    constructor(host, port = 6379) {
        this.client = redis.createClient({
            socket: {
                host: host,
                port: port,
                connectTimeout: 5000,
                keepAlive: 30000
            }
        });

        this.client.on('error', (err) => console.error('Redis error:', err));
        this.client.connect();
    }

    async setValue(key, value, ttl = null) {
        const stringValue = JSON.stringify(value);
        if (ttl) {
            await this.client.setEx(key, ttl, stringValue);
        } else {
            await this.client.set(key, stringValue);
        }
    }

    async getValue(key) {
        const value = await this.client.get(key);
        return value ? JSON.parse(value) : null;
    }

    async deleteKey(key) {
        await this.client.del(key);
    }

    async setHash(key, mapping, ttl = null) {
        await this.client.hSet(key, mapping);
        if (ttl) {
            await this.client.expire(key, ttl);
        }
    }

    async getHash(key) {
        return await this.client.hGetAll(key);
    }

    async incrementCounter(key, amount = 1) {
        return await this.client.incrBy(key, amount);
    }

    async addToSet(key, ...values) {
        await this.client.sAdd(key, values);
    }

    async getSetMembers(key) {
        return await this.client.sMembers(key);
    }

    async pushToList(key, ...values) {
        await this.client.lPush(key, values);
    }

    async getListRange(key, start = 0, end = -1) {
        return await this.client.lRange(key, start, end);
    }

    async setWithNX(key, value, ttl) {
        const result = await this.client.set(key, value, {
            EX: ttl,
            NX: true
        });
        return result === 'OK';
    }

    async close() {
        await this.client.quit();
    }
}

module.exports = RedisClient;
```

### Caching Patterns

**Cache-Aside Pattern (Python)**:
```python
import redis
import json
from functools import wraps

class CacheAside:
    def __init__(self, redis_client, db_client):
        self.cache = redis_client
        self.db = db_client

    def get_user(self, user_id):
        """Cache-aside pattern for user retrieval"""
        cache_key = f'user:{user_id}'

        # 1. Check cache
        cached = self.cache.get(cache_key)
        if cached:
            return json.loads(cached)

        # 2. Fetch from database
        user = self.db.get_user(user_id)

        if user:
            # 3. Store in cache (1 hour TTL)
            self.cache.setex(cache_key, 3600, json.dumps(user))

        return user

    def cache_decorator(self, ttl=3600, key_prefix=''):
        """Decorator for automatic caching"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key from function name and arguments
                cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

                # Check cache
                cached = self.cache.get(cache_key)
                if cached:
                    return json.loads(cached)

                # Execute function
                result = func(*args, **kwargs)

                # Cache result
                if result:
                    self.cache.setex(cache_key, ttl, json.dumps(result))

                return result
            return wrapper
        return decorator

# Usage
cache = CacheAside(redis_client, db_client)

@cache.cache_decorator(ttl=1800, key_prefix='product')
def get_product(product_id):
    return db.query(f"SELECT * FROM products WHERE id = {product_id}")
```

**Write-Through Pattern (Python)**:
```python
class WriteThroughCache:
    def __init__(self, redis_client, db_client):
        self.cache = redis_client
        self.db = db_client

    def update_user(self, user_id, user_data):
        """Write-through pattern: update DB and cache simultaneously"""
        # 1. Update database
        self.db.update_user(user_id, user_data)

        # 2. Update cache
        cache_key = f'user:{user_id}'
        self.cache.setex(cache_key, 3600, json.dumps(user_data))

        return user_data

    def delete_user(self, user_id):
        """Delete from both DB and cache"""
        # 1. Delete from database
        self.db.delete_user(user_id)

        # 2. Invalidate cache
        cache_key = f'user:{user_id}'
        self.cache.delete(cache_key)
```

**Write-Behind (Write-Back) Pattern (Python)**:
```python
import threading
import queue
import time

class WriteBehindCache:
    def __init__(self, redis_client, db_client, batch_size=100, flush_interval=5):
        self.cache = redis_client
        self.db = db_client
        self.write_queue = queue.Queue()
        self.batch_size = batch_size
        self.flush_interval = flush_interval

        # Start background writer
        self.writer_thread = threading.Thread(target=self._background_writer, daemon=True)
        self.writer_thread.start()

    def update_user(self, user_id, user_data):
        """Write to cache immediately, queue for DB write"""
        # 1. Update cache immediately
        cache_key = f'user:{user_id}'
        self.cache.setex(cache_key, 3600, json.dumps(user_data))

        # 2. Queue for database write
        self.write_queue.put(('update', user_id, user_data))

        return user_data

    def _background_writer(self):
        """Background thread to flush writes to database"""
        while True:
            batch = []
            try:
                # Collect batch
                while len(batch) < self.batch_size:
                    item = self.write_queue.get(timeout=self.flush_interval)
                    batch.append(item)
            except queue.Empty:
                pass

            # Flush batch to database
            if batch:
                self._flush_batch(batch)

    def _flush_batch(self, batch):
        """Flush batch of writes to database"""
        for operation, user_id, user_data in batch:
            if operation == 'update':
                self.db.update_user(user_id, user_data)
```

### Session Storage

**Session Management with Redis (Python)**:
```python
import redis
import json
import uuid
from datetime import timedelta

class SessionManager:
    def __init__(self, redis_client, ttl=1800):
        self.redis = redis_client
        self.ttl = ttl

    def create_session(self, user_id, session_data):
        """Create new session"""
        session_id = str(uuid.uuid4())
        session_key = f'session:{session_id}'

        session_data['user_id'] = user_id
        self.redis.setex(session_key, self.ttl, json.dumps(session_data))

        return session_id

    def get_session(self, session_id):
        """Get session data"""
        session_key = f'session:{session_id}'
        data = self.redis.get(session_key)

        if data:
            # Refresh TTL on access
            self.redis.expire(session_key, self.ttl)
            return json.loads(data)

        return None

    def update_session(self, session_id, updates):
        """Update session data"""
        session_key = f'session:{session_id}'
        current_data = self.get_session(session_id)

        if current_data:
            current_data.update(updates)
            self.redis.setex(session_key, self.ttl, json.dumps(current_data))
            return True

        return False

    def delete_session(self, session_id):
        """Delete session"""
        session_key = f'session:{session_id}'
        self.redis.delete(session_key)

# Usage with Flask
from flask import Flask, session, request
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='10.0.0.3', port=6379, decode_responses=True)
session_mgr = SessionManager(redis_client)

@app.route('/login', methods=['POST'])
def login():
    user_id = authenticate_user(request.json)
    session_id = session_mgr.create_session(user_id, {'ip': request.remote_addr})
    return {'session_id': session_id}

@app.route('/protected')
def protected():
    session_id = request.headers.get('X-Session-ID')
    session_data = session_mgr.get_session(session_id)

    if not session_data:
        return {'error': 'Unauthorized'}, 401

    return {'data': 'Protected resource', 'user_id': session_data['user_id']}
```

### Pub/Sub with Redis

**Publisher/Subscriber Pattern (Python)**:
```python
import redis
import json
import threading

class RedisPubSub:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.pubsub = self.redis.pubsub()

    def publish(self, channel, message):
        """Publish message to channel"""
        self.redis.publish(channel, json.dumps(message))

    def subscribe(self, channel, callback):
        """Subscribe to channel with callback"""
        self.pubsub.subscribe(**{channel: lambda msg: callback(json.loads(msg['data']))})

        # Start listener thread
        thread = self.pubsub.run_in_thread(sleep_time=0.001)
        return thread

    def pattern_subscribe(self, pattern, callback):
        """Subscribe to channels matching pattern"""
        self.pubsub.psubscribe(**{pattern: lambda msg: callback(json.loads(msg['data']))})
        thread = self.pubsub.run_in_thread(sleep_time=0.001)
        return thread

# Usage
redis_client = redis.Redis(host='10.0.0.3', port=6379, decode_responses=True)
pubsub = RedisPubSub(redis_client)

# Publisher
def publish_order_event(order_id, event_type, data):
    pubsub.publish(f'orders:{order_id}', {
        'event_type': event_type,
        'data': data
    })

# Subscriber
def handle_order_event(message):
    print(f"Received order event: {message}")

listener = pubsub.subscribe('orders:*', handle_order_event)
```

## Pub/Sub Integration

### Publisher/Subscriber Patterns

**Basic Pub/Sub (Python)**:
```python
from google.cloud import pubsub_v1
import json
from concurrent import futures

class PubSubClient:
    def __init__(self, project_id):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish_message(self, topic_id, message_data, attributes=None):
        """Publish message to topic"""
        topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Convert message to bytes
        message_bytes = json.dumps(message_data).encode('utf-8')

        # Publish with attributes
        future = self.publisher.publish(
            topic_path,
            message_bytes,
            **(attributes or {})
        )

        # Wait for publish to complete
        message_id = future.result()
        print(f"Published message ID: {message_id}")
        return message_id

    def publish_batch(self, topic_id, messages):
        """Batch publish messages"""
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        publish_futures = []

        for message_data in messages:
            message_bytes = json.dumps(message_data).encode('utf-8')
            future = self.publisher.publish(topic_path, message_bytes)
            publish_futures.append(future)

        # Wait for all to complete
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
        message_ids = [f.result() for f in publish_futures]
        return message_ids

    def subscribe(self, subscription_id, callback):
        """Subscribe to messages"""
        subscription_path = self.subscriber.subscription_path(
            self.project_id,
            subscription_id
        )

        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=callback
        )

        print(f"Listening for messages on {subscription_path}")
        return streaming_pull_future

# Usage
pubsub = PubSubClient('my-project')

# Publish
pubsub.publish_message('orders', {
    'order_id': '12345',
    'user_id': 'user123',
    'total': 99.99
}, attributes={'priority': 'high'})

# Subscribe
def message_callback(message):
    try:
        data = json.loads(message.data.decode('utf-8'))
        print(f"Received: {data}")
        message.ack()
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

future = pubsub.subscribe('orders-sub', message_callback)
```

**Pub/Sub with Node.js**:
```javascript
const {PubSub} = require('@google-cloud/pubsub');

class PubSubClient {
    constructor(projectId) {
        this.pubsub = new PubSub({projectId});
    }

    async publishMessage(topicName, messageData, attributes = {}) {
        const topic = this.pubsub.topic(topicName);
        const messageBuffer = Buffer.from(JSON.stringify(messageData));

        const messageId = await topic.publishMessage({
            data: messageBuffer,
            attributes: attributes
        });

        console.log(`Message ${messageId} published`);
        return messageId;
    }

    async publishBatch(topicName, messages) {
        const topic = this.pubsub.topic(topicName);

        const publishPromises = messages.map(msg => {
            const buffer = Buffer.from(JSON.stringify(msg));
            return topic.publishMessage({data: buffer});
        });

        const messageIds = await Promise.all(publishPromises);
        return messageIds;
    }

    subscribe(subscriptionName, messageHandler) {
        const subscription = this.pubsub.subscription(subscriptionName);

        subscription.on('message', async (message) => {
            try {
                const data = JSON.parse(message.data.toString());
                await messageHandler(data, message.attributes);
                message.ack();
            } catch (error) {
                console.error('Error processing message:', error);
                message.nack();
            }
        });

        subscription.on('error', (error) => {
            console.error('Subscription error:', error);
        });

        console.log(`Listening on subscription: ${subscriptionName}`);
        return subscription;
    }
}

// Usage
const pubsub = new PubSubClient('my-project');

// Publish
await pubsub.publishMessage('orders', {
    orderId: '12345',
    userId: 'user123',
    total: 99.99
}, {priority: 'high'});

// Subscribe
pubsub.subscribe('orders-sub', async (data, attributes) => {
    console.log('Received:', data);
    console.log('Attributes:', attributes);
});

module.exports = PubSubClient;
```

### Message Ordering

**Ordered Message Publishing (Python)**:
```python
from google.cloud import pubsub_v1

def publish_ordered_messages(project_id, topic_id, ordering_key):
    """Publish messages with ordering key"""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Enable message ordering
    publisher_options = pubsub_v1.types.PublisherOptions(
        enable_message_ordering=True
    )
    publisher = pubsub_v1.PublisherClient(publisher_options=publisher_options)

    for i in range(10):
        message_data = json.dumps({'sequence': i, 'data': f'message-{i}'})
        future = publisher.publish(
            topic_path,
            message_data.encode('utf-8'),
            ordering_key=ordering_key
        )
        print(f"Published message {i} with ordering key {ordering_key}")
        future.result()

# Subscribe with ordering
def subscribe_with_ordering(project_id, subscription_id):
    """Subscribe to ordered messages"""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received ordered message: {message.data}")
        message.ack()

    flow_control = pubsub_v1.types.FlowControl(max_messages=10)

    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback,
        flow_control=flow_control
    )

    return streaming_pull_future
```

### Dead Letter Topics

**Dead Letter Queue Configuration (Python)**:
```python
from google.cloud import pubsub_v1
from google.api_core import retry

def create_subscription_with_dead_letter(project_id, topic_id, subscription_id, dead_letter_topic_id):
    """Create subscription with dead letter topic"""
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    dead_letter_policy = pubsub_v1.types.DeadLetterPolicy(
        dead_letter_topic=dead_letter_topic_path,
        max_delivery_attempts=5
    )

    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "dead_letter_policy": dead_letter_policy,
                "ack_deadline_seconds": 60
            }
        )

    print(f"Created subscription with dead letter topic: {subscription.name}")
    return subscription

def process_dead_letter_messages(project_id, dead_letter_subscription_id):
    """Process messages from dead letter queue"""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, dead_letter_subscription_id)

    def callback(message):
        print(f"Dead letter message: {message.data}")
        print(f"Delivery attempts: {message.delivery_attempt}")

        # Log or alert on dead letter
        log_dead_letter(message)

        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    return streaming_pull_future
```

### Exactly-Once Delivery

**Exactly-Once Processing (Python)**:
```python
from google.cloud import pubsub_v1
from google.cloud import firestore

def subscribe_with_exactly_once(project_id, subscription_id):
    """Subscribe with exactly-once delivery enabled"""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Enable exactly-once delivery (requires subscription configuration)
    def callback(message):
        # Process with idempotency key
        process_message_idempotent(message)
        message.ack()

    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback
    )

    return streaming_pull_future

def process_message_idempotent(message):
    """Process message with idempotency check"""
    db = firestore.Client()
    message_id = message.message_id

    # Check if already processed
    doc_ref = db.collection('processed_messages').document(message_id)
    doc = doc_ref.get()

    if doc.exists:
        print(f"Message {message_id} already processed")
        return

    # Process message
    try:
        data = json.loads(message.data.decode('utf-8'))
        process_order(data)

        # Mark as processed
        doc_ref.set({
            'processed_at': firestore.SERVER_TIMESTAMP,
            'data': data
        })

        print(f"Message {message_id} processed successfully")
    except Exception as e:
        print(f"Error processing message: {e}")
        raise

def process_order(data):
    """Process order (business logic)"""
    print(f"Processing order: {data}")
```

### Streaming Pull

**Optimized Streaming Pull (Python)**:
```python
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

def streaming_pull_with_flow_control(project_id, subscription_id):
    """Streaming pull with flow control and error handling"""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        try:
            print(f"Received message: {message.data}")
            # Process message
            process_message(message.data)
            message.ack()
        except Exception as e:
            print(f"Error: {e}")
            message.nack()

    # Configure flow control
    flow_control = pubsub_v1.types.FlowControl(
        max_messages=100,  # Max outstanding messages
        max_bytes=10 * 1024 * 1024,  # Max 10 MB outstanding
        max_duration_per_lease_extension=60,  # Max lease extension
        max_lease_duration=600  # Max total lease time
    )

    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback,
        flow_control=flow_control
    )

    # Handle shutdown
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

    subscriber.close()

def process_message(data):
    """Process message data"""
    message_data = json.loads(data.decode('utf-8'))
    print(f"Processing: {message_data}")
```

## Data Integration Patterns

### ETL Patterns

**Extract, Transform, Load (Python)**:
```python
from google.cloud import storage, bigquery
import csv
import io

class ETLPipeline:
    def __init__(self, project_id):
        self.storage_client = storage.Client(project=project_id)
        self.bq_client = bigquery.Client(project=project_id)

    def extract_from_storage(self, bucket_name, blob_name):
        """Extract data from Cloud Storage"""
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Download as string
        csv_data = blob.download_as_text()

        # Parse CSV
        reader = csv.DictReader(io.StringIO(csv_data))
        return list(reader)

    def transform_data(self, records):
        """Transform data"""
        transformed = []

        for record in records:
            # Data cleaning and transformation
            transformed_record = {
                'user_id': record['id'],
                'email': record['email'].lower().strip(),
                'name': record['name'].title(),
                'signup_date': record['created_at'],
                'is_active': record['status'] == 'active'
            }
            transformed.append(transformed_record)

        return transformed

    def load_to_bigquery(self, dataset_id, table_id, records):
        """Load data to BigQuery"""
        table_ref = f"{self.bq_client.project}.{dataset_id}.{table_id}"

        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("email", "STRING"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("signup_date", "TIMESTAMP"),
                bigquery.SchemaField("is_active", "BOOLEAN"),
            ],
            write_disposition="WRITE_APPEND",
        )

        job = self.bq_client.load_table_from_json(
            records,
            table_ref,
            job_config=job_config
        )

        job.result()  # Wait for completion
        print(f"Loaded {len(records)} rows to {table_id}")

    def run_etl(self, source_bucket, source_blob, dataset_id, table_id):
        """Run complete ETL pipeline"""
        # Extract
        raw_data = self.extract_from_storage(source_bucket, source_blob)
        print(f"Extracted {len(raw_data)} records")

        # Transform
        transformed_data = self.transform_data(raw_data)
        print(f"Transformed {len(transformed_data)} records")

        # Load
        self.load_to_bigquery(dataset_id, table_id, transformed_data)
        print("ETL completed successfully")

# Usage
etl = ETLPipeline('my-project')
etl.run_etl('data-bucket', 'users/export.csv', 'analytics', 'users')
```

### Batch Processing

**Batch Data Processing (Python)**:
```python
from google.cloud import storage, firestore
from concurrent.futures import ThreadPoolExecutor, as_completed

class BatchProcessor:
    def __init__(self, project_id):
        self.storage_client = storage.Client(project=project_id)
        self.db = firestore.Client(project=project_id)

    def batch_import_to_firestore(self, bucket_name, prefix, batch_size=500):
        """Batch import files from Cloud Storage to Firestore"""
        bucket = self.storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        for blob in blobs:
            print(f"Processing {blob.name}")
            data = json.loads(blob.download_as_text())

            # Batch write to Firestore
            batch = self.db.batch()
            count = 0

            for record in data:
                doc_ref = self.db.collection('imports').document()
                batch.set(doc_ref, record)
                count += 1

                if count >= batch_size:
                    batch.commit()
                    batch = self.db.batch()
                    count = 0

            if count > 0:
                batch.commit()

            print(f"Imported {len(data)} records from {blob.name}")

    def parallel_batch_process(self, items, process_func, max_workers=10):
        """Process items in parallel batches"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {executor.submit(process_func, item): item for item in items}

            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    print(f"Processed {item}: {result}")
                except Exception as e:
                    print(f"Error processing {item}: {e}")
```

### Streaming Data Integration

**Real-time Streaming (Python)**:
```python
from google.cloud import pubsub_v1, bigquery
from google.cloud.bigquery import SchemaField
import json

class StreamingIntegration:
    def __init__(self, project_id):
        self.project_id = project_id
        self.subscriber = pubsub_v1.SubscriberClient()
        self.bq_client = bigquery.Client(project=project_id)

    def stream_pubsub_to_bigquery(self, subscription_id, dataset_id, table_id):
        """Stream Pub/Sub messages to BigQuery"""
        subscription_path = self.subscriber.subscription_path(
            self.project_id,
            subscription_id
        )

        table_ref = f"{self.project_id}.{dataset_id}.{table_id}"

        def callback(message):
            try:
                data = json.loads(message.data.decode('utf-8'))

                # Insert to BigQuery
                errors = self.bq_client.insert_rows_json(table_ref, [data])

                if not errors:
                    message.ack()
                else:
                    print(f"Errors inserting to BigQuery: {errors}")
                    message.nack()
            except Exception as e:
                print(f"Error processing message: {e}")
                message.nack()

        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=callback
        )

        print(f"Streaming from {subscription_id} to {table_id}")
        return streaming_pull_future
```

## Development Scenarios

### Scenario 1: E-Commerce Order Processing

**Complete Order Processing System**:
```python
from google.cloud import pubsub_v1, firestore, tasks_v2
import json

class OrderProcessingSystem:
    def __init__(self, project_id):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.db = firestore.Client()
        self.tasks_client = tasks_v2.CloudTasksClient()

    def create_order(self, user_id, items, total):
        """Create order with inventory check"""
        @firestore.transactional
        def create_order_transaction(transaction):
            # Check inventory for all items
            for item in items:
                product_ref = self.db.collection('products').document(item['product_id'])
                product = product_ref.get(transaction=transaction)

                if not product.exists:
                    raise ValueError(f"Product {item['product_id']} not found")

                available = product.get('inventory')
                if available < item['quantity']:
                    raise ValueError(f"Insufficient inventory for {item['product_id']}")

                # Update inventory
                transaction.update(product_ref, {
                    'inventory': available - item['quantity']
                })

            # Create order
            order_ref = self.db.collection('orders').document()
            order_data = {
                'user_id': user_id,
                'items': items,
                'total': total,
                'status': 'pending',
                'created_at': firestore.SERVER_TIMESTAMP
            }
            transaction.set(order_ref, order_data)

            return order_ref.id

        # Execute transaction
        transaction = self.db.transaction()
        order_id = create_order_transaction(transaction)

        # Publish order created event
        self.publish_order_event(order_id, 'created', {'user_id': user_id, 'total': total})

        # Schedule payment processing
        self.schedule_payment_task(order_id)

        return order_id

    def publish_order_event(self, order_id, event_type, data):
        """Publish order event to Pub/Sub"""
        topic_path = self.publisher.topic_path(self.project_id, 'order-events')

        message_data = {
            'order_id': order_id,
            'event_type': event_type,
            'data': data
        }

        future = self.publisher.publish(
            topic_path,
            json.dumps(message_data).encode('utf-8'),
            order_id=order_id,
            event_type=event_type
        )

        future.result()
        print(f"Published {event_type} event for order {order_id}")

    def schedule_payment_task(self, order_id):
        """Schedule async payment processing task"""
        parent = self.tasks_client.queue_path(
            self.project_id,
            'us-central1',
            'payment-queue'
        )

        task = {
            'http_request': {
                'http_method': tasks_v2.HttpMethod.POST,
                'url': f'https://myapp.com/process-payment',
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'order_id': order_id}).encode()
            }
        }

        response = self.tasks_client.create_task(
            request={'parent': parent, 'task': task}
        )
        print(f"Created payment task: {response.name}")

# Usage
order_system = OrderProcessingSystem('my-project')

order_id = order_system.create_order(
    user_id='user123',
    items=[
        {'product_id': 'prod1', 'quantity': 2, 'price': 29.99},
        {'product_id': 'prod2', 'quantity': 1, 'price': 49.99}
    ],
    total=109.97
)

print(f"Order created: {order_id}")
```

### Scenario 2: Real-time Analytics Dashboard

**Real-time Data Aggregation**:
```python
from google.cloud import firestore, pubsub_v1
import json
from datetime import datetime, timedelta

class AnalyticsDashboard:
    def __init__(self, project_id):
        self.project_id = project_id
        self.db = firestore.Client()
        self.subscriber = pubsub_v1.SubscriberClient()

    def aggregate_user_activity(self, user_id, activity_type):
        """Aggregate user activity in real-time"""
        # Update user activity counter
        stats_ref = self.db.collection('user_stats').document(user_id)

        stats_ref.set({
            f'activities.{activity_type}': firestore.Increment(1),
            'last_activity': firestore.SERVER_TIMESTAMP
        }, merge=True)

        # Update daily aggregates
        today = datetime.utcnow().strftime('%Y-%m-%d')
        daily_ref = self.db.collection('daily_stats').document(today)

        daily_ref.set({
            f'activities.{activity_type}': firestore.Increment(1),
            'total_users': firestore.Increment(1)
        }, merge=True)

    def subscribe_to_events(self, subscription_id):
        """Subscribe to activity events"""
        subscription_path = self.subscriber.subscription_path(
            self.project_id,
            subscription_id
        )

        def callback(message):
            try:
                data = json.loads(message.data.decode('utf-8'))
                self.aggregate_user_activity(
                    data['user_id'],
                    data['activity_type']
                )
                message.ack()
            except Exception as e:
                print(f"Error: {e}")
                message.nack()

        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=callback
        )

        return streaming_pull_future

    def get_dashboard_data(self):
        """Get current dashboard metrics"""
        # Get today's stats
        today = datetime.utcnow().strftime('%Y-%m-%d')
        daily_ref = self.db.collection('daily_stats').document(today)
        daily_stats = daily_ref.get()

        if daily_stats.exists:
            return daily_stats.to_dict()

        return {}
```

### Scenario 3: File Processing Pipeline

**Serverless File Processing**:
```python
from google.cloud import storage, firestore, pubsub_v1
import json

def process_uploaded_file(event, context):
    """Cloud Function triggered by Cloud Storage upload"""
    file_name = event['name']
    bucket_name = event['bucket']

    print(f"Processing file: {file_name} from bucket: {bucket_name}")

    # Download and process file
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Process based on file type
    if file_name.endswith('.csv'):
        process_csv_file(blob)
    elif file_name.endswith('.json'):
        process_json_file(blob)

    # Store metadata in Firestore
    db = firestore.Client()
    db.collection('processed_files').add({
        'file_name': file_name,
        'bucket': bucket_name,
        'processed_at': firestore.SERVER_TIMESTAMP,
        'size': event['size']
    })

    # Publish completion event
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('my-project', 'file-processed')
    publisher.publish(
        topic_path,
        json.dumps({'file_name': file_name}).encode('utf-8')
    )

def process_csv_file(blob):
    """Process CSV file"""
    import csv
    import io

    content = blob.download_as_text()
    reader = csv.DictReader(io.StringIO(content))

    db = firestore.Client()
    batch = db.batch()
    count = 0

    for row in reader:
        doc_ref = db.collection('csv_imports').document()
        batch.set(doc_ref, row)
        count += 1

        if count >= 500:
            batch.commit()
            batch = db.batch()
            count = 0

    if count > 0:
        batch.commit()

def process_json_file(blob):
    """Process JSON file"""
    content = blob.download_as_text()
    data = json.loads(content)

    db = firestore.Client()
    batch = db.batch()

    for item in data:
        doc_ref = db.collection('json_imports').document()
        batch.set(doc_ref, item)

    batch.commit()
```

## Exam Tips for Professional Cloud Developer

### Data Storage Service Selection

**Key Decision Factors**:

1. **Cloud SQL**:
   - Use for: Relational data, ACID transactions, existing MySQL/PostgreSQL apps
   - Exam tips: Know connection methods (proxy, private IP, Unix socket)
   - Remember: Connection pooling is critical for serverless
   - Common question: Migrating from on-premises RDBMS

2. **Cloud Spanner**:
   - Use for: Global transactions, horizontal scalability, strong consistency
   - Exam tips: Understand session management and transaction types
   - Remember: Higher cost than Cloud SQL
   - Common question: Multi-region, strongly consistent applications

3. **Firestore**:
   - Use for: Document data, real-time updates, mobile/web apps
   - Exam tips: Know query limitations and index requirements
   - Remember: Transactions limited to 500 documents
   - Common question: Real-time collaborative applications

4. **Bigtable**:
   - Use for: Time-series, IoT, analytical workloads, >1TB data
   - Exam tips: Row key design is critical for performance
   - Remember: Not good for small datasets or ad-hoc queries
   - Common question: High-throughput time-series data

5. **Cloud Storage**:
   - Use for: Unstructured data, backups, static assets
   - Exam tips: Know signed URLs, lifecycle policies, storage classes
   - Remember: Use resumable uploads for large files
   - Common question: User file uploads and static hosting

### Integration Patterns

**Pub/Sub Best Practices**:
- At-least-once delivery by default (plan for duplicates)
- Use ordering keys for ordered delivery within a key
- Dead letter topics for failed message handling
- Flow control prevents overwhelming subscribers
- Exactly-once delivery requires idempotency

**Caching Strategies**:
- Cache-aside: Most common, application controls cache
- Write-through: Cache updated with every write
- Write-behind: Async cache updates for performance
- TTL selection based on data staleness requirements
- Use Memorystore for session state in serverless

**Connection Pooling**:
- Always use for Cloud SQL in serverless environments
- Configure pool_size based on instance capacity
- Set pool_recycle to handle connection limits
- Use pool_pre_ping to detect stale connections
- Cloud SQL Proxy simplifies connection management

### Common Exam Scenarios

**Scenario**: Application needs to store user sessions
**Answer**: Use Memorystore (Redis) with appropriate TTL

**Scenario**: Process uploaded files asynchronously
**Answer**: Cloud Storage → Pub/Sub → Cloud Functions

**Scenario**: Ensure exactly-once order processing
**Answer**: Use Firestore transactions with idempotency keys

**Scenario**: Real-time inventory updates across regions
**Answer**: Cloud Spanner for global consistency

**Scenario**: Store and query IoT sensor data (millions/sec)
**Answer**: Bigtable with time-based row keys

**Scenario**: Connect Cloud Run to Cloud SQL securely
**Answer**: Use Cloud SQL Proxy or Private IP with VPC connector

### Performance Optimization

**Database Optimization**:
- Use indexes for frequently queried fields
- Implement connection pooling
- Use read replicas for read-heavy workloads
- Batch operations where possible
- Monitor query performance and slow queries

**Caching Optimization**:
- Cache expensive database queries
- Use appropriate TTL based on update frequency
- Implement cache warming for predictable traffic
- Monitor cache hit rates
- Use cache-aside for flexibility

**Storage Optimization**:
- Use parallel composite uploads for large files
- Implement resumable uploads with retry
- Stream large files instead of loading in memory
- Use signed URLs for direct client uploads
- Choose appropriate storage class for access patterns

### Security Best Practices

**Access Control**:
- Use service accounts with least privilege
- Enable VPC for private connectivity
- Use Cloud SQL Proxy for secure connections
- Implement signed URLs for temporary access
- Enable audit logging for compliance

**Data Protection**:
- Enable encryption at rest and in transit
- Use customer-managed encryption keys (CMEK) when required
- Implement data retention policies
- Sanitize and validate all inputs
- Use Secret Manager for credentials

### Error Handling and Retry

**Retry Strategies**:
```python
from google.api_core import retry

# Automatic retry for transient errors
@retry.Retry(predicate=retry.if_transient_error)
def query_with_retry():
    return client.query(sql).result()

# Custom retry logic
@retry.Retry(
    predicate=retry.if_exception_type(Exception),
    initial=1.0,
    maximum=60.0,
    multiplier=2.0,
    timeout=300.0
)
def operation_with_backoff():
    # Your operation
    pass
```

**Error Handling**:
- Implement exponential backoff for rate limits
- Use dead letter queues for failed messages
- Log errors with structured logging
- Monitor error rates and set alerts
- Implement circuit breakers for cascading failures

## Additional Resources

- [Cloud SQL Best Practices](https://cloud.google.com/sql/docs/postgres/best-practices)
- [Firestore Data Model](https://firebase.google.com/docs/firestore/data-model)
- [Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)
- [Memorystore Best Practices](https://docs.cloud.google.com/memorystore/docs/redis/memory-management-best-practices)
- [Bigtable Schema Design](https://cloud.google.com/bigtable/docs/schema-design)
- [Cloud Spanner Best Practices](https://docs.cloud.google.com/spanner/docs/sql-best-practices)
- [Professional Cloud Developer Exam Guide](https://cloud.google.com/certification/cloud-developer)

## Key terms

- **Cloud Storage** - the Google Cloud object storage service for unstructured data, organised in buckets.
- **Firestore** - a Google Cloud serverless NoSQL document database.
- **Cloud Spanner** - a Google Cloud relational database that offers horizontal scaling and strong consistency across regions.
- **Bigtable** - a Google Cloud wide-column NoSQL database for large, low-latency analytical and operational workloads.
- **Memorystore** - the Google Cloud managed in-memory caching service for Redis and Memcached.
- **Pub/Sub** - the Google Cloud messaging service that decouples senders from receivers using topics and subscriptions.
- **Dead-letter topic** - a Pub/Sub topic that receives messages that could not be delivered after a set number of attempts.

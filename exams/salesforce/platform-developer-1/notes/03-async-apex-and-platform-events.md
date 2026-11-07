# 03 - Async Apex and Platform Events

When sync Apex isn't enough: long-running, callouts in trigger context, scheduled, large-volume.

## Decision matrix

| Need | Tool |
|---|---|
| Quick fire-and-forget callout / DML after current transaction | `@future` |
| Pass complex types or chain jobs | Queueable |
| Process millions of records | Batch |
| Run on a schedule | Schedulable (often kicks off Batch) |
| React to events from any source (UI, API, Apex, Flow) | Platform Events |
| Big object batch | Batch with custom iterable |

---

## Future Methods

```apex
public class MyClass {
    @future
    public static void sendNotification(Set<Id> userIds) {
        // ...
    }

    @future(callout=true)
    public static void doHttpCallout(String url) {
        Http h = new Http();
        HttpRequest req = new HttpRequest();
        req.setEndpoint(url);
        req.setMethod('GET');
        HttpResponse res = h.send(req);
    }
}

// Call:
MyClass.sendNotification(new Set<Id>{userId1, userId2});
```

### Constraints

- Must be `static`
- Must return `void`
- Args: only primitives, collections of primitives, Lists/Maps of primitives. **No sObjects** (use IDs and re-query in the future method).
- Cannot call from another @future method
- Cannot call from Batch's execute / Visualforce constructor
- 50 future calls per transaction
- 250,000 / day org-wide

### When to use

- HTTP callout from a trigger (sync triggers can't make callouts)
- Decouple slow downstream from current transaction
- Higher governor limits (some limits double for async)

---

## Queueable Apex

The modern @future replacement.

```apex
public class MyQueueable implements Queueable {
    private List<Id> recordIds;

    public MyQueueable(List<Id> ids) {
        this.recordIds = ids;
    }

    public void execute(QueueableContext context) {
        // ... can pass sObjects/custom types in constructor
        // Can chain by enqueueing another job
        if (someCondition) {
            System.enqueueJob(new AnotherQueueable());
        }
    }
}

// Call:
Id jobId = System.enqueueJob(new MyQueueable(ids));
```

### Properties

- Pass complex objects (sObjects, custom classes) via constructor / instance vars
- Chain unlimited jobs (each `execute` can enqueue more)
- 50 jobs per transaction
- 250,000 / day
- Implement `Database.AllowsCallouts` for HTTP callouts

### Queueable + callout

```apex
public class MyJob implements Queueable, Database.AllowsCallouts {
    public void execute(QueueableContext ctx) {
        // HTTP callout allowed here
    }
}
```

---

## Batch Apex

Process millions of records in chunks.

```apex
public class AccountUpdateBatch implements Database.Batchable<sObject> {

    public Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator('SELECT Id, Industry FROM Account WHERE Industry = null');
    }

    public void execute(Database.BatchableContext bc, List<Account> scope) {
        for (Account a : scope) {
            a.Industry = 'Other';
        }
        update scope;
    }

    public void finish(Database.BatchableContext bc) {
        // Send completion email
    }
}

// Run:
Database.executeBatch(new AccountUpdateBatch(), 200);  // batch size 200 (default)
```

### Properties

- `start()` returns QueryLocator (50M record max) or Iterable
- `execute()` runs once per batch (default 200 records, max 2,000)
- `finish()` runs once at end (good for notifications, follow-up jobs)
- 5 concurrent batch jobs per org
- 250,000 batch executions per day org-wide

### Stateful batch

```apex
public class MyBatch implements Database.Batchable<sObject>, Database.Stateful {
    Integer counter = 0;  // preserved across batches

    public Database.QueryLocator start(...) { }
    public void execute(...) { counter++; }
    public void finish(...) { System.debug(counter); }
}
```

`Database.Stateful` preserves member variables across batch executions; otherwise, instance vars are reset per batch.

### Batch + callout

```apex
public class MyBatch implements Database.Batchable<sObject>, Database.AllowsCallouts {
    // Callouts allowed in execute()
}
```

---

## Schedulable Apex

```apex
public class NightlyBatchScheduler implements Schedulable {
    public void execute(SchedulableContext ctx) {
        Database.executeBatch(new AccountUpdateBatch());
    }
}

// Schedule:
String cron = '0 0 2 * * ?';  // every day at 2:00 AM
System.schedule('Nightly Account Update', cron, new NightlyBatchScheduler());
```

Cron syntax: `seconds minutes hours dayOfMonth month dayOfWeek [year]`.

---

## Platform Events

Pub/sub for event-driven architecture across Apex, Flow, external systems, LWC.

### Define an event

Like a custom object: `My_Event__e` (suffix `__e`). Add custom fields.

### Publish from Apex

```apex
My_Event__e evt = new My_Event__e(Account_Id__c=accId, Reason__c='Stage Changed');
Database.SaveResult sr = EventBus.publish(evt);
```

### Subscribe in Apex (trigger on the event)

```apex
trigger MyEventTrigger on My_Event__e (after insert) {
    for (My_Event__e evt : Trigger.new) {
        // React
    }
}
```

### Subscribe in LWC

```javascript
import { subscribe, unsubscribe, onError } from 'lightning/empApi';
this.subscription = await subscribe('/event/My_Event__e', -1, callback);
```

### Subscribe in Flow

Use a Platform Event-Triggered Flow.

### Use cases

- Decouple parts of your app
- Cross-org integration via Streaming API
- Real-time UI updates in LWC
- Replace tightly-coupled trigger logic

---

## Choosing async type

| Scenario | Tool |
|---|---|
| Trigger needs to call an HTTP API | `@future(callout=true)` or Queueable with `Database.AllowsCallouts` |
| Trigger needs to update unrelated records | After-insert/update Trigger directly (or @future to defer) |
| Need to process all 5M Accounts | Batch |
| Need to run something every Monday at 9 AM | Schedulable + Batch |
| Need to chain N async jobs | Queueable, enqueueing the next from `execute()` |
| Pub/sub events across systems | Platform Events |

---

## Common exam triggers

- "Trigger needs HTTP callout" → @future(callout=true) or Queueable
- "Process 10 million records nightly" → Schedulable + Batch
- "Pass an sObject to async" → Queueable (future doesn't accept sObjects)
- "Chain jobs together" → Queueable with enqueueJob in execute
- "Real-time event from LWC to Apex" → Platform Event
- "Decouple slow downstream from current save" → @future or Queueable
- "Track progress across batches" → `Database.Stateful` interface
- "Run logic at exactly 2 AM daily" → Schedulable with CRON expression

## Key terms

- **Future method** - an Apex method marked `@future` that runs asynchronously when system resources are free.
- **Queueable Apex** - an asynchronous Apex class that can take complex types as input and be chained to another job.
- **Batch Apex** - an Apex class that processes large record sets in chunks, each chunk running as its own transaction.
- **Schedulable Apex** - an Apex class that runs at a set time using the Schedulable interface.
- **Platform event** - a custom event message used for event-driven communication between Salesforce and external systems.

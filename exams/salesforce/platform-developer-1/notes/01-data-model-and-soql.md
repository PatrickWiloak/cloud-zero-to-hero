# 01 - Data Model and SOQL/SOSL

## Object model

Salesforce has standard objects (Account, Contact, etc.) and custom objects (`__c` suffix). Both behave the same way to Apex.

### sObject in Apex

```apex
Account a = new Account(Name='Acme');
insert a;
System.debug(a.Id);  // populated after insert

// Generic sObject
sObject s = a;
String name = (String) s.get('Name');
```

### Field references

- Direct: `account.Name`
- Custom: `account.MyField__c` (note `__c` suffix)
- Relationship: `account.Owner.Name` (one level up)
- Custom relationships: `account.MyParent__r.Name` (`__r` for relationship suffix)

---

## SOQL (Salesforce Object Query Language)

SQL-like, type-safe in Apex.

### Basic queries

```apex
// Static query
List<Account> accs = [SELECT Id, Name, Industry FROM Account
                       WHERE Industry = 'Technology'
                       LIMIT 10];

// Bind variables (preferred over string concat)
String industry = 'Technology';
List<Account> accs2 = [SELECT Id FROM Account WHERE Industry = :industry];

// Dynamic SOQL (string)
String query = 'SELECT Id, Name FROM Account WHERE Industry = \'' + industry + '\'';
List<Account> accs3 = Database.query(query);  // SOQL injection risk - sanitize input!
```

### Relationships in SOQL

#### Child-to-parent (dot notation)

```sql
SELECT Id, Name, Account.Name, Account.Industry FROM Contact WHERE Account.Industry = 'Tech'
```

#### Parent-to-child (subquery)

```sql
SELECT Id, Name, (SELECT Id, FirstName FROM Contacts) FROM Account
```

For custom relationships, use `Children__r` (`__r` is the relationship API name):

```sql
SELECT Id, (SELECT Id FROM My_Children__r) FROM My_Parent__c
```

### WHERE clauses

```sql
WHERE Industry = 'Technology'
WHERE Industry IN ('Technology', 'Finance')
WHERE Name LIKE 'Acme%'
WHERE CreatedDate = LAST_N_DAYS:30
WHERE CreatedDate = LAST_QUARTER
WHERE CloseDate > TODAY
WHERE Active__c = TRUE
WHERE Industry = NULL  -- match nulls
```

### Ordering and limiting

```sql
ORDER BY Name ASC, CreatedDate DESC NULLS LAST
LIMIT 50
OFFSET 100  -- max OFFSET is 2000
```

### Aggregate queries

```sql
SELECT Industry, COUNT(Id), AVG(AnnualRevenue) total
FROM Account
GROUP BY Industry
HAVING COUNT(Id) > 10
```

Returns `AggregateResult` records:

```apex
for (AggregateResult ar : [SELECT Industry, COUNT(Id) cnt FROM Account GROUP BY Industry]) {
    System.debug(ar.get('Industry') + ': ' + ar.get('cnt'));
}
```

### Date / DateTime functions

- `CALENDAR_YEAR(CloseDate)`, `CALENDAR_MONTH(CloseDate)`, `CALENDAR_QUARTER(CloseDate)`
- `FISCAL_YEAR()`, `FISCAL_MONTH()`, `FISCAL_QUARTER()`
- `DAY_ONLY()` - extract date from datetime

### TYPEOF (polymorphic)

For polymorphic fields like `Owner` or `Who`/`What` on Task:

```sql
SELECT TYPEOF Owner WHEN User THEN Username, Email WHEN Group THEN Name END FROM Lead
```

### FOR VIEW / FOR REFERENCE

Update `RecentlyViewed` table when querying:

```sql
SELECT Id FROM Account FOR VIEW
```

### FOR UPDATE

Lock records during a transaction (prevent concurrent updates):

```sql
SELECT Id FROM Account WHERE Id = :accId FOR UPDATE
```

### SOQL governor limits

- 100 queries per sync transaction (200 async)
- 50,000 records per query
- Use `Database.QueryLocator` (Batch Apex) for >50K

---

## SOSL (Salesforce Object Search Language)

Multi-object full-text search:

```apex
List<List<sObject>> results = [FIND 'Acme*' IN ALL FIELDS
                                RETURNING Account(Name, Industry),
                                          Contact(LastName, Email),
                                          Lead(LastName)];

List<Account> accs = (List<Account>) results[0];
List<Contact> contacts = (List<Contact>) results[1];
```

### When to use SOSL vs SOQL

- **SOQL** - know the object, want filtered results
- **SOSL** - keyword search across multiple objects

SOSL is indexed-search backed; faster than SOQL for full-text matching but doesn't support all WHERE-style filters.

---

## sObject collections

### List

```apex
List<Account> accs = new List<Account>();
accs.add(a1);
for (Account a : accs) { }
Account first = accs[0];
Integer size = accs.size();
```

### Set

```apex
Set<Id> accountIds = new Set<Id>();
for (Account a : accs) {
    accountIds.add(a.Id);
}
```

### Map

```apex
Map<Id, Account> accMap = new Map<Id, Account>(accs);  // builds Map keyed by Id
Account a = accMap.get(someId);

// Map of Id to children
Map<Id, List<Contact>> contactsByAccountId = new Map<Id, List<Contact>>();
for (Contact c : contacts) {
    if (!contactsByAccountId.containsKey(c.AccountId)) {
        contactsByAccountId.put(c.AccountId, new List<Contact>());
    }
    contactsByAccountId.get(c.AccountId).add(c);
}
```

---

## Schema metadata in Apex

```apex
Schema.SObjectType type = Account.sObjectType;
Schema.DescribeSObjectResult describe = type.getDescribe();
Map<String, Schema.SObjectField> fields = describe.fields.getMap();
Schema.DescribeFieldResult fieldDescribe = fields.get('Industry').getDescribe();
List<Schema.PicklistEntry> entries = fieldDescribe.getPicklistValues();
```

Useful for dynamic Apex that adapts to schema changes.

---

## Common exam triggers

- "Query Accounts and their related Contacts in one go" → Subquery: `SELECT Id, (SELECT Id FROM Contacts) FROM Account`
- "Reference parent Account from Contact" → Dot: `SELECT AccountId, Account.Name FROM Contact`
- "Avoid SOQL governor limit on >50K records" → Batch Apex with QueryLocator
- "Search across Account/Contact/Lead by keyword" → SOSL
- "Aggregate sum of revenue by Industry" → `SELECT Industry, SUM(AnnualRevenue) FROM Account GROUP BY Industry`
- "Bulkify trigger" → Use Maps and Sets to gather IDs, do single SOQL outside loop
- "Lock records to prevent concurrent updates" → `SELECT ... FOR UPDATE`
- "Dynamic field reference" → Schema.getGlobalDescribe / DescribeSObjectResult

## Key terms

- **SOQL** - the Salesforce Object Query Language, used to read records from one object and its related objects.
- **SOSL** - the Salesforce Object Search Language, used to search text across multiple objects at once.
- **sObject** - the generic type for any Salesforce record, such as an Account or a custom object record.
- **Master-detail relationship** - a tight parent-child link where the child inherits sharing from the parent and is deleted with it.
- **Lookup relationship** - a loose link between two objects that does not make one depend on the other.

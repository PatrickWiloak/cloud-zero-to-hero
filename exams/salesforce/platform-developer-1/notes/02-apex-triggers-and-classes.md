# 02 - Apex: Triggers, Classes, Exceptions

## Apex class basics

```apex
public class AccountService {
    // Static method (class-level)
    public static void updateAllAccountsRevenue() { }

    // Instance method
    public void updateRevenue(List<Account> accs) { }

    // Constructor
    public AccountService() { }
}
```

### Access modifiers

- `public` - within namespace
- `private` - within class only
- `global` - cross-namespace (managed packages)
- `protected` - inheriting classes
- `virtual` - allows overriding
- `abstract` - must override
- `final` - cannot override

### Sharing modes

- `public with sharing class X` - enforces user's record sharing
- `public without sharing class X` - bypasses sharing (system context)
- `public inherited sharing class X` - inherits from caller; safer default for utility classes

Triggers default to `without sharing` unless declared on a `with sharing` class. Most utility services use `with sharing` to respect user permissions.

---

## Apex Triggers

```apex
trigger AccountTrigger on Account (before insert, before update,
                                     after insert, after update,
                                     before delete, after delete, after undelete) {
    // Logic goes here
}
```

### Trigger context

- `Trigger.new` - List of new sObject versions (before/after insert/update; null on delete)
- `Trigger.old` - List of old sObject versions (before/after update/delete; null on insert/undelete)
- `Trigger.newMap` - Map<Id, sObject> of new records (after insert/update only since records have IDs)
- `Trigger.oldMap` - Map<Id, sObject> of old records (update/delete)
- Boolean flags: `Trigger.isBefore`, `isAfter`, `isInsert`, `isUpdate`, `isDelete`, `isUndelete`, `isExecuting`
- `Trigger.size` - record count
- `Trigger.operationType` - enum (BEFORE_INSERT, AFTER_UPDATE, etc.)

### Operation timing

| Operation | Use |
|---|---|
| **before insert** | Modify field on the record being inserted; validate before save |
| **before update** | Modify field on update before save; validate |
| **before delete** | Prevent deletion via `addError()` |
| **after insert** | Need the record's Id; create related records; integrate downstream |
| **after update** | Update related records; trigger workflows |
| **after delete** | Cleanup related data |
| **after undelete** | React to record restored from Recycle Bin |

### Best practices (memorize)

1. **One trigger per object** - use a dispatcher class with handlers per event
2. **Bulkify** - work with `Trigger.new` as a List, never assume single record
3. **No SOQL/DML inside loops** - aggregate IDs first, query outside, update in bulk
4. **Logic in handler classes** - keep triggers thin
5. **Recursion control** - static class flag to prevent re-entry
6. **Error handling** - `addError()` for validation; throw exception for fatal errors

### Bulkified pattern example

```apex
trigger ContactTrigger on Contact (after insert, after update) {
    Set<Id> accountIds = new Set<Id>();
    for (Contact c : Trigger.new) {
        if (c.AccountId != null) accountIds.add(c.AccountId);
    }

    // Single SOQL for all related records
    Map<Id, Account> accs = new Map<Id, Account>(
        [SELECT Id, Total_Contacts__c FROM Account WHERE Id IN :accountIds]
    );

    // Logic
    for (Contact c : Trigger.new) {
        if (c.AccountId != null) {
            Account a = accs.get(c.AccountId);
            a.Total_Contacts__c = (a.Total_Contacts__c == null ? 0 : a.Total_Contacts__c) + 1;
        }
    }

    // Single DML
    update accs.values();
}
```

### Trigger handler pattern

```apex
trigger AccountTrigger on Account (before insert, after update) {
    new AccountTriggerHandler().run();
}

public class AccountTriggerHandler {
    public void run() {
        if (Trigger.isBefore && Trigger.isInsert) beforeInsert(Trigger.new);
        if (Trigger.isAfter && Trigger.isUpdate) afterUpdate(Trigger.new, Trigger.oldMap);
    }

    private void beforeInsert(List<Account> newAccounts) {
        for (Account a : newAccounts) {
            if (a.Name == null) a.Name = 'Default';
        }
    }

    private void afterUpdate(List<Account> newAccs, Map<Id, Account> oldMap) {
        // ...
    }
}
```

---

## Recursion guard

Trigger recursion happens when DML inside a trigger fires the same trigger again.

```apex
public class TriggerHelper {
    public static Boolean accountTriggerRunning = false;
}

trigger AccountTrigger on Account (after update) {
    if (TriggerHelper.accountTriggerRunning) return;
    TriggerHelper.accountTriggerRunning = true;
    try {
        // Logic
    } finally {
        TriggerHelper.accountTriggerRunning = false;
    }
}
```

---

## Exception handling

```apex
try {
    insert new Account(Name=null);  // will throw
} catch (DmlException e) {
    System.debug(e.getMessage());
} catch (Exception e) {
    // catch-all
} finally {
    // cleanup
}
```

### Custom exceptions

```apex
public class MyAppException extends Exception {}

throw new MyAppException('Custom error');
```

Custom exceptions must `extend Exception`.

### Common Apex exceptions

- `DmlException` - DML failed
- `QueryException` - SOQL failed (e.g., zero rows when single expected)
- `LimitException` - hit a governor limit (cannot be caught and resumed)
- `NullPointerException`
- `TypeException` - type cast failure
- `SObjectException` - sObject misuse

### `addError()` for graceful failure in triggers

```apex
trigger AccountTrigger on Account (before delete) {
    for (Account a : Trigger.old) {
        if (a.Type == 'Critical') {
            a.addError('Cannot delete critical accounts.');
        }
    }
}
```

This blocks the operation and returns a user-friendly error - cleaner than throwing exceptions.

---

## Common exam triggers

- "Bulkify a trigger" → Use Maps/Sets, no SOQL/DML in loops
- "Modify field on the record being inserted" → before insert / before update
- "Need the new record's Id" → after insert (Id is populated)
- "Block deletion of critical records" → before delete with `addError()`
- "Trigger fires twice for one record" → recursion; add static flag guard
- "Multiple triggers on Account doing different things" → consolidate into one trigger + dispatcher pattern
- "Catch DML failure and continue" → `Database.insert(records, false)` returns SaveResult[] without throwing on partial failure
- "Custom error message" → `addError()` (in before-trigger context) or throw custom exception

## Key terms

- **Apex trigger** - code that runs before or after a record is inserted, updated, deleted or undeleted.
- **Before trigger** - a trigger that runs before records are saved, used to validate or change values on the records themselves.
- **After trigger** - a trigger that runs after records are saved, used to act on related records or on values set by the system.
- **Bulkification** - writing code to handle many records in one run instead of one at a time, to stay within governor limits.
- **Governor limits** - runtime limits that Salesforce enforces on Apex so that no one tenant uses too many shared resources.

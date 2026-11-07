---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 4 min
---

# Splunk Core Certified User Study Strategy

## Follow the weights

| Domain | Weight | Where to spend time |
|---|---:|---|
| Basic Searching | 22% | Time picker, results page, timeline, jobs, saving |
| Using Fields in Searches | 20% | Case rules, operators, sidebar |
| Search Language Fundamentals | 15% | Pipeline and five commands |
| Using Basic Transforming Commands | 15% | `top`, `rare`, `stats` |
| Creating Reports and Dashboards | 12% | Save, permissions, panels |
| Creating and Using Lookups | 6% | File, definition, automatic |
| Splunk Basics | 5% | Components and apps |
| Creating Scheduled Reports and Alerts | 5% | Types, triggers, throttling |

## Distinctions to own

- **Forwarder, indexer, search head**: collect, store, search.
- **Field names are case sensitive; values are not** in a plain search. `where` is case sensitive for strings.
- **`!=` versus `NOT`**: only `NOT` includes events missing the field.
- **`fields` versus `table`**: events with fewer fields versus a table.
- **`count` versus `dc`**, and **`values` versus `list`**.
- **`top` versus `rare`**: most versus least, ten by default, with percentages.
- **Report versus export**: a saved question versus a snapshot of an answer.
- **Lookup file versus lookup definition**, and **`OUTPUT` versus `OUTPUTNEW`**.
- **Scheduled report versus alert**: always delivers versus only on a condition.

## Reading the question

Entry-level questions are often a short description of a goal followed by four feature names. Restate the goal in your own words before reading the options, then pick the feature whose purpose matches. If two options both seem right, look for the word that separates them: "different", "least", "every", "overwrite", "only when".

## Practice honestly

The exam is on the product, so a few hours in a real instance beat many hours of reading. Rebuild each example in the notes by hand and look at what the interface does. If you cannot get an instance, the Splunk Search Tutorial pages show the screens and results.

# spark-streaming-sandbox
Sandbox fo Spark Streaming studies

## Setup and Running

1. Clone this repo
2. Install Docker ([Docs](https://docs.docker.com/install/))
3. Install all dependencies and build docker image with:
```
make docker-build
```
3. Run app with:
```
make run
```

## Comments on Development Process

- Disclaimer: Although it was given me a week to finish the task, those were very busy and often offline days, so, as I warned the recruiter, I had very little time to dedicate to this assessment.
- I had no prior experience with Spark (apart from minor tweaks in legacy scripts) or Spark Streaming/Structured Streaming, so the first step was to familiarize myself with the technology and concepts.
- I chose Python over Scala so I wouldn't spend time learning another language.
- The first task was completed almost immediately. On the following ones, the hard part was understanding how to manipulate the data under the restrictions of the streaming API and how to use `sinks` and the `foreachbatch` function to write to the filesystem.
- I've used a "pseudo-randomized" timestamp generator UDF to emulate the arrival of events over a few seconds, so I could slide a window over it. This feels hacky and there probably is a simpler solution for sliding windows over "untimestamped" event streams, but time was short and I thought that this solution would serve the demonstration purpose.
- I've outlined the unit tests I intended to implement but didn't have the time to actually do it. Some refactoring of the code would be needed, further separating the code into smaller, testable units (Context creation, loading, processing, persisting...).

Thank you for your time and consideration.

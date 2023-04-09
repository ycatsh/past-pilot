# Past Pilot
An Ed-tech platform for managing academic resources like past papers, with private key-based storage and NLP integration for easy search for similar or specific questions.  

## Funcionality
- Past Pilot is a web app that allows users to upload, download, and share academic resources, such as past papers.
- It uses private key-based storage and integrates NLP to help users find relevant information from their resources.
- It enables users to find similar type of questions and scan through their friends resources. 
- We used [sentence-transformers](https://www.sbert.net/) to calculate text similarity between the user inputs and resources.

## End-User Flow Chart
```mermaid
graph TD
    s([Start])-->ut{User Type}
    ut --> rec1(Signed Out)
    ut --> rec2(Signed In)
    rec1 --> p1[/User Input for NLP search using shared keys/]
    rec2 --> st{Manage Resources or NLP Search}
    st -->|NLP Search|p1
    st -->|Manage Resources|st2{Modify or Access PDFs}
    st2 -->|Access|p2[/User Input key to find or view resources/]
    st2 -->|Modify|p3[/User Input PDF files to upload or delete PDFs/]
    p1 -->e([End])
    p2 -->|Sign Out|e
    p3 -->|Sign Out|e
```

Video Demonstration: https://youtu.be/FDsQhK5odS0

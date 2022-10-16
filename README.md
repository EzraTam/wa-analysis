# wa-analysis

Services for WhatsApp chat data ingest and processing those. Emphasize is on Indonesian language.

Implemented functionalities:
- Ingest: Transforming raw data to DF with columns time, author, and message
- Analysis Utils: Clean the data from certain objects and extract the eventually in a separate column
- Emoji analysis utils: Extract emojis from text, extract sentiment score based on them
- Process optimization utils: Utils for optimizing the computational performance. Yet implemented is parallel computing decorator

Functionalities to implement:
- Data cleaning from Indonesian colloquial words
- Indonesian language sentiment analysis

# AI-Research-Assistant

RAG Pipeline with a dataset of research papers, textbooks, and more used to help the user.

To use, simply use my link
https://research-frontend-pi.vercel.app/

The Grok api will stall if you request too quickly so wait a second before requesting again

Previous queries are not saved meaning the model can't use it as context so be specific with your queries

The database contains some ML/Systems/Calculus/Math so keep your questions in that range

Or if youd like to host your own to make it more personalized

Get your PINE api key from Pinecone
Your Groq api key from
and the TG api key from Together

With this you can load the database on your own but some tips are:

Make sure your embedding dimensions match your vector dimensions

If hosting, do not host a model on your api backend, its too resource intensive

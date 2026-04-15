# Week 13 — AI Learning
Topic: Feature engineering
Started: 2026-04-14
Week date: 2026-03-30

---

Rough notes: 
- "Feature engineering": take raw data, understand the "important" parts of it that you'd want your model to act on, and convert it into a representation that models can work with easily (e.g., how I extracted the bigram features from the names dataset in my makemore project, and converted it into one-hot encoding)  
- types of features, obviously, vary based on data type: audio, text, video, images 
- feature engineering is a trial & error process 
- Modern deep learning automates feature engineering through a process called representation learning (or feature learning). Instead of human experts manually designing rules to extract information, deep neural networks learn to discover the most relevant patterns directly from raw data during training.

--- 

Feature engineering & relevance in the world of LLM-based generative AI: 

Feature engineering remains essential for GenAI and LLMs, but it has shifted toward context preparation and data quality.

* Numerical & Tabular Translation: Converting raw numbers into text-based relationships (like percentiles) helps LLMs process data more accurately.
* Context Engineering (RAG): Designing how data is chunked and metadata is tagged ensures the model retrieves the most relevant information.
* Prompt Precision: Strategic inputs reduce ambiguity, much like traditional features helped older models "see" patterns.
* Hybrid Systems: Traditional, feature-heavy models (like XGBoost) are still used alongside GenAI for speed and regulatory transparency.
* LLMs as Tools: LLMs are now frequently used to brainstorm and automate the creation of new features for other models.

--- 

Links: 
- Feature Engineering for AI: Transforming Raw Data into Predictions: https://www.youtube.com/watch?v=Bg3CjiJ67Cc 
- Feature Engineering | Applied Machine Learning, Part 1: https://www.youtube.com/watch?v=ABV2YS9jbzE 
- What is feature engineering | Feature Engineering Tutorial Python #1: https://www.youtube.com/watch?v=pYVScuY-GPk
- Intro to Feature Engineering with TensorFlow - Machine Learning Recipes #9: https://www.youtube.com/watch?v=d12ra3b_M-0
- Feature engineering vs Feature Learning (tips tricks 46): 
- https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/feature-engineering.html 

--- 

Things that seem important for a feature engineering platform 
- central feature store 
- data viz 
- PySDK 

--- 

TODO: 
- https://www.youtube.com/watch?v=WElBhXr9B7c

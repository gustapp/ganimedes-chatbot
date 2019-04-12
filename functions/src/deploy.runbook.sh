cd usp/projects/ganimedes-chatbot/functions/src/

cp -a usp/projects/ganimedes-chatbot/functions/src/artifacts/nltk_data/* nltk_data/

gcloud functions deploy course-suggestion \
  --entry-point get_course_suggestion \
  --region us-central1 \
  --runtime python37 \
  --trigger-http

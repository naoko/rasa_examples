import os
import json

from rasa_nlu.training_data import load_data
from rasa_nlu.evaluate import run_evaluation
from rasa_nlu.model import Trainer
from rasa_nlu import config


def pprint(o):
    # small helper to make dict dumps a bit prettier
    print(json.dumps(o, indent=2))


# loading the nlu training samples
training_data = load_data("data/nlu.md")

# trainer to educate our pipeline
trainer = Trainer(config.load("config/nlu_pipeline.yml"))

# train the model!
interpreter = trainer.train(training_data, verbose=True)

# store it for future use
model_directory = trainer.persist(
    "models/nlu", fixed_model_name="current")

print(">>> Running evaluation")
os.makedirs("reports", exist_ok=True)

error_report_path = "reports/errors.json"
if os.path.exists(error_report_path):
    os.unlink(error_report_path)
run_evaluation("data/nlu.md",
               model_directory,
               errors_filename="reports/errors.json")

if os.path.exists(error_report_path):
    print(f">>> See {error_report_path} "
          "for evaluation result")

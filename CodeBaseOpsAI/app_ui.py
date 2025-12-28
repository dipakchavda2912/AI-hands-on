import logging

import streamlit as st

from config import Env
from config import setup_logging
from main import Main
from utils import NodeOpsUtils

logger = logging.getLogger(__name__)
setup_logging()
Env.load_env()
main = Main()
main.init()

st.title("AI Repo Cloning Assistant")
user_query = st.header("Please allow to reclone the repository.")

actions = [
  {
    "label": "Clone Repository",
    "action": NodeOpsUtils.clone_repo,
    "status": "pending",
  },
  {
    "label": "Update Environment Variables",
    "action": NodeOpsUtils.set_env,
    "status": "pending",
  },
  {
    "label": "Update AWS region",
    "action": NodeOpsUtils.set_region,
    "status": "pending",
  },
]

if st.button("Allow"):
  for index, action in enumerate(actions):
    if action["status"] == "pending":
      progressingStatus = action["label"] + " in progress..."
      with st.spinner(progressingStatus):
        actions[index]["status"] = "in_progress"
        action["action"](main)
      st.success(action["label"] + " completed!")
      actions[index]["status"] = "completed"

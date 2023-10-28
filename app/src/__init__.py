from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from src.mapper import sqlite_mapper as sql

env_path = Path(__file__).resolve().parent.joinpath('../profiles/.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# add whitelist for CORS allow
with open(Path(__file__).resolve().parent.joinpath('../whitelist.txt'), 'r') as f:
    CORS(app, origins=f.read().split('\n'), methods=['OPTIONS', 'GET', 'POST'])

# DDL
sql.create_all()

# regist facade
from src.facade import sign as _

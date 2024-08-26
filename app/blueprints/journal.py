from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import journal
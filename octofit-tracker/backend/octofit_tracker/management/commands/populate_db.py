from django.core.management.base import BaseCommand
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activity.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Insert users
        users = [
            {"username": "thundergod", "email": "thundergod@mhigh.edu", "password": "thundergodpassword"},
            {"username": "metalgeek", "email": "metalgeek@mhigh.edu", "password": "metalgeekpassword"},
            {"username": "zerocool", "email": "zerocool@mhigh.edu", "password": "zerocoolpassword"},
            {"username": "crashoverride", "email": "crashoverride@mhigh.edu", "password": "crashoverridepassword"},
            {"username": "sleeptoken", "email": "sleeptoken@mhigh.edu", "password": "sleeptokenpassword"},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Insert team
        team = {"name": "Blue Team", "members": list(user_ids)}
        db.teams.insert_one(team)

        # Insert activities
        activities = [
            {"user_id": user_ids[0], "activity_type": "Cycling", "duration": 60},
            {"user_id": user_ids[1], "activity_type": "Crossfit", "duration": 120},
            {"user_id": user_ids[2], "activity_type": "Running", "duration": 90},
            {"user_id": user_ids[3], "activity_type": "Strength", "duration": 30},
            {"user_id": user_ids[4], "activity_type": "Swimming", "duration": 75},
        ]
        db.activity.insert_many(activities)

        # Insert leaderboard entries
        leaderboard = [
            {"user_id": user_ids[0], "score": 100},
            {"user_id": user_ids[1], "score": 90},
            {"user_id": user_ids[2], "score": 95},
            {"user_id": user_ids[3], "score": 85},
            {"user_id": user_ids[4], "score": 80},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Insert workouts
        workouts = [
            {"name": "Cycling Training", "description": "Training for a road cycling event"},
            {"name": "Crossfit", "description": "Training for a crossfit competition"},
            {"name": "Running Training", "description": "Training for a marathon"},
            {"name": "Strength Training", "description": "Training for strength"},
            {"name": "Swimming Training", "description": "Training for a swimming competition"},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data using pymongo.'))
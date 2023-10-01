# web3payment/models.py
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100, default='')
    symbol = models.CharField(max_length=10, default='')
    description = models.TextField(default='')
    token_symbol = models.CharField(max_length=10, default='')
    photos = models.TextField(default='')
    links = models.TextField(default='')
    goal = models.IntegerField(default=0)
    owner_address = models.TextField(default='')

    # Add the new fields with defaults
    totalFunds = models.IntegerField(default=0)
    actionTokensNum = models.IntegerField(default=0)
    tokenPrice = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    # Add other project-related fields

class User(models.Model):
    address = models.CharField(max_length=42)  # Ethereum address of the user
    balance = models.IntegerField(default=0)

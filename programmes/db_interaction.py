import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_user(pseudo, email, password, adresse, telephone):
    conn = get_db_connection()
    res = conn.execute('INSERT INTO users (pseudo, email, password, adresse, telephone) VALUES (?, ?, ?,?, ?)',(pseudo, email, password, adresse, telephone))
    conn.commit()
    conn.close()
    
def get_user(email, password):
    conn = get_db_connection()
    res = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?',(email, password)).fetchone()
    conn.commit()
    conn.close()
    
def get_recipes(recipe_ids):
    conn = get_db_connection()
    query = 'SELECT * FROM recettes WHERE id IN ({})'.format(','.join('?' for _ in recipe_ids))
    res = conn.execute(query, recipe_ids).fetchall()
    if not res:
        return []
    return res

def get_all_recipes_name () :
    conn = get_db_connection()
    res = conn.execute('SELECT titre FROM recettes').fetchall()
    conn.commit()
    conn.close()
    return res

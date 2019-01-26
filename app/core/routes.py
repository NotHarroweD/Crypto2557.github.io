import json
import os
import numpy as np
from datetime import datetime
from flask import (render_template, flash, redirect, url_for, 
    request, jsonify, current_app)

from app.core import bp

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@bp.route('/pets/', methods=['GET', 'POST'])
def pets():
    pet_priority_url = os.path.join(current_app.root_path, "static/json", "pet_priority.json")
    pet_priority = json.load(open(pet_priority_url))

    pets_url = os.path.join(current_app.root_path, "static/json", "pets.json")
    pets = json.load(open(pets_url))

    for key, item in pet_priority.items():
        pets[item]["priority"] = key

    pets_ordered = json.loads(json.dumps(dict([(pet, pets[pet]) for pet in sorted(pets, key=lambda d: int(pets[d]["priority"]))])))
    return render_template('pets.html', title='Pets', pets=pets_ordered, ceil=np.ceil)

@bp.route('/units/', methods=['GET', 'POST'])
def units():
    units_url = os.path.join(current_app.root_path, "static/json", "units.json")
    units = json.load(open(units_url))
    pets_url = os.path.join(current_app.root_path, "static/json", "pets.json")
    pets = json.load(open(pets_url))
    max_buffs = [max([len(unit["buffs"]) for key, unit in units.items() if(unit["rotation"] == i)]) for i in range(1, 14)]
    max_buffs.reverse()
    max_buffs = np.repeat(np.array(max_buffs), 
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], axis=0)
    max_add_buffs = [max([len(pets[unit["pet"]]["additional_buffs"]) for key, unit in units.items() if(unit["rotation"] == i)]) for i in range(1, 14)]
    max_add_buffs.reverse()
    max_add_buffs = np.repeat(np.array(max_add_buffs), 
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], axis=0)
    return render_template('units.html', title='Units', units=units, pets=pets, max_buffs=max_buffs, max_add_buffs=max_add_buffs)

@bp.route('/tickets/', methods=['GET', 'POST'])
def tickets():
    units_url = os.path.join(current_app.root_path, "static/json", "units.json")
    units = json.load(open(units_url))
    tickets_url = os.path.join(current_app.root_path, "static/json", "ticket_order.json")
    tickets = json.load(open(tickets_url))
    return render_template('tickets.html', title='Tickets', units=units, tickets=tickets)

@bp.route('/static/json/pets/<petid>.json', methods=['GET', 'POST'])
def get_pet(petid):
    pets_url = os.path.join(current_app.root_path, "static/json", "pets.json")
    pets = json.load(open(pets_url))
    return jsonify({"petid":petid, "pet": pets[petid.replace("_", " ")]})

@bp.route('/static/json/units/<unitid>.json', methods=['GET', 'POST'])
def get_unit(unitid):
    units_url = os.path.join(current_app.root_path, "static/json", "units.json")
    units = json.load(open(units_url))
    return jsonify(unit=units[unitid.replace("_", " ")])

@bp.route('/static/json/priority.json', methods=['GET', 'POST'])
def get_priority():
    pet_priority_url = os.path.join(current_app.root_path, "static/json", "pet_priority.json")
    pet_priority = json.load(open(pet_priority_url))
    return jsonify(priority=pet_priority)

@bp.route('/meta_progression/', methods=['GET', 'POST'])
def meta_progression():   
    metas_url = os.path.join(current_app.root_path, "static/json", "metas.json")
    metas = json.load(open(metas_url))
    units_url = os.path.join(current_app.root_path, "static/json", "units.json")
    units = json.load(open(units_url))
    return render_template('meta_progression.html', metas=metas, units=units)
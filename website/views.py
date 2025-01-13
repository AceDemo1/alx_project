from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, CarbonEmission
from  . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is to short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('notes.html', user=current_user)

@views.route('/cal', methods=['GET', 'POST'])
@login_required
def cal():
    result = None
    if request.method == 'POST':
        try:
            expression = request.form.get('expression')
            # Evaluate the expression safely
            result = eval(expression)
        except Exception as e:
            flash('Invalid calculation!', category='error')
            result = 'Error'
    
    return render_template('cal.html', result=result, user=current_user)

@views.route('/carbon-emission', methods=['GET', 'POST'])
@login_required
def carbon_emission():
    total_emission = None
    transportation = None
    energy = None
    diet = None
    waste = None
    if request.method == 'POST':
        try:
            # Get form data
            transportation = request.form.get('transportation', 0)
            energy = request.form.get('energy', 0)
            diet = request.form.get('diet', None)
            waste = request.form.get('waste', 0)

            # Check if at least one field is selected
            if not transportation and not energy and not waste and not diet:
                flash('At least one field must be selected.', category='error')
                return render_template('carbon-emission.html', total_emission=total_emission, user=current_user)

            # Initialize emissions
            transportation_emission = 0
            energy_emission = 0
            waste_emission = 0
            diet_emission = 0

            # Calculate emissions only for provided fields
            if transportation:
                transportation_emission = float(transportation) * 0.21 * 52  # km/week to kg/year
            
            if energy:
                energy_emission = float(energy) * 0.233 * 12  # kWh/month to kg/year
            
            if waste:
                waste_emission = float(waste) * 52  # kg/week to kg/year
            
            if diet:
                diet_emission = {
                    'vegan': 0.7,
                    'vegetarian': 1.2,
                    'omnivore': 2.5
                }.get(diet, 0) * 365  # Default to 0 if diet is not found

            # Total carbon emission
            total_emission = transportation_emission + energy_emission + diet_emission + waste_emission

            # Save to database if any emission is calculated
            if total_emission > 0:
                new_emission = CarbonEmission(
                    user_id=current_user.id,
                    transportation=transportation_emission,
                    energy=energy_emission,
                    diet=diet,
                    waste=waste_emission,
                    total_emission=total_emission
                )
                db.session.add(new_emission)
                db.session.commit()
                flash('Carbon emission calculated successfully!', category='success')
        except Exception as e:
            flash('Error in calculation. Please check your inputs.', category='error')
                                                         
    return render_template('carbon-emission.html', total_emission=total_emission, transportation=transportation, energy=energy, diet=diet, waste=waste, user=current_user)

@views.route('/carbon-history')
@login_required
def carbon_history():
    # Fetch all emissions for the logged-in user
    emissions = CarbonEmission.query.filter_by(user_id=current_user.id).order_by(CarbonEmission.date.desc()).all()
    return render_template('carbon-history.html', emissions=emissions, user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note.get('note_id')
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted successfully!', category='success')
        else:
            flash('You cannot delete this note', category='error')

    return jsonify({})

@views.route('/delete-emission', methods=['POST'])
def delete_emission():
    data = json.loads(request.data)
    emission_id = data.get('emission_id')
    data = CarbonEmission.query.get(emission_id)
    if data:
        if data.user_id == current_user.id:
            db.session.delete(data)
            db.session.commit()
            flash('Emission deleted successfully!', category='success')
        else:
            flash('You cannot delete this Emission', category='error')

    return jsonify({})
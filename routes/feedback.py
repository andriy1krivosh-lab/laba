from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import add_feedback, get_feedbacks

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET'])
def feedback_page():
    items = get_feedbacks()
    return render_template('feedback.html', items=items)

@feedback_bp.route('/feedback/add', methods=['POST'])
def feedback_add():
    name = request.form.get('name', 'Анонім')
    message = request.form.get('message', '')
    if not message.strip():
        flash('Повідомлення не може бути пустим', 'error')
        return redirect(url_for('feedback.feedback_page'))
    add_feedback(name, message)
    return redirect(url_for('feedback.feedback_page'))

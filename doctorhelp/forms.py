from flask import Markup
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from doctorhelp.models import User


fields_list = [ ("Allergist", "Allergist"),
                ("Anaesthesiologist", "Anaesthesiologist"),
                ("Andrologist", "Andrologist"),
                ("Cardiologist"," Cardiologist"),
                ("Cardiac Electrophysiologist","Cardiac Electrophysiologist"),
                ("Dermatologist","Dermatologist"),
                ("Emergency Room (ER) Doctors","Emergency Room (ER) Doctors"),
                ("Endocrinologist","Endocrinologist"),
                ("Epidemiologist","Epidemiologist"),
                ("Family Medicine Physician","Family Medicine Physician"),
                ("Gastroenterologist","Gastroenterologist"),
                ("Geriatrician","Geriatrician"),
                ("Hyperbaric Physician","Hyperbaric Physician"),
                ("Hematologist","Hematologist"),
                ("Hepatologist","Hepatologist"),
                ("Immunologist","Immunologist"),
                ("Infectious Disease Specialist","Infectious Disease Specialist"),
                ("Intensivist","Intensivist"), 
                ("Internal Medicine Specialist","Internal Medicine Specialist"),
                ("Oral Surgeon","Oral Surgeon"),
                ("Medical Examiner","Medical Examiner"),
                ("Medical Geneticist","Medical Geneticist"),
                ("Neonatologist","Neonatologist"),
                ("Nephrologist","Nephrologist"),
                ("Neurologist","Neurologist"),
                ("Neurosurgeon","Neurosurgeon"),
                ("Nuclear Medicine Specialist","Nuclear Medicine Specialist"),
                ("Obstetrician/Gynecologist (OB/GYN)","Obstetrician/Gynecologist (OB/GYN)"),
                ("Obstetrician/Gynecologist (OB/GYN)","Occupational Medicine Specialist"),
                ("Oncologist","Oncologist"),
                ("Ophthalmologist","Ophthalmologist"),
                ("Orthopedic Surgeon","Orthopedic Surgeon"),
                ("Otolaryngologist","Otolaryngologist"),
                ("Parasitologist","Parasitologist"),
                ("Pathologist","Pathologist"),
                ("Perinatologist","Perinatologist"),
                ("Periodontist","Periodontist"),
                ("Pediatrician","Pediatrician"),
                ("Physiatrist","Physiatrist"),
                ("Plastic Surgeon","Plastic Surgeon"),
                ("Psychiatrist","Psychiatrist"),
                ("Pulmonologist","Pulmonologist"),
                ("Radiologist","Radiologist"),
                ("Rheumatologist","Rheumatologist"),
                ("Sleep Disorders Specialist","Sleep Disorders Specialist"),
                ("Spinal Cord Injury Specialist","Spinal Cord Injury Specialist"),
                ("Sports Medicine Specialist","Sports Medicine Specialist"),
                ("Surgeon","Surgeon"),
                ("Thoracic Surgeon","Thoracic Surgeon"),
                ("Urologist","Urologist"),
                ("Vascular Surgeon","Vascular Surgeon"),
                ("Veterinarian","Veterinarian"),
                ("Palliative Care Specialist","Palliative Care Specialist"),
                ("Acupuncturist","Acupuncturist"),
                ("Audiologist","Audiologist"),
                ("Ayurvedic Practitioner","Ayurvedic Practitioner"),
                ("Chiropractor","Chiropractor"),
                ("Diagnostician","Diagnostician"),
                ("Homeopathic Doctor","Homeopathic Doctor"),
                ("Microbiologist","Microbiologist"),
                ("Naturopathic Doctor","Naturopathic Doctor"),
                ("Pharmacist","Pharmacist"),
                ("Physiotherapist","Physiotherapist"),
                ("Podiatrist/Chiropodist","Podiatrist/Chiropodist"),
                ("Registered Massage Therapist","Registered Massage Therapist")]

                

class InlineButtonWidget(object):
    html = """
    <button %s type="submit">%s</button>
    """

    def __init__(self, label, input_type='submit'):
        self.input_type = input_type
        self.label = label

    def __call__(self, **kwargs):
        param = []
        for key in kwargs:
            param.append(key + "=\"" + kwargs[key] + "\"")
        return Markup(self.html % (" ".join(param), self.label))

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    name = StringField('Full Name', validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("Male", "Male"),("Female", "Female"),("Other", "Other")], validators=[DataRequired()])
    dob = StringField("Date of Birth", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    submit = InlineButtonWidget('Sign Up')

    def validate_username(self, username):
        try:
            user = User.query.filter_by(username=username.data)[0]
        except:
            return
        raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        try:
            user = User.query.filter_by(email=email.data)[0]
        except:
            return
        raise ValidationError("That email is taken. Please choose a different one.")


class DoctorRegistrationForm(FlaskForm):
    fields = SelectMultipleField('Category', choices=fields_list, validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    submit = InlineButtonWidget('Sign Up')

    def validate_username(self, username):
        try:
            user = User.query.filter_by(username=username.data)[0]
        except:
            return
        raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        try:
            user = User.query.filter_by(email=email.data)[0]
        except:
            return
        raise ValidationError("That email is taken. Please choose a different one.")



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    doctor_or_patient = BooleanField('Remember Me')
    submit = InlineButtonWidget('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    fields = SelectMultipleField('Category', choices=fields_list, validators=[DataRequired()])
    anonymous = BooleanField('Would you like to remain anonymous?')
    submit = InlineButtonWidget('Post')


class CategorySearchForm(FlaskForm):
	category = SelectMultipleField('Select a category to search for.', choices=fields_list, validators=[DataRequired()])
	submit = InlineButtonWidget('Search')
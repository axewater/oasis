# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField, PasswordField, TextAreaField, RadioField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Email


class WhitelistForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add to Whitelist')

class EditProfileForm(FlaskForm):
    avatar = FileField('Profile Avatar', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    country = SelectField('Country', choices=[
        ('', 'Select a country'),
        ('NL', 'Netherlands'),
        ('US', 'United States'),
        ('GB', 'United Kingdom'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('X', 'Mars')
    ])
    about = TextAreaField('About me', validators=[Length(max=500)])

class SettingsForm(FlaskForm):
    openai_api_key = StringField('OpenAI API Key')
    gcloud_api_key = StringField('GCloud API Key')
    submit = SubmitField('Save')


class UserDetailForm(FlaskForm):
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')
    tts_engine = StringField('TTS Engine')
    speech_enabled = RadioField('Speech Enabled', choices=[('True', 'Enabled'), ('False', 'Disabled')])


class UserPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')


class ChatbotForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    systemprompt = TextAreaField('System Prompt', validators=[DataRequired()])
    avatarpath = FileField('Avatar Image', validators=[FileAllowed(['jpg', 'png'])])  # Removed 'DataRequired()'
    voicetype = SelectField('Voice Type', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    llm_model = SelectField('LLM Model', choices=[('gpt-3.5-turbo', 'GPT-3.5 Turbo'), ('gpt-4', 'GPT-4')], validators=[DataRequired()])
    tags = StringField('Tags (comma separated)', validators=[Optional()])
    rating = IntegerField('Initial Rating', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Save')

class NewsletterForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    recipients = StringField('Recipients')
    send = SubmitField('Send')

class EditUserForm(FlaskForm):

    name = SelectField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = StringField('Role', validators=[DataRequired()])
    state = RadioField('State', choices=[('1', 'Active'), ('0', 'Inactive')])
    tts_engine = SelectField('TTS Engine', choices=[('default', 'Default'), ('webspeech', 'WebSpeech'),
                                                    ('elevenlabs', 'Eleven Labs'), ('google', 'Google'),
                                                    ('amazon', 'Amazon'), ('azure', 'Azure')])
    quota_messages = IntegerField('Quota Messages', validators=[DataRequired(), NumberRange(min=0, max=999999)])
    avatarpath = StringField('Avatar Path', validators=[DataRequired()])
    country = SelectField('Country',
                          choices=[('netherlands', 'Netherlands'), ('germany', 'Germany'), ('belgium', 'Belgium'),
                                   ('france', 'France'), ('uk', 'UK'), ('usa', 'USA'), ('mars', 'Mars')])
    about = TextAreaField('About')
    submit = SubmitField('Save')
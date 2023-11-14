# modules/routes.py
import traceback
import openai, ast, uuid, json, random, requests, html, os, re
from config import Config
from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint, jsonify, session, abort, current_app, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from flask_mail import Message as MailMessage
from wtforms import StringField, PasswordField, SubmitField, FieldList, BooleanField
from wtforms.validators import DataRequired, Email, Length
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy import func, Integer, Text
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from modules import db, mail
from modules.forms import SettingsForm, ChatbotForm, UserPasswordForm, UserDetailForm, EditProfileForm, NewsletterForm, WhitelistForm, EditUserForm
from modules.models import User, Whitelist, Chatbot, Blacklist, Message, Favorite, Tag, Highscore

from uuid import uuid4
from tiktoken import get_encoding
from tiktoken import encoding_for_model
from openai.api_resources.abstract.api_resource import APIResource
from datetime import datetime, timedelta
from PIL import Image, ImageOps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from authlib.jose import jwt
from authlib.jose.errors import DecodeError


bp = Blueprint('main', __name__)
openai.api_key = Config.OPENAI_API_KEY
MAX_TOKENS = 3800
SYSTEM_PROMPT_TOKENS = 296
enc = encoding_for_model("gpt-3.5-turbo")
log_filename = "log_file.txt"
used_tokens = set()



# Define the RegistrationForm class
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    print("Route: / or /index")
    if current_user.is_authenticated:
        print("User is authenticated")
        return redirect(url_for('main.restricted'))
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter(func.lower(User.name) == func.lower(username)).first()
        if user is None or not user.check_password(request.form['password']):
            flash('Invalid username or password')
            return redirect(url_for('main.index'))
        login_user(user, remember=True)
        print(f"Logged in user: {user}")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.restricted')
        return redirect(next_page)
    return render_template('homepage.html', title='Persona Super Chat')

@bp.route('/favicon.ico')
def favicon():
    # send_from_directory = "/" # remove or rename this line
    favidir = "images"
    full_dir = os.path.join(current_app.static_folder, favidir) # store the full directory in a variable
    print(full_dir) # print the full directory
    return send_from_directory(full_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/chatbot_browser', methods=['GET'])
@login_required
def chatbot_browser():
    print("Route: /chatbot_browser")
    print("Chatbot_browser called")
    return render_template('chatbot_browser.html')



@bp.route('/api/chatbots', methods=['GET'])
@login_required
def get_chatbots():
    print("Route: /api/chatbots")
    tags = request.args.get('tags')
    if tags:
        tags = tags.split(',')
        print("Tags:", tags)
        chatbots = Chatbot.query.join(tags_association).join(Tag).filter(Tag.tag_name.in_(tags)).all()
    else:
        chatbots = Chatbot.query.all()
    return jsonify([chatbot.to_dict() for chatbot in chatbots])


@bp.route('/api/chatbots/<int:chatbot_id>/upvote', methods=['POST'])
@login_required
def upvote_chatbot(chatbot_id):
    print("Route: /api/chatbots/<int:chatbot_id>/upvote")
    chatbot = Chatbot.query.get(chatbot_id)
    if chatbot:
        chatbot.rating += 1
        db.session.commit()
        return jsonify({"status": "success", "message": "Upvoted successfully", "rating": chatbot.rating})
    else:
        return jsonify({"status": "error", "message": "Chatbot not found"}), 404

@bp.route('/api/chatbots/<int:chatbot_id>/downvote', methods=['POST'])
@login_required
def downvote_chatbot(chatbot_id):
    print("Route: /api/chatbots/<int:chatbot_id>/downvote")
    chatbot = Chatbot.query.get(chatbot_id)
    if chatbot:
        chatbot.rating -= 1
        db.session.commit()
        return jsonify({"status": "success", "message": "Downvoted successfully", "rating": chatbot.rating})
    else:
        return jsonify({"status": "error", "message": "Chatbot not found"}), 404



@bp.route('/api/chatbots/<int:id>', methods=['GET'])
@login_required
def get_chatbot(id):
    print(f"Route: /api/chatbots/{id}")
    print(f"api/chatbots/{id} called")
    chatbot = Chatbot.query.get_or_404(id)
    return jsonify(chatbot.to_dict())


@bp.route('/api/favorites', methods=['POST'])
@login_required
def create_favorite():
    print("Route: /api/favorites")
    user_id = current_user.id
    chatbot_id = request.json['chatbot_id']

    new_favorite = Favorite(user_id=user_id, chatbot_id=chatbot_id)
    db.session.add(new_favorite)
    db.session.commit()

    return new_favorite.to_dict(), 201

@bp.route('/api/favorites', methods=['GET'])
@login_required
def get_favorites():
    print("Route: /api/favorites")
    user_id = current_user.get_id()
    favorite_chatbots = [favorite.chatbot_id for favorite in Favorite.query.filter_by(user_id=user_id).all()]

    return jsonify(favorite_chatbots)

@bp.route('/api/favorites', methods=['DELETE'])
@login_required
def delete_favorite():
    print("Route: /api/favorites")
    data = request.get_json()
    user_id = current_user.get_id()
    chatbot_id = data.get('chatbot_id')

    favorite = Favorite.query.filter_by(user_id=user_id, chatbot_id=chatbot_id).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Deleted from favorites'}), 200
    else:
        return jsonify({'message': 'Favorite not found'}), 404


@bp.route('/chatbots/<int:id>', methods=['GET'])
@login_required
def chatbot_detail(id):
    print(f"Route: /chatbots/{id}")
    chatbot = Chatbot.query.get_or_404(id)
    is_favorite = Favorite.query.filter_by(user_id=current_user.id, chatbot_id=id).first() is not None
    return render_template('chatbot_detail.html', chatbot=chatbot, is_favorite=is_favorite)


@bp.route('/chatbots/<int:id>/delete', methods=['POST'])
@login_required
def delete_chatbot(id):
    print(f"Route: /chatbots/{id}/delete")
    if current_user.role != 'admin':
        abort(403)  # Forbidden
    chatbot = Chatbot.query.get(id)
    if chatbot:
        # Delete the avatar image associated with the bot
        avatar_path = chatbot.avatarpath
        if avatar_path:
            delete_avatar(avatar_path)

        chatbot.delete()
        return jsonify({'status': 'success', 'message': 'Chatbot deleted.'}), 200
    return jsonify({'status': 'failure', 'message': 'Chatbot not found.'}), 404


@bp.route('/chatroom/<int:id>')
@login_required
def chatroom(id):
    print(f"Route: /chatroom/{id}")
    user_id = current_user.id
    bot = Chatbot.query.get_or_404(id)
    speech_enabled = current_user.speech_enabled
    tts_engine = current_user.tts_engine
    avatarpath_thumbnail = url_for('static', filename=current_user.avatarpath.rsplit('.', 1)[0] + '_thumbnail.' +
                                                      current_user.avatarpath.rsplit('.', 1)[1])
    avatarpath = url_for('static', filename=bot.avatarpath)
    user_role = current_user.role


    print(f"#CHATROOM Loaded: User {user_id} Role {user_role} Bot #{id} Speech: {speech_enabled} TTS: {tts_engine}")
    print(f"#CHATROOM Voice type: {bot.voicetype}")
    messages = Message.query.filter_by(owner=user_id, bot_id=id).order_by(Message.order.asc()).all()
    thread_id = messages[0].thread if messages else None
    print(f"#CHATROOM Thread ID: {thread_id}")
    messages = [message.to_dict() for message in messages]


    chatbot_detail_url = url_for('main.chatbot_detail', id=bot.id)
    chatbot_edit_url = url_for('main.edit_chatbot', id=bot.id)
    # Generate the avatar HTML based on the user role
    if current_user.role == 'admin':
        avatar_html = f'<a href="{url_for("main.edit_chatbot", id=bot.id)}"><img class="avatar" src="{avatarpath}" alt="AI Avatar" title="{bot.name}"></a>'
    else:
        avatar_html = f'<a href="{url_for("main.chatbot_detail", id=bot.id)}"><img class="avatar" src="{avatarpath}" alt="AI Avatar" title="{bot.name}"></a>'
    return render_template('chatroom.html', title='Chatroom', bot=bot, messages=messages, voicetype=bot.voicetype,
                           thread_id=thread_id, speech_enabled=speech_enabled, tts_engine=tts_engine,
                           avatarpath_thumbnail=avatarpath_thumbnail,
                           avatarpath=avatarpath, user_role=user_role, chatbot_detail_url=chatbot_detail_url,
                           chatbot_edit_url=chatbot_edit_url, avatar_html=avatar_html)





@bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    try:
        print("#API/CHAT")
        user_message = html.escape(request.form['message'])  # Sanitize the user's message here
        bot_id = request.form['bot_id']
        thread_id = request.form.get('thread_id', str(uuid.uuid4()))
        user_id = current_user.id
        user = User.query.get(user_id)
        print(f"#API/CHAT POST values received : botid {bot_id}, thread {thread_id}, user {user_id}")
        # check if the user has exceeded their message quota
        print("#API/CHAT Checking message quota")
        if user.count_messages >= user.quota_messages:
            return jsonify(response='Sorry, you have reached your quota of '
                                    + str(user.quota_messages)
                                    + ', please go to your account page and upgrade your subscription',
                           thread_id=thread_id)

        print(f"#API/CHAT Checking for existing messages for user {user_id} bot {bot_id}")
        existing_message = Message.query.filter_by(owner=user_id, bot_id=bot_id).first()

        if existing_message:
            print(f"#API/CHAT messages found, setting current thread_id to the same")
            # if there is any existing message, use the same thread_id
            thread_id = existing_message.thread
        else:
            # if there are no messages, generate a new UUID
            print(f"#API/CHAT No existing messages found, generating new UUID")
            thread_id = str(uuid.uuid4())

        bot = Chatbot.query.get_or_404(bot_id)

        system_prompt = f"You are {bot.name}\n"
        system_prompt += f" - You will only answer like you are {bot.name}. Do not write explanations.\n"
        system_prompt += " - DO NOT BREAK CHARACTER, never reveal you are an AI language model.\n"
        system_prompt += " - Always write in talking style, not written style.\n"
        system_prompt += bot.systemprompt

        api_conversation = build_api_conversation(bot_id, thread_id, system_prompt, user_message)
        print("#API/CHAT bot_id:", bot_id)
        print("#API/CHAT thread_id:", thread_id)

        response = openai.ChatCompletion.create(
            model=bot.llm_model or 'gpt-3.5-turbo',
            messages=api_conversation
        )

        ai_message = response['choices'][0]['message']['content']

        message_order = Message.query.filter_by(bot_id=bot_id, thread=thread_id).count() + 1

        print(f"#API/CHAT Saving user message to the database. thread# {thread_id}")
        user_msg = Message(owner=current_user.id, content=user_message, role="user", bot_id=bot_id,
                           order=message_order, thread=thread_id)
        db.session.add(user_msg)

        message_order += 1
        user.count_messages += 1
        print(f"#API/CHAT Saving AI message to db. thread# {thread_id}")
        ai_msg = Message(owner=current_user.id, content=ai_message, role="ai", bot_id=bot_id, order=message_order,
                         thread=user_msg.thread)
        db.session.add(ai_msg)

        print("#API/CHAT Names and values being saved:")
        for attr, value in vars(ai_msg).items():
            print(f"{attr}: {value}")

        print("#API/CHAT Committing messages to the database...")
        db.session.commit()

        print(f"#API/CHAT responding thread id {thread_id}")
        return jsonify(response=ai_message, thread_id=ai_msg.thread)

    except Exception as e:
        print(f"#API/CHAT Error: {str(e)}")
        db.session.rollback()  # if any error occur rollback the transaction
        return jsonify(error=str(e))




@bp.route('/delete_thread', methods=['POST'])
@login_required
def delete_thread():
    data = request.get_json()
    thread_id = data.get('thread_id')
    print(f"#API/DELETE_THREAD : {thread_id}")
    try:
        Message.query.filter(Message.thread == thread_id).delete()
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})




@bp.route('/api/current_user_role', methods=['GET'])
@login_required
def get_current_user_role():
    print("Route: /api/current_user_role")
    return jsonify({'role': current_user.role}), 200



@bp.route('/api/check_username', methods=['POST'])
@login_required
def check_username():
    print("Route: /api/check_username")
    data = request.get_json()  # Get the JSON data from the request
    username = data.get('username')

    if not username:
        print(f"Check username: Missing username")
        return jsonify({"error": "Missing username parameter"}), 400
    print(f"Checking username: {username}")
    existing_user = User.query.filter(func.lower(User.name) == func.lower(username)).first()
    return jsonify({"exists": existing_user is not None})


@bp.route('/bot_generator', methods=['GET', 'POST'])
@login_required
def bot_generator():
    print("Route: /bot_generator")
    random_num = random.randint(1, 6)

    if request.method == 'POST':
        bot_name = request.form['bot_name']
        if not bot_name:
            flash('Please enter a bot name')
            return redirect(url_for('main.bot_generator'))

        systemprompt, error = generate_system_prompt(bot_name)

        if error:
            flash(error)
            return render_template('chatbot_generator.html', title='Bot Generator')

        session['bot_name'] = bot_name
        session['systemprompt'] = systemprompt
        return redirect(url_for('main.confirm_bot'))

    return render_template('chatbot_generator.html', random_num=random_num, title='Bot Generator')

@bp.route('/create_bot', methods=['POST'])
@login_required
def create_bot():
    print("Route: /create_bot")
    bot_name = request.form['bot_name']
    if not valid_bot_name(bot_name):
        flash('Invalid bot name. Use only letters, hyphens, or apostrophes.')
        return redirect(url_for('main.bot_generator'))

    sanitized_bot_name = re.sub('[\W_]+', '_', bot_name)
    avatar_path = "avatar/"+sanitized_bot_name+".jpg"
    session['avatar_path'] = avatar_path
    existing_bot = Chatbot.query.filter_by(name=bot_name).first()

    if existing_bot:
        flash('A bot with this name already exists.')
        return redirect(url_for('main.bot_generator'))

    flash('Sending ChatGPT API request...')
    try:
        systemprompt, error = generate_system_prompt(bot_name)

        if error:
            print(f"Error: {error}")
            flash(f"Error: {error}")
            return redirect(url_for('main.bot_generator'))

        print(f"ChatGPT API request: {bot_name}")
        # Parsing the JSON and forming the systemprompt text
        json_data = systemprompt

        systemprompt = f"You are {json_data['name']}\n- Only respond using the tone, manner and vocabulary of {json_data['name']}.\n- Do not write any explanations.\n{json_data['summary']}\n{json_data['famous_for']}\n{json_data['speaking_style']}\n{json_data['words_used']}\nYour life goal is : {json_data['life_goal']}\nYour personality type is : {json_data['personality_mbti']}"

        # Saving the gender to session for later use
        session['voicetype'] = json_data['gender']

        # search and replace
        # systemprompt = systemprompt.replace("I am", "You are")
        # systemprompt = systemprompt.replace(" I ", " You ")

        # Generate image and get the path
        avatar_path = generate_images(sanitized_bot_name)
        if avatar_path is None:
            print("Error generating image")
            flash("Error generating image")
            return redirect(url_for('main.bot_generator'))
        print("# Store bot information in the session")

        session['bot_name'] = bot_name
        session['systemprompt'] = systemprompt
        session['avatar_path'] = avatar_path

        print(f"Bot Name: {bot_name}")
        print(f"System Prompt: {systemprompt}")
        print(f"Avatar Path: {avatar_path}")
        flash('Bot information generated successfully!')
    except OperationalError:
        flash('There was a problem connecting to the database.')
    except IOError:
        flash('There was a problem with file operations.')
    except Exception as e:
        print(f"Unexpected error: {e}")
        flash('An unexpected error occurred.')
    except OperationalError:
        flash('There was a problem connecting to the database.')
    except IOError:
        flash('There was a problem with file operations.')
    except Exception as e:
        print(f"Unexpected error: {e}")
        flash('An unexpected error occurred.')
    return redirect(url_for('main.confirm_bot'))


@bp.route('/confirm_bot', methods=['GET', 'POST'])
@login_required
def confirm_bot():
    print("Route: /confirm_bot")
    bot_name = session.get('bot_name')
    systemprompt = session.get('systemprompt')
    voicetype = session.get('voicetype')
    avatar_path = session.get('avatar_path')

    return render_template('chatbot_confirm.html', title='Confirm Bot', bot_name=bot_name, systemprompt=systemprompt,
                           voicetype=voicetype, avatar_path=avatar_path)

@bp.route('/save_bot', methods=['POST'])
@login_required
def save_bot():
    print("Route: /save_bot")
    bot_name = session.get('bot_name')
    systemprompt = session.get('systemprompt')
    avatar_path = session.get('avatar_path')
    voicetype = session.get('voicetype')
    tags = session.get('tags', [])

    try:
        existing_bot = Chatbot.query.filter_by(name=bot_name).first()
        if existing_bot:
            flash('A bot with this name already exists.')
            return redirect(url_for('main.bot_generator'))

        # Create or get the tag instances
        tag_instances = []
        for tag_name in tags:
            tag_instance = Tag.query.filter_by(tag_name=tag_name).first()
            if not tag_instance:
                tag_instance = Tag(tag_name=tag_name)
                db.session.add(tag_instance)
                db.session.commit()

            tag_instances.append(tag_instance)

        new_bot = Chatbot(name=bot_name, systemprompt=systemprompt, avatarpath=avatar_path, voicetype=voicetype)
        new_bot.tags = tag_instances  # Associate tags with the bot

        db.session.add(new_bot)
        db.session.commit()

        flash(f'New Chatbot {bot_name} has been saved !')

        # Remove session data after successfully storing the bot.
        session.pop('bot_name', None)
        session.pop('systemprompt', None)
        session.pop('avatar_path', None)
        session.pop('voicetype', None)
        session.pop('tags', None)  # Don't forget to remove tags from the session as well!

    except Exception as e:
        flash('There was an error saving the bot.')
        print(f"Error: {e}")
        return redirect(url_for('main.bot_generator'))

    return redirect(url_for('main.bot_generator'))

@bp.route('/delete_avatar/<path:avatar_path>', methods=['POST'])
@login_required
def delete_avatar(avatar_path):
    print("Route: /delete_avatar")
    print("avatar_path:", avatar_path)

    # Get the full path of the avatar image
    full_avatar_path = os.path.join(current_app.static_folder, avatar_path)
    print("full_avatar_path:", full_avatar_path)

    # Check if the file exists
    if os.path.exists(full_avatar_path):
        # Delete the file
        os.remove(full_avatar_path)
        flash(f'Avatar image {full_avatar_path} deleted successfully!')
    else:
        flash(f'Avatar image {full_avatar_path} not found.')

    return redirect(url_for('main.bot_generator'))

@bp.route('/chatbots/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_chatbot(id):
    print("Route: /chatbots/edit")
    print("id:", id)

    if current_user.role != 'admin':
        print("CHATBOTEDIT: User role is not admin, access forbidden.")

        abort(403)  # Forbidden

    chatbot = Chatbot.query.get_or_404(id)
    form = ChatbotForm(obj=chatbot)

    if form.validate_on_submit():
        print("CHATBOTEDIT: form validation successful.")

        file = form.avatarpath.data
        if file and isinstance(file, FileStorage):
            old_avatarpath = chatbot.avatarpath
            old_thumbnailpath = os.path.splitext(old_avatarpath)[0] + '_thumbnail' + os.path.splitext(old_avatarpath)[1]
            filename = secure_filename(file.filename)
            uuid_filename = str(uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER_CHATBOTS'], uuid_filename)
            file.save(image_path)

            # Create square avatar
            img = Image.open(image_path)
            img = square_image(img, 500)
            img.save(image_path)

            # Create square thumbnail
            img = Image.open(image_path)
            img = square_image(img, 50)
            thumbnail_path = os.path.splitext(image_path)[0] + '_thumbnail' + os.path.splitext(image_path)[1]
            img.save(thumbnail_path)

            if old_avatarpath != 'avatars/default.jpg':
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_CHATBOTS'], os.path.basename(old_avatarpath)))
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_CHATBOTS'], os.path.basename(old_thumbnailpath)))
                except Exception as e:
                    print(f"Error deleting old avatar: {e}")
                    flash("Error deleting old avatar. Please try again.", 'error')

            chatbot.avatarpath = 'avatars/' + uuid_filename
        else:
            if not chatbot.avatarpath:
                chatbot.avatarpath = 'avatars/default.jpg'

        chatbot.name = form.name.data
        chatbot.systemprompt = form.systemprompt.data
        chatbot.voicetype = form.voicetype.data
        chatbot.llm_model = form.llm_model.data

        if form.tags.data:
            tag_list = form.tags.data.split(',')
            chatbot.tags = []
            for tag_name in tag_list:
                tag = Tag.query.filter_by(tag_name=tag_name.strip()).first()
                if not tag:
                    tag = Tag(tag_name=tag_name.strip())
                    db.session.add(tag)
                chatbot.tags.append(tag)

        form.tags.data = ','.join(tag.tag_name for tag in chatbot.tags)

        if form.rating.data is not None:
            chatbot.rating = form.rating.data
            print("Updated chatbot rating:", chatbot.rating)

        db.session.commit()
        print("Chatbot details updated successfully!")

        return redirect(url_for('main.chatbot_detail', id=id))

    form.tags.data = ', '.join(tag.tag_name for tag in chatbot.tags)
    return render_template('chatbot_edit.html', form=form, chatbot=chatbot)

@bp.route('/help')
def privacy():
    print("Route: /help")
    return render_template('help.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    print("Route: /register")

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Extract domain from email
            email_domain = form.email.data.split('@')[-1]
            print(f"Debug: Extracted domain - {email_domain}")

            # Replace wildcard * with SQL wildcard % in the whitelist entries
            whitelist = Whitelist.query.filter(Whitelist.email.like(f"%@{email_domain}")).first()
            if not whitelist:
                print(f"Debug: No matching whitelist entry found for - {form.email.data}")
                flash('Your email is not whitelisted.')
                return redirect(url_for('main.register'))

            print(f"Debug: Whitelist entry found - {whitelist.email}")

            existing_user = User.query.filter_by(name=form.username.data).first()
            if existing_user is not None:
                print(f"Debug: User already exists - {form.username.data}")
                flash('User already exists. Please Log in.')
                return redirect(url_for('main.register'))

            # Generate UUID and check for uniqueness
            user_uuid = str(uuid4())
            existing_uuid = User.query.filter_by(user_id=user_uuid).first()
            if existing_uuid is not None:
                print("Debug: UUID collision detected.")
                flash('An error occurred while registering. Please try again.')
                return redirect(url_for('main.register'))

            # Create a new User object with role set to a default value (e.g., 'user')
            user = User(
                user_id=user_uuid,
                name=form.username.data,
                email=form.email.data,
                role='user',
                created=datetime.utcnow()
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            print("Debug: New user registered successfully!")
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('main.index'))
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError occurred: {e}")
            flash('An error occurred while registering. Please try again.')

    return render_template('registration.html', title='Register', form=form)


@bp.route('/restricted')
@login_required
def restricted():
    print("Route: /restricted")
    return render_template('restricted_area.html', title='Restricted Area')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.restricted'))

    print("Route: /login")

    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter(func.lower(User.name) == func.lower(username)).first()
        if user is None or not user.check_password(request.form['password']):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))

        user.lastlogin = datetime.utcnow()
        db.session.commit()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.restricted')

        return redirect(next_page)

    return render_template('login.html', title='Log In')

@bp.route('/settings_account', methods=['GET', 'POST'])
@login_required
def account():
    print("Route: /settings_account")

    user = User.query.filter_by(id=current_user.id).first()
    form = UserDetailForm(speech_enabled=str(user.speech_enabled), tts_engine=user.tts_engine)
    print(f"User tts_engine: {user.tts_engine}")

    if form.validate_on_submit():
        print(f"Form tts_engine: {form.tts_engine.data}")

        user.tts_engine = form.tts_engine.data
        user.speech_enabled = form.speech_enabled.data == 'True'

        try:
            db.session.commit()
            print(f"User state after commit: tts_engine={user.tts_engine}, speech_enabled={user.speech_enabled}")

            flash('Account details updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error updating account details: {e}")
            flash('Failed to update account details. Please try again.', 'error')

        return redirect(url_for('main.account'))

    return render_template('settings_account.html', title='Account', form=form, user=user)

@bp.route('/settings_profile_edit', methods=['GET', 'POST'])
@login_required
def settings_profile_edit():
    print("Route: Settings profile edit")
    form = EditProfileForm()

    if form.validate_on_submit():
        file = form.avatar.data
        if file:
            old_avatarpath = current_user.avatarpath
            old_thumbnailpath = os.path.splitext(old_avatarpath)[0] + '_thumbnail' + os.path.splitext(old_avatarpath)[1]
            filename = secure_filename(file.filename)
            uuid_filename = str(uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER_USER'], uuid_filename)
            file.save(image_path)

            # Create square avatar
            img = Image.open(image_path)
            img = square_image(img, 500)
            img.save(image_path)

            # Create square thumbnail
            img = Image.open(image_path)
            img = square_image(img, 50)
            thumbnail_path = os.path.splitext(image_path)[0] + '_thumbnail' + os.path.splitext(image_path)[1]
            img.save(thumbnail_path)

            if old_avatarpath != 'avatars_users/default.jpg':
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_USER'], os.path.basename(old_avatarpath)))
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER_USER'], os.path.basename(old_thumbnailpath)))
                except Exception as e:
                    print(f"Error deleting old avatar: {e}")
                    flash("Error deleting old avatar. Please try again.", 'error')

            current_user.avatarpath = 'avatars_users/' + uuid_filename
        else:
            if not current_user.avatarpath:
                current_user.avatarpath = 'avatars_users/default.jpg'

        current_user.country = form.country.data if form.country.data else current_user.country
        current_user.about = form.about.data if form.about.data else current_user.about

        try:
            db.session.commit()
            print("Form validated and submitted successfully")
            print(f"Avatar Path: {current_user.avatarpath}")
            print(f"Country: {current_user.country}")
            print(f"About: {current_user.about}")

            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error updating profile: {e}")
            flash('Failed to update profile. Please try again.', 'error')

        return redirect(url_for('main.settings_profile_edit'))
    else:
        # Set the initial values from the database
        form.country.data = current_user.country
        form.about.data = current_user.about

    print("Form validation failed" if request.method == 'POST' else "Settings profile Form rendering")
    print(f"Avatar Path: {current_user.avatarpath}")
    print(f"Country: {current_user.country}")
    print(f"About: {current_user.about}")

    for field, errors in form.errors.items():
        for error in errors:
            print(f"Error in field '{getattr(form, field).label.text}': {error}")
            flash(f"Error in field '{getattr(form, field).label.text}': {error}", 'error')

    return render_template('settings_profile_edit.html', form=form, avatarpath=current_user.avatarpath)

@bp.route('/settings_profile_view', methods=['GET'])
@login_required
def settings_profile_view():
    print("Route: Settings profile view")
    return render_template('settings_profile_view.html')


@bp.route('/settings_password', methods=['GET', 'POST'])
@login_required
def account_pw():
    form = UserPasswordForm()
    print("Request method:", request.method)  # Debug line
    user = User.query.get(current_user.id)

    if form.validate_on_submit():
        try:
            print("Form data:", form.data)  # Debug line
            user.set_password(form.password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            print('Password changed successfully for user ID:', current_user.id)
            return redirect(url_for('main.account_pw'))
        except Exception as e:
            db.session.rollback()
            print('An error occurred while changing the password:', str(e))
            flash('An error occurred. Please try again.', 'error')

    return render_template('settings_password.html', title='Change Password', form=form, user=user)

@bp.route('/settings_api', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    print("Request method:", request.method)  # Debug line
    if form.validate_on_submit():
        if form.openai_api_key.data:
            current_user.openai_api_key = form.openai_api_key.data
        if form.gcloud_api_key.data:
            current_user.gcloud_api_key = form.gcloud_api_key.data

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print("SQLAlchemyError occurred:", str(e))

        flash('Settings have been updated.')
    elif request.method == 'GET':
        form.openai_api_key.data = current_user.openai_api_key
        form.gcloud_api_key.data = current_user.gcloud_api_key

    return render_template('settings_api.html', title='Settings', form=form)

@bp.route('/settings_sub')
@login_required
def subscribe():
    print("SETTINGS_SUB: Request method:", request.method)
    return render_template('settings_sub.html', role=current_user.role)

@bp.route('/settings_pricing')
@login_required
def pricing():
    print("SETTINGS_PRICING: Request method:", request.method)
    return render_template('settings_pricing.html', role=current_user.role)

@bp.route('/admin_main')
@login_required
def admin_main():
    print("ADMIN MAIN: Request method:", request.method)
    return render_template('admin_main.html')



@bp.route('/admin_newsletter', methods=['GET', 'POST'])
@login_required
def newsletter():
    print("ADMIN NEWSLETTER: Request method:", request.method)
    form = NewsletterForm()
    users = User.query.all()
    if form.validate_on_submit():
        recipients = form.recipients.data.split(',')
        print(f"ADMIN NEWSLETTER: Recipient list : {recipients}")
        msg = MailMessage(form.subject.data)
        msg.body = form.content.data
        msg.sender = 'personasuperchat@gmail.com'
        msg.recipients = recipients
        try:
            print(f"ADMIN NEWSLETTER: Newsletter sent")
            mail.send(msg)
            flash('Newsletter sent successfully!', 'success')
        except Exception as e:
            flash(str(e), 'error')
        return redirect(url_for('main.newsletter'))
    return render_template('admin_newsletter.html', title='Newsletter', form=form, users=users)

@bp.route('/admin_whitelist', methods=['GET', 'POST'])
@login_required
def whitelist():
    form = WhitelistForm()
    if form.validate_on_submit():
        email = form.email.data
        new_whitelist = Whitelist(email=email)
        db.session.add(new_whitelist)
        try:
            db.session.commit()
            flash('The email was successfully added to the whitelist!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('The email is already in the whitelist!', 'danger')
        return redirect(url_for('main.whitelist'))
    whitelist = Whitelist.query.all()
    return render_template('admin_whitelist.html', title='Whitelist', whitelist=whitelist, form=form)


@bp.route('/admin_usrmgr', methods=['GET', 'POST'])
@login_required
def usermanager():
    print('ADMIN_USRMGR: Entering usermanager function')
    form = EditUserForm()
    users = User.query.all()
    user_choices = [(user.id, user.name) for user in users]
    form.name.choices = user_choices
    print(f'ADMIN_USRMGR: Form name choices are: {form.name.choices}')

    if form.validate_on_submit():
        print("Form is valid")
        user = User.query.get(form.name.data)
        if user is not None:
            print(f"User selected is: {user.name}")
            # update user attributes with form data
            user.email = form.email.data
            user.role = form.role.data
            user.state = form.state.data
            user.tts_engine = form.tts_engine.data
            user.quota_messages = form.quota_messages.data
            user.avatarpath = form.avatarpath.data
            user.country = form.country.data
            user.about = form.about.data
            # commit changes to database
            try:
                db.session.commit()
                print("Changes saved to database")
                flash('Changes saved.')
                return redirect(url_for('admin_usrmgr'))
            except Exception as e:
                print(f"Error saving changes to database: {e}")
                flash(f"Error saving changes to database: {e}")
                return redirect(url_for('admin_usrmgr'))
        else:
            print("No user selected")
            flash("No user selected")
            return redirect(url_for('admin_usrmgr'))

    if request.method == 'GET':
        print("Request method is GET")
        user = User.query.get(form.name.data)
        if user is not None:
            print(f"User selected is: {user.name}")
            # populate editable fields with user data
            form.email.data = user.email
            form.role.data = user.role
            form.state.data = user.state
            form.tts_engine.data = user.tts_engine
            form.quota_messages.data = user.quota_messages
            form.avatarpath.data = user.avatarpath
            form.country.data = user.country
            form.about.data = user.about
            # populate non editable fields with user data
            password_hash = user.password_hash
            openai_api_key = user.openai_api_key
            gcloud_api_key = user.gcloud_api_key
            speech_enabled = user.speech_enabled
            created = user.created
            lastlogin = user.lastlogin
            count_messages = user.count_messages
            fav_tags = user.fav_tags
            fav_bots = user.fav_bots
            user_id = user.user_id

        else:
            print("No user selected")
            # set defaults or empty values if no user is selected
            form.email.data = ""
            form.role.data = ""
            form.state.data = ""
            form.tts_engine.data = ""
            form.quota_messages.data = 0
            form.avatarpath.data = ""
            form.country.data = ""
            form.about.data = ""
            password_hash = ""
            openai_api_key = ""
            gcloud_api_key = ""
            speech_enabled = ""
            created = ""
            lastlogin = ""
            count_messages = 0
            fav_tags = ""
            fav_bots = ""
            user_id = ""

        print(user)
        print(created)
        return render_template('admin_usrmgr.html', title='User Manager', form=form, password_hash=password_hash,
                               openai_api_key=openai_api_key, gcloud_api_key=gcloud_api_key,
                               speech_enabled=speech_enabled, created=created, lastlogin=lastlogin,
                               count_messages=count_messages, fav_tags=fav_tags, fav_bots=fav_bots, user_id=user_id)

def _authenticate_and_redirect(username, password):
    user = User.query.filter(func.lower(User.name) == func.lower(username)).first()
    if user is None or not user.check_password(password):
        flash('Invalid username or password')
        return redirect(url_for('main.login'))

    user.lastlogin = datetime.utcnow()
    db.session.commit()
    login_user(user, remember=True)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('main.restricted')
    return redirect(next_page)

def count_tokens(text):
    tokens = enc.encode(text)
    return len(tokens)

def build_api_conversation(bot_id, thread_id, system_prompt, user_message):
    conversation = [
        {"role": "user", "content": user_message},
    ]

    previous_messages = Message.query.filter_by(bot_id=bot_id, thread=thread_id).order_by(Message.order.desc()).all()

    tokens_so_far = count_tokens(user_message)

    for message in previous_messages:
        message_role = "assistant" if message.role == "ai" else message.role
        message_tokens = count_tokens(message.content)
        if message_tokens + tokens_so_far <= MAX_TOKENS:
            conversation.insert(0, {"role": message_role, "content": message.content})
            tokens_so_far += message_tokens
        else:
            break

    # Add the system message
    conversation.insert(0, {"role": "system", "content": system_prompt})

    return conversation

def valid_bot_name(bot_name):
    if len(bot_name) > 100:
        error = "Bot name should be less than or equal to 100 characters."
        return False, error

    if not re.match("^[A-Za-z0-9 '-]+$", bot_name):
        error = "Bot name can only contain letters, numbers, spaces, hyphens, and apostrophes."
        return False, error

    return True, None


def generate_system_prompt(bot_name):
    if Blacklist.query.filter(Blacklist.banned_name.ilike(f"%{bot_name}%")).first() is not None:
        return None, 'This name is not allowed. Please try a different name.'
    try:
        content = f'''
        You are a personality file generator.
        You will be given the name of a famous person.
        Write a personality file about that person in JSON format.
        This is an example personality file of Donald Trump in JSON:

        {{
            "name": "Donald Trump",
            "summary": "You are the former US president",
            "gender": "male",
            "famous_for": "Being the US president and being on a TV show",
            "speaking_style": "Your speaking style is unorganized and full of non-sequiturs",
            "words_used": "You use the words 'stupid' and 'great' a lot and like saying 'You're fired!'",
            "life_goal": "build a wall and make Mexico pay for it.",
            "category_tags": "president, politician, billionaire, celebrity, republican" 
            "personality_mbti": "ESTP"
        }}
        Notice how we never insert " in any of the values, that would break the JSON format.
        Use your knowledge of the famous person to fill in the relevant data fields

        Explanation of the fields

        Name : The name of the person
        Summary : insert 1 line summary about the  person
        gender : insert gender of the person
        famous_for: insert what the person is famous for
        speaking_style: insert their typical manner of talking
        words_used: insert words that the famous person tends to use
        life_goal: life goal of the famous person
        category_tags: comma separated list of categorization tags (should be 5 tags of 1-2 words each, prefer to concatenate words like young-achiever or use abbreviations like WSOP)
        personality_mbti: insert personality type of the famous person

        '''
        # The following block manually constructs the API request
        api_request = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": content},
                {"role": "user", "content": f"Please start with this person : {bot_name}"}
            ],
            "max_tokens": 250,
            "temperature": 0.9,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        print(f"API request: \n{json.dumps(api_request, indent=4)}")
        chatz = openai.ChatCompletion.create(**api_request)
        print(f"Response from OpenAI ChatGPT API: \n{chatz}")
        systemprompt = chatz['choices'][0]['message']['content']
        print(f"Response from OpenAI ChatGPT API json dump: \n{json.dumps(chatz, indent=4)}")
        # Parse the JSON part of the systemprompt
        try:
            json_start = systemprompt.find('{')
            json_end = systemprompt.rfind('}') + 1
            json_str = systemprompt[json_start:json_end]
            json_dict = json.loads(json_str)
            # Extract tags
            tag_str = json_dict.get('category_tags', '')
            tags = [tag.strip() for tag in tag_str.split(',')]
            session['tags'] = tags
        except json.decoder.JSONDecodeError as je:
            print(f"JSON parsing error: {je}")
            return None, 'There was a JSON parsing  error generating the bot.'
        except Exception as e:
            print(f"Error: {e}")
            return None, 'There was an error generating the bot after API call.'
    except Exception as e:
        print(f"Error: {e}")
        return None, 'There was an error generating the bot in setup phase.'
    return json_dict, None

def generate_images(bot_name):
    print(f'Generating image for: {bot_name}')
    deepai_api_key = current_app.config.get('DEEPAI_API_KEY')
    if not deepai_api_key:
        print("DEEPAI_API_KEY is not set in the application config")
        return None

    data = {
        'text': bot_name,  # Use the provided bot_name parameter
        'grid_size': '1',
        'width': '512',
        'height': '512'
    }
    headers = {'api-key': deepai_api_key}

    try:
        # Print the API request
        request_url = 'https://api.deepai.org/api/text2img'
        print(f"Sending API request to: {request_url}")
        print("Headers:", headers)
        print("Data:", data)

        response = requests.post(request_url, headers=headers, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request to DeepAI failed: {e}")
        return None

    try:
        output_url = response.json()['output_url']
        img_data = requests.get(output_url).content
        with open(f'modules/static/avatars/{bot_name}.jpg', 'wb') as handler:
            handler.write(img_data)
        return f'avatars/{bot_name}.jpg'
    except Exception as e:
        print(f"Error processing DeepAI response: {e}")
        return None

def square_image(image, size):
    # Resize the image to the desired size while maintaining aspect ratio
    image.thumbnail((size, size))

    # If the image is not square, pad it with black bars
    if image.size[0] != size or image.size[1] != size:
        new_image = Image.new('RGB', (size, size), color='black')
        offset = ((size - image.size[0]) // 2, (size - image.size[1]) // 2)
        new_image.paste(image, offset)
        image = new_image

    return image










#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
##########################                                                            ###########################
##########################                                                            ###########################
##########################                                                            ###########################
##########################                   GAME SECTION BELOW                       ###########################
##########################                                                            ###########################
##########################                                                            ###########################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################



@bp.route('/games/game_selection')
@login_required
def game_selection():
    print("Route: /games/game_selection")
    user_id = current_user.id

    return render_template('games/game_selection.html')


@bp.route('/api/get_highscores', methods=['GET'])
@login_required
def get_highscores():
    game_name = request.args.get('game_name')
    print(f"Received game name: {game_name}")

    if not game_name:
        print("Game name not provided.")
        return jsonify({'error': 'Game name not provided'}), 400

    # Retrieve and return the highscores for the given game
    try:
        highscores = db.session.query(Highscore, User.name).join(User, Highscore.user_id == User.user_id) \
            .filter(Highscore.game_name == game_name) \
            .order_by(Highscore.highscore.desc()).limit(5).all()
        print(f"High scores for {game_name} retrieved successfully.")
    except Exception as e:
        print(f"Failed to query database: {str(e)}")
        return jsonify({'error': 'Database query failed', 'details': str(e)}), 500

    score_data = [{'user_name': hs[1], 'highscore': hs[0].highscore} for hs in highscores]
    for data in score_data:
        print(f"User '{data['user_name']}' has highscore: {data['highscore']}")  # Printing out each user's highscore

    return jsonify(score_data), 200

@bp.route('/api/save_highscore', methods=['POST'])
@login_required
@limiter.limit("5 per hour")  # Rate limit to 5 requests per hour
def save_highscore():
    token = request.headers.get('X-Auth-Token')
    print(f"Received token: {token}")
    token = html.unescape(token)
    try:
        data = jwt.decode(token, current_app.secret_key)
    except DecodeError as e:
        print("Invalid token:", str(e))
        return jsonify({'error': 'Invalid token'}), 401

    print(f"Decoded token data: {data}")

    # Check if token has been used before
    if token in used_tokens:
        print("Token has already been used")
        return jsonify({'error': 'Token has already been used'}), 403

    user_id = data['user_id']
    game_name = request.json['game_name']
    highscore = request.json['highscore']

    # Check if highscore is an integer
    if not isinstance(highscore, int):
        print(f"Game: {game_name} User ID: {user_id} attempted to cheat with entry {highscore}")
        return jsonify({'error': 'Invalid score, only integers are accepted'}), 400

    print(f"User ID: {user_id}, Game Name: {game_name}, Highscore: {highscore}")

    # Save the highscore
    new_highscore = Highscore(game_name=game_name, highscore=highscore, user_id=user_id)
    db.session.add(new_highscore)
    try:
        db.session.commit()
        print("Highscore saved successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to commit to database: {e}")
        return jsonify({'error': 'Failed to save highscore', 'details': str(e)}), 500

    # Mark the token as used
    used_tokens.add(token)

    return jsonify({'message': 'Highscore saved successfully'}), 200



@bp.route('/games/quiz')
@login_required
def quiz():
    print("GAMES: Staring quiz")

    # Generate a token for the user
    try:
        user_id = current_user.get_id()
        user = User.query.get(user_id)
    except Exception as e:
        print(f"Failed to retrieve user details: {str(e)}")
        return jsonify({'error': 'Failed to retrieve user details', 'details': str(e)}), 500

    if not user:
        print(f"User not found.")
        return jsonify({'error': 'User not found'}), 404

    try:
        token = jwt.encode({'alg': 'HS256', 'exp': int((datetime.utcnow() + timedelta(hours=1)).timestamp())},
                           {'user_id': user.user_id}, current_app.secret_key)
    except Exception as e:
        print(f"Failed to encode token: {str(e)}")
        return jsonify({'error': 'Failed to encode token', 'details': str(e)}), 500

    print(f"GAMES: Token generated : {token}")
    session['token'] = token  # Store the token in the session for later use
    return render_template('games/game_quiz.html', token=token.decode('utf-8'))
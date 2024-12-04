from flask import Blueprint, request, jsonify, current_app
from .controller import UserController, StoryController, MediaController

# Створюємо Blueprints для кожного контролера
user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')
story_bp = Blueprint('story_bp', __name__, url_prefix='/api/stories')
media_bp = Blueprint('media_bp', __name__, url_prefix='/api/media')


# lab4 M:1 and M:M
select_bp = Blueprint('select_bp', __name__, url_prefix='/api/select')


api_bp = Blueprint('api_bp', __name__, url_prefix='/api/lab5')

# ---------- User Routes ----------
@user_bp.route('/', methods=['GET'])
def get_all_users():
    return UserController.get_all_users()

@user_bp.route('/with-stories', methods=['GET'])
def get_all_users_with_stories():
    return UserController.get_all_users_with_stories()

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return UserController.get_user(user_id)

@user_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    return UserController.add_user(data)

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    return UserController.update_user(user_id, data)

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserController.delete_user(user_id)


# ---------- Story Routes ----------
@story_bp.route('/', methods=['GET'])
def get_all_stories():
    return StoryController.get_all_stories()

@story_bp.route('/with-media', methods=['GET'])
def get_all_stories_with_media():
    return StoryController.get_all_stories_with_media()

@story_bp.route('/<int:story_id>', methods=['GET'])
def get_story(story_id):
    return StoryController.get_story(story_id)

@story_bp.route('/', methods=['POST'])
def add_story():
    data = request.get_json()
    return StoryController.add_story(data)

@story_bp.route('/<int:story_id>', methods=['PUT'])
def update_story(story_id):
    data = request.get_json()
    return StoryController.update_story(story_id, data)

@story_bp.route('/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    return StoryController.delete_story(story_id)


# ---------- Media Routes ----------
@media_bp.route('/', methods=['GET'])
def get_all_media():
    return MediaController.get_all_media()

@media_bp.route('/<int:media_id>', methods=['GET'])
def get_media(media_id):
    return MediaController.get_media(media_id)

@media_bp.route('/', methods=['POST'])
def add_media():
    data = request.get_json()
    return MediaController.add_media(data)

@media_bp.route('/<int:media_id>', methods=['PUT'])
def update_media(media_id):
    data = request.get_json()
    return MediaController.update_media(media_id, data)

@media_bp.route('/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    return MediaController.delete_media(media_id)











# lab4
@select_bp.route('/statistic', methods=['GET'])
def statistic():
    print("CalculateSum_Static")
    query = """SELECT Stories.story_id, Tags.tag_name
        FROM Stories
        JOIN StoryTags ON Stories.story_id = StoryTags.story_id
        JOIN Tags ON StoryTags.tag_id = Tags.tag_id
        ORDER BY Stories.story_id;
                """

    connection = current_app.mysql.connection

    # try:
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return jsonify(result), 200
    
    return jsonify({'message': 'No data found'}), 404


@select_bp.route('/get_all_users_with_stories', methods=['GET'])
def get_all_users_with_stories():
    query = """SELECT Users.username, Stories.story_id
        FROM Users
        LEFT JOIN Stories ON Users.user_id = Stories.user_id
        ORDER BY Users.username;
                """

    connection = current_app.mysql.connection

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return jsonify(result), 200
    
    return jsonify({'message': 'No data found'}), 404









# lab5

@api_bp.route('/get_sum_media_id', methods=['GET'])
def get_sum_media_id():
    query = "SELECT CalculateSum_Static() AS total_sum"
    
    connection = current_app.mysql.connection
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)

        if result[0] is not None:
            return jsonify({'total_sum': result[0]}), 200
        else:
            return jsonify({'message': 'No data found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve total sum: {str(e)}'}), 500
    finally:
        cursor.close()

@api_bp.route('/insert_dummy_categories', methods=['POST'])
def insert_dummy_categories():
    query = "CALL InsertDummyCategories()"
    
    connection = current_app.mysql.connection
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit() 

        return jsonify({'message': 'Dummy categories inserted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to insert dummy categories: {str(e)}'}), 500
    finally:
        cursor.close()


@api_bp.route('/add_media_category', methods=['POST'])
def add_media_category():
    from flask import request
    data = request.json
    media_id = data.get('media_id')
    category_id = data.get('category_id')
    
    if not media_id or not category_id:
        return jsonify({'error': 'Missing required fields'}), 400
    
    query = "INSERT INTO MediaCategories (media_id, category_id) VALUES (%s, %s)"
    
    connection = current_app.mysql.connection
    try:
        cursor = connection.cursor()
        cursor.execute(query, (media_id, category_id))
        connection.commit()

        return jsonify({'message': 'Media category added successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to add media category: {str(e)}'}), 500
    finally:
        cursor.close()

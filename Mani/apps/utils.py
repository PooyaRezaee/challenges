def serialize_users(users_obj):
    users = []

    for user in users_obj:
        users.append({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'class_room_id': user.classroom_id,
            'created_at': str(user.created),
        })

    return users

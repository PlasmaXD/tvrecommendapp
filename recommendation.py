from database import get_user_favorites, get_reviews

def recommend_programs(user_id):
    favorite_program_ids = get_user_favorites(user_id)
    print(f"Favorite programs for user {user_id}: {favorite_program_ids}")
    if not favorite_program_ids:
        print(f"No favorite programs found for user {user_id}")
        return []

    recommendations = []
    for program_id in favorite_program_ids:
        reviews = get_reviews(program_id)
        print(f"Reviews for program {program_id}: {reviews}")
        for review in reviews:
            reviewer_id = review[0]
            if reviewer_id and reviewer_id != user_id:
                recommended_programs = get_user_favorites(reviewer_id)
                print(f"User {reviewer_id}'s favorite programs: {recommended_programs}")
                for rec_id in recommended_programs:
                    if rec_id not in favorite_program_ids and rec_id not in recommendations:
                        recommendations.append(rec_id)
    
    print(f"Recommended programs for user {user_id}: {recommendations}")
    recommended_programs_details = [{'url': pid, 'title': f'Program {pid}', 'supplement': f'Details of Program {pid}'} for pid in recommendations]
    return recommended_programs_details

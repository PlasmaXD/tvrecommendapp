# from database import get_user_favorites, get_reviews

# def recommend_programs(user_id):
#     favorite_program_ids = get_user_favorites(user_id)
#     print(f"Favorite programs for user {user_id}: {favorite_program_ids}")
#     if not favorite_program_ids:
#         print(f"No favorite programs found for user {user_id}")
#         return []

#     recommendations = []
#     for program_id in favorite_program_ids:
#         reviews = get_reviews(program_id)
#         print(f"Reviews for program {program_id}: {reviews}")
#         for review in reviews:
#             reviewer_id = review[0]
#             if reviewer_id and reviewer_id != user_id:
#                 recommended_programs = get_user_favorites(reviewer_id)
#                 print(f"User {reviewer_id}'s favorite programs: {recommended_programs}")
#                 for rec_id in recommended_programs:
#                     if rec_id not in favorite_program_ids and rec_id not in recommendations:
#                         recommendations.append(rec_id)
    
#     print(f"Recommended programs for user {user_id}: {recommendations}")
#     recommended_programs_details = [{'url': pid, 'title': f'Program {pid}', 'supplement': f'Details of Program {pid}'} for pid in recommendations]
#     return recommended_programs_details
from database import get_all_reviews, get_program_details, add_program
from scraper import get_program_details_from_scraper
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

def recommend_programs(user_id, n_recommendations=10):
    reviews = get_all_reviews()
    # if len(reviews) == 0:
    #     print("No reviews available. Skipping recommendations.")
    #     return []


    data = [(user, item, float(rating)) for user, item, rating in reviews]

    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(pd.DataFrame(data, columns=['user_id', 'program_id', 'rating']), reader)

    trainset, testset = train_test_split(dataset, test_size=0.25)

    algo = SVD()
    algo.fit(trainset)

    user_history = [item for (user, item, rating) in reviews if user == user_id]

    all_programs = list(set([item for (user, item, rating) in reviews]))

    unseen_programs = [item for item in all_programs if item not in user_history]

    predictions = [algo.predict(user_id, item) for item in unseen_programs]
    predictions.sort(key=lambda x: x.est, reverse=True)

    top_n_recommendations = predictions[:n_recommendations]
    recommended_programs_ids = [pred.iid for pred in top_n_recommendations]

    recommended_programs_details = get_program_details_by_ids(recommended_programs_ids)
    return recommended_programs_details

# def get_program_details_by_ids(program_ids):
#     details = []
#     for program_id in program_ids:
#         detail = get_program_details(program_id)
#         if detail['title'].startswith('Program'):
#             # デフォルト値の場合はスクレイパーで詳細を取得
#             scraped_details = get_program_details_from_scraper(program_id)
#             if scraped_details:
#                 add_program(program_id, scraped_details['url'], scraped_details['title'], scraped_details['supplement'])
#                 details.append(scraped_details)
#             else:
#                 details.append(detail)
#         else:
#             details.append(detail)
#     return details
def get_program_details_by_ids(program_ids):
    details = []
    for program_id in program_ids:
        detail = get_program_details(program_id)
        if detail['title'].startswith('Program'):
            # デフォルト値の場合はスクレイパーで詳細を取得
            scraped_details = get_program_details_from_scraper(program_id)
            if scraped_details:
                add_program(program_id, scraped_details['url'], scraped_details['title'], scraped_details['supplement'])
                details.append(scraped_details)
            else:
                details.append(detail)
        else:
            details.append(detail)
    return details

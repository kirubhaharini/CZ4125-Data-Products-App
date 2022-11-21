
import numpy as np


"""
Given a query:
1. apply stage one - filters books by genre
2. apply stage two - rerank results
"""
def semanticSearch(query, book_collection, genre_collection, genre_embedder, ranking_model, keyword_model, 
                   stage_one_limit = 200, stage_two_limit = 10, num_genre_per_keyword = 3):
    # stage one - filter by genre
    stage_one_cursor, desired_genres = _stage_one(query, book_collection, genre_collection, genre_embedder, keyword_model, limit = stage_one_limit, num_genre_per_keyword = num_genre_per_keyword)
    # stage two - rerank with Transformer
    stage_two_cursor = _stage_two(stage_one_cursor, query, ranking_model, book_collection, limit = stage_two_limit)
    return [doc for doc in stage_two_cursor], desired_genres

"""
Use Collaborative Filtering model to recommend, given user_id
"""
def personalizedSearch(collection, model, user_id, num_rec):
    # sorted by best recommendations first 
    # i generate more recommendations from the model(cuz the datasbase isn't fully filled yet)
    recommended_item_ids = model.recommend(user_id, num_rec = num_rec*10).tolist()
    # get documents from mongo - looping through one by one to retain the order of best recommendations first
    output = []
    for i,_id in enumerate(recommended_item_ids):
        doc = collection.find_one({"ISBN":_id})
        if doc is None:
            # there's a chance the book isn't found, because the database currently isn't fully filled yet
            continue
        output.append(doc)
        if len(output) >= num_rec:
            break
    return output
    
"""
Given a query:
1. extract user's desired genres
2. return candidate books (mongo cursor)
note: if no results, relax criteria 
i.e candidates need at least one from ['War','Combat','Terrorism','Fairies','Fae','Fairy Tales']
rather than at least one from ['War','Combat','Terrorism'] AND ['Fairies','Fae','Fairy Tales']
"""
def _stage_one(query, book_collection, genre_collection, genre_embedder, keyword_model, limit = 200, num_genre_per_keyword = 3):
    # extract user's desired genres
    desired_genres = search_genre_by_query(genre_collection, query, genre_embedder, keyword_model, topk = num_genre_per_keyword)
    # expression used to filter mongo
    filtering_expression = _get_expression_genre(desired_genres)
    # if no results, relax the criteria 
    if book_collection.find_one(filtering_expression) is None:
        desired_genres = [np.array(desired_genres).flatten().tolist()]
        filtering_expression = _get_expression_genre(desired_genres)
    # filter mongo
    results_cursor = book_collection.find(filtering_expression).limit(limit)
    return results_cursor, desired_genres

"""
Given a query:
1. Get similarity score to the summary of every candidate item
2. return the top k (cursor)
"""
def _stage_two(mongo_cursor, query, ranking_model, book_collection, limit = 10):
    _ids = []
    # get summaries of each candidate
    crossencoder_input = []
    for doc in mongo_cursor:
        _ids.append(doc["ISBN"])
        crossencoder_input.append([query, ",".join(doc["Genre"]) +". "+ doc["Summary"][0]])
    # rank and sort
    ranking_scores = ranking_model.predict(crossencoder_input)
    topk_book_ids = sorted(zip(_ids, ranking_scores), reverse = True, key = lambda ele:ele[1])[:limit]
    topk_book_ids = [_id for _id, score in topk_book_ids]
    # return cursor of top k books
    return book_collection.find({"ISBN":{"$in":topk_book_ids}})


"""
FAST - Given query:
1. extract keywords  
2. For each keyword compute similarity to every genre in database (Utilize matrix multiplication)
3. return top k matching genres for each keyword
note: I assume the scenario that the user input at most 3 key ideas/keyword, this keeps candidate size small and much less noisy
"""
def search_genre_by_query(collection, query, embedding_model, keyword_model, topk = 3, return_scores = False):
    # extract query keywords
    keyword_model.extract_keywords_from_text(query)
    keywords = keyword_model.get_ranked_phrases()[:3]
    keywords = query if len(keywords)==0 else keywords   # if no keywords were extracted, use the whole query
    # get document containing all genres
    document = collection.find_one({})
    # embed query keywords
    query_embedding = embedding_model.encode(keywords)
    # compute scores and sort
    scores = np.dot(query_embedding,np.array(document["embedding"]).T)
    # return top k genres for each keyword
    matched_genres = []
    for s in scores:
        temp = sorted(zip(document["genre"],s), key = lambda ele: ele[1], reverse = True)[:topk]
        if not return_scores:
            matched_genres.append([ele[0] for ele in temp])
        else:
            matched_genres.append(temp)
    return matched_genres

"""
I will optimize keyword extraction for the following scenario:
- the user will input a short description of AT MOST 3 main ideas/keywords
Following this scenario, many low ranking or noisy keywords from rake can be filtered out.
This optimizes the pipeline because the candidate size will be smaller and have less noise
"""
def _keyword_optimization(rake_output):
    rake_output

"""
expression used to filter mongo
"""
def _get_expression_genre(desired_genres):
    return {
        "$and":[
            {"$or":[{"Genre":g1} for g1 in g0]} for g0 in desired_genres
        ]
    }


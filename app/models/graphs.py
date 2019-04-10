import pygal    
from pygal.style import LightColorizedStyle
from app import db
from bson.objectid import ObjectId
from flask_login import current_user



class Graphs:

    unwanted_cuisines = ['north-african', '', 'english', 'cajun--creole']


    def likes_chart():
        bar_chart = pygal.Bar(fill=True, interpolate='cubic', style=LightColorizedStyle)
        bar_chart.title = 'Average Likes / Dislikes per Cuisine'
        bar_chart.x_labels = ['Likes', 'Dislikes']
        cursor = db.recipes.aggregate([{"$group": {"_id": "$filters.cuisine", "likes": { "$avg": '$users.likes' }, "dislikes": { "$avg": '$users.dislikes' }}}])
        
        for item in cursor:
            if item['_id'] not in Graphs.unwanted_cuisines:
                bar_chart.add(item['_id'], [round(item['likes'], 0), round(item['dislikes'], 0)])

        return bar_chart.render_data_uri() 


    def kcal_chart():
        pie_chart = pygal.Pie(inner_radius=.4, fill=True, interpolate='cubic', style=LightColorizedStyle)
        pie_chart.title = 'Average KCAL per Cuisine'

        cursor = db.recipes.aggregate([
                { "$project":
                        {
                            "_id": "$filters.cuisine",
                            "arr": { "$arrayElemAt": [ "$nutrition", 0 ] }
                        }
                },
                { "$project":
                        {
                            "_id": "$_id",
                            "kcal": { "$arrayElemAt": [ "$arr", 1 ] }
                        }
                },
                { "$group": {
                       "_id": "$_id",
                       "avgKcal": { "$avg": {
                                "$toInt": "$kcal"
                           }
                        }
                   }
                }
            ])
    
        for item in cursor:
            if item['_id'] not in Graphs.unwanted_cuisines:
                pie_chart.add(item['_id'], round(item['avgKcal'], 0))
                
        return pie_chart.render_data_uri() 


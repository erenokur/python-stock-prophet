from flask import Blueprint

stock_analysis = Blueprint('stock_analysis', __name__)

from app.stock_analysis import technical_analysis, fundamental_analysis, news_analysis, sector_analysis
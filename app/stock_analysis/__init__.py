from flask import Blueprint

stock_analysis = Blueprint('stock_analysis', __name__)

from app.stock_analysis import technical_analysis, balance_sheet_analysis, news_analysis, sector_analysis
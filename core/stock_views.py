from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import logging
from .utils import get_stock_data, get_stock_price_data

logger = logging.getLogger(__name__)

class StockDataView(APIView):
    def get(self, request, *args, **kwargs):
        ticker = request.query_params.get('ticker')
        if not ticker:
            return Response({'error': 'Ticker is required'}, status=HTTP_400_BAD_REQUEST)
        try:
            data = get_stock_data(ticker)
            return Response(data, status=HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching stock data for ticker {ticker}: {e}")
            return Response({'error': 'Failed to fetch stock data'}, status=HTTP_400_BAD_REQUEST)

class StockPriceView(APIView):
    def get(self, request, *args, **kwargs):
        ticker = request.query_params.get('ticker')
        if not ticker:
            return Response({'error': 'Ticker is required'}, status=HTTP_400_BAD_REQUEST)
        try:
            data = get_stock_price_data(ticker)
            return Response(data, status=HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching stock data for ticker {ticker}: {e}")
            return Response({'error': 'Failed to fetch stock data'}, status=HTTP_400_BAD_REQUEST)

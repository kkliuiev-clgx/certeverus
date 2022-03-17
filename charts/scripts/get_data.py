# Run as: 
# ./manage.py shell < charts/scripts/get_data.py
#
from charts.utils import get_waterfall
from charts.models import Client

client = Client.objects.first()
data = get_waterfall(client)

print(data)

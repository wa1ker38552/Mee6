import mee6
import os

client = mee6.Client(os.environ['TOKEN'], mee6.Config())
client.run_flask(host='0.0.0.0', port=8080)
client.run(economy_channel=867990271042916412, counting_channel=1015923752422346782)

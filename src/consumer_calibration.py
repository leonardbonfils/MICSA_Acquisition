from getch import getch
from time import time
from kafka import KafkaConsumer

# Kafka topic
topics = [
    'micsaData'
]

# Kafka options
options = {
    'bootstrap_servers'      : '10.194.24.26:9092',
    'enable_auto_commit'     : True,
    'auto_commit_interval_ms': 5000,
    'fetch_max_wait_ms'      : 100,
    'fetch_min_bytes'        : 1,
    'fetch_max_bytes'        : 1024 * 1024
}

# Create Kafka consumer
consumer = KafkaConsumer(*topics, **options)

# Instructions for user
print("Calibration")
print("First 5 seconds : decontracted muscle")
print("Last 5 seconds : contracted muscle\n")

# Write average value in a file
calibrationFile = open("calibrationFile.txt", 'w')

# Variables to calculate average value
averageValue = 0
valueCount = 0
getValue = 0

# Instructions for user
print("Decontract muscle and press any key now")
getch()
print("Hold 5 seconds")
start = time()

# Read kafka topic
for message in consumer:
    
    # value from type byte to float
    message = float(message.value.decode())
    
    # add current value to average
    averageValue += message
    valueCount += 1

    # After 5 seconds, switch contraction or exit program
    currentTime = time()
    if (currentTime - start > 5):
        getValue += 1

        # Write average to file and exit
        if (getValue == 2):
            averageValue /= valueCount
            calibrationFile.write(str(averageValue))
            break

        # Instructions for user
        else:
            print("Contract muscle and press any key now")
            getch()
            print("Hold 5 seconds")
            start = time()

# Close file
calibrationFile.close()
print("Calibration completed")
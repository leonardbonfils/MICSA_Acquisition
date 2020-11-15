# MICSA
SynapsETS - Project MICSA
Producer Kafka

# Command list for execution ( will vary based on data source)
# This is what you need to do:
1. First step download Docker 
2. Execute the following commands ( You need to be a super user):
	- sudo docker build -t image .
	- CAREFUL! You must follow the folowing rules 
	- The keyboard is seen as an exterior device and will cause issues if not listed as a device used by the docker
	- Use the following command to tell docker the keyboard is a device : 
	- sudo docker run --device=/dev/ttyUSB0 -i image 
3. IMPORTANT! Based on your source for the data the USB port will changed, make sure your are using the correct port.




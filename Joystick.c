/*
Nintendo Switch Fightstick - Proof-of-Concept

Based on the LUFA library's Low-Level Joystick Demo
	(C) Dean Camera
Based on the HORI's Pokken Tournament Pro Pad design
	(C) HORI

This project implements a modified version of HORI's Pokken Tournament Pro Pad
USB descriptors to allow for the creation of custom controllers for the
Nintendo Switch. This also works to a limited degree on the PS3.

Since System Update v3.0.0, the Nintendo Switch recognizes the Pokken
Tournament Pro Pad as a Pro Controller. Physical design limitations prevent
the Pokken Controller from functioning at the same level as the Pro
Controller. However, by default most of the descriptors are there, with the
exception of Home and Capture. Descriptor modification allows us to unlock
these buttons for our use.
*/



#include "Joystick.h"
#include <LUFA/Drivers/Peripheral/Serial.h>
#include <LUFA/Drivers/Misc/RingBuffer.h>


typedef struct {
	uint16_t instruction;
	uint16_t duration;
} command;

static const command step[] = {
	{0, 50},  // Do Nothing
	{48, 5},  // Press Triggers
	{0, 50},  // Do Nothing
	{48, 5},  // Press Triggers
	{0, 50},  // Do Nothing
	{4, 5},	  // Press A
	{0, 50},  // Do Nothing
	{4, 5},	  // Press A
	{0, 250}, // Do Nothing
};
#define ECHOES 2
int echoes = 0;
USB_JoystickReport_Input_t last_report;
static USB_JoystickReport_Input_t globalInput;
static RingBuffer_t Buffer;
uint8_t BufferData[128];
uint8_t instructions;

// Main entry point.
int main(void) {
	// We'll start by performing hardware and peripheral setup.
	SetupHardware();
	// We'll then enable global interrupts for our use.
	GlobalInterruptEnable();

	//Loop through our step array to synch our controller to the switch
	size_t n = sizeof(step)/sizeof(step[0]);
	int i;
	for(i=0; i < n; ++i){
		uint16_t input = step[i].instruction;
		globalInput.Button = input;
		uint16_t time = 0;
		while(time < step[i].duration){
			HID_Task(&time);
			USB_USBTask();
		}
	}

	//  11101010 high = 234
	//  01100000 low = 96
	//  Reset our character to be a null character and create a dummy int
	//  to pass into our functions.
	//  We make a dummy variable because we only handle duration during our synching step
	//  and not when receiving an input from our script. Our script handles the duration for us
	uint16_t dummy = 0;
	instructions = 0;
	globalInput.Button = 0;

	// Once that's done, we'll enter an infinite loop.
	for (;;)
	{
		// //Only try to read bytes if our buffer is not full
		if(!(RingBuffer_IsFull(&Buffer))){
			//Check if we've received a byte
			if (Serial_IsCharReceived())
			{
				uint8_t read = Serial_ReceiveByte();
				Serial_SendByte(read);
				if(instructions == 0){
					instructions = read;
				} else {
					RingBuffer_Insert(&Buffer, read);
				}
			}

			if (instructions != 0 && RingBuffer_GetCount(&Buffer) == instructions * 2)
			{
				int i;
				resetInput();
				for(i = 0; i < instructions; i++){
					uint8_t low = RingBuffer_Remove(&Buffer);
					uint8_t high = RingBuffer_Remove(&Buffer);
					uint16_t combined = (high << 8) | low;
					updateInput(combined);
				}
				instructions = 0;
			}

		}
		// check if a serial is recieved and update our variable with it
		// We need to run our task to process and deliver data for our IN and OUT endpoints.
		HID_Task(&dummy);
		// We also need to run the main USB management task.
		USB_USBTask();
	}
}

//Updates our globalInput Variable
void updateInput(uint16_t combined)
{
	uint8_t stick = 0;
	uint8_t choice = (combined & 49152) >> 14;
	switch(choice){
		//Reset our globalInput to neutral
		case 0:
			resetInput();
			break;
		
		//Update our button input
		case 1:
			//We are doing an AND operation on our combined input to get the 14 bits
			//that store our button presses
			//Ex: 0100 0000 0100 1100 is our input that stores a ZL + X + A input for shield surf in BOTW
			//  & 0011 1111 1111 1111 is the bit representation of 16383
			//  = 0000 0000 0100 1100 which is what we save to the button variable of our globalInput
			globalInput.Button = combined & 16383;
			break;

		//Update one of our stick values
		case 2:
			// We need to check if we are a Left/Right stick and if we are X/Y input
			stick = (combined & 16383) >> 8;

			//0 means update our LX Value
			if(stick == 0){
				globalInput.LX = (combined & 255);
			} else if (stick == 1){ //1 is our LY value
				globalInput.LY = (combined & 255);
			} else if (stick == 2){ //2 is our RX value
				globalInput.RX = (combined & 255);
			} else { //we update the RY value
				globalInput.RY = (combined & 255);
			}
			
			break;
		//Update our D-pad value
		case 3:
			globalInput.HAT = (combined & 255);
			break;
	}
}

//Resets our globalInput Variable
void resetInput(void){
	memset(&globalInput, 0, sizeof(USB_JoystickReport_Input_t));
	globalInput.Button = 0;
	globalInput.LX = STICK_CENTER;
	globalInput.LY = STICK_CENTER;
	globalInput.RX = STICK_CENTER;
	globalInput.RY = STICK_CENTER;
	globalInput.HAT = HAT_CENTER;
}

// Configures hardware and peripherals, such as the USB peripherals.
void SetupHardware(void) {
	// We need to disable watchdog if enabled by bootloader/fuses.
	MCUSR &= ~(1 << WDRF);
	wdt_disable();

	// We need to disable clock division before initializing the USB hardware.
	clock_prescale_set(clock_div_1);
	// We can then initialize our hardware and peripherals, including the USB stack.

	//enable pin 9 for output
	//Used for output to our buzzer
	DDRB = 1 << 5;
	PORTB = 0;

	//Initalize our serial with baud 9600
	Serial_Init(9600,0);

	// Reset our globalInput to neutral
	resetInput();

	//Initalize our Ring Buffer as well
	RingBuffer_InitBuffer(&Buffer, BufferData, sizeof(BufferData));

	// The USB stack should be initialized last.
	USB_Init();

}

// Fired to indicate that the device is enumerating.
void EVENT_USB_Device_Connect(void) {
	// We can indicate that we're enumerating here (via status LEDs, sound, etc.).
}

// Fired to indicate that the device is no longer connected to a host.
void EVENT_USB_Device_Disconnect(void) {
	// We can indicate that our device is not ready (via status LEDs, sound, etc.).
}

// Fired when the host set the current configuration of the USB device after enumeration.
void EVENT_USB_Device_ConfigurationChanged(void) {
	bool ConfigSuccess = true;

	// We setup the HID report endpoints.
	ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_OUT_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);
	ConfigSuccess &= Endpoint_ConfigureEndpoint(JOYSTICK_IN_EPADDR, EP_TYPE_INTERRUPT, JOYSTICK_EPSIZE, 1);

	// We can read ConfigSuccess to indicate a success or failure at this point.
}

// Process control requests sent to the device from the USB host.
void EVENT_USB_Device_ControlRequest(void) {
	// We can handle two control requests: a GetReport and a SetReport.

	// Not used here, it looks like we don't receive control request from the Switch.
}

// Process and deliver data from IN and OUT endpoints.
void HID_Task(uint16_t *duration){
	// If the device isn't connected and properly configured, we can't do anything here.
	if (USB_DeviceState != DEVICE_STATE_Configured) return;
	// We'll start with the OUT endpoint.
	Endpoint_SelectEndpoint(JOYSTICK_OUT_EPADDR);
	// We'll check to see if we received something on the OUT endpoint.
	if (Endpoint_IsOUTReceived())
	{
		// If we did, and the packet has data, we'll react to it.
		if (Endpoint_IsReadWriteAllowed())
		{
			// We'll create a place to store our data received from the host.
			USB_JoystickReport_Output_t JoystickOutputData;
			// We'll then take in that data, setting it up in our storage.
			while(Endpoint_Read_Stream_LE(&JoystickOutputData, sizeof(JoystickOutputData), NULL) != ENDPOINT_RWSTREAM_NoError);
			// At this point, we can react to this data.

			// However, since we're not doing anything with this data, we abandon it.
		}
		// Regardless of whether we reacted to the data, we acknowledge an OUT packet on this endpoint.
		Endpoint_ClearOUT();
	}

	// We'll then move on to the IN endpoint.
	Endpoint_SelectEndpoint(JOYSTICK_IN_EPADDR);
	// We first check to see if the host is ready to accept data.
	if (Endpoint_IsINReady())
	{
		// We'll create an empty report.
		USB_JoystickReport_Input_t JoystickInputData;
		// We'll then populate this report with what we want to send to the host.
		GetNextReport(&JoystickInputData,duration);
		// Once populated, we can output this data to the host. We do this by first writing the data to the control stream.
		while(Endpoint_Write_Stream_LE(&JoystickInputData, sizeof(JoystickInputData), NULL) != ENDPOINT_RWSTREAM_NoError);
		// We then send an IN packet on this endpoint.
		Endpoint_ClearIN();
	}
}

// Prepare the next report for the host.
void GetNextReport(USB_JoystickReport_Input_t *const ReportData, uint16_t *duration){
	// Prepare an empty report
	memset(ReportData, 0, sizeof(USB_JoystickReport_Input_t));

	// Repeat ECHOES times the last report
	if (echoes > 0)
	{
		memcpy(ReportData, &last_report, sizeof(USB_JoystickReport_Input_t));
		echoes--;
		return;
	}

	//Set our ReportData to match our globalInput
	ReportData->Button = globalInput.Button;
	ReportData->LX = globalInput.LX;
	ReportData->LY = globalInput.LY;
	ReportData->RX = globalInput.RX;
	ReportData->RY = globalInput.RY;
	ReportData->HAT = globalInput.HAT;

	//Update our duration
	//This is really only used for the start up sequence when
	//The arduino connects to the switch
	//All duration of our button presses after is handled in our script
	*duration += 1;

	// Prepare to echo this report
	memcpy(&last_report, ReportData, sizeof(USB_JoystickReport_Input_t));
	echoes = ECHOES;
}

# phychips-pr7-command-demo


### checksum in c/c++
```c++
unsigned char RcpApi::calculateChecksum(unsigned char *message, unsigned short length)
{
	unsigned short checksum = 0;

	for(int i = 0; i < length; i++)
	{
		checksum += message[i];
		checksum += (checksum >> 8);
		checksum &= 0xff;
	}

	if( (checksum == (~(PREAMBLE_COMMAND) & 0xff) ) | (checksum == (~(PREAMBLE_RESPONSE) & 0xff) ) )		//If same as preamble (0xCC or 0xAA)
		checksum += 1;

	checksum = ~checksum & 0xff;

	return (unsigned char) checksum;
}
```
BOOL IoctlResult; 
HANDLE hndFile; 
LONG IoctlCode; 
ULONG bytesOutput; 
 	 
if (argc < 2) { 
    printf("Invalid input!\n\n"); 
 	exit(1); 
} 
 
hndFile = CreateFile("\\\\.\\R:", 0, FILE_SHARE_WRITE | FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL); 
 
if (hndFile == INVALID_HANDLE_VALUE) { 
    printf("Error while getting the device!\n");         
    exit(1); 
} 

switch (argv[1][0]) { 
 	case 'w': 
 	 	IoctlCode = IOCTL_WRITE_DISKIMAGE_FILE; 
 	 	break; 
 	case 'r': 
 	 	IoctlCode = IOCTL_READ_DISKIMAGE_FILE; 
 	 	break; 
 	default: 
 	 	printf("Wrong input - %c!\n", argv[1][0]); 
 	 	exit(1); 
} 

if (DeviceIoControl(hndFile, IoctlCode, NULL, 0, NULL, 0, &bytesOutput, NULL)) { 
 	printf("Operation complete with SUCCESS!\n"); 
} else { 
    printf("Ioctl failed with code %ld\n", GetLastError()); 
} 

if (!CloseHandle(hndFile)) { 
    printf("Error while closing!\n"); 
} 

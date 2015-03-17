function s = pcConfigureSerial()

%s = instrhwinfo('Serial');

% Define the used serial port
com = 'COM21';

% Check all serial ports are closed
if isempty(instrfind) == 0
    fclose(instrfindall);
    delete(instrfindall);
end

% Set the serial port properties
s = serial(com,'BaudRate',115200, 'Parity', 'odd', 'StopBits', 2);
%get(s)

s.ReadAsyncMode = 'continuous';

%pcBreakInterruptCallback()

% Set callback function according to the specified event
%s.BreakInterruptFcn = @pcBreakInterruptCallback;
%s.OutputEmptyFcn = @pcBreakInterruptCallback;
%s.BytesAvailableFcn = @pcBreakInterruptCallback;
%s.BytesAvailableFcnMode = 'byte';
%s.BytesAvailableFcnCount = 1;

% Initialize connection by opening the port
fopen(s);



end
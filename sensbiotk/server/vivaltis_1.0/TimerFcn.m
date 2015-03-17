function TimerFcn(obj,event,s,T,Q,amp)
tic
global maxPulseWidth minPulseWidth pulseWidthOffset intensity maxIntensity minIntensity intensityScale podId

%% judge if all the data is sent
k = get(T,'TasksExecuted');

if k == length(Q)
    stop(T); %when all the data are sent, the timer is stoped.
    disp('stop now');
    
else k = k+1;
    
end


%% update pulsewidth

pulseWidth = [Q(k) 0 0 0 0 0 0 0];

% pcSetPulseWidth(s,pulseWidth,maxPulseWidth,minPulseWidth,pulseWidthOffset);
% Create Pulse Width frame
cmdId           = uint8( hex2dec('99') );        % Configuration command
length0         = uint8(9);
outputId        = uint8(0);
pulseWidth      = uint16( round( Q(k) ) );
crc             = uint16( hex2dec('CAFE') );

% Send Pulse Width frame
requestFrame = [cmdId length0 outputId podId ...
    typecast(pulseWidth, 'uint8') typecast(pulseWidth, 'uint8') typecast(pulseWidth, 'uint8') ...
    typecast(crc, 'uint8') ];
fwrite(s, requestFrame, 'uint8');


%intensity = [amp(k) 0 0 0 0 0 0 0];

% pcSetIntensity(s,intensity,maxIntensity,minIntensity,intensityScale);
toc


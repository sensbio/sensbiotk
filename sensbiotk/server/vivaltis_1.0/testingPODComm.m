%% script to use Vivaltis Stimulator from matlab
%% Mitsuhiro Hayashibe, INRIA Demar, 26 Nov. 2013
%% Mickael Toussaint, Vivaltis
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;
clear all
close all;


%% POD limits
global maxPulseWidth minPulseWidth pulseWidthOffset maxIntensity minIntensity intensityScale tStart podId

% mA
maxIntensity = 50;
minIntensity = 0;

% us
pulseWidthOffset = 33.5;        % With the POD, the lower bound of the pulse width is '50 us' and the pulse width step is '1 us'
maxPulseWidth = 350;
minPulseWidth = pulseWidthOffset;

% ms
maxPeriod = 500;
minPeriod = 25;

%% define random stimulation pulsewidth
pwFrom = 0.3; pwTo = 1;
num = 10;
Rmax = pwFrom + (pwTo - pwFrom) * rand(1,num);

pwRandom = [];
for i= 1 : num
    PW = maxPulseWidth * Rmax(i);
    pwRandom = [pwRandom,linspace(0,PW,20),linspace(PW,PW,40),linspace(PW,0,20),linspace(0,0,80)];
end

%% define fatigue stimulation pulsewidth
num = 10;
Rmax = 0.8;
amp1 = input('# Please input stimulation amplitude (mA): ');

amp = [];
pwFatigue = [];
for i= 1 : num
    PW = maxPulseWidth * Rmax;
    pwFatigue = [pwFatigue,linspace(0,PW,20),linspace(PW,PW,40),linspace(PW,0,20),linspace(0,0,80)];
    amp =  [amp,linspace(amp1,amp1,80),linspace(1,1,80)];
end

%% basic POD configuration
s = pcConfigureSerial();

%% RF Controller Initialization
nPODmax = 10;
for i=1:nPODmax
    podInfo(i) = struct('type',0,'networkId',0,'state',0,'version',[0 0 0 0],'color',0);
end
pods = struct('nAvailable',0,'info',podInfo);

% Create Initialization frame and send
request.cmdId   = uint8( hex2dec('13') );        % Initialization command
request.length  = uint8(1);
request.data    = uint8(0);
request.crc     = uint16( hex2dec('CAFE') );

stimPods = struct(pods);
[strErr, pods, stimPods] = pcSendRequest_n_WaitReply(s, request, pods);

if( strcmp(strErr, 'None') )
    % Select the targeted POD
    if stimPods.nAvailable > 0
        isPodSelected = 0;
        while isPodSelected == 0
            podId = input('\n# Please Select the POD ID : ');
            podId = uint8(podId);
            i = 1;
            while (i <= stimPods.nAvailable) && ( stimPods.info(i).networkId ~= podId )
                i = i + 1;
            end
            if i <= stimPods.nAvailable
                if stimPods.info(i).networkId == podId
                    isPodSelected = 1;
                end
            end
        end
        
        fprintf('\t >> POD_%i selected \n', stimPods.info(i).networkId);
    else
        fprintf('\n # Warn : - No Available POD - \n')
        strErr = 'Exit';
    end
end

%% Targeted POD Configuration
if( strcmp(strErr, 'None') )
    % Create Configuration frame
    request.cmdId   = uint8( hex2dec('40') );        % Configuration command
    request.length  = uint8(31);
    
    outputId        = uint8(0);
    patternTypeId   = uint8( hex2dec('0B') );     % 0x0B for biphasic
    ahesionDetect   = uint8(0);
    delay           = uint8(0);
    increaseTime    = uint8(0);
    maxTime         = uint8(30);            % second
    decreaseTime    = uint8(0);
    nullTime        = uint8(0);
    frequency       = uint16(40);           % Hz
    pulseWidth      = uint16(200);           % µs
    curAmplitude    = uint16(amp1*10);
    maxAmplitude    = uint16(maxIntensity*10);
    incrementStep   = uint8(5);             % 100 nA or 10^{-4}A
    nRepetition     = uint8(0);
    
    request.data    = [outputId podId patternTypeId ahesionDetect delay ...
        increaseTime maxTime decreaseTime nullTime ...
        typecast(frequency, 'uint8') typecast(pulseWidth, 'uint8') ...
        typecast(frequency, 'uint8') typecast(pulseWidth, 'uint8') ...
        typecast(frequency, 'uint8') typecast(pulseWidth, 'uint8') ...
        typecast(curAmplitude, 'uint8') typecast(maxAmplitude, 'uint8') ...
        incrementStep nRepetition];
    request.crc     = uint16( hex2dec('CAFE') );
    
    % Send Configuration frame
    [strErr, pods, stimPods] = pcSendRequest_n_WaitReply(s, request, pods);
    if( strcmp(strErr, 'None') )
        fprintf('\t >> POD_%i configured \n', podId)
    end
end


%% create timer to update the puslewidth and send to the stimulator
if( strcmp(strErr, 'None') )
    
    %% create timer to update the puslewidth and send to the stimulator
    T = timer('ExecutionMode','fixedRate','period',0.025,'TasksToExecute',max(size(pwRandom)));
    set(T,'TimerFcn',{@TimerFcn,s,T,pwRandom,amp},'StopFcn',{@StopFcn,s,T});
    
    
    %% Start POD
    
    % Create Start frame
    request.cmdId   = uint8( hex2dec('30') );        % Start command
    request.length  = uint8(2);
    
    targetedAppliId = uint8(1);
    
    request.data    = [podId targetedAppliId];
    request.crc     = uint16( hex2dec('CAFE') );
    
    % Send Configuration frame
    [strErr, pods, stimPods] = pcSendRequest_n_WaitReply(s, request, pods);
    if( strcmp(strErr, 'None') )
        fprintf('\t >> POD_%i started \n', podId)
    end
end

%% start timer

start(T);

tStart = tic;

% while(1)
%     % Create Pulse Width frame
%     cmdId           = uint8( hex2dec('99') );        % Configuration command
%     length          = uint8(9);
%     outputId        = uint8(0);
%     pulseWidth      = uint16(10);
%     crc             = uint16( hex2dec('CAFE') );
%
%     % Send Pulse Width frame
%     requestFrame = [cmdId length outputId podId ...
%         typecast(pulseWidth, 'uint8') typecast(pulseWidth, 'uint8') typecast(pulseWidth, 'uint8') ...
%         typecast(crc, 'uint8') ];
%     fwrite(s, requestFrame, 'uint8');
%
%     pause(1);

%                 % Wait Pulse Width reply
%                 i = 0;
%                 while s.BytesAvailable == 0
%                     i = i + 1;
%                 end
%
%                 % Get Pulse Width reply
%                 replyFrame = fread(s, s.BytesAvailable, 'uint8');
%
%                 % Analyze the Pulse Width reply
%                 if( replyFrame(1) == hex2dec('55') )
%                     length      = replyFrame(2);
%                     errorType   = replyFrame(3);
%                     errorId     = replyFrame(4);
%                     podIdRe     = replyFrame(5);
%                     %                                     requestId   = replyFrame(6);
%
%                     if(errorType == 0)
%
%                         fprintf('\t >> POD_%i Pulse Width is set \n', podId)
%                     else
%                         'Error : Pulse Width error !!!'
%                     end
%                 else
%                     'Error : Invalid code id from Pulse Width reply frame !!!'
%                 end
% end
%
%
%             % Create Stop frame
%             cmdId           = uint8( hex2dec('31') );        % Configuration command
%             length          = uint8(2);
%             targetedAppliId = uint8(1);
%             crc             = uint16( hex2dec('CAFE') );
%
%             % Send Stop frame
%             requestFrame = [cmdId length podId targetedAppliId typecast(crc, 'uint8') ];
%             fwrite(s, requestFrame, 'uint8');
%
%             % Wait Stop reply
%             i = 0;
%             while s.BytesAvailable == 0
%                 i = i + 1;
%             end
%
%             % Get Stop reply
%             replyFrame = fread(s, s.BytesAvailable, 'uint8');
%
%             % Analyze the Stop reply
%             if( replyFrame(1) == hex2dec('55') )
%                 length      = replyFrame(2);
%                 errorType   = replyFrame(3);
%                 errorId     = replyFrame(4);
%                 podIdRe     = replyFrame(5);
%                 %                                 requestId   = replyFrame(6);
%
%                 if(errorType == 0)
%
%                     fprintf('\t >> POD_%i is stoped \n', podId)
%                 else
%                     'Error : Stop error !!!'
%                 end
%             else
%                 'Error : Invalid code id from Stop reply frame !!!'
%             end
%         else
%             'Error : Start error !!!'
%         end
%     else
%         'Error : Invalid code id from Start reply frame !!!'
%     end
% else
%     'Error : Configuration error !!!'
% end
% else
%     'Error : Invalid code id from Configuration reply frame !!!'
%     end
%
%     if(strErr ~= 'None')
%         fprintf('\t X-> Error : %s !!!', strErr);
%     end
%
%
%
%
%
%     %% start timer
%
%     start(T);
%
%     tStart = tic;
%
%     %
%     % s.BytesAvailable
%
%     disp('fin')
%
%     % intensityScale = pcConfigureProstim(s,maxIntensity);
%     %
%     %
%     % %% sending some stim params (intensity and period)
%     %
%     %
%     % % intensity = [amp 0 0 0 0 0 0 0];
%     % % pcSetIntensity(s,intensity,maxIntensity,minIntensity,intensityScale);
%     %
%     % period = [25 0 0 0 0 0 0 0];
%     % pcSetPeriod(s,period,maxPeriod,minPeriod);
%     %

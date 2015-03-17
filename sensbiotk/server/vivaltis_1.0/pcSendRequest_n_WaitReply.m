function [strErr, pods, availablePods] = pcSendRequest_n_WaitReply(srl, rqst, pods)


availablePods = struct(pods);

% Create request frame
requestFrame = [rqst.cmdId rqst.length rqst.data typecast(rqst.crc, 'uint8') ];

% Send request frame
%requestDate = datestr(clock)
requestTime = datestr(clock, 'yyyy-mm-dd HH:MM:SS:FFF');
fwrite(srl, requestFrame, 'uint8');

% Get reply cmd and reply data size
i = 0;
while srl.BytesAvailable < 2
    i = i + 1;
end
reply.cmd = fread(srl, 1, 'uint8');
reply.length = fread(srl, 1, 'uint8');

% Get reply
while srl.BytesAvailable < reply.length
    i = i + 1;
end
reply.data = fread(srl, reply.length, 'uint8');
replyTime = datestr(clock, 'yyyy-mm-dd HH:MM:SS:FFF');


strErr      = 'None';
errorType   = reply.data(1);
errorId     = reply.data(2);
podIdRe     = reply.data(3);
requestId   = reply.data(4);

% Analyze the reply
switch rqst.cmdId
    
    % Initialization
    case hex2dec('13')
        
        if( reply.cmd == hex2dec('36') )
            
            nPOD    = reply.data(1);
            pods.nAvailable = 0;
            
            % Get each available POD
            fprintf('\n\t - Available Stimulation PODs : \n')
            
            for i = 1:nPOD
                idx = ( 8*(i-1) );
                pods.info(i).type       = reply.data(idx + 2);
                pods.info(i).networkId  = reply.data(idx + 3);
                pods.info(i).state      = reply.data(idx + 4);
                pods.info(i).version    = reply.data(idx + 5 : idx + 8)';
                pods.info(i).color      = reply.data(idx + 9);
                
                if (pods.info(i).type == 1) | (pods.info(i).type == 8)
                    pods.nAvailable = pods.nAvailable + 1;
                    availablePods.info(pods.nAvailable) = pods.info(i);
                    fprintf('\t\t |_ POD_%i is available \n', pods.info(i).networkId)
                end
            end
            availablePods.nAvailable = pods.nAvailable;
        else
            strErr = 'Error : Invalid code identifier from Initialization reply frame !!!' ;
        end
        
        % Detection
    case 12
        disp('detection');
        
        % Configuration - Start
    case { hex2dec('40'), hex2dec('30') } 
        
        % Analyze the reply
        if( reply.cmd == hex2dec('55') )
            
            if(errorType ~= 0)
                
            end
        end
        
    otherwise
        strErr = 'Unknown reply code';
end

end


function pcBreakInterruptCallback(serialObj, event)

serialObj.BytesAvailable
serialObj.BytesAvailable
serialObj.BytesAvailable
out = fread(serialObj, serialObj.BytesAvailable, 'uint8')

% persistent decodeState;
% persistent i;
% 
% if nargin == 0
%     i = 0;
%     decodeState = 'ReturnId';
% else
%     
%     switch decodeState
%         
%         case 'ReturnId'
%             
%             out = fread(serialObj, nData = serialObj.BytesAvailable, 'uint8')
%             decodeState = 'Length'
%             
%             serialObj.BytesAvailableFcnCount = 1;
%             
%         case 'Length'
%             
%             out = fread(serialObj,1,'uint8');
%             decodeState = 'Data'
%             serialObj.BytesAvailableFcnCount = nData;
%             
%         case 'Data'
%             
%             out = fread(serialObj,1,'uint8');
%             decodeState = 'ReturnId'
%             s.BytesAvailableFcnCount = 1;
%             
%         otherwise
%             'Unknown case '            
%     end
%     
% end
% 
% i = i+1
end

